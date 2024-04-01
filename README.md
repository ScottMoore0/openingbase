This repository contains:
- A Python programme that generates a list of all chess positions which are x plies from the FIDE starting position, with x specified by the user.
- Outputs from the programme.

The programme prints a text document once it has finished running, and each line contains a different chess position, as well as how many plies it takes to reach that position, and also whether it is a checkmate or mate-in-N position (for those positions where a forced mate is possible within the maximum number of plies specified from the starting position).

Time taken to output for each ply on my computer (illustrative):

ply(0): 0.00 seconds

ply(1): 0.00 seconds

ply(2): 0.03 seconds

ply(3): 0.62 seconds

ply(4): 14.55 seconds

