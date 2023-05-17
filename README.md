# chessless
A non-interactive terminal user interface with the Stockfish chess engine. Removes the use of user state so that Stockfish's commands can be run using a singular command.

To access most of its commands, Stockfish is normally run interactively as a program inside the terminal. This is acceptable for a user but in some use cases where another program uses Stockfish, it is more ideal to run multiple commands in one pass. `undaemonize.py` addresses this problem by accepting a concatenated list of commands and printing the same stdout just without manual stdin.

Also includes a script that you can run to play chess against Stockfish on a curses-style interface. Currently this script is just a proof-of-concept with basic features.

## Usage
text

For the list of Stockfish commands, refer to its official [Commands](https://github.com/official-stockfish/Stockfish/wiki/Commands) documentation.

## Contributions
text

## See Also
[Official Stockfish GitHub page](https://github.com/official-stockfish/Stockfish)
