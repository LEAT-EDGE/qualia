# Changelog

```{contents} Table of Contents
---
depth: 3
---
```

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
