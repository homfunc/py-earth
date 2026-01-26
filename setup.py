"""
Simple build backend to handle Cython extensions with dependencies.
"""

import numpy
from setuptools import Extension, setup
from Cython.Build import cythonize


def get_extensions():
    """Returns list of C extension modules to compile."""
    numpy_inc = numpy.get_include()
    local_inc = "src/pyearth"

    # Define Cython modules to compile - _types must be first!
    ext_modules = [
        Extension("pyearth._types", ["src/pyearth/_types.pyx"], include_dirs=[numpy_inc]),
        Extension("pyearth._util", ["src/pyearth/_util.pyx"], include_dirs=[numpy_inc]),
        Extension("pyearth._basis", ["src/pyearth/_basis.pyx"], include_dirs=[numpy_inc]),
        Extension("pyearth._record", ["src/pyearth/_record.pyx"], include_dirs=[numpy_inc]),
        Extension(
            "pyearth._pruning", ["src/pyearth/_pruning.pyx"], include_dirs=[local_inc, numpy_inc]
        ),
        Extension(
            "pyearth._forward", ["src/pyearth/_forward.pyx"], include_dirs=[local_inc, numpy_inc]
        ),
        Extension(
            "pyearth._knot_search",
            ["src/pyearth/_knot_search.pyx"],
            include_dirs=[local_inc, numpy_inc],
        ),
        Extension("pyearth._qr", ["src/pyearth/_qr.pyx"], include_dirs=[local_inc, numpy_inc]),
    ]

    # Cythonize extensions with proper directives
    compiler_directives = {
        "language_level": "3",
        "embedsignature": True,
        "cdivision": True,
        "boundscheck": False,
        "wraparound": False,
    }

    return cythonize(
        ext_modules,
        compiler_directives=compiler_directives,
        language_level=3,
    )


if __name__ == "__main__":
    # This won't be called by `python -m build`
    # But can be used for local development
    setup(
        ext_modules=get_extensions(),
    )
