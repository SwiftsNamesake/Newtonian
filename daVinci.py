#
# Newtonian - daVinci.py
#
# Jonatan H Sundqvist
# Jayant Shivarajan
#
# August 1 2014
#
# Desc
#

# TODO | - Use annotations (?)
#		 - Assert, robustness, handling and checking errors
#		 - Decouple coordinate system from tkinter (?)
#		 	-- Would facilitate slow (floating-point) animation
#		 - Expose separate draw API to (or via) Sprites (?)
#		 	- Drawbacks: potential circular-reference, performance (?), more work
#		 	- Advantages: greater consistency, allows higher-level operations, makes Sprites reusable
#		 - Direct coupling to Newton (?)
#		 - Invisible objects, view ports


# SPEC | - 
#		 -


import tkinter as tk

from PIL.ImageTk import PhotoImage, Image
from math import sin, cos

def choose(optional, default):
	return optional if optional is not None else default


class Sprite:

	'''
	Docstring goes here

	'''

	def __init__(self, canvas, vertices, shape, image=None, animator=None, **options):
		
		''' '''

		# TODO: Make sure wrapper is synched with canvas object (gettattr?)
		# TODO: Normalize position arg

		# Normalize arguments
		if image is not None:
			self.image = PhotoImage(Image.open(image)) if isinstance(image, str) else image
			options['image'] = self.image
			shape = 'image'

		# Initialize properties, create sprite
		self.canvas = canvas
		self.shape 	= shape
		self.id 	= self.shapeMethod(shape)(vertices, **options)

		self.visible 	= canvas.itemcget(self.id, 'state') == tk.NORMAL
		self.pos 		= self.position()

		self.animator = choose(animator, lambda sprite, dt: None) # TODO: Make bound method somehow (?)


	def shapeMethod(self, shape):

		''' '''

		return {
			'rectangle': self.canvas.create_rectangle,
			'oval': 	 self.canvas.create_oval,
			'polygon': 	 self.canvas.create_polygon,
			'image': 	 self.canvas.create_image
		}[shape]


	def visible(self, visible=None, toggle=None):
		''' Retrieves or sets visibility '''
		if visible == toggle == None:
			return canvas.itemcget(self.id, 'state') == tk.NORMAL
		elif visible != None:
			canvas.itemconfig('state', tk.NORMAL if visible else tk.HIDDEN)
		else:
			canvas.itemconfig('state', not self.visible())


	def animate(self, dt):

		''' '''

		self.animator(self, dt)


	def attributes(self, *attributes, **overrides):
		''' Sets or retrieves item related Canvas attributes '''
		# TODO: Allow simultaneous setting and retrieving?

		if len(overrides > 0):
			self.canvas.itemconfig(self.id, **overrides)

		if len(attributes) > 0:
			values = {}
			for attr in attributes:
				values[attr] = self.canvas.itemcget(self.id, attr)
			return values
		

	def position(self, x=None, y=None):
		''' Sets or retrieves position '''
		if x == y == None:
			return self.canvas.coords(self.id)



class daVinci:

	'''
	Docstring goes here

	'''

	def __init__(self, size):

		''' '''
		
		# TODO: Tags, IDs, sprite queries (currently uses Canvas id)

		# Initialize properties
		# TODO: Make sure canvas is packed correctly
		self.size 	= size
		self.canvas = tk.Canvas(width=size[0], height=size[1])
		self.canvas.pack()

		self.sprites = []


		# Animation
		self.FPS = 30			# Frames per second
		self.dt  = 1/self.FPS 	# Time between consecutive frames


	def addSprite(self, vertices, shape, sprite=None, image=None, animator=None, **options):

		''' '''

		sprite = choose(sprite, Sprite(self.canvas, vertices, shape, image=image, animator=animator, **options))
		self.sprites.append(sprite)
		return sprite.id


	def animate(self):

		''' '''

		for sprite in self.sprites:
			sprite.animate(self.dt)


	def begin(self, window):
		
		''' '''

		self.animate()
		window.after(int(self.dt*1000), lambda: self.begin(window))



def moveApple():
	frame = 0
	def closure(shape, dt):
		nonlocal frame
		shape.canvas.move(shape.id, int(60*dt), int(50*sin(dt*(frame+1))-50*sin(dt*(frame))))
		print(int(50*(sin(dt*(frame+1))-sin(dt*(frame)))))
		frame += 1
	return closure


def main():

	''' '''

	win = tk.Tk()
	win.geometry('%dx%d' % (1920//2, 1080//2))

	Image.open('apple.png')

	painter = daVinci((1920//2, 1080//2))
	painter.addSprite((20, 45, 66, 93), 'rectangle', fill='blue', animator=lambda shape, dt: shape.canvas.move(shape.id, int(50*dt),int(50*dt)))
	painter.addSprite((20, 45, 66, 93), 'oval', fill='yellow', animator=lambda shape, dt: shape.canvas.move(shape.id, int(82*dt),int(30*dt)))
	painter.addSprite(((20, 45), (66, 93), (2, 70)), 'polygon', fill='orange', animator=lambda shape, dt: shape.canvas.move(shape.id, int(10*dt),int(50*dt)))
	painter.addSprite((35, 200), 'image', image='apple.png', animator=moveApple())
	painter.begin(win)
	# 

	win.mainloop()


if __name__ == '__main__':
	main()