# Showing Jay how to create windows with tkinter

import tkinter as tk

size = width, height = 300, 300

window = tk.Tk()
window.title('Newtonian')
window.geometry('%dx%d' % size)

canvas = tk.Canvas(width=width, height=height)
canvas.pack()

ground = canvas.create_rectangle((0, height-20, width, height), fill='green', width=0) # (left-X, top-Y, right-X, bottom-Y), fill colour, border width
sky = canvas.create_rectangle((0, 0, width, height-20), fill='lightBlue', width=0)

ball = canvas.create_oval((5, 5, 30, 30), fill='red')

window.mainloop()