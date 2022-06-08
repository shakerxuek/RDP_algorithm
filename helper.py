from RDP import ramer_douglas_peucker
import shapefile

def processShapefile(filePath, frameSize, epsilon):

	sf = shapefile.Reader(filePath)

	shapeTypeString = None

	if sf.shapeType == 3 or sf.shapeType == 13 or sf.shapeType == 23:
		shapeTypeString = 'LINESTRING'
	elif sf.shapeType == 5 or sf.shapeType == 15 or sf.shapeType == 25:
		shapeTypeString = 'POLYGON'
	else:
		raise ValueError('Shape type was not identified!')

	shapes = sf.shapes()

	minX = min(shapes, key=lambda shape: shape.bbox[0]).bbox[0]
	minY = min(shapes, key=lambda shape: shape.bbox[1]).bbox[1]
	maxX = max(shapes, key=lambda shape: shape.bbox[2]).bbox[2]
	maxY = max(shapes, key=lambda shape: shape.bbox[3]).bbox[3]

	rangeX = maxX - minX
	rangeY = maxY - minY

	# Used to adjust shapefile format when transforming to pixel coordinates (hackish way to convert coordinates)
	ratioX = rangeX/rangeY
	ratioY = rangeY/rangeX
	#print(ratioX, ratioY)

	if ratioX > 1:
		ratioX = 1
	if ratioY > 1:
		ratioY = 1

	# Size of frame
	sizeMax = frameSize
	sizeMin = 0
	rangeFinal = sizeMax - sizeMin

	def normalize(point):
		x = ((point[0] - minX) / rangeX) * rangeFinal * ratioX + sizeMin
		# Subtracting by sizeMax to flip the map
		y = abs(((point[1] - minY) / rangeY) * rangeFinal * ratioY - sizeMax)
		return str(x) + ' ' + str(y)

	shapeFull = []
	shapeRedux = []

	for shape in shapes:
		points = shape.points
		# Simplify points!
		fewerPoints = ramer_douglas_peucker(points, epsilon)

		# Normalize values
		points = list(map(lambda p: normalize(p), points))
		fewerPoints = list(map(lambda p: normalize(p), fewerPoints))
		
		geometry = shapeTypeString + '((' + ','.join(points) + '))\n'
		geometryRedux = shapeTypeString + '((' + ','.join(fewerPoints) + '))\n'
		
		shapeFull.append(geometry)
		shapeRedux.append(geometryRedux)
	
	return shapeFull, shapeRedux