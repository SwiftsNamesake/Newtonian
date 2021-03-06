#
# Newtonian - test.py
#
# Jonatan H Sundqvist
# Jayant Shivarajan
#
# July 10 2014
#
# Showing Jay how to create windows with tkinter
#

# TODO | - Vector alias for complex numbers (?)
#		 - Bounding boxes and tangents, non-rectangular collision-checks
#		 - Extensive refactoring, break up into modules

# SPEC | - 
#		 -


import tkinter as tk # Windows and events

from PIL.ImageTk import PhotoImage, Image # Loading icons

from utilities import * # Vector utilities

from collections import namedtuple	# Should probably be removed
from itertools import cycle			# Used for iterating over plot points

from cmath import polar, rect, pi as π # Complex number functions and related constants
from math import copysign, sqrt, sin   #


def createWindow(size):

	''' '''

	# Create and configure window
	window = tk.Tk()
	window.title('Newtonian')
	window.size = size.real, size.imag
	window.geometry('%dx%d' % window.size)
	
	# Set icon
	window.icon = PhotoImage(Image.open('apple.png'))
	window.call('wm', 'iconphoto', window._w, window.icon)
	
	# Settings
	window.PAUSE = False

	# Create canvas
	canvas = tk.Canvas(width=width, height=height, bd=0)
	canvas.pack()

	return window, canvas


class AnimationState:

	''' '''

	# TODO: Facilities for pretty printing simulation state (translucent tk.Text?)

	def __init__(self, P, V, A, S, O, W, H):
	#def __init__(self, P : 'Position vector', V : 'Velocity vector', A : 'Acceleration vector', S : 'Scale vector', O : 'Origin offset'):

		'''
		Doc goes here

		'''

		# Physics
		self.P = P 	 # Position vector
		self.V = V 	 # Velocity vector
		self.A = A 	 # Acceleration vector
		self.S = S 	 # Size vector # TODO: Make this a real vector (ie. invert Y)
		
		# General
		self.T  = 0.0 # Time
		self.TS = 1.0 # Time scale (simulation time/real time)

		# Coordinates
		self.s = 100-100j 		# Scale (px/m) # TODO: Do not hard-code this value
		self.W = W 				# Width of world
		self.H = H 				# Height of world TODO: Convert to world coords (✓); Extract width and height (✓)
		self.O = 0.0+self.H*1j 	# Offset (m) (world origin -> screen origin)


	def pointToScreenCoords(self, point):
		''' Converts from world space to canvas space '''
		# TODO: Rename (?)
		return (int((point.real-self.O.real)*self.s.real), int((point.imag-self.O.imag)*self.s.imag)) # TODO: Allow X origin offset (✓)


	def pointToWorldCoords(self, point):
		''' Converts from canvas space to world space '''
		# TODO: Rename (?)
		# TODO: Return vector (?)
		return ((point.real/self.s.real)+self.O.real, (point.imag/self.s.imag)+self.O.imag)


	def toScreen(self, point):
		return self.pointToScreenCoords(point)


	def toWorld(self, point):
		return self.pointToWorldCoords(point)


	def centre(self, point, size):
		''' Calculates centre from point and size vector '''
		return point+size/2


	def worldToScreen(self):
		''' '''
		# TODO: Implement world-space to screen space method (✓)
		# TODO: Allow rotated coordinate systems (?)
		# TODO: Clean this up, add docstring
		TOPLEFT 	= self.pointToScreenCoords(self.P)
		BOTTOMRIGHT = self.pointToScreenCoords(self.P+self.S)
		#screen = ((P.real+self.O.real)*s.real, (P.imag+self.O.imag)*s.imag, (P.real+S.real+self.O.imag)*s.real, (P.imag+S.imag+self.O.real)*s.imag)
		screen = TOPLEFT + BOTTOMRIGHT
		#print('X: %.2fpx, Y: %.2fpx' % screen[:2])
		#print('Width: %dpx, Height: %dpx' % (screen[2]-screen[0], screen[1]-screen[3]))
		return screen


# Create window and canvas
size = 720+480j
width, height = size.real, size.imag
window, canvas = createWindow(size)

# TODO: Encapsulate coordinate system conversion logic (cf. AnimationState) (...)
# TODO: Encapsulate animation and related parameters (cf. AnimationState)

# Coordinate system
s = 100-100j 	# Scale vector (px/m) # TODO: Make this a vector too (✓)
G = 0.2 		# Ground height (m)
S = 0.2-0.2j 	# Size vector (distance from top left) (m)

