# notecache — Notebook Caching

Created by Joshua Shew
([joshua.t.shew@gmail.com]("mailto:joshua.t.shew@gmail.com")).

## Introduction

*A package for state-dependent caching of large intermediate data frames in*
*Jupyter Notebook.*

Jupyter Notebook caching tool for large intermediate data frames with
state-dependent reevaluation. See the following usage example.

Without `notecache`:

```python
df = expensive_computation([multiple_large_arguments])
```

With `notecache`:

```python
import notecache
state = {"arg1": arg1, "arg2": another_arg}
def generate(state) -> DataFrame:
    return expensive_computation(state["arg1"], state["arg2"])
df = notecache.load(state, generate, unique_id = "large-data-frame")
```

The first time this cell is executed, `expensive_computation` will be run to
generate the result. Following executions of this cell will load the result
instead of calling `expensive_computation`, *even if the notebook has closed*
*and reopened*. The result is recomputation *if and only if* a change to `state`
has been detected.

## Installation

`notecache` can be found on [PyPI](https://pypi.org/project/notecache/). It can
be installed with `pip`.

```bash
pip install notecache
```

## Basic Usage

This package has one public function, `load`. It is used to both store and load
any given object. The 3 most important arguments passed into `load` are:

1. `state`

    This argument should contain all the information that is required to compute
    the object that is to be stored. A change in `state` between two calls to
    `load` (with the same `unique_id`) will cause the object to be generated
    instead of loaded from cache.

1. `generate`

    This is the function that is used to generate the target object. The return
    value of `load` contains the return value of `generate(state)`.

1. `unique_id`

    The `sha512` hash value of `unique_id` is used to create a unique file name
    to store the object. Overlapping `unique_id` in different calls to `load`
    may cause cache objects to be overwritten.

`load` returns a named tuple, and the object can be accessed with
`load([args]).object`.

## Usage Examples

- `notecache` is used in the
[Zoll Foundation Grant Project](https://bit.ly/3PdMEQO) to cache large data
frames that are generated after expensive sorting and processing steps
(see the [source code](https://bit.ly/3QhRUn7)).
- Contact the repository author if you used this package in a public repository
or if you know of anywhere else it is used so that it can be featured in this
list.

## Developer Instructions

### Installation

1. Fork the repository
1. Clone your fork with `git clone ...`
1. Run the installation script: `./scripts/initialize.sh`
1. Confirm successful installation by running unit tests
    1. Activate the virtual environment: `source .venv/bin/activate`
    1. Run the tests: `pytest tests/unit`

### Issues

Submit issues to the GitHub repository with steps to reproduce any bugs. Feature
requests and optimization ideas can also be submitted as issues.

### Making Code Contributions

1. Make changes on a branch in your fork
1. Create tests to define behavior and get them passing
1. Create a pull request with a description of the changes
