# Installation of Qualia SNN plugin
First create your virtual environnement and install Qualia-core by following this [documentation](../../GettingStarted/Installation). Don't forget to start your virtual environnement !

We'll follow this tree:
```bash
qualia
├── qualia_env                # qualia venv created using uv
├── qualia-codegen-core       # qualia core codegen directory
├── qualia-core               # qualia core codegen directory
├── qualia-codegen-plugin-snn # qualia snn codegen directory
└── qualia-plugin-snn         # qualia snn directory
```

Let's  set up our environment:

```bash
# Don't forget to activate your venv
source qualia_env/bin/activate 

# Install Qualia-SNN plugin
git clone https://github.com/LEAT-EDGE/qualia-plugin-snn.git
cd qualia-plugin-snn
uv pip install -e .
cd ..

# Install Qualia-SNN-Codegen plugin
git clone https://github.com/LEAT-EDGE/qualia-codegen-plugin-snn.git
cd qualia-codegen-plugin-snn
uv pip install -e .
cd ..
```

You can go back to the [Getting Started SNN](./GettingStartedSNN).