# Changelog

## 2.5.0 (19/02/2025)

### Qualia-Core

#### New features
- Bump maximum Python version to 3.13.
- Add `MNIST` Dataset.
- Add `FashionMNIST` Dataset.
- Add `ExponentialNoise` DataAugmentation.
- `dataugmentation.pytorch.{ResizedCrop,Rotation2D}`: add `interpolation` parameter.
- `deployment.stm32cubeai.NucleoL452REP`: upgrade to X-CUBE-AI 8.1.0.
- `deployment.stm32cubeai.NucleoL452REP`: use CMake project instead of STM32CubeIDE.
- `postprocessing.Keras2TFLite`: use `new_converter` by default.
- Add `Windows` Qualia-CodeGen deployer.

#### Bug fixes
- Fix handling of configuration files without deployer.
- `deployment.qualia_codegen.CMake`: Fix compatibility with CMake < 3.24.
- `deployment.qualia_codegen.CMake`: Fallback to `make` if `ninja` is not found.
- `preprocessing.Normalize`: fix use of list for `axis` parameter.
- `utils.TensorFlowInitializer`: fix environment variables initialization on Windows.

#### Breaking changes
- `learningmodel.pytorch.ResNetStride`: rename `force_projection_with_stride` parameter to `force_projection_with_pooling` and disable by default.
- `dataaugmentation.pytorch.GaussianNoise`: generate different noise for all dimensions.

### Qualia-Plugin-SNN

#### New features
- Bump maximum Python version to 3.13.
- Add `DVSGesture` and `DVSGestureWithPreprocessing` Datasets.
- Add `SHD` Dataset.
- Add `Group2TimeStepsBySample` Preprocessing.
- Add `IntegrateEventsByFixedDuration` Preprocessing.
- Add `IntegrateEventsByFixedFramesNumber` Preprocessing.
- Add `OperationCounter` Postprocessing.
- Add `Windows` Qualia-CodeGen deployer.
- `postprocessing.EnergyEstimationMetric`: add support for quantized layers.
- `postprocessing.EnergyEstimationMetric`: add support for Add layer in FNN.
- `postprocessing.EnergyEstimationMetric`: add T. Louis operation energy estimation types "saturation", "linear", "quadratic".
- `postprocessing.EnergyEstimationMetric`: add T. Louis memory energy estimation model.
- `postprocessing.QualiaCodeGen`: add `timestep_mode` parameter (`'duplicate'` by default, use `'iterate'` when using `SpikingJellyTimeStepsInData`)
- `postprocessing.QualiaCodeGen`: handle SpikingJelly AvgPool/MaxPool layers.
- `learningframework.SpikingJellyTimeStepsInData`: handle non-timestep-aware dataaugmentation by merging timestep dimension with batch dimensions.

#### Bug fixes
- `learningframework.SpikingJellyTimeStepsInData`: fix dimension reordering for 2D input data.
- `learningframework.SpikingJellyMultiStepTimeStepsInData`: fix dimension reordering.
- `postprocessing.EnergyEstimationMetric`: compute acc for bias in Conv spike layer with non-spike input.
- `postprocessing.EnergyEstimationMetric`: compute FC spike layer with non-spike input as sparse with MAC operations.
- `postprocessing.EnergyEstimationMetric`: no MAC operation for FNN Add layer.

#### Breaking changes

### Qualia-CodeGen-Core

#### New features
- Bump maximum Python version to 3.13.

#### Bug fixes
- `examples/Linux/CMakeLists.txt`: prevent linking with non-existant sanitizer lib on Windows.

### Qualia-CodeGen-Plugin-SNN

#### New features
- Bump maximum Python version to 3.13.
- `assets/model.hh`: add `MODEL_INPUT_TIMESTEP_MODE_{DUPLICATE,ITERATE}` constant to declare chosen timestep handling mode.
- `examples/`: handle `'iterate'` timestep mode (timesteps in data).

#### Bug fixes
- `examples/Linux/SpikingNeuralNetwork.h`: prevent overflow when accumulating over timesteps.

## 2.4.0 (24/01/2025)

### Qualia-Core

#### New features
- `deployment.qualia_codegen.Linux`: use CMake project.
- Add `NucleoH7S3L8` Qualia-CodeGen deployment target.
- Add `NucleoU575ZIQ` Qualia-CodeGen deployment target.
- `evaluation.host.Qualia`: collect all metrics.
- `evaluation.target.Qualia`: get latency measurement from target.
- Add `CMSISMFCC` DataAugmentation.
- Add `Cutout1D` DataAugmentation.
- Add `EZBirds` Dataset.
- `learningframework.PyTorch`: implement `save_graph_plot()` to plot model topology to SVG file using torch.fx.
- Add `SlopeMetric` PyTorch metric: linear regression slope.
- `learningmodel.pytorch.QuantizedCNN`: add support for quantized GSP.
- Add `ResNetSampleNorm` PyTorch model: ResNet with SampleNorm layer after input.
- Add `ResNetStride` PyTorch model: ResNet with `strides` parameter for strided convolutions and `pool_sizes` for max-pooling.
- Add `SampleNorm` and `QuantizedSampleNorm` PyTorch layers.
- `postprocessing.QualiaCodeGen`: custom metrics instanciation with `metrics` param.

