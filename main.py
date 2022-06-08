# tkinter_example.py
# Based on template written by Ben Knoechel, Oct 25, 2012.

# Because I import Tkinter, I have to preceed every method defined in Tkinter
# with Tkinter.etc. This is actually not good style but I do this to emphasis
# ONE consistent way of importing modules in Python, you could use
#
# from Tkinter import *
import tkinter as Tkinter
from tkinter.filedialog import askopenfilename
from helper import processShapefile
import random

class ExampleTk:
	
	def __init__(self,master):

		# Setting static window size
		master.resizable(width=False, height=False)

		master.wm_title('Ramer–Douglas–Peucker algorithm')
		master.iconbitmap('icon.ico')

		# Creating menu
		menuBar = Tkinter.Menu(master)

		fileMenu = Tkinter.Menu(menuBar, tearoff=0)
		fileMenu.add_command(label="Open", command=self.open_file)
		fileMenu.add_separator()
		fileMenu.add_command(label="Exit", command=master.destroy)

		shapeMenu = Tkinter.Menu(menuBar, tearoff=0)
		shapeMenu.add_command(label="Draw", command=self.draw_geometry)
		shapeMenu.add_separator()
		shapeMenu.add_command(label="Reset", command=self.reset)

		menuBar.add_cascade(label="File", menu=fileMenu)
		menuBar.add_cascade(label="Shape", menu=shapeMenu)
		master.config(menu=menuBar)

		# We create a frame as our high level container
		frame = Tkinter.Frame(master)
		frame.pack()

		# Shapefile info label
		self.var = Tkinter.StringVar()
		label = Tkinter.Label(frame, textvariable=self.var)
		self.var.set("No shapefile selected.")
		label.pack(side=Tkinter.TOP)

		# Epsilon label and text widget
		epFrame = Tkinter.Frame(frame)
		epFrame.pack()
		
		epVar = Tkinter.StringVar()
		epLabel = Tkinter.Label(epFrame, textvariable=epVar)
		epVar.set("RDP Epsilon: ")
		epLabel.pack(side=Tkinter.LEFT)

		# Forcing user to only type number
		vcmd = (master.register(self.validate),
				'%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
		self.epsilon_text = Tkinter.Entry(epFrame, validate = 'key', validatecommand=vcmd)
		self.epsilon_text.pack(side=Tkinter.LEFT)

		# Canvas widget, keep reference in self.map
		self.frameSize = 500
		self.offset = 10
		self.map = Tkinter.Canvas(frame, width=self.frameSize, height=self.frameSize, bg='white')
		self.map.pack(side=Tkinter.LEFT)

		self.mapRedux = Tkinter.Canvas(frame, width=self.frameSize, height=self.frameSize, bg='white')
		self.mapRedux.pack(side=Tkinter.RIGHT)

		self.fileName = None
		self.shapeFull = None
		self.shapeRedux = None
		self.lastEpsilon = None

	# Validate epsilon input
	def validate(self, action, index, value_if_allowed,
					   prior_value, text, validation_type, trigger_type, widget_name):

		if text == '' or value_if_allowed == '' or (str.isdigit(text) and value_if_allowed != '' and int(value_if_allowed) > 0):
			return True
		else:
			return False
	
	# Search and open file
	def open_file(self):
		self.fileName = askopenfilename(filetypes=[("Shapefiles", "*.shp")])
		self.var.set(self.fileName[self.fileName.rfind('/') + 1:])
		# Try to process if epsilon was set
		self.processShapefile()
		# Try to draw full shape right after being loaded
		self.draw_geometry(full_shape_only=True)

	def processShapefile(self, full_shape_only=False):
		tmpEpsilon = self.epsilon_text.get()
		self.map.delete(Tkinter.ALL)
		self.mapRedux.delete(Tkinter.ALL)
		if tmpEpsilon != '' and int(tmpEpsilon) > 0:
			
			full, redux = processShapefile(self.fileName, self.frameSize - 2*self.offset, int(tmpEpsilon))
			
			self.shapeFull = ''.join(full)
			self.shapeRedux = ''.join(redux)
			self.lastEpsilon = tmpEpsilon
		elif full_shape_only:
			full, _ = processShapefile(self.fileName, self.frameSize - 2*self.offset, 1)
			self.shapeFull = ''.join(full)

	# Clears the canvas
	def reset(self):
		self.map.delete(Tkinter.ALL)
		self.mapRedux.delete(Tkinter.ALL)
		self.shapeFull = None
		self.shapeRedux = None
		self.lastEpsilon = None

	def draw_geometry(self, full_shape_only=False):
		if self.shapeFull == None or self.shapeRedux == None or self.lastEpsilon != self.epsilon_text.get():
			self.processShapefile()

		if self.shapeFull != None and self.shapeRedux != None and self.epsilon_text.get() != '':
			self.draw_on_map(self.map, self.shapeFull, self.offset)
			self.draw_on_map(self.mapRedux, self.shapeRedux, self.offset)
		elif full_shape_only:
			self.processShapefile(full_shape_only=True)
			self.draw_on_map(self.map, self.shapeFull, self.offset)

	def draw_on_map(self, mapFrame, shape, offset):

		mapFrame.delete(Tkinter.ALL)
		lines = shape.split('\n')
		plotPoints = []
		pointSize = 2
		
		for line in lines:
			try:
				# Put line into s to save some typing
				s = line.lower()
				
				if s.startswith('point'):
					s = s.replace('point','').strip().strip('(').strip(')').strip()
					p = s.split()
					p = [float(p[0]) + offset, float(p[1]) + offset]
					# Oval is defined by a rectangle, we create a 6x6 square
					# centered over the point and it draws a circle for us
					mapFrame.create_oval(p[0]-pointSize, p[1]-pointSize, p[0]+pointSize, p[1]+pointSize, fill='black')
					
				elif s.startswith('linestring'):
					s = s.replace('linestring','').strip().strip('(').strip(')').strip()
					s = s.split(',')
					
					coordinates = list(map(lambda p:(float(p.split()[0]) + offset, float(p.split()[1]) + offset), s))
					points = [item for sublist in coordinates for item in sublist]
					plotPoints.extend(coordinates)

					# To use random colors for each line..
					#[...]fill="#"+("%06x"%random.randint(0,16777215)))
					
					mapFrame.create_line(points, width=4, fill='orange')
					
				elif s.startswith('polygon'):
					s = s.replace('polygon','').strip().strip('(').strip(')').strip()
					s = s.split(',')

					coordinates = list(map(lambda p:(float(p.split()[0]) + offset, float(p.split()[1]) + offset), s))
					points = [item for sublist in coordinates for item in sublist]
					plotPoints.extend(coordinates)

					# To use random colors for each polygon..
					#[...]fill="#"+("%06x"%random.randint(0,16777215)))

					mapFrame.create_polygon(points[:-2], fill="orange")
				else:
					continue
			except:
				# Usually I would alert the user
				# In this case, if I didn't understand a line of WKT, just
				# ignore it, move to next line from text widget
				None
		
		for point in plotPoints:
			x = point[0]
			y = point[1]
			mapFrame.create_oval(x-pointSize, y-pointSize, x+pointSize, y+pointSize, fill='black')

# Code to actually create a Tk GUI
r = Tkinter.Tk()
e = ExampleTk(r)
r.mainloop()
