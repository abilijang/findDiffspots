import numpy as np
cimport numpy as np
cimport cython
from libc.math cimport floor, sqrt, fmin

DTYPE = np.float32
ctypedef np.float32_t  DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
cdef azumith(float[:, :] data, float[:, :] dsts, center):
	cdef int xsize = data.shape[1]
	cdef int ysize = data.shape[0]
	cdef float ctx = center[0]
	cdef float cty = center[1]
	cdef float[:, :] azum = np.zeros([ysize, xsize], dtype=DTYPE)

	for j in range(ysize):
		for i in range(xsize):
			azum[j, i] = (j - cty) / (i - ctx)
			dsts[j, i] = sqrt((j - cty)**2 + (i - ctx)**2) 

	return azum

@cython.boundscheck(False)
@cython.wraparound(False)
cdef backsim(float[:] average):
	cdef float[:, :] bg = np.zeros([ysize, xsize], dtype=DTYPE)

	for j in range(ysize):
		for i in range(xsize):
			d = floor(dsts[j, i])
			if d <= bins:
				bg[j, i] = average[d]

	return bg

@cython.boundscheck(False)
@cython.wraparound(False)			
def subtract(float[:, :] data, center, azumith):
	cdef float ctx = center[0]
	cdef float cty = center[1]
	cdef float azm1 = azumith[0]
	cdef float azm2 = azumith[1]

	# if ctx > cty:
	# 	cdef int bins = floor(cty)
	# else:
	# 	cdef int bins = floor(ctx)
	cdef int bins = floor(fmin(ctx, cty))

	cdef float[:] average = np.zeros(bins, dtype=DTYPE)
	cdef float[:] counts = np.zeros(bins, dtype=DTYPE)
	cdef float[:, :] dsts = np.zeros([ysize, xsize], dtype=DTYPE)
	cdef float[:, :] azum = azumith(data, center)
	cdef Py_ssize_t i, j, k
	cdef int d

	for j in range(ysize):
		for i in range(xsize):
			d = floor(dsts[j, i])
			if azum[j, i] < azm2 and azum[j, i] > azm1 and \
				d <= bins and dsts[j, i] > 60
				average[d] = data[j, i]
				counts[d] += 1

	for k in range(bins):
		average[k] = average[k] / counts[k]

	return backsim(average)



				