# Installation of Qualia SNN plugin
First create your virtual environnement and install Qualia-core by following this [documentation](../../GettingStarted/Installation). Don't forget to start your virtual environnement !
Let's create a new project and set up our environment:

```bash
mkdir qualia-snn
cd qualia-snn

# Install Qualia-SNN plugin
git clone https://github.com/LEAT-EDGE/qualia-plugin-snn.git
cd qualia-plugin-snn
pip install -e .
cd ..

# Install Qualia-SNN-Codegen plugin
git clone https://github.com/LEAT-EDGE/qualia-codegen-plugin-snn.git
cd qualua-codegen-plugin-snn
pip install -e .
cd ..
```

Or using uv:
```bash
mkdir qualia-snn
cd qualia-snn

# Install Qualia-SNN plugin
git clone https://github.com/LEAT-EDGE/qualia-plugin-snn.git
cd qualia-plugin-snn
uv pip install -e .
cd ..

# Install Qualia-SNN-Codegen plugin
git clone https://github.com/LEAT-EDGE/qualia-codegen-plugin-snn.git
cd qualua-codegen-plugin-snn
uv pip install -e .
cd ..
```
