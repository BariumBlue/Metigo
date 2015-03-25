#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import math, os, sys


try:
	import pygame
	from pygame.locals import *
	if not pygame.font: print 'Warning, fonts disabled'
	if not pygame.mixer: print 'Warning, sound disabled'
except ImportError:
	print 'text version only. To run text version, pass "i" or "interactive" as an argument'

#Text interactive game
class text_game():


	def __init__(self, gh):
		self.gh = gh

	def startgame(self):
		self.play_loop()

	def play_loop(self):

		while True:
			self.gh.text_disp()

			uin = raw_input( '\n ==============\nPlace [form: color x y t]: ' )
			self.interpret_input( uin )

	def interpret_input(self, uin):
		nums = []
		new_num = ''

		while True:

			if uin!='' and uin[0] in 'bw':
				new_num += uin[0]
			elif uin!='' and uin[0] in '0123456789':
				new_num += uin[0]
			elif new_num!='':
				nums += [new_num]
				new_num = ''

			if uin=='': break

			uin = uin[1:]

		try:
			color, xpos, ypos, tpos = nums
			ind = 0 if color in 'w' else 1; xpos = int(xpos); ypos = int(ypos); tpos = int(tpos)
		except ValueError:
			print '\n - ! - Error processing inout - ! - \n'
			return

		#init piece
		self.gh.new_piece( ind, xpos, ypos, tpos )



#Graphical interactive game
class graphical_game():

	def __init__(self, gh):

		self.gh = gh
		# self.screenWidth, self.screenHeight = 1080, 800
		self.screenWidth, self.screenHeight = 1920, 1080


		self.screen = pygame.display.set_mode( (self.screenWidth, self.screenHeight) )


		self.xborder, self.yborder = 50, 50

		self.board_margin = 25


		assetsdir = ''

		if os.path.isfile( "assets/images/Chessboard4x6.png" ):
			assetsdir = "assets/"
		else: assetsdir = '../assets/'

		self.play_board =  pygame.image.load( assetsdir + "images/Chessboard4x6.png" )
		# self.play_board =  pygame.image.load( assetsdir + "images/Chessboard6x8.png" )
		self.boardw, self.boardh = self.play_board.get_rect().width, self.play_board.get_rect().height

		self.squarew = int( self.boardw / self.gh.tl.boardw)
		self.squareh = int( self.boardh / self.gh.tl.boardh)

		self.background = pygame.image.load( assetsdir + "images/bg.png" )
		self.bgw, self.bgh = self.background.get_rect().width, self.background.get_rect().height

		self.white_go = pygame.image.load( assetsdir + "images/white_go.png" )
		self.black_go = pygame.image.load( assetsdir + "images/black_go.png" )

		self.orig_o = pygame.image.load( assetsdir + "images/OriginalO.png" )




	def startgame(self):
		pygame.init()

		self.font = pygame.font.Font(None, 36)

		clock = pygame.time.Clock()


		self.gh.text_disp()

		while 1:
			clock.tick(20)

			self.process_user_events()

			self.display()
			pygame.display.flip()


	def process_user_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
			elif event.type == KEYDOWN and event.key == K_ESCAPE:
				return
			elif event.type == MOUSEBUTTONDOWN:
				xpos, ypos, tpos = self.get_click_square( event.pos )
				if not self.gh.tl.in_bounds(xpos, ypos, tpos): continue

				square = self.gh.tl.get_square( xpos, ypos, tpos )
				if square.on!=[]:
					piece = square.on[0]
					piece.erase(self.gh.tl)
					return

				#left click
				if event.button==1:
					self.gh.new_piece( 0, xpos, ypos, tpos )
				#right click
				elif event.button==3:
					self.gh.new_piece( 1, xpos, ypos, tpos )

	#update the display window
	def display(self):
			#show the background
			self.screen.fill( (0,0,0) )# black
			x,y = 0,0
			while y<self.screenHeight:
				while x<self.screenWidth:
					self.screen.blit(self.background, (x, y))
					x += self.bgw
				x = 0
				y += self.bgh

			#show the boards
			for i in range(self.gh.tl.nboards):
				boardx = self.xborder + (self.boardw+self.board_margin)*i
				boardy = self.yborder

				#show the board
				self.screen.blit( self.play_board, (boardx, boardy) )

				#show the board number
				text = self.font.render(str(i), 1, (255, 255, 255))
				self.screen.blit( text, (boardx+self.boardw/2-7, boardy-18) )

				#show the pieces
				board = self.gh.tl.boards[i]
				for sq in board.squares:
					if sq.on==[]: continue
					piece = sq.on[0]

					if piece.pdat.term_disp == '●':
						dispx, dispy = boardx + piece.x*self.squarew, boardy + piece.y*self.squareh
						self.screen.blit( self.white_go, (dispx, dispy) )

					elif piece.pdat.term_disp == '○':
						dispx, dispy = boardx + piece.x*self.squarew, boardy + piece.y*self.squareh
						self.screen.blit( self.black_go, (dispx, dispy) )

					if piece.past_node==None:
						self.screen.blit( self.orig_o, (dispx+16, dispy+16) )




	#return the coords of the clicked square (if any)
	def get_click_square(self, pos):

		carouselx, carousely = pos[0]-self.xborder, pos[1]-self.yborder

		boardposx = carouselx % (self.boardw+self.board_margin)
		boardposy = carousely

		tpos = carouselx / (self.boardw+self.board_margin)

		squarex, squarey = int(boardposx/self.squarew), int(boardposy/self.squareh)

		return (squarex, squarey, tpos)






