## Troubleshooting

If you encounter issues:

1. **Environment Issues**:
   ```bash
   # Check Python version
   python --version  # Should be 3.9-3.12 (3.11 recommended)
   
   # Verify Qualia installation
   pip show qualia-core
   ```

2. **Dataset Issues**:
   - Verify the dataset path in `config.toml` matches your directory structure
   - Ensure all dataset files are present and readable

3. **Training Issues**:
   - Check GPU availability (if using)
   - Monitor system resources
   - Review training logs in `log/<bench_name>/learningmodel/`

## Getting Help

- Check error messages carefully
- Verify your Python version (3.12 recommended)
- Ensure your virtual environment is activated
- Validate all dependencies are installed correctly

Remember to activate your environment before using Qualia:
```bash
# For uv:
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows

# For PDM:
$(pdm venv activate qualia_env)

# For pip:
source qualia_env/bin/activate  # Unix/macOS
qualia_env\Scripts\activate     # Windows
```