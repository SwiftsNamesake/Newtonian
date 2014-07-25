#
# test.py
#
# Jonatan H Sundqvist
# Jayant Shivarajan
# July 10 2014
#
# Showing Jay how to create windows with tkinter
#

# TODO | - Vector alias for complex numbers (?)
#		 -

# SPEC | - 
#		 -


import tkinter as tk

from collections import namedtuple	#
from itertools import cycle			# Used for iterating over plot points

from cmath import polar, rect, pi as π
from math import copysign, sqrt, sin

size = width, height = 720, 480

window = tk.Tk()
window.title('Newtonian')
window.geometry('%dx%d' % size)

canvas = tk.Canvas(width=width, height=height, bd=0)
canvas.pack()

window.PAUSE = False

class AnimationState:

	''' '''

	# TODO: Facilities for pretty printing simulation state (translucent tk.Text?)

	def __init__(self, P, V, A, S, O, W, H):
	#def __init__(self, P : 'Position vector', V : 'Velocity vector', A : 'Acceleration vector', S : 'Scale vector', O : 'Origin offset'):
		# Physics
		self.P = P 	 # Position vector
		self.V = V 	 # Velocity vector
		self.A = A 	 # Acceleration vector
		self.S = S 	 # Size vector # TODO: Make this a real vector (ie invert Y)
		self.T = 0.0 # Time

		# Coordinates
		
		self.s = 100-100j 		# Scale (px/m)
		self.W = W
		self.H = H # TODO: Convert to world coords (✓); Extract width and height (✓)
		self.O = 0.0+self.H*1j 	# Offset (m) (world origin -> screen origin)


	def pointToScreenCoords(self, point):
		''' Converts from world space to canvas space '''
		# TODO: Rename (?)
		return (int((point.real-self.O.real)*self.s.real), int((point.imag-self.O.imag)*self.s.imag)) # TODO: Allow X origin offset (✓)


	def pointToWorldCoords(self, point):
		''' Converts from canvas space to world space '''
		# TODO: Rename (?)
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
		TOPLEFT = self.pointToScreenCoords(self.P)
		BOTTOMRIGHT = self.pointToScreenCoords(self.P+self.S)
		#screen = ((P.real+self.O.real)*s.real, (P.imag+self.O.imag)*s.imag, (P.real+S.real+self.O.imag)*s.real, (P.imag+S.imag+self.O.real)*s.imag)
		screen = TOPLEFT + BOTTOMRIGHT
		#print('X: %.2fpx, Y: %.2fpx' % screen[:2])
		#print('Width: %dpx, Height: %dpx' % (screen[2]-screen[0], screen[1]-screen[3]))
		return screen



# TODO: Encapsulate coordinate system conversion logic (cf. AnimationState) (...)
# TODO: Encapsulate animation and related parameters (cf. AnimationState)
s = 100.0-100j 	# Scale vector (px/m) # TODO: Make this a vector too (✓)
G = 0.2 		# Ground height (m)
S = 0.2-0.2j 	# Size vector (distance from top left) (m)

W = abs(width/s.real)  # TODO: Fix this value ?
H = abs(height/s.imag) # TODO: Fix this value

O = 0.0+H*1j 	# Offset between world origin and screen origin

P = 0.15+0.8j	# Position vector (top left) (m)
A = 0.00-9.82j 	# Acceleration vector (m/s^2)
#V = 2.06+2.6j	# Velocity vector (m/s)
V = rect(2.0, 20*π/180.0)

FPS = 30 	  # Frames per second
dt  = 1.0/FPS # Time between consecutive frames (s)
dtS = 1.0 	  # Scale of dt
# TODO: Decouple real dt and simulation dt (?) (...)

state = AnimationState(P, V, A, S, O, W, H)

ground 	= canvas.create_rectangle((0, height+int(G*s.imag), width, height), fill='green', width=0) # (left-X, top-Y, right-X, bottom-Y), fill colour, border width
sky 	= canvas.create_rectangle((0, 0, width, height+int(G*s.imag)), fill='lightBlue', width=0)
ball 	= canvas.create_oval(state.worldToScreen(), fill='red')

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
		world = state.pointToWorldCoords(event.x+event.y*1j)
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


def pause(event):
	window.PAUSE = not window.PAUSE


def move(event):
	if state.selected:
		print('moving')
		state.P = complex(*state.toWorld(event.x+event.y*1j))
		canvas.coords(ball, state.worldToScreen())


def toggleSelected(selected):
	print('toggle select')
	state.selected = not state.selected
	window.PAUSE = not window.PAUSE


window.bind('<Motion>', clickClosure())
window.bind('<space>', pause)
canvas.tag_bind(ball, '<Button-1>', toggleSelected)
canvas.tag_bind(ball, '<ButtonRelease-1>', toggleSelected)
window.bind('<Motion>', move)



def position(t, p0, v0, a):
	''' Calculates position as a function of time, based on initial position, initial velocity, and acceleration '''
	# TOOD: Oxford comma (?)
	# TODO: Better names (?)
	# TODO: Explain proof (?)

	def p(pos, vel, acc):
		return (pos + vel*t + (1/2)*acc*t**2)

	return p(p0.real, v0.real, a.real)+p(p0.imag, v0.imag, a.imag)*1j # x + yi