W = abs(width/s.real)  # TODO: Fix this value ?
H = abs(height/s.imag) # TODO: Fix this value

O = 0.0+H*1j 	# Offset between world origin and screen origin

# Physics
P = 5.35+1.8j	# Position vector (top left) (m)
A = 0.00-9.82j 	# Acceleration vector (m/s^2)
V = rect(3.6, 135*π/180.0)
#V = 2.06+2.6j	# Velocity vector (m/s)

# Animation
FPS = 30 	  # Frames per second
dt  = 1.0/FPS # Time between consecutive frames (s)
dtS = 1.0 	  # Scale of dt
# TODO: Decouple real dt and simulation dt (?) (...)

state = AnimationState(P, V, A, S, O, W, H)

ground 	= canvas.create_rectangle((0, height+int(G*s.imag), width, height), fill='green', width=0) # (left-X, top-Y, right-X, bottom-Y), fill colour, border width
sky 	= canvas.create_rectangle((0, 0, width, height+int(G*s.imag)), fill='lightBlue', width=0)

pentagon = {
	'centre': state.centre(0+0j, state.W+state.H*1j),
	'vertices': polygon(0.6, 5, state.centre(0+0j, state.W+state.H*1j))
}

pentagon['id'] = canvas.create_polygon(tuple( state.toScreen(vertex) for vertex in pentagon['vertices']), fill='orange', width=4)

ball 	= canvas.create_oval(state.worldToScreen(), fill='red')
# ball = canvas.create_image(*state.worldToScreen()[:2], image=window.icon)

#rect = namedtuple('Rect', 'left top right bottom, cx, cy, width, height')(P.real, P.imag, P.real+S.real, P.imag-S.imag, P.real+S.real/2, P.imag-S.imag/2, S.real, S.imag)
#print('BALL\n')
#for attr in rect._fields:
#	print('%s: %.2fm' % (attr, getattr(rect,attr)))


def clickClosure():
	''' Encapsulates data required by the callback '''
	#axisX = canvas.create_line((0, 0, width, 0), width=3, fill='red')
	#axisY = canvas.create_line((0, 0, 0, height), width=3, fill='blue')
	text = canvas.create_text((10,10), text='', anchor=tk.NW, font='Monospace 10')

	follow = False # Let the coordinates follow the cursor

	def showCoords(event):
		''' Prints world and screen coordinates as well as displaying the axes intersecting the cursor '''
		world = state.toWorld(event.x+event.y*1j)
		prev = canvas.coords(text)

		# TODO: Make them line up (...)
		msg  = 'World   | X={:<8}Y={:.2f}m\nScreen | X={:<8}Y={:d}px\n'.format('{:.2f}m,'.format(world[0]), world[1], '{:d}px,'.format(event.x), event.y)
		#ln1 = '|X={:<10}|'.format('{:.2f}m,'.format(world[0]))
		#ln2 = '|X={:<11}|'.format('{:d}px,'.format(event.x))
		canvas.itemconfig(text, text=msg)
		#canvas.move(text, event.x-prev[0], event.y-prev[1])
		
		#canvas.coords(axisX, (event.x, 0, event.x, height))  # Parallel with Y-axis
		#canvas.coords(axisY, (0, event.y, width, event.y)) # Parallel with X-axis

		if follow:
			prev = canvas.bbox(text)
			anch = (tk.N if event.y < (prev[3]-prev[1]) else tk.S) + (tk.E if width-event.x < (prev[2]-prev[0]) else tk.W)
			canvas.itemconfig(text, anchor=anch)

	return showCoords

state.selected = False