#### Bug fixes
- Make local git repository and git dependency optional.
- Make `deploy.optimize` param optional.
- `learningframework.Keras`: `save_graph_plot()` outputs to `out/learningmodel` subdirectory instead of current directory.
- `learningframework.PyTorch`: do not attempt to compute predictions if confusion matrix is disabled.
- `preprocessing`, `postprocessing`: make Matplotlib optional when visualization modules are not used.
- `postprocessing.QuantizationAwareTraining`: `testacc` metric is optional.

#### Breaking changes
- `learningmodel.pytorch.CNN`: GSP makes last Conv layer implicit without BatchNorm.

### Qualia-Plugin-SNN

#### New features
- Add `SpikingJellyMultiStepTimeStepsInData` LearningFramework.
- Add `Add` and `QuantizedAdd` layers with SpikingJelly support.
- Add `NucleoL452REP` Qualia-CodeGen deployment target.
- `postprocessing.EnergyEstimationMetric`: input/output spike count.
- `postprocessing.EnergyEstimationMetric`: handle multi-step mode and hybrid layers.
- `postprocessing.EnergyEstimationMetric`: add support for ResNet.

#### Bug fixes
- `postprocessing.EnergyEstimationMetric`: take timsteps into account for biases.
- `postprocessing.EnergyEstimationMetric`: take potential reads into account.
- `postprocessing.EnergyEstimationMetric`: do not count reset and leak in case no IF activation.
- `postprocessing.EnergyEstimationMetric`: compute Conv/FC as dense with MACs if input is non-binary.
- `postprocessing.EnergyEstimationMetric`: use `e_rdram()` for `e_rdpot_conv_snn()`.

#### Breaking changes
- `learningmodel.pytorch.SCNN`: GSP makes last Conv layer implicit without BatchNorm.

### Qualia-CodeGen-Core

#### New features
- Add `Concatenate` layer for Keras.
- Add `Slice` layer for Keras 2.x `SlicingOpLambda` and Keras 3.x `GetItem`.
- Add `Permute` layer for `torch.permute()`.
- Add `SampleNorm` layer for Keras custom layer.
- Add `MetricsConverter`: generate instanciation of C++ metrics.
- `assets/include/model.hh`: add output quantization information.
- `examples/Linux`: CMake project.
- `examples/Linux`: use libqualia-neuralnetwork.
- Add `examples/NucleoH7S3L8`.
- Add `examples/NucleoU575ZIQ`.
- `examples/NucleoL452REP`: measure latency on target.
- `libqualia-neuralnetwork/Metrics`: add Accuracy, MAE, MSE, PCC and linear regression slope metrics in C++.
- `libqualia-neuralnetwork/NeuralNetwork`: quantize targets to match outputs.
- `libqualia-neuralnetwork`: install as Python package.
- `libqualia-neuralnetwork/NeuralNetwork`: add metrics computation.

#### Bug fixes
- `graph.TorchModelGraph`: fix `AdaptiveAvgPool1d` argument.
- `graph.TorchModelGraph`: fix handling of method before any module.
- `graph.TorchModelGraph`: filter args of methods.
- `graph.TorchModelGraph`: fix input shape of methods.
- `graph.KerasModelGraph`: fix input/output shape access for some Keras 3.x layers.
- `graph.KerasModelGraph`: fix for Keras 3.x layers without dtype.
- `graph.KerasModelGraph`: handle improperly ordered Keras graphs.
- `assets/model.cc`: support multiple input layers.
- `assets/layers/conv1d.cc`: fix usage of `arm_convolve_HWC_q15_fast_nonsquare()` due to undocumented constraint.
- `examples/Linux`: disable `-floop-nest-optimize`, broken with libisl 0.27.

#### Breaking changes
- `learningmodel.pytorch.SCNN`: GSP makes last Conv layer implicit without BatchNorm.
- `examples/NucleoL452REP`: default to 80 MHz core clock, optional 48 MHz setting.

### Qualia-CodeGen-Plugin-SNN

#### New features
- `assets/include/model.hh`: add output quantization information.
- `examples/Linux`: CMake project.
- `examples/Linux`: use libqualia-neuralnetwork with SNN support.
- Add `examples/NucleoL452REP`.

#### Bug fixes
- `graph.TorchModelGraph`: fix handling of method before any module.

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
