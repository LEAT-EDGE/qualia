# Adding New Datasets to Qualia

## Base Structure 

The dataset implementation should follow this basic structure:

```python
from __future__ import annotations
import sys
import logging
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
        # Remove validation if not needed
        self.sets.remove('valid')
```

## Implementation Patterns

Let's look at two common patterns found in Qualia's datasets:

### Pattern 1: Simple Dataset (Like BrainMIX)
For datasets with straightforward loading from files:

```python
class SimpleDataset(RawDataset):
    def __init__(self, path: str) -> None:
        super().__init__()
        self.__path = Path(path)
        self.sets.remove('valid')  # If no validation set

    @override
    def __call__(self) -> RawDataModel:
        # Load data files
        with (self.__path/'train.pickle').open('rb') as fd:
            train_data = pickle.load(fd)
        with (self.__path/'test.pickle').open('rb') as fd:
            test_data = pickle.load(fd)

        # Process data
        train_x = train_data['x']
        train_y = train_data['y']
        test_x = test_data['x']
        test_y = test_data['y']

        # Create RawData objects
        train = RawData(train_x, train_y)
        test = RawData(test_x, test_y)

        return RawDataModel(
            sets=RawDataSets(train=train, test=test),
            name=self.name
        )
```

### Pattern 2: Complex Dataset (Like CIFAR10)
For datasets requiring more processing:

```python
@dataclass
class DatasetFile:
    data: numpy.typing.NDArray[np.uint8]
    labels: list[int]
    # Add other needed fields

class ComplexDataset(RawDataset):
    def __init__(self, path: str = '', dtype: str = 'float32') -> None:
        super().__init__()
        self.__path = Path(path)
        self.__dtype = dtype
        self.sets.remove('valid')

    def __load_file(self, file: Path) -> DatasetFile:
        """Helper method to load data files"""
        with file.open('rb') as fo:
            raw = pickle.load(fo, encoding='bytes')
            # Process raw data as needed
            return DatasetFile(**processed_data)

    def __load_train(self, path: Path) -> RawData:
        """Separate method for loading training data"""
        start = time.time()
        
        # Load and process training data
        data = self.__load_file(path/'train_file')
        
        # Process into correct format
        x = data.data.reshape((-1, height, width, channels))
        y = np.array(data.labels)
        
        logger.info('Train data loaded in %s s', time.time() - start)
        return RawData(x, y)

    def __load_test(self, path: Path) -> RawData:
        """Separate method for loading test data"""
        start = time.time()
        
        # Load and process test data
        data = self.__load_file(path/'test_file')
        
        # Process into correct format
        x = data.data.reshape((-1, height, width, channels))
        y = np.array(data.labels)
        
        logger.info('Test data loaded in %s s', time.time() - start)
        return RawData(x, y)

    @override
    def __call__(self) -> RawDataModel:
        return RawDataModel(
            sets=RawDataSets(
                train=self.__load_train(self.__path),
                test=self.__load_test(self.__path)
            ),
            name=self.name
        )
```

## Key Implementation Points

1. **Type Hints and Imports**
```python
from __future__ import annotations  # Always include
import sys
from typing import override  # Use typing_extensions for Python < 3.12
```

2. **Logging**
```python
import logging
logger = logging.getLogger(__name__)
# Use throughout code:
logger.info('Loading data...')
logger.debug('Processing batch %d', batch_num)
```

3. **Path Handling**
```python
from pathlib import Path
self.__path = Path(path)  # Convert string paths to Path objects
```

4. **Performance Monitoring**
```python
start = time.time()
# ... load data ...
logger.info('Operation completed in %s s', time.time() - start)
```

5. **Data Processing Helper Methods**
```python
def __process_data(self, raw_data: np.ndarray) -> np.ndarray:
    """Create helper methods for data processing steps"""
    # Reshape, normalize, etc.
    return processed_data
```

## Best Practices from Existing Implementations

1. **Use Private Methods**
   - Prefix internal methods with double underscore
   - Keep implementation details encapsulated

2. **Handle Data Types**
   - Allow dtype specification when relevant
   - Convert data to correct type explicitly

3. **Error Handling**
   - Check file existence
   - Validate data shapes and types
   - Log errors appropriately

4. **Documentation**
   - Comment non-obvious processing steps
   - Log important operations and timing
   - Use proper type hints

## Example Configuration

Add configuration example in `conf/dataset_name/`:

```toml
[dataset]
name = "MyNewDataset"
path = "path/to/data"
dtype = "float32"  # If supported

[preprocessing]
# Add any needed preprocessing steps
```
