# Library of Graph Algorithms for Python

## Introduction
Library of Graph Algorithms for Python is a simple Python library providing implementations of various graph algorithms. It is more or less an educational/experimental project serving as sandbox for improvement of my Python skills. The following algorithms are provided:
- Topological Sort
- Dijsktra Algorithm (Shortest Path)


## Runtime Environment, Source Code Organization etc.

### Python Version and Dependencies


### Library Code


### Test Code


## Creation of Distribution Package
In order to build the distribution package, execute the following command in the root directory of the project:
```
python setup.py sdist bdist_wheel
```

The command above creates both source archive (in .tar.gz format) and distribution in wheel format.


## Execution of Unit Tests
In order to execute the unit tests, execute the following command in the root directory of the project:
```
python -m pytest -v tests
```
