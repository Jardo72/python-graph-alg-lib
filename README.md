# Library of Graph Algorithms for Python

## Introduction
Library of Graph Algorithms for Python is a simple Python library providing implementations of various graph algorithms. It is more or less an educational/experimental project serving me as Python sandbox. The current version of the library provides the following algorithms:
- topological sort
- shortest path search for unweighted graphs
- shortest path search for weighted graphs (Dijkstra's algorithm)
- minimum spanning tree for connected graphs (Prim's algorithm)


## Runtime Environment, Source Code Organization etc.

### Python Version and Dependencies
When implementing the library, I used Python 3.8. Slightly older versions of Python might work as well, but there is no guarantee. The library code uses only the Python Standard Library. In other words it does not depend on any other modules. Unit tests depend on PyTest 5.4.3. If you want to measure the code coverage, you will also need PyTest Coverage 2.10.0 (i.e. optional test dependency). Similarly, if you want to generate test reports in HTML format, PyTest HTML plugin is needed.

<a name="library-code"></a>
### Library Code
The library code is divided to five modules:
- [graphlib.graph](./graphlib/graph.py) module provides two graph implementations (adjacency matrix, adjacency set), plus
an abstract base class prescribing the public API of any graph implementation.
- [graphlib.algorithms](./graphlib/algorithms.py) provides implementations of various graph algorithms like topological sort, shortest path search, minimum spanning tree search etc.
- [graphlib.util](./graphlib/util.py) module provides functionalities that support the implementation of the algorithms, for instance a priority queue.
- [graphlib.dump](./graphlib/dump.py) module provides dump-functions that can pretty-print various structures like graph, result of shortest path search, minimum spanning tree etc. These functions can write their output to a file, to stdout, or to an instance of io.StringIO.
- [graphlib.jsondef](./graphlib/jsondef.py) module provides functions that can build a graph accorging to a JSON definition.


### Test Code
The test code is concentrated in the [tests](./tests) directory, which is just a flat structure of modules with test code. For each of the library modules listed in the [Library Code](#library-code) section, there is a corresponding test module. The names of all test modules start with the prefix `test_`, so that PyTest can recognize them as test modules. Within each test module, test methods are grouped to test suite classes. A test suite class is a simple class serving as collection (grouping) of test methods exercising the same functionality. All test dependencies are captured in the [test dependencies](./test-requirements.txt) file. Visualization of the diagrams used by the test code can be found in the [test-graphs](./test-graphs) directory.

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

The following command triggers the execution of the unit tests, and it also generates code coverage report in HTML format. The command also generates detailed test results in HTML format to the file `test-results.html`.
```
python -m pytest --cov=graphlib --cov-branch --cov-report html --html=test-results.html tests
```

The command above will only work if you have installed the corresponding PyTest plug-ins (see [test dependencies](./test-requirements.txt)).
