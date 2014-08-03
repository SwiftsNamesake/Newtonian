#
# Newtonian - Westminister.py
#
# Jonatan H Sundqvist
# Jayant Shivarajan
#
# August 1 2014
#
# Desc
#

# TODO | - Support for commands and key bindings in JSON files (?)
#		 - 
#		 - 

# SPEC | - 
#		 -


import tkinter as tk 	# Windows and events
import daVinci			# Drawing and animation

from PIL.ImageTk import Image, PhotoImage


class Westminster:

	'''
	Docstring goes here

	'''

	def __init__(self, size=(300, 300), title='Newtonian', icon='apple.ico'):

		''' '''

		#
		self.window = self.createWindow(size, title, icon)
		self.run()

		#


	def createWindow(self, size : (int, int), title : str, icon : str) -> 'Window':

		''' '''

		# Create and configure window
		window = tk.Tk()
		window.title(title)
		window.size = size
		window.geometry('%dx%d' % window.size)
		
		# Set icon
		window.icon = PhotoImage(Image.open(icon))
		window.call('wm', 'iconphoto', window._w, window.icon)

		return window


	def createMenus(self):
		
		''' '''

		menubar = tk.Menu()
		return menubar


	def bindEvents(self):
		
		''' '''

		window.bind('<Motion>', clickClosure())
		window.bind('<space>', pauseClosure())
		canvas.tag_bind(ball, '<Button-1>', toggleSelected)
		canvas.tag_bind(ball, '<ButtonRelease-1>', toggleSelected)
		#window.bind('<Motion>', move)


	def run(self):
		
		''' '''

		self.window.mainloop()



if __name__ == '__main__':
	app = Westminister()