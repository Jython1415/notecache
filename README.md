# notecache — Notebook Caching

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
