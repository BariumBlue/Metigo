#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import sys, random, time


global debug

def debug_print(self, *args):
	if debug:
		for a in args:
		    print a,


class GameHandler:

	def __init__(self, startboard, nboards, width, height, debug_arg=False):
		self.pieces = []
		global debug
		debug = debug_arg

		#load images, set/get used map/rules
		self.init_pieces()

		#start game
		self.tl = Timeline(self, startboard, nboards, width, height)

		#print banner
		self.banner()

	def banner(self):
		print '\n\n ======== Metigo v0.1 ======== \n'

	def disp_update(self, data, dt):
		#update images
		#display overlay text
		pass


	#displays on the terminal the current timeline
	def text_disp(self):

		tl = self.tl

		print '\n--------------------------------------------------\n'

		#print board numbers
		for bnum in range(len(tl.boards)):
			sys.stdout.write( str(bnum)+' ' )
			for p in range(tl.boardw): sys.stdout.write('  ')
		sys.stdout.write('\n')

		#print the boards
		for row in range(tl.boardh):
			for board in tl.boards:

				for column in range(tl.boardw):
					piece = board.get_square(column, row).on
					if piece!=[]:
						sys.stdout.write( piece[0].pdat.term_disp + ' ' )
					else:
						sys.stdout.write('_ ')

				sys.stdout.write('  ')

			sys.stdout.write('\n')

	def init_pieces(self):
		self.pieces = [
			PieceDat('white', 'unit', None, '●' ),
			PieceDat('black', 'unit', None, '○' )
		]


	def new_piece(self, ind, x, y, t):
		newpiece = PieceNode( self.pieces[ind] )
		newpiece.place(self.tl, x, y, t)
		newpiece.propogate(self.tl)




#contains all boards of a game/round, in chronological order
class Timeline:
	def __init__(self, gh, startboard, nboards, boardw, boardh):
		self.boards = []
		self.nboards = nboards
		for b in range(nboards): self.boards.append( Board(boardw, boardh) )

		# self.selected_piece = None
		self.boardw = boardw
		self.boardh = boardh

	def in_bounds(self, x,y,t):
		if t<0 or t>self.nboards:return False
		return self.boards[t].in_bounds(x,y)

	def get_square(self, x,y,t):
		return self.boards[t%self.nboards].get_square(x,y)


#a board; a slice of the timeline
class Board:

	def __init__(self, w,h):
		self.w = w
		self.h = h
		self.squares = [ Square() for i in range(w*h) ]

	def in_bounds(self, x, y):
		if x>=self.w or y>=self.h or x<0 or y<0: return False
		return True

	def get_square(self, x,y):
		if not self.in_bounds(x,y): return None
		return self.squares[ y*self.w + x ]


class Square:

	def __init__(self):
		self.on = []

#global event that happens on the timeline
class TimelineEvent:
	#types:
	#   new_unit
	def __init__(self, evtype, pieces):
		self.type = evtype
		self.pieces = pieces


#event that occurs to one or more pieces
class PieceEvent:

	#event types:
	#   doNothing
	#   move
	#   Kill
	#
	# doNothing / move:
	#   pieces: [cur_piece, future_piece]
	# kill:
	#   pieces: [killer_piece, killed_piece]

	#pieces is a list of relevant pieces, depending on event type
	def __init__(self, e_type, pieces):
		self.type = e_type
		self.pieces = pieces




