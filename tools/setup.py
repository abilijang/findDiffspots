from distutils.core import Extension, setup
from Cython.Build import cythonize

ext = Extension(name="bgsim", sources=["bgsubstract.pyx"])
setup(ext_modules=cythonize(ext, annotate=True))

#extensions = [Extension('findSpots', ['find_spot.pyx'])]
#setup(..., ext_modules=cythonize(extensions, gdb_debug=True))