def pauseClosure():

	#lockScreen = canvas.create_rectangle((0, 0, width, height), fill='#6666', alpha=0.6, state=tk.HIDDEN)
	lockScreen = canvas.create_text((width//2, height//2), text='Paused', fill='#354E4C', state=tk.HIDDEN, anchor=tk.CENTER, font='Helvetica 32')

	def fade(to, frm, frames):
		# NOTE: Quick and dirty solution for fading in the Paused text

		def delta(channel):
			return (frm[channel]-to[channel])/frames

		dR, dG, dB = delta(0), delta(1), delta(2)
		frames = ('#%.2x%.2x%.2x' % (to[0]+frame*dR, to[1]+frame*dG, to[2]+frame*dB) for frame in range(frames))

		def nextFrame():
			canvas.itemconfig(lockScreen, fill=next(frames))

		return nextFrame


	def togglePause(event):

		window.PAUSE = not window.PAUSE
		canvas.itemconfig(lockScreen, state=[tk.HIDDEN, tk.NORMAL][window.PAUSE])
		canvas.lift(lockScreen)

		if window.PAUSE:
			FPS = 30
			anim = fade((255,255,255), (0x35, 0x4E, 0x4C), FPS) # Animation callback
			for frame in range(FPS):
				# NOTE: Quick and dirty solution for fading in the Paused text
				window.after(int(frame*1.0/FPS*1000), anim)

	return togglePause


def move(event):
	if state.selected:
		print('moving')
		state.P = complex(*state.toWorld(event.x+event.y*1j))
		canvas.coords(ball, state.worldToScreen())


def toggleSelected(selected):
	print('toggle select')
	state.selected = not state.selected
	window.PAUSE   = not window.PAUSE


window.bind('<Motion>', clickClosure())
window.bind('<space>', pauseClosure())
canvas.tag_bind(ball, '<Button-1>', toggleSelected)
canvas.tag_bind(ball, '<ButtonRelease-1>', toggleSelected)
#window.bind('<Motion>', move)


def closure(state):

	''' '''

	count = int(1.2/dt) # Delay / 
	plot  = [canvas.create_oval((-3,-3,0,0), fill='#022EEF', width=0) for x in range(count)]
	plot  = cycle(plot)

	colours = cycle([('#0000%.2x' % r) for r in range(0, 256, 16)])
	#colours = cycle(['orange', 'black', 'purple', 'white', '#22CE4F', 'red', '#FC11CF'])

	#arrow = canvas.create_line(state.toScreen(state.P/10)+state.toScreen((state.P+state.V)/10), arrow=tk.LAST)
	
	arrows = []

	# Construct vector lines and legend from list of vectors and associated colours
	for index, vec in enumerate([(state.V, 'purple'), (state.A, 'orange')]):
		vertices = state.toScreen(state.centre(state.P,state.S))+state.toScreen(state.centre(state.P,state.S)+vec[0]/10) 	# Tuple of endpoint coordinates
		xArrow   = canvas.create_line(vertices[:2]+(vertices[2], vertices[1]), arrow=tk.LAST, width=3, fill=vec[1]) 		# X component
		yArrow   = canvas.create_line(vertices[:2]+(vertices[0], vertices[3]), arrow=tk.LAST, width=3, fill=vec[1]) 		# Y component
		
		legend	 = canvas.create_line((width-30, 30+index*15, width-10, 30+index*15), fill=vec[1], width=6, capstyle=tk.ROUND)
		label	 = canvas.create_text((width-45, 30+index*15), text=('V', 'A')[index], anchor=tk.CENTER)
		arrows.append((xArrow, yArrow, legend, label)) # Append Canvas object IDs


	def drawVector(IDs, vec):
		''' '''
		P, S = state.P, state.S
		vertices = state.toScreen(state.centre(P,S))+state.toScreen(state.centre(P,S)+vec/10)
		canvas.coords(IDs[0], vertices[:2]+(vertices[2], vertices[1]))
		canvas.coords(IDs[1], vertices[:2]+(vertices[0], vertices[3]))


	def movePoint(point, x, y, **options):
		''' '''
		# TODO: Generic plotting capabilities
		coords = canvas.coords(point)
		canvas.move(point, x-coords[0], y-coords[1])
		canvas.itemconfig(point, **options)


	MAX = namedtuple('MAX', 'X Y')(state.W-S.real, state.H)	# TODO: Make this a vector instead (?)
	MIN = namedtuple('MIN', 'X Y')(0, G-S.imag)				# TODO: Make this a vector instead (?)

	# MIN = 0+(G-S.imag)*1j
	# MAX = (state.W-S.real)+state.H*1j


	def animate():

		'''
		Docstring goes here

		'''

		P, V, A, S, T = state.P, state.V, state.A, state.S, state.T # Unpack state
		
		simDt = dt*dtS # Simulation dt

		# Collisions

		# TODO: See if the Canvas has a hidden white border

		# TODO: Check collisions this way for all edges (✓)
		# TODO: Extract bounce behaviour (flipping real part or imag part, etc.)
		# TODO: More sophisticated collisions (tangents, normal force, etc.)
		# TODO: Work out when the collision occurs, don't just reset (✓)
		# TODO: Round velocity down to 0 for very small values (?)
		# TODO: Handle edges cases (eg. multiple collisions within the same frame) (...)
		# TODO: Needs optimizing and simplifying once we're done
		# NOTE: We're giving the ball energy when we're adjusting it s position after a collision.
		# This seems to be the cause of the mysteriously increasing Y-velocity. (solved)

		#tColMin = timeUntil(P, MIN.X+MIN.Y*1j, V, A)  # Top left
		#tColMax = timeUntil(P, MAX.X+MAX.Y*1j, V, A)  # Bottom right

		#xColMin = (0 <= tColMin.real <= simDt)
		#xColMax = (0 <= tColMax.real <= simDt)

		#yColMin = (0 <= tColMin.imag <= simDt)
		#yColMax = (0 <= tColMax.imag <= simDt)

		Tx = 0
		xColl = True
		Px, Vx, Ax = P.real, V.real, A.real

		while xColl:
			xColl, Px, Vx, t = collide(Px, Vx, Ax, simDt-Tx, MIN.X, MAX.X, 1.0)
			if xColl: print(xColl, Px, Vx)
			Tx += t

		Ty = 0
		yColl = True
		Py, Vy, Ay = P.imag, V.imag, A.imag

		while yColl:
			yColl, Py, Vy, t = collide(Py, Vy, Ay, simDt-Ty, MIN.Y, MAX.Y, 0.9)
			Ty += t
			#print('Ty', Ty)

		#if xColMin or xColMax:
		#	# Collide
		#	Tx = tColMax.real if xColMax else tColMin.real	# Time at collision
		#	Px = axisPos(Tx, P.real, V.real, A.real) 		# Position at collision
		#	Vx = -(V.real + A.real*Tx)*0.9 					# Velocity at collision (inverted when it bounces)
		#
		#	# Bounce
		#	# TODO: Check for further collision here
		#	Px = axisPos(simDt-Tx, Px, Vx, A.real)
		#	Vx = Vx + A.real*(simDt-Tx)
		#else:
		#	Px = axisPos(simDt, P.real, V.real, A.real)
		#	Vx = V.real + A.real*simDt
		#
		#if yColMin or yColMax:
		#	# Collide
		#	Ty = tColMax.imag if yColMax else tColMin.imag	# Time at collision
		#	Py = axisPos(Ty, P.imag, V.imag, A.imag) 		# Position at collision
		#	Vy = -(V.imag + A.imag*Ty)*0.9 					# Velocity at collision (inverted when it bounces)
		#
		#	# Bounce
		#	Py = axisPos(simDt-Ty, Py, Vy, A.imag)
		#	Vy = Vy + A.imag*(simDt-Ty)
		#else:
		#	Py = axisPos(simDt, P.imag, V.imag, A.imag)
		#	Vy = V.imag + A.imag*simDt
		

		# This statement is used for debugging timeUntil()
		#print('%.2fs|%.2fm' % { 'Left':    (tColMin.real, P.real),
		#						'Ground':  (tColMin.imag, P.imag+S.imag-G),
		#						'Right':   (tColMax.real, P.real+S.real),
		#						'Ceiling': (tColMax.imag, P.imag) }['Left'])


		# Update position, velocity, time
		#P = position(dt*dtS, state.P, state.V, state.A)
		#V += A*dt*dtS
		P = Px+Py*1j
		V = Vx+Vy*1j
		T += simDt

		#print('X=%.2fm, Y=%.2fm (T=%.2fs)' % (P.real, P.imag, T))
		
		# Redraw
		canvas.coords(ball, state.worldToScreen())
		# canvas.coords(ball, state.worldToScreen()[:2])
		
		pentagon['vertices'] = rotateVertices(0.2*2*π*simDt, pentagon['centre'], *pentagon['vertices'])
		newCoords = ()
		
		for vertex in pentagon['vertices']:
			newCoords += state.toScreen(vertex)
		canvas.coords(pentagon['id'], newCoords)

		for IDs, vec in zip(arrows, (V, A)):
			drawVector(IDs, vec)

		#canvas.coords(arrow, state.toScreen(state.centre(P,S))+state.toScreen(P+V/10))
		
		movePoint(next(plot), *state.toScreen(state.centre(P,S)), fill=next(colours))

		state.P, state.V, state.A, state.S, state.T = P, V, A, S, T

		# Plot
		# TODO: Reuse items (✓)

	def wrapper():
		''' Provides administrative logic for the animate() function '''
		# Check if paused
		if not window.PAUSE:
			animate()
		window.after(int(dt*1000), wrapper) # Schedule the next frame, in dt * 1000 milliseconds

	return wrapper

state.animator = closure(state)
state.animator()

def changeA():
	state.A = float(input())*1j

changeA()

window.mainloop()