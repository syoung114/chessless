import sys
import subprocess
import queue
import time
from threading import Thread

class SubprocessCM:
    '''A RAII-like class (called a context manager in Python) that automates `subprocess.Popen` lifetime'''
    #subprocess.Popen doesn't support `with` by default. I find this strange because processes can leak like files.
    #I consider myself more of a C(-like) programmer so not having RAII for something like this unusual. Fine, I'll do it myself.
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __enter__(self):
        #Note that I could perform a None check to ensure that overridden processes do not leak. For the simplicity of this program I won't do it.
        self.process = subprocess.Popen(*self.args, **self.kwargs)
        return self.process

    def __exit__(self, exc_type, exc_value, traceback):
        if self.process:
            self.process.terminate()

def undaemonize(pathargs, stdins):
    '''
    Runs a normally interactive terminal program as a single command.
    Note that this function has security implications if it is used in a larger program. Arbitrary execution.
    :param str[] pathargs the program and initial arguments needed to run it
    :param str[] stdins the interactive commands we are now running 'stateless'
    '''

    def enqueue_output(out, queue): #I am inlining this function because it makes no sense to have in the global scope
        for line in iter(out.readline, b''):
            queue.put(line)
        out.close()
    
    with SubprocessCM(
        pathargs,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        universal_newlines=True,
        bufsize=1,
        close_fds='posix' in sys.builtin_module_names
    ) as process:
        #init the 'things' that allow for non-blocking polling of stdout
        #see https://stackoverflow.com/a/4896288/8724072
        output_queue = queue.Queue()
        output_thread = Thread(target=enqueue_output, args=(process.stdout, output_queue), daemon=True)
        output_thread.start()
        
        #pass in the commands
        for stdin in stdins:
            process.stdin.write(stdin + '\n')
            process.stdin.flush() 
        
        #get the outputs
        output_fails = 0
        keep_printing = True
        stdout = ''
        while output_fails < 3: #a classic magic number. shoot me.
            try:
                line = output_queue.get_nowait()
            except queue.Empty:
                output_fails += 1
            else:
                stdout += line
                output_fails = 0
            time.sleep(0.1) #TODO find more elegant solution to sleep

        return stdout

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Runs a normally interactive terminal program as a single command')
    parser.add_argument('pathargs', type=str, help='Path to the terminal program and the initial arguments needed to run it')
    parser.add_argument('stdins', type=str, help='A delimited string representing a list of commands to run \'stateless\'')

    default_delim = ';'
    parser.add_argument('-dp', '--pathargs_delim', type=str, default=default_delim, help='The delimiter sequence that denotes each element in the pathargs string')
    parser.add_argument('-ds', '--stdins_delim', type=str, default=default_delim, help='The delimiter sequence that denotes each element in the stdins string')

    #tokenise and store the values
    args = parser.parse_args()
    subprogram_pathargs = args.pathargs.split(args.pathargs_delim)
    subprogram_stdins = args.stdins.split(args.stdins_delim)

    out = undaemonize(subprogram_pathargs, subprogram_stdins)
    print(out, end='')
    

