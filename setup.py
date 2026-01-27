from setuptools import setup, Extension
import numpy as np
from Cython.Build import cythonize

try:
    from Cython.Distutils import build_ext

    have_cython = True
except ImportError:
    have_cython = False

# Get the include directory for NumPy
numpy_include = np.get_include()

extensions = [
    Extension(
        "pyearth._util",
        ["src/pyearth/_util.pyx"],
        include_dirs=[numpy_include],
    ),
    Extension(
        "pyearth._types",
        ["src/pyearth/_types.pyx"],
        include_dirs=[numpy_include],
    ),
    Extension(
        "pyearth._record",
        ["src/pyearth/_record.pyx"],
        include_dirs=[numpy_include],
    ),
    Extension(
        "pyearth._basis",
        ["src/pyearth/_basis.pyx"],
        include_dirs=[numpy_include],
    ),
    Extension(
        "pyearth._qr",
        ["src/pyearth/_qr.pyx"],
        include_dirs=[numpy_include],
        define_macros=[("CYTHON_CCOMPLEX", "0")],
    ),
    Extension(
        "pyearth._forward",
        ["src/pyearth/_forward.pyx"],
        include_dirs=[numpy_include],
        define_macros=[("CYTHON_CCOMPLEX", "0")],
    ),
    Extension(
        "pyearth._pruning",
        ["src/pyearth/_pruning.pyx"],
        include_dirs=[numpy_include],
    ),
    Extension(
        "pyearth._knot_search",
        ["src/pyearth/_knot_search.pyx"],
        include_dirs=[numpy_include],
        define_macros=[("CYTHON_CCOMPLEX", "0")],
    ),
]

if have_cython:
    cmdclass = {"build_ext": build_ext}
    extensions = cythonize(extensions)

setup(
    cmdclass=cmdclass,
    ext_modules=extensions,
)
