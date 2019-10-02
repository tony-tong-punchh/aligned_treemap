from setuptools import setup
from aligned_treemap import __version__


setup(
    name="aligned_treemap",
    version=__version__,
    packages=["aligned_treemap"],
    author="Tony Tong, Uri Laserson",
    author_email="ttong@pro-ai.org",
    description="Pure Python implementation of treemap, aligned_treemap, and squarify",
    long_description="Pure Python implementation of treemap, aligned_treemap, and squarify",
    license="Apache v2",
    keywords="one-level treemap visualization layout graphics with ordered alignment along x and y axes",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    requires=["numpy", "matplotlib"],
    url="https://github.com/tony-tong-punchh/aligned_treemap",
)