def timeUntil(P : 'vector', V : 'vector', A) -> 'vector':
	''' Calculates time until object has reached 0 (separately for X and Y) '''
	# TODO: Reaches a given point instead (?)
	#dt = sqrt(2*dy/abs(A.imag)) + 2*V.imag/abs(A.imag)
	dtX = -V.real/A.real + sqrt((V.real**2/A.real-2*P.real)/A.real) if A.real != 0 else -P.real/V.real
	dtY = -V.imag/A.imag + sqrt((V.imag**2/A.imag-2*P.imag)/A.imag) if A.imag != 0 else -P.imag/V.imag

	return dtX+dtY*1j


def closure(state):

	''' '''

	count = int(1.2/dt) # Delay / 
	plot  = [ canvas.create_oval((-3,-3,0,0), fill='#022EEF', width=0) for x in range(count) ]
	plot  = cycle(plot)

	#arrow = canvas.create_line(state.toScreen(state.P/10)+state.toScreen((state.P+state.V)/10), arrow=tk.LAST)
	
	arrows = []

	# Construct vector lines and legend from list of vectors and associated colours
	for index, vec in enumerate([(state.V, 'purple'), (state.A, 'green')]):
		vertices = state.toScreen(state.centre(state.P,state.S))+state.toScreen(state.centre(state.P,state.S)+vec[0]/10) # Tuple of endpoint coordinates
		xArrow   = canvas.create_line(vertices[:2]+(vertices[2], vertices[1]), arrow=tk.LAST, fill=vec[1]) # X component
		yArrow   = canvas.create_line(vertices[:2]+(vertices[0], vertices[3]), arrow=tk.LAST, fill=vec[1]) # Y component
		
		legend	 = canvas.create_line((width-30, 30+index*15, width-10, 30+index*15), fill=vec[1], width=6, capstyle=tk.ROUND)
		label	 = canvas.create_text((width-45, 30+index*15), text=('V', 'A')[index], anchor=tk.CENTER)
		arrows.append((xArrow, yArrow, legend, label)) # Append Canvas object IDs


	def drawVector(IDs, vec):
		P, S = state.P, state.S
		vertices = state.toScreen(state.centre(P,S))+state.toScreen(state.centre(P,S)+vec/10)
		canvas.coords(IDs[0], vertices[:2]+(vertices[2], vertices[1]))
		canvas.coords(IDs[1], vertices[:2]+(vertices[0], vertices[3]))


	def movePoint(point, x, y):
		coords = canvas.coords(point)
		canvas.move(point, x-coords[0], y-coords[1])

	MIN = namedtuple('MIN', 'X Y')(0, G-S.imag)				# TODO: Make this a vector instead (?)
	MAX = namedtuple('MAX', 'X Y')(state.W-S.real, state.H)	# TODO: Make this a vector instead (?)

	def animate():

		''' '''

		# Calculate position
		P, V, A, S, T = state.P, state.V, state.A, state.S, state.T # Unpack state
		

		# TODO: Check collisions this way for all edges (...)
		tColMin = timeUntil(MIN.X+MIN.Y*1j, V, A)  # Top left
		tColMax = timeUntil(MAX.X+MAX.Y*1j, V, A) # Bottom right

		simDt = dt*dtS

		for T in (tColMin.real, tColMin.imag, tColMax.real, tColMax.imag):
			if 0 <= T < simDt:
				# We will collide within this frame
				pass
				#print('DT: %.2f' % T)
		#		# TODO: Solve by splitting animation frame into pre-collision, post-collision (?)
		#		P = P.real+MIN.Y*1j
		#		V = V.real+abs(V.imag)*1j # Collide with ground
		#		#simDt += tCol
			
		print('%.2fs|%.2fm' % (tColMin.imag, P.imag+S.imag-G))

		# Update position, velocity, time
		P = position(dt*dtS, state.P, state.V, state.A)
		V += A*dt*dtS
		T += dt*dtS

		# Collisions
		# TODO: Extract bounce behaviour (flipping real part or imag part, etc.)
		# TODO: See if the Canvas has a hidden white border
		# TODO: Work out when the collision occurs, don't just reset
		# NOTE: We're giving the ball energy when we're adjusting its position after a collision.
		# This seems to be the cause of the mysteriously increasing Y-velocity.

		if P.imag <= MIN.Y:
			#print('ground')
			#V = V.conjugate()
			V = V.real+abs(V.imag)*1j # Collide with ground
			P = P.real+MIN.Y*1j
		elif P.imag >= MAX.Y:
			#print('ceiling')
			#V = V.conjugate()
			V = V.real-abs(V.imag)*1j # Collide with 'ceiling'
			P = P.real+MAX.Y*1j

		if P.real <= MIN.X:
			#print('left')
			V = abs(V.real)+V.imag*1j # Collide with left edge
			P = MIN.X+P.imag*1j
		elif P.real >= MAX.X:
			#print('right')
			V = -abs(V.real)+V.imag*1j # Collide with right edge
			P =  MAX.X+P.imag*1j

		#print('X=%.2fm, Y=%.2fm (T=%.2fs)' % (P.real, P.imag, T))
		
		# Redraw
		canvas.coords(ball, state.worldToScreen())
		
		for IDs, vec in zip(arrows, (V, A)):
			drawVector(IDs, vec)

		#canvas.coords(arrow, state.toScreen(state.centre(P,S))+state.toScreen(P+V/10))
		
		movePoint(next(plot), *state.toScreen(state.centre(P,S)))

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

window.mainloop()