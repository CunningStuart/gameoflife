import sys
import pygame as pg
import numpy as np

def draw_boarders():
	for i in range(int(width/square_size)):
		pg.draw.line(screen, pg.Color(50,50,50), [i*square_size,0], [i*square_size,height], width=1)

	for i in range(int(height/square_size)):
		pg.draw.line(screen, pg.Color(50,50,50), [0,i*square_size], [width,i*square_size], width=1)


def draw_squares(size, board, mouse_state):
	mouse_held = True
	old_xgrid_pos = -1
	old_ygrid_pos = -1

	# While the mouse button is being held
	while mouse_held:
		# Get which cell the mouse is in
		xgrid_pos = int(int(pg.mouse.get_pos()[0])/size)*size
		ygrid_pos = int(int(pg.mouse.get_pos()[1])/size)*size

		# Check if the mouse has moved to a new position
		if old_xgrid_pos != xgrid_pos or old_ygrid_pos != ygrid_pos:
			
			if mouse_state[0]:
				board[int(ygrid_pos/size)][int(xgrid_pos/size)] = 1
			elif mouse_state[2]:
				board[int(ygrid_pos/size)][int(xgrid_pos/size)] = 0


			if mouse_state[0]:
				pg.draw.rect(background, pg.Color(255,255,0), pg.Rect(xgrid_pos,ygrid_pos,size,size))
			elif mouse_state[2]:
				pg.draw.rect(background, pg.Color(0,0,0), pg.Rect(xgrid_pos,ygrid_pos,size,size))

			draw_boarders()
			pg.display.flip()

		old_xgrid_pos = xgrid_pos
		old_ygrid_pos = ygrid_pos

		for event_test in pg.event.get():
			if event_test.type == pg.MOUSEBUTTONUP:
				mouse_held = False

	return board


def fill(colour,w,h):
	pg.draw.rect(background, colour, pg.Rect(0,0,w,h))
	draw_boarders()
	pg.display.flip()


def update_screen(b,w,h,size):
	b_size = np.shape(b)

	pg.draw.rect(background, pg.Color(0,0,0), pg.Rect(0,0,b_size[1]*size,b_size[0]*size))

	for i in range(int(h/size)):
		for j in range(int(w/size)):
			#print(b[i][j])
			if b[i][j] == 1:
				pg.draw.rect(background, pg.Color(255,255,0), pg.Rect(j*size,i*size,size,size))

			if b[i][j] == 2:
				pg.draw.rect(background, pg.Color(255,0,255), pg.Rect(j*size,i*size,size,size))

	draw_boarders()
	pg.display.flip()


def new_state(b):
	size = np.shape(b)

	new_b = np.zeros(size)

	for i in range(size[1]):
		for j in range(size[0]):
			neighbours = slicer(b,i,j)

			if b[j][i] == 1:
				total = np.sum(neighbours) - 1
			else:
				total = np.sum(neighbours)

			if b[j][i] == 1 and (total == 2 or total == 3):
				new_b[j][i] = 1
			elif b[j][i] == 0 and total == 3:
				new_b[j][i] = 1
			else:
				new_b[j][i] = 0

	return new_b

def slicer(b,i,j):
	if i == 0: 
		i_low_bound = i
	else:
		i_low_bound = i-1

	if j == 0: 
		j_low_bound = j
	else:
		j_low_bound = j-1

	return b[j_low_bound:j+2,i_low_bound:i+2]



pg.init()

square_size = int(sys.argv[3])
width = int(int(sys.argv[1])/square_size)*square_size
height = int(int(sys.argv[2])/square_size)*square_size
size = [width,height]

background = pg.display.set_mode(size)
screen = pg.display.set_mode(size)

board = np.zeros([int(height/square_size),int(width/square_size)])

board0 = board.copy()

# Draw vertical and horizontal lines to cover game board
draw_boarders()

# Update display
pg.display.flip()

edit = True

while True:
	# Sequence for editing the game board
	pg.time.delay(50)
	while edit == True:

		for event in pg.event.get():
			# Draw squares onto the grid
			if event.type == pg.MOUSEBUTTONDOWN:
				board = draw_squares(square_size, board, pg.mouse.get_pressed())

			# Fill all
			if event.type == pg.KEYUP and event.key == pg.K_f:
				fill(pg.Color(255,255,0), width, height)
				board = np.ones([int(height/square_size),int(width/square_size)])

			# Clear all			
			if event.type == pg.KEYUP and event.key == pg.K_c:
				fill(pg.Color(0,0,0), width, height)
				board = np.zeros([int(height/square_size),int(width/square_size)])

			# Reset board to original state
			if event.type == pg.KEYUP and event.key == pg.K_r:
				board = board0.copy()
				update_screen(board,width,height,square_size)


			# Turn off editing mode
			if event.type == pg.KEYUP and event.key == pg.K_SPACE:
				edit = False

			# PRINT BOARD TO CONSOLE
			if event.type == pg.KEYUP and event.key == pg.K_b:
				print(board)
				print()

			# Quit the game if 'q' is pressed
			if event.type == pg.KEYUP and event.key == pg.K_q:
				print("Quitting Game.")
				pg.display.quit()
				pg.quit()
				sys.exit()

	board0 = board.copy()


	# Sequence for running the game of life
	while edit == False:

		board = new_state(board)
		update_screen(board,width,height,square_size)

		for event in pg.event.get():
			# Turn on editing mode
			if event.type == pg.KEYUP and event.key == pg.K_SPACE:
				edit = True

			
			# Iterate a new state
			if event.type == pg.KEYUP and event.key == pg.K_i:
				#print(np.shape(board))
				board = new_state(board)
				update_screen(board,width,height,square_size)
			

			if event.type == pg.KEYUP and event.key == pg.K_b:
				update_screen(board,width,height,square_size)

			# Quit the game if 'q' is pressed
			if event.type == pg.KEYUP and event.key == pg.K_q:
				print("Quitting Game.")
				pg.display.quit()
				pg.quit()
				exit()
