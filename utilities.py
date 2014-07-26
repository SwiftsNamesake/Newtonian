#
# Newtonian - utilities.py
#
# July 22 2014
#
# Jayant Shivarajan
# Jonatan Sundqvist
#
# Vector utilities
#

# TODO | - Consistent and readable naming scheme (cf. axisPos, position)
#		 -

# SPEC | - 
#		 -


from cmath import polar, rect, pi as π
from math import copysign, sqrt, sin


vector = complex


def axisPos(t : float, P : float, V : float, A : float) -> float:
	''' Calculates position on one axis '''
	return P + V*t + (1/2)*A*t**2


def position(t : float, P0 : vector, V0 : vector, A : vector) -> vector:
	''' Calculates position as a function of time, based on initial position, initial velocity, and acceleration '''
	# TOOD: Oxford comma (?)
	# TODO: Better names (?)
	# TODO: Explain proof (?)

	return axisPos(t, P0.real, V0.real, A.real)+axisPos(t, P0.imag, V0.imag, A.imag)*1j # x + yi


def tCollision(dy, V, A):
	''' Calculates time until collision occurs with ground '''
	# Deprecated; use timeUntil()
	#dt = sqrt(2*dy/abs(A.imag)) + 2*V.imag/abs(A.imag)
	dt = -V.imag/A.imag + sqrt((V.imag**2/A.imag-2*dy)/A.imag)

	return dt


def solveParabola(From : 'Real', To : 'Real', V : 'Real', A : 'Real') -> 'Real':

	'''
	Solves the specified parabola for T, even when any one of V and A is 0.
	When the values of V and A are such that no solution exists, returns -1.
	Negative values are otherwise meaningless in this context (although they might be
	mathematically sound), since we are looking ahead in time.

	'''

	# TODO: Clean this up, see if a more elegant solution exists
	# TODO: Optimize, profiling
	# TODO: Reference by notes, verify the equations

	if (A == 0) and (V != 0):
		# Not a parabola (linear equation)
		#print('Linear equation')
		return -(From-To)/V
	elif (A == 0) and (V == 0):
		# Not a function (line parallel or perpendicular to X-axis)
		#print('Not a function')
		return [-1, 0][From == To]
	elif 2*(From-To)/A > (V/A)**2:
		# Solution is imaginary
		#print('No real solutions')
		return -1
	else:
		# Function is a parabola and has a real solution
		#print('Solvable')
		return -V/A + sqrt((V/A)**2 - 2*(From-To)/A)

	# return {
	# 	(True, False, None) : (From-To)/V,
	# 	(True, True, None)  : [-1, 0][From == To],
	# 	(None, None, True)  : ,
	#	(None, None, None)  :
	# }[(A == 0, V == 0, 2*(From-To)/A > (V/A)**2)]()


def timeUntil(From : vector, To : vector, V : vector, A : vector) -> vector:
	
	'''
	Calculates time until a specific point is reached (separately for X and Y axis),
	given the position, velocity, and acceleration.

	'''

	# TODO: Handle inputs with no solution (Infinity, negative numbers?) (✓)
	# TODO: Handle V=0 and A=0 (✓)

	dtX = solveParabola(From.real, To.real, V.real, A.real)
	dtY = solveParabola(From.imag, To.imag, V.imag, A.imag)

	return dtX+dtY*1j


def rotate(point, pivot, angle):
	''' Rotates point around a given pivot '''
	return (point-pivot)*rect(1, angle) + pivot


def rotateVertices(angle, pivot, *vertices):
	''' '''
	return tuple(rotate(vertex, pivot, angle) for vertex in vertices)


def polygon(radius, sides, centre):
	''' Calculates the coordinates for a regular polygon '''
	# TODO: Make this more generic (*angles argument, *radii argument?)
	return tuple(rotate(centre+radius*1j, centre, (angle*π/180.0)) for angle in range(0, 360, int(360/sides)))