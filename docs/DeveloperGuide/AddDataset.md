# Adding New Datasets to Qualia

## Base Structure

Start by creating a new Python module in the `dataset` folder of the code base (Qualia-Core or a Qualia-Plugin source folder), called `MyNewDataset.py` in this example.
Inside this module, create a `MyNewDataset` class that inherits from `RawDataset`.

Adapt the `__call__` method to load your data and return the appropriate objects described below.

Here's a complete example showing the essential structure:

```python
from __future__ import annotations
import sys
import logging
import numpy as np
from pathlib import Path
from qualia_core.datamodel import RawDataModel
from qualia_core.datamodel.RawDataModel import RawData, RawDataSets

if sys.version_info >= (3, 12):
    from typing import override
else:
    from typing_extensions import override

logger = logging.getLogger(__name__)

class MyNewDataset(RawDataset):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.__path = Path(path)
        # Remove validation set if not needed
        self.sets.remove('valid')

    @override
    def __call__(self) -> RawDataModel:
        # Load your data files here
        # Example with numpy arrays:
        train_x = np.load(self.__path / 'train_x.npy')  # Shape: [N, S, C] for 1D or [N, H, W, C] for 2D
        train_y = np.load(self.__path / 'train_y.npy')  # Shape: [N] for class numbers
        
        test_x = np.load(self.__path / 'test_x.npy')
        test_y = np.load(self.__path / 'test_y.npy')

        # Create RawData objects for each set
        train = RawData(train_x, train_y)
        test = RawData(test_x, test_y)

        # Return the complete model
        return RawDataModel(
            sets=RawDataSets(train=train, test=test),
            name=self.name
        )
```

## Core Data Structures

### RawData
- Represents a single dataset partition
- Contains:
  - `x`: Input data as numpy.ndarray
  - `y`: Ground truth labels as numpy.ndarray
- Provides methods for importing/exporting in compressed format (useful for saving/loading preprocessed datasets)

### RawDataSets
- Groups dataset partitions together
- Contains:
  - `train`: Training set (RawData)
  - `test`: Test set (RawData)
  - `valid`: Validation set (RawData, optional)

### RawDataModel
- Top-level container returned by dataset's `__call__` method
- Contains:
  - `sets`: RawDataSets object
  - `name`: Dataset name

## Expected Data Dimensions

### 1D Data (e.g., time series)
- Input shape: `[N, S, C]`
  - N: Number of input data
  - S: Time samples
  - C: Channels

### 2D Data (e.g., images)
- Input shape: `[N, H, W, C]`
  - N: Number of input data
  - H: Height
  - W: Width
  - C: Channels

### Ground Truth (Labels)
- Classification:
  - Option 1: Class numbers as integers `[N]` (use preprocessing.Class2BinMatrix later for one-hot encoding)
  - Option 2: One-hot encoded matrix `[N, num_classes]`

## Configuration and Parameters

Parameters can be declared in the constructor and set via configuration file, e.g.:

```python
def __init__(self, path: str = '', dtype: str = 'float32') -> None:
    super().__init__()
    self.__path = Path(path)
    self.__dtype = dtype
```

Configuration file (`conf/mynewdataset/config.toml`):
```toml
[dataset]
kind = "MyNewDataset"
params.path = "data/mynewdataset"
params.dtype = "float32"
```

## Final Steps

After creating your dataset class, import it in `dataset/__init__.py`:

```python
from .MyNewDataset import MyNewDataset

__all__ = [..., 'MyNewDataset']
```
