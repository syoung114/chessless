import undaemonize
import curses
import chess
import re
import argparse

START_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
play_as_black = False
depth = 5
fen = START_FEN
board = chess.Board(fen)
regex = re.compile(r"[a-h][1-8][a-h][1-8](b|n|r|q)?")

def get_arguments():
    parser = argparse.ArgumentParser(description='Small script to play chess in a curses interface')
    parser.add_argument('white_or_black', type=str, help='Do you want to play as white or as black?')
    parser.add_argument('--depth', default=depth, type=int, help='How deep should stockfish analyze? Increases difficulty but also thinking time.')

    args = parser.parse_args()
    play_as_black_inner = args.white_or_black == 'black'
    depth_inner = args.depth
    return play_as_black_inner, depth_inner
    
def stockfish_move():
    stockfish = undaemonize.undaemonize(
        './Stockfish/src/stockfish',
        f'position fen \'{board.fen()}\';go depth {depth}'.split(';'),
        True
    ).rstrip()

    sf_move = regex.search(stockfish).group(0)
    sf_uci = chess.Move.from_uci(sf_move)
    board.push(sf_uci)

def main(stdscr):
    quit_synonyms = ['quit', 'exit', 'q', ':q', ':wq']

    def player_move(cmd):
        uci_cmd = chess.Move.from_uci(cmd)

        if uci_cmd in board.legal_moves:
            board.push(uci_cmd)

    def flip_board():
        ranks = str(board).strip().split('\n')
        flipped_board = '\n'.join(ranks)[::-1]
        return flipped_board

    if play_as_black:
        stockfish_move()
 
    while True:
        # Clear the screen
        stdscr.clear()
        
        if play_as_black:
            b_str = flip_board()
        else:
            b_str = str(board)

        stdscr.addstr(0, 0, b_str + '\n> ')

        ## Create an input window
        input_win = curses.newwin(1, curses.COLS-2, 2, 2)
        stdscr.keypad(True)
        curses.echo()

        # Get the user's input
        cmd = stdscr.getstr().decode("utf-8").lower()

        #Basic input validation
        if cmd in quit_synonyms:
            break

        if len(cmd) < 4 or len(cmd) > 5:
            continue

        try:
            player_move(cmd)
        except chess.InvalidMoveError:
            continue
        stockfish_move()

        stdscr.refresh()

if __name__ == '__main__': #no reason to import this code
    play_as_black, depth = get_arguments()
    curses.wrapper(main)
