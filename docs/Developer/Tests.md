# Tests

```{contents} Table of Contents
---
depth: 3
---
```

## Run tests

Make sure the `tests` dependency group is installed, e.g.:
```
pdm install -G tests
```

To run all tests excluding on-target deployment tests:
```
pytest -m "not dependency and not deploy" -n auto --dist=loadgroup -vvv -s # xdist incompatible with dependency
pytest -m "dependency and not deploy" -vvv -s
```
The first command will run independent tests in parallel. The second one will run remaining tests with dependencies sequentially.

To run a specific test:
```
pytests -vvv -s tests/<path_to_test_module>::<test_class>::<test_method>
```
