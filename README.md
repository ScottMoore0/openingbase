This repository contains:
- A Python programme that generates a list of all chess positions which are x plies from the FIDE starting position, with x specified by the user.
- Outputs from the programme.

The programme prints a text document once it has finished running, and each line contains a different chess position, as well as how many plies it takes to reach that position, and also whether it is a checkmate or mate-in-N position (for those positions where a forced mate is possible within the maximum number of plies specified from the starting position).

To-do: Output uniquely-realisable positions only - no duplicates. For the time being, the below figures reflect duplicates being included.

Time taken to output for each ply on my computer (illustrative), and file size:

ply(0): 0.00 seconds (62 bytes)

ply(1): 0.00 seconds (1,336 bytes)

ply(2): 0.03 seconds (27 KB)

ply(3): 0.62 seconds (606 KB)

ply(4): 14.55 seconds (13.6 MB)

ply(5): 336.96 seconds (5 minutes ~37 seconds) (340 MB) (comparable to 5-man Syzygy tablebase)

ply(6) (projected): 7750.08 seconds (2 hours, 9 minutes, ~10 seconds) (8.5 GB)

ply(7) (projected): 178,251.84 seconds (49 hours, 30 minutes, ~51 seconds) (212 GB) (comparable to 6-man Syzygy tablebase)

Further projected sizes:

ply(8) (projected): 5.3 TB (comparable to 7-man Syzygy tablebase)

ply(9) (projected): 132.7 TB

ply(10) (projected): 3.3 PB (comparable to estimates for the 8-man Syzygy tablebase)


From https://wismuth.com/chess/statistics-positions.html:

Number of distinct chess positions
  
ply 0	1

ply 1	20

ply 2	400

ply 3	5362

ply 4	72078

ply 5	822518

ply 6	9417681

ply 7	96400068

ply 8	988187354

ply 9	9183421888

ply 10	85375278064

ply 11	726155461002
