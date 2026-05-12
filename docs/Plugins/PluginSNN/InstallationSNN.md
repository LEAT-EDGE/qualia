# Installation of Qualia SNN plugin

Qualia SNN plugin is dependent on Qualia-Core.
Before starting this installation, you need to have Qualia-Core and Qualia-Codegen-Core installed with the appropriate virtual environment (see: [Qualia Installation](../../GettingStarted/Installation.md)).

## Working Directory & Virtual Environment

Start your virtual environment!  
In your Qualia folder:

```bash
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows
```

### Working Directory Tree

By following this installation, you will have the following directory tree: 

```bash
qualia
├── qualia_env                # qualia venv created using uv
├── qualia-codegen-core       # qualia core codegen directory
├── qualia-core               # qualia core directory 
├── qualia-codegen-plugin-snn # qualia snn codegen directory
└── qualia-plugin-snn         # qualia snn directory
```

### Virtual Environments

Let's update our environment. In the Qualia folder:

```bash
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

That's it, you can now run SNNs!  
You can go back to the [Getting Started SNN](./GettingStartedSNN).
