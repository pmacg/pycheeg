from setuptools import setup, find_packages

VERSION = '0.1.0'
DESCRIPTION = 'Sweep set algorithms for finding cuts in graphs.'
LONG_DESCRIPTION =\
    "Algorithms for finding the cheeger cut and the cheeger-trevisan cut in networkx graphs."

# Setting up
setup(
    name="pycheeg",
    version=VERSION,
    author="Peter Macgregor",
    author_email="<macgregor.pr@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["numpy", "scipy", "networkx"],

    keywords=['python', 'sweep set', 'cheeger cut', 'conductance', 'bipartiteness'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Operating System :: POSIX :: Linux'
    ]
)