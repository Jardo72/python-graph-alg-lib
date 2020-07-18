# Library of Graph Algorithms for Python

## Introduction
Library of Graph Algorithms for Python is a simple Python library providing implementations of various graph algorithms. It is more or less an educational/experimental project serving as sandbox for improvement of my Python skills. The following algorithms are provided:
- Topological Sort
- Dijsktra Algorithm (Shortest Path)


## Runtime Environment, Source Code Organization etc.

### Python Version and Dependencies
TODO
- Python 3.8
- library code depends only on the Python Standard Library; it does not depend on any other module
- unit tests depend on PyTest 5.4.3
- optionally PyTest Coverage 2.10.0 if you want to measre the code coverage

### Library Code
The library code is divided to four modules:
- `graphlib.grap` module provides two graph implementation (adjacency matrix, adjacency set), plus
an abstract base class prescribing the public API of any graph implementation.
- `graphlib.algorithms`
- `graphlib.util` module provides functionalities that support the implementation of the algorithms, for instance a priority queue.
- `graphlib.dump` module provides dump-functions that can pretty-print various structures like graph, result of shortest path search, minimum spanning tree etc. These functions can write their output to a file, to stdout, or to an instance of io.StringIO.


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

The following command triggers the execution of the unit tests, and it also generate code coverage report in HTML format. The command also generates detailed test results in HTML format to the file `test-results.html`.
```
python -m pytest --cov=graphlib --cov-branch --cov-report html tests --html=test-results.html
```