#a unit at a specific point in time
class PieceNode:
	
	def __init__(self, pdat):
		self.x = -1
		self.y = -1
		self.t = -1
		self.pdat = pdat
		self.events = []
		self.in_play = False

		self.past_node = None

		self.checking = False #whether checking whether surronded

		self.iterations = 2

	def get_future(self, tl):
		for ev in self.events:

			if ev.type=='kill':
				#check killer or killed
					#killer
				if self == ev.pieces[0]:
					continue

					#victim
				if self==ev.pieces[1] and ev.pieces[0].in_play==False:
					debug_print( '  get_future: piece has been killed' )
					return None

			elif ev.type in ['doNothing', 'move']:
				return ev.pieces[1]

		debug_print( '  no current future! adding a doNothing. piece:', self.disp() )
		self.do_nothing(tl)
		return self.get_future(tl)


	#update whether we're still dead
	def check_is_dead(self):

		self.in_play = True

		if self.past_node!=None and self.past_node.in_play==False:
			debug_print('  past was dead')
			self.in_play = False
			return

		for ev in self.events:
			if ev.type=='kill':
				debug_print( '  found kill!', ev.pieces[0].in_play, ev.pieces[1]==self)
			if ev.type=='kill' and ev.pieces[0].in_play==True and ev.pieces[1]==self:
				debug_print( '  kill caused death')
				self.in_play = False
				return

	#propogate a unit that doesn't exist in the far future yet
	def propogate(self, tl):
		cur_unit = self
		while cur_unit!=None: cur_unit = cur_unit.get_future(tl)


	def update(self, tl):

		debug_print('updating piece at', self.x, self.y, self.t, self)

		#check whether something's changed
		was_dead = self.in_play
		self.check_is_dead()



		#if nothing has actually changed
		if self.in_play==was_dead:
			return

		#now dead
		if self.in_play==False:
			self.remove_future(tl)
			self.unplace(tl)
		#now alive
		elif self.in_play==True:
			self.re_place_cur_and_future(tl)

		#update any possibly affecred units
		for ev in self.events:
			for p in ev.pieces:
				if p in [self, None]: continue
				p.update(tl)


	#remove a single node from the board
	def unplace(self, tl):

		self.in_play = False

		square = tl.get_square( self.x, self.y, self.t )
		if self in square.on: square.on.remove(self)

		for ev in self.events:
			for p in ev.pieces:
				if p not in [None, self]:
					p.update(tl)


	def do_nothing(self, tl):
		debug_print( '  doing nothing, at', self.x, self.y, self.t )
		# if self.t==tl.nboards-1 or self.iterations==0:
			# future=None
		if self.iterations==0:
			future=None
		else:
			future = PieceNode(self.pdat)
			future.place(tl, self.x, self.y, (self.t+1)%tl.nboards )
			future.past_node = self
			future.iterations = self.iterations-1
		self.events.insert( 0, PieceEvent('doNothing', [self, future]) )

	def kill(self, tl, other):
		debug_print( 'killing unit at', other.x, other.y, other.t)

		#check we're not trying to kill a unit that's already killed us
		# for ev in other.events:
		# 	if ev.type==

		kill_ev = PieceEvent('kill', [self, other])
		self.events.append( kill_ev )
		other.events.insert( 0, kill_ev )

		debug_print( ' kill_ev is', kill_ev.type, kill_ev.pieces, kill_ev)

		other.update(tl)

	#place a single node on the board
	def place(self, tl, x,y,t):
		debug_print( '  placing unit on', x,y,t )
		square = tl.boards[t].get_square(x,y)
		self.x, self.y, self.t = x,y,t

		if square==None: print 'Error: can\'t place at',x,y,'!'; return

		self.in_play = True

		if square.on!=[] and square.on!=[self]:
			other = square.on[0]
			debug_print( 'landing on square with someone on it! other:', other.disp(), 'self:', self.disp() )
			# self.kill( other )
			self.in_play = False
			return
		if self not in square.on:
			debug_print('\tunit did not exist on square, adding' )
			square.on.append(self)

			#erase any surronded units
			for neighborx, neighbory in [(0,-1),(0,1),(-1,0),(1,0)]:
				nsquare = tl.boards[t].get_square( x+neighborx, y+neighbory )
				if nsquare==None: continue
				if nsquare.on!=[]:
					other = nsquare.on[0]
					if other.pdat.player!=self.pdat.player:
						debug_print( 'checking if enemy is surronded' )
						if other.is_surronded(tl):
							debug_print( 'enemy was surronded, erasing' )
							other.erase_neighboring(tl)

		if self.is_surronded(tl):
			self.erase_neighboring(tl)



	#put back nodes that were previously dead
	def re_place_cur_and_future(self, tl):
		cur_unit = self
		while cur_unit!=None:
			cur_unit.place( tl, cur_unit.x, cur_unit.y, cur_unit.t )
			cur_unit = cur_unit.get_future(tl)

	#unplace all future nodes
	def remove_future(self, tl):
		#remove any and all futures
		future = self.get_future( tl )
		if future!=None: 
			future.remove_future(tl)
			future.unplace(tl)

	#erase yourself and neighboring allied units
	def erase_neighboring(self, tl):
		board = tl.boards[self.t]
		self.in_play = False

		for neighborx, neighbory in [(0,-1),(0,1),(-1,0),(1,0)]:
			nsquare = board.get_square( self.x+neighborx, self.y+neighbory )
			if nsquare==None: continue

			other = nsquare.on[0]
			if other.pdat.player == self.pdat.player:
				if other.in_play==False: continue
				other.erase_neighboring(tl)

		self.erase(tl)

	#erase self and future from play
	def erase(self, tl):

		future = self.get_future(tl)

		self.unplace( tl )

		#remove this piece from past's memory
		if self.past_node!=None:
			for ev in self.past_node.events:
				if ev.type=='doNothing':
					ev.pieces[1] = None

		self.past_node = None

		#remove future
		if future!=None:
			future.erase(tl)


		#remove relevant events

	#check whether this piece possibly along with other is surronded
	def is_surronded(self, tl):
		if self.checking==True: return True

		self.checking = True

		board = tl.boards[self.t]

		#if there is an open spot around this piece or any connected neighboring pieces
		for neighborx, neighbory in [(0,-1),(0,1),(-1,0),(1,0)]:
			nsquare = board.get_square( self.x+neighborx, self.y+neighbory )
			if nsquare==None: continue

			debug_print( '  is_surronded: checking', self.x+neighborx, self.y+neighbory, 'square is', nsquare.on )

			#found an empty square!
			if nsquare.on==[]:
				self.checking = False
				return False

			#check neighbors
			other = nsquare.on[0]
			if other.pdat.player==self.pdat.player:
				if other.is_surronded(tl)==False:
					self.checking = False
					return False

		self.checking = False
		return True


	def move_to(self, tl, x, y, t):
		#remove old future[s]
		self.remove_future(tl)

		new_future = PieceNode( self.pdat )
		new_future.place( tl, x, y, t )
		new_future.past_node = self
		new_future.propogate(tl)

		move_ev = PieceEvent('move', [self, new_future])
		self.events.insert(0, move_ev)

	def disp(self):
		return '%s %s: %s@{%i,%i,%i}' % (self.pdat.name, self.pdat.term_disp, 'alive'if self.in_play else 'dead', self.x, self.y, self.t) + str(self)


#general data about a piece
class PieceDat:

	def __init__( self, player, pname, img, term_disp, pmoves = None):

		debug_print( 'init pdat, ', player, pname, img, term_disp )

		self.player  = player
		self.name	= pname
		self.moves   = pmoves

		self.term_disp = term_disp
		self.img	 = img
