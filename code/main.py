#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import metigo
import interactive
import sys

# board = [ (0, (1,1)), (1, (2, 2)) ]

def main(args):

	board = [ 
	    # { 'pdat_index':0, 'xpos':1, 'ypos':1},
	    # { 'pdat_index':1, 'xpos':2, 'ypos':2},
	]

	gh = metigo.GameHandler( board, 6, 4, 6 )
	tl = gh.tl
	
	if len(args)==1:
		game = interactive.graphical_game( gh )
	elif args[1][0]=='i':
		game = interactive.text_game( gh )
	else:
		print 'only arg is "i" or "interactive"'
	game.startgame()

if __name__ == "__main__":
    main(sys.argv)
