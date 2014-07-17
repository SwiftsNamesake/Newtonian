# Showing Jay how to create windows with tkinter

import tkinter as tk

size = width, height = 300, 300

window = tk.Tk()
window.title('Newtonian')
window.geometry('%dx%d' % size)

canvas = tk.Canvas(width=width, height=height)
canvas.pack()

S = 0.2+0.2j # Size (m)
s = 100.0 	 # Scale (px/m) # TODO: Make this a vector too (check)

P = (5+5j)/s	# Position vector (m)
A = 0+9.82j 	# Acceleration vector (m/s^2)
V = 2.6-3.6j	# Velocity vector (m/s)

FPS = 30
dt = 1.0/FPS # Time between consecutive frames (s)

ground 	= canvas.create_rectangle((0, height-20, width, height), fill='green', width=0) # (left-X, top-Y, right-X, bottom-Y), fill colour, border width
sky 	= canvas.create_rectangle((0, 0, width, height-20), fill='lightBlue', width=0)
ball 	= canvas.create_oval((P.real*s, P.imag*s, (P.real+S.real)*s, (P.imag+S.imag)*s), fill='red')


def closure(P, V, A):
	vectors = [P, V, A]
	T = 0
	def animate():
		P, V, A = vectors
		V += A*dt
		P += V*dt
	
		canvas.coords(ball, (P.real*s, P.imag*s, (P.real+S.real)*s, (P.imag+S.imag)*s))
		print('X=%dm, Y=%dm (t=%fs)', (P.real, P.imag, 0.0))
		window.after(int(dt*1000), animate)
		vectors[:] = [P, V, A]
	return animate

closure(P, V, A)()

window.mainloop()