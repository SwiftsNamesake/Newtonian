# Showing Jay how to create windows with tkinter

import tkinter as tk

from collections import namedtuple

size = width, height = 300, 300

window = tk.Tk()
window.title('Newtonian')
window.geometry('%dx%d' % size)

canvas = tk.Canvas(width=width, height=height)
canvas.pack()


class AnimationState:
	def __init__(self, P, V, A, S, O):
		# Physics
		self.P = P 	 # Position vector
		self.V = V 	 # Velocity vector
		self.A = A 	 # Acceleration vector
		self.S = S 	 # Size vector # TODO: Make this a real vector (ie invert Y)
		self.T = 0.0 # Time

		# Coordinates
		
		self.s = 100-100j 		# Scale (px/m)
		self.W = abs(300/self.s.real)
		self.H = abs(300/self.s.imag) # TODO: Convert to world coords (✓); Extract width and height
		self.O = 0.0+self.H*1j 	# Offset (m) (world origin -> screen origin)


	def pointToScreenCoords(self, point):
		#
		return (int((point.real-self.O.real)*self.s.real), int((point.imag-self.O.imag)*self.s.imag)) # TODO: Allow X origin offset (✓)

	def pointToWorldCoords(self, point):
		#
		return ((point.real/self.s.real)+self.O.real, (point.imag/self.s.imag)+self.O.imag)

	def worldToScreen(self):
		# TODO: Implement world-space to screen space method
		TOPLEFT = self.pointToScreenCoords(self.P)
		BOTTOMRIGHT = self.pointToScreenCoords(self.P+self.S)
		#screen = ((P.real+self.O.real)*s.real, (P.imag+self.O.imag)*s.imag, (P.real+S.real+self.O.imag)*s.real, (P.imag+S.imag+self.O.real)*s.imag)
		screen = TOPLEFT + BOTTOMRIGHT
		#print('X: %.2fpx, Y: %.2fpx' % screen[:2])
		#print('Width: %dpx, Height: %dpx' % (screen[2]-screen[0], screen[1]-screen[3]))
		return screen



# TODO: Encapsulate coordinate system conversion logic (cf. AnimationState) (...)
s = 100.0-100j 	# Scale vectpr (px/m) # TODO: Make this a vector too (✓)
G = 0.2 		# Ground height (m)
S = 0.2-0.2j 	# Size vector (distance from top left) (m)

W = width/s.real  # TODO: Fix this value ?
H = height/s.imag # TODO: Fix this value

O = 0.0+H*1j 	# Offset between world origin and screen origin

P = 0.05+0.8j	# Position vector (top left) (m)
A = 0.09-9.82j 	# Acceleration vector (m/s^2)
V = 0.60+5.6j	# Velocity vector (m/s)

FPS = 30 	  # Frames per second
dt  = 1.0/FPS # Time between consecutive frames (s)

state = AnimationState(P, V, A, S, O)

ground 	= canvas.create_rectangle((0, height+int(G*s.imag), width, height), fill='green', width=0) # (left-X, top-Y, right-X, bottom-Y), fill colour, border width
sky 	= canvas.create_rectangle((0, 0, width, height+int(G*s.imag)), fill='lightBlue', width=0)
ball 	= canvas.create_oval(state.worldToScreen(), fill='red')

#rect = namedtuple('Rect', 'left top right bottom, cx, cy, width, height')(P.real, P.imag, P.real+S.real, P.imag-S.imag, P.real+S.real/2, P.imag-S.imag/2, S.real, S.imag)
#print('BALL\n')
#for attr in rect._fields:
#	print('%s: %.2fm' % (attr, getattr(rect,attr)))


def clickClosure():
	text = canvas.create_text((0,0), text='', anchor=tk.SW)
	def printCoords(event):
		''' Prints world and screen coordinates '''
		world = state.pointToWorldCoords(event.x+event.y*1j)
		prev = canvas.coords(text)

		canvas.move(text, event.x-prev[0], event.y-prev[1])
		canvas.itemconfig(text, text='World|X=%.2fm, Y=%.2fm\nScreen|X=%dpx, Y=%dpx' % (world + (event.x, event.y)))

	return printCoords


window.bind('<Motion>', clickClosure())

def closure(state):
	def animate():
		# Calculate position
		P, V, A, S, T = state.P, state.V, state.A, state.S, state.T
		V += A*dt # Is this correct ?
		P += V*dt # Is this corect ?
		T += dt   # Increment time

		# Collisions
		# TODO: Extract bounce behaviour (flipping real part or imag part, etc.)
		# TODO: See if the Canvas has a hidden white border
		if (P+S).imag <= G:
			V = (V.real+abs(V.imag)*1j) # Collide with ground
			P = P.real+(G-S.imag)*1j
		elif P.imag >= state.H:
			V = (V.real-abs(V.imag)*1j) # Collide with 'ceiling'
			P = P.real+state.H*1j

		if P.real <= 0:
			V = (abs(V.real)+V.imag*1j) # Collide with ground
			P = 0+P.imag*1j
		elif (P+S).real >= state.W:
			V = (-abs(V.real)+V.imag*1j) # Collide with ground
			P = (state.W-S.real)+P.imag*1j
		#print('X=%.2fm, Y=%.2fm (T=%.2fs)' % (P.real, P.imag, T))
		
		# Redraw
		canvas.coords(ball, state.worldToScreen())
		state.P, state.V, state.A, state.S, state.T = P, V, A, S, T
		window.after(int(dt*1000), animate) # Schedule the next frame, in dt * 1000 milliseconds

	return animate

closure(state)()

window.mainloop()