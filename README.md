Metigo - Meta-Time Go
=======================

A version of Go that takes place across a timeline of boards; there's a board for times 0,1,2,3,... and each board propagates into the board ahead of it.

=======================

**Dependencies**

python2, and preferably [Pygame](http://pygame.org/download.shtml).

You can play in 'text' mode by calling the script with an 'i' or 'interactive' argument. Not recommended.

=======================

**Playing**

The rules are standard go rules; surround your enemy to capture their pieces, try to dominate the playing field. 
Killing a piece will kill it's future selves as well.

Pieces are propagated three boards ahead, and wrap from the last board back to the first.

Left mouse to place a white piece, right mouse to place a black piece. Click on an existing piece to remove it and it's future.

Pieces with a reddish '0' are the entry pieces; any piece ahead of it in time at the same time are that piece's future selves.

======================

**Screenshots**

Game start. Place a piece by either left or click clicking

![Imgur](http://i.imgur.com/HppCncw.png)

One white piece and one black piece placed on the board. Notice that the black piece wrapped back to the 0 board

![Imgur](http://i.imgur.com/w85D7ln.png)

Before black captures a white piece

![Imgur](http://i.imgur.com/BrXGzKC.png)

After capturing the white piece. Notice that the white piece's future selves were also removed

![Imgur](http://i.imgur.com/EqxNfMx.png)