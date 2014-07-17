# Showing Jay how to create windows with tkinter

import tkinter as tk

size = width, height = 300, 300

window = tk.Tk()
window.title('Newtonian')
window.geometry('%dx%d' % size)

canvas = tk.Canvas(width=width, height=height)
canvas.pack()

S = 0.2+0.2j 	# Size (m)
s = 100.0-100j 	# Scale (px/m) # TODO: Make this a vector too (✓)

P = 0.05+2.8j	# Position vector (m)
A = 0-9.82j 	# Acceleration vector (m/s^2)
V = 2.6-3.6j	# Velocity vector (m/s)

FPS = 30
dt = 1.0/FPS # Time between consecutive frames (s)

ground 	= canvas.create_rectangle((0, height-20, width, height), fill='green', width=0) # (left-X, top-Y, right-X, bottom-Y), fill colour, border width
sky 	= canvas.create_rectangle((0, 0, width, height-20), fill='lightBlue', width=0)
ball 	= canvas.create_oval((P.real*s.real, P.imag*s.imag, (P.real+S.real)*s.real, (P.imag+S.imag)*s.imag), fill='red')

class AnimationState:
	def __init__(self, P, V, A):
		self.P = P 	 # Position vector
		self.V = V 	 # Velocity vector
		self.A = A 	 # Acceleration vector
		self.T = 0.0 # Time

def closure(P, V, A):
	state = AnimationState(P, V, A)
	def animate():
		P, V, A, T = state.P, state.V, state.A, state.T
		V += A*dt
		P += V*dt
		T += dt

		print('X=%.2fm, Y=%.2fm (T=%.2fs)' % (P.real, P.imag, T))
	
		canvas.coords(ball, (P.real*s.real, P.imag*s.imag, (P.real+S.real)*s.real, (P.imag+S.imag)*s.imag))
		state.P, state.V, state.A, state.T = P, V, A, T
		window.after(int(dt*1000), animate)
		
	return animate

closure(P, V, A)()

window.mainloop()