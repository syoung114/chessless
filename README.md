# chessless
A non-interactive terminal user interface with the Stockfish chess engine. Removes the use of user state so that Stockfish's commands can be run using a singular command.

To access most of its commands, Stockfish is normally run interactively as a program inside the terminal. This is acceptable for a user but in some use cases where another program uses Stockfish, it is more ideal to run multiple commands in one pass. `undaemonize.py` addresses this problem by accepting a concatenated list of commands and printing the same stdout just without manual stdin.

Also includes a script that you can run to play chess against Stockfish on a curses-style interface. Currently this script is just a proof-of-concept with basic features.

## Usage
To run Stockfish stateless in this directory, run the following code:

```console
$ chmod +x init.sh
$ ./init.sh
$ python
Python xxxxxxxxxxxxxxxxxx on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import undaemonize
>>> ud = undaemonize.undaemonize('./Stockfish/src/stockfish', 'YOUR;COMMANDS;HERE'.split(';'))
>>> print(ud)
```

You may also run undaemonize via non-interactive python assuming that you have run `./init.sh`.

For the list of Stockfish commands, refer to its official [Commands](https://github.com/official-stockfish/Stockfish/wiki/Commands) documentation.

The playchess script is simply run by:

```
$ python playchess.py white|black [--depth int]
```

Moves are given in the UCI notation, i.e `e2e4` or `e7e8q`. For castling, just move the king two files over when it is legal to do so, i.e `e1g1` or `e1c1`.

## Contributions
Contributions are welcome. Please raise an issue to inform me of suggested changes and to see if it is worth a pull request.

## See Also
[Official Stockfish GitHub page](https://github.com/official-stockfish/Stockfish)
