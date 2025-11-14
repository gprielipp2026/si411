# Lab 06 - Memory

Completed by George Prielipp (265112)

## Summarize Lessons learned

1) Which algorithm seems to work best?

    The algorithm that seemed to work the best is LRU. It is consistent with 296 faults, no matter how many frames are available to it.

2) Does the choice of algorithm matter more when there are more pages, or fewer pages?

    The choice of algorithm matter more as the number pages increases. When there are more pages, there is a higher chance that the page needed is not in memory (especially if the number of frames is small). What should be noted from the data, is that LRU and AGING performed exactly the same once enough frames were given to the AGING algorithm.



## Data / Results

| Number of frames | Algorithm | Faults | Number of Ops | Fault Rate |
| --- | --- | --- | --- | --- |
|  8 | FIFO | 433 | 10138 | 0.042710593805484316 |
| 16 | FIFO | 353 | 10138 | 0.03481949102387059 |
| 64 | FIFO | 304 | 10138 | 0.03481949102387059 |
| - | - | - | - | -|
|  8 | LRU | 296 | 10138 | 0.029197080291970802 |
| 16 | LRU | 296 | 10138 | 0.029197080291970802 |
| 64 | LRU | 296 | 10138 | 0.029197080291970802 |
| - | - | - | - | -|
|  8 | AGING | 303 | 10138 | 0.029887551785362003 |
| 16 | AGING | 296 | 10138 | 0.029197080291970802 |
| 64 | AGING | 296 | 10138 | 0.029197080291970802 |
