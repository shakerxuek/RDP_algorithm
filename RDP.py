# part B
from Lab3 import Point_distance 
#To avoid the problem that two points maybe too close to each other, I have made a little change to the Q9 of Lab3 with a if condition.

def ramer_douglas_peucker(points, epsilon):
	# firstly, we use a loop to find out which point has the largest distance from the imaginary line passing through the first and the last points
	lardist=0.0
	num=0
	results=[]
	for i in range(1,len(points)-1):
		dist=Point_distance(points[i],points[0],points[-1])
		if dist>lardist:
			lardist=dist
			num=i
	# then we try to compare the largest distance with the epsilon to check whether this point should be reserved	
	if lardist>=epsilon:
		results=ramer_douglas_peucker(points[:num+1],epsilon)+ramer_douglas_peucker(points[num:],epsilon)
		# we separate all the points into two list according to the position of the point with maximum distance
	else:
		results.append(points[0])
		results.append(points[-1])

	return results