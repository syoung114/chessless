import curses
import undaemonize
import chess
import re

START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

def main(stdscr):
    fen = START_FEN
    board = chess.Board(fen)
    regex = re.compile(r"[a-zA-Z]\d[a-zA-Z]\d(b|n|r|q)?")
    while True:
        # Clear the screen
        stdscr.clear()

        stdscr.addstr(0, 0, str(board) + '\n> ')
        #stdscr.addstr(0, 0, display+'> ')

        ## Create an input window
        input_win = curses.newwin(1, curses.COLS-2, 2, 2)
        stdscr.keypad(True)
        curses.echo()

        ## Get the user's input
        cmd = stdscr.getstr().decode("utf-8")

        #Basic input validation
        if cmd == 'exit':
            break        
        if len(cmd) < 4 or len(cmd) > 5:
            continue

        #convert teh command into UCI
        uci_cmd = chess.Move.from_uci(cmd)

        if uci_cmd in board.legal_moves:
            board.push(uci_cmd)

        #next_fen = board.fen()

        stockfish = undaemonize.undaemonize(
            './Stockfish/src/stockfish',
            f'position fen \'{board.fen()}\';go depth 20'.split(';'),
            True
        ).rstrip()

        sf_move = regex.search(stockfish).group(0)
        #stdscr.addstr(sf_move)
        sf_uci = chess.Move.from_uci(sf_move)
        board.push(sf_uci)

        #fen = next_fen

        ## Refresh the screen
        stdscr.refresh()

        ## Wait for user input
        #stdscr.getch()

if __name__ == '__main__':
    #no reason to import this code
    curses.wrapper(main)
