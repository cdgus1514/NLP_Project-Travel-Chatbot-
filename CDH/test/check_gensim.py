import platform
print(platform.platform())

import sys
print("Python", sys.version)

import numpy
print("Numpy", numpy.__version__)

import scipy
print("SciPy", scipy.__version__)

import gensim
print("gensim", gensim.__version__)

from gensim.models import word2vec
print(word2vec.FAST_VERSION)