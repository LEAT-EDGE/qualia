# Changelog

```{contents} Table of Contents
---
depth: 3
---
```

## 2.3.0 (15/07/2024)

### Qualia-Core

#### New features
- Bump maximum Python version to 3.12.
- `learningframework.PyTorch`: custom metric name for checkpoints with `checkpoint_metric` param.
- `learningframework.PyTorch`: optionally disable confusion matrix with `enable_confusion_matrix` param.
- `learningframework.PyTorch`: custom loss with `loss` param.
- `learningframework.PyTorch`: custom metric selection with `metrics` param.
- Add `BrainMIX` dataset.
- Add `Amplitude` DataAugmentation.
- Add `CopySet` PreProcessing.
- `postprocessing.Keras2TFLite`, `postprocessing.RemoveKerasSoftmax`, `postprocessing.Torch2Keras`: add support for Keras 3.x.
- Add `VisualizeFeatureMaps` PostProcessing.
- `postprocessing.FuseBatchNorm`: add `evaluate` param to optionally disable evaluation.
- `learningmodel.pytorch.Quantizer`: add `v` tensor type for more flexibility with Qualia-Plugin-SNN.

#### Bug fixes
- `preprocessing.DatasetSplitterBySubjects`: add `dest` set to available sets.
- `preprocessing.DatasetSplitter`: update `dest` info set.
- `learningframework.PyTorch`: fix default metric for checkpoint (`valavgclsacc`).
- `learningframework.PyTorch`: fix seeding after several training (integer overflow).
- `learningframework.PyTorch`: micro computation for prec, rec, and f1 metrics.
- Root logger stdout stream can output DEBUG level so that child logger can log debug messages. Default level is still INFO.
- `learningmodel.pytorch.layers.QuantizedLayer`: fix multiple inheritance Protocol on Python 3.10.
- Fix parsing of `[[parameter_research]]` section in configuration file. Actual behaviour of `parameter_research` is still untested.

#### Breaking changes
- Some metrics previously computed as macro (prec, rec, f1) are now computed as micro, results will be different on unbalanced datasets.

### Qualia-Plugin-SNN

#### New features
- Bump maximum Python version to 3.12.
- `postprocessing.EnergyEstimationMetric`: print `ModelGraph`.
- `postprocessing.EnergyEstimationMetric`: trace `GlobalSumPooling` (not counted in metric).
- `learningmodel.pytorch.layers.quantized_SNN_layers.py`: membrane potential uses new tensor type `v` to enable quantizer configuration decoupled from activations.

#### Bug fixes
- `learningmodel.pytorch.SNN`: inherit from SpikingJelly's `StepModule` to avoid warning when using `set_step_mode()` on the network.
- `postprocessing.FuseBatchNorm`: copy `step_mode` and inherit returned `GraphModule` from SpikingJelly's `StepModule`.
- `pyproject.toml`: require `pytorch` dependency group of `qualia-core`.

### Qualia-CodeGen-Core

#### New features
- Bump maximum Python version to 3.12.
- `graph.KerasModelGraph`: Add support for Keras 3.x.
- `graph.KerasModelGraph`: add support for `padding='same'` param of `Conv` layers.

#### Bug fixes
- `graph.TorchModelGraph`: fix ouput shape for methods.`
- `graph.TorchModelGraph`: keep first dim as-is when generating dummy input (propagate timestep dim with Qualia-CodeGen-Plugin-SNN).

### Qualia-CodeGen-Plugin-SNN

#### New features
- Bump maximum Python version to 3.12.

#### Bug fixes
- `graph.TorchModelGraph`: reset network to make sure potential are not initialized with wrong shape.


## 2.2.0 (01/03/2024)

### Qualia-Core

#### New features
- Pass separate scale factor for bias to Qualia-CodeGen.
- `bench.use_test_as_valid` configuration option to use the test dataset for validation metrics when no validation dataset is available.
- Add `QuantizationAwareFX` PostProcessing module as an alternative to `QuantizationAwareTraining` using `torch.fx` to build the quantized model, replacing layers with their quantized alternatives when possible.
- QuantizedLayer: add `from_module()` method to build a quantized layer from a non-quantized one with same configuration and weights.
- `TorchVisionModel` LearningModel: allow using original classifier.
- `TorchVisionModel` LearningModel: allow choosing the last layer for the feature extractor.
- Add CIFAR-10 TorchVision's MobileNetv2 configuration for float32 training and int16 quantization.
- Add `Normalize` DataAugmentation using `torchvision.transforms.Normalize`.
- Add `TorchVisionModelTransforms` DataAugmentation for use with `TorchVisionModel` to adapt input data.
- `PyTorch` LearningFramework: show loss in progress bar.
- Colored console logging to stderr for warnings and errors.
- `qualia_codegen.NucleoL452REP`: use CMake project instead of STM32CubeIDE.


#### Bug fixes
- Fix detection of seperate quantizer for bias.
- Fix for no `[[preprocessing]]` section in configuration file.
- Fix `TorchVisionModel` LearningModel construction.
- `qualia_codegen.Linux` Deployer: try to fix overflow detection.

#### Breaking changes
- `activations_range.txt` file: introduce bias_q column.
Existing models will have to be re-quantized in order to be deployed using Qualia-CodeGen, this does not change the classification results if seperate quantizer for bias was not used.
- Symmetric quantization uses the full range down to `-2^{b-1}` instead of restricting lower bound to `-2^{b-1} - 1`. Existing models will have to be re-quantized and this may slightly change the classification results.

### Qualia-Plugin-SNN

#### Bug fixes

- QuantizedIFNode/QuantizedLIFNode: return correct round mode for membrane potential and hyperparameters for Qualia-CodeGen.

### Qualia-CodeGen-Core

#### New features

- Add support for separate scale factor for bias.
- Add support for 1D/2D grouped convolutions (incl. depthwise convolutions).
- Add left shift overflow detection when `TRAPV_SHIFT` is defined and not using CMSIS-NN.
- TorchModelGraph: add support for ReLU6 activation layer.
- TorchModelGraph: add support for `operator.add()` function in addition to Add layer.
- TorchModelGraph: add support for `torch.nn.functional.adaptive_avg_pool2d` function.
- TorchModelGraph: add support for `torch.flatten()` function in addition to Flatten layer.
- Add NucleoL452REP example project using CMake instead of STM32CubeIDE.
- Add common libqualia-neuralnetwork for string to float decoding, quantization of inputs and classification task results, used only for NucleoL452REP CMake project for now.
- Abort compilation in case of unsupported activation function for layer.

#### Bug fixes

- TorchModelGraph: fix AdaptiveAvgPool1d layer.
- Linux example: fix single.cpp build.
- SparkFunEdge example: fix round-to-nearest support.


## 2.1.0 (16/01/2024)

### Qualia-Core

#### New features

- Deployment Qualia-CodeGen: Add support for nearest rounding mode (in addition to floor rounding mode) on Linux, NucleoL452REP (incl. CMSIS-NN), SparkFun Edge (incl. CMSIS-NN) and Longan Nano (incl. NMSIS-NN).

#### Bug fixes

- Fix importing qualia_core packages after plugins initialization.
- Fix some Python 3.9 compatibility issues.
- LearningModel MLP/QuantizedMLP: Fix layers instanciation.
- PostProcessing QuantizationAwareTraining: Use validation set instead of test set for validation with.

#### Other changes

- Various refactor, cleanup and typing fixes (quantized layer inheritance, `qualia_core.deployment`, `qualia_core.postprocessing.QualiaCodeGen`, `qualia_core.evaluation`).

#### Breaking changes

- `activations_range.txt` file: remove unused global_max columns and introduced round_mode columns.
Existing models will have to be re-quantized in order to be deployed using Qualia-CodeGen, this does not change the classification results.
- Nearest rounding mode for quantization with PyTorch now rounds upwards for half tie-breaker instead of round half to even in order to match Qualia-CodeGen.
Existing models using nearest rounding mode will have to be re-quantized and this may slightly change the classification results.

### Qualia-Plugin-SNN

#### Bug fixes

- LearningModel SResNet/QuantizedSResNet Fix using 2D layers.
- PostProcessing EnergyEstimationMetric: Fix display of message when non-binary inputs/outputs are included in the total.

#### Other changes

- Some refactor for quantized layer inheritance.

### Qualia-CodeGen-Core

#### New features

- Add support for nearest rounding mode for weights and activations in all supported layers and for inputs in all included example targets, with and without CMSIS-NN/NMSIS-NN.
- Generate a new `include/defines.h` file to be used as a global pre-processor macros definition file (used to set global rounding mode for CMSIS-NN/NMSIS-NN for now).
- Add an `exclude` argument to `Quantizer.quantize_weights()` to exclude some weights type by name in a custom plugin.

#### Bug fixes

- Longan Nano: build NMSIS-NN from upstream sources instead of using pre-built binary in order to apply custom optimizations and support floor rounding mode instead of nearest.
- `graph.layers`: fix weights property inheritance

### Qualia-CodeGen-Plugin-SNN

#### New features

- Add support for nearest rounding mode for potentials in `if` and `lif` layers and for inputs in the included Linux target.

#### Bug fixes

- `graph.layers`: fix weights property inheritance


## 2.0.0 (24/11/2023)

Initial release of Qualia

## 1.0.0 (15/09/2021)

Initial release of MicroAI
