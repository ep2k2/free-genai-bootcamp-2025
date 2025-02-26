# Installation Guide

This guide walks through setting up the Japanese Song Vocabulary Parser project environment.

## Prerequisites

- WSL:Ubuntu
- Python 3.x
- Git

## Installation Steps

### 1. Install UV Package Manager
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version

# Install system tools via uv
uv pip install parallel-python
```

### 2. Clone Repository

```bash
# Ensure you're in the agent-exp directory
cd agent-exp

# Clone octotools
git clone https://github.com/octotools/octotools
cd octotools
```

### 3. Create and Activate Virtual Environment

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate
```

### 4. Install Dependencies
Note that octotools requirements pulls in a lot. If you encounter timeout issues during dependency installation, increase the UV timeout:

```bash
# Ensure you're in the octotools directory
pwd  # Should show path ending in /octotools

# Set longer timeout (optional - only if needed)
export UV_HTTP_TIMEOUT=120

# Install dependencies
uv pip install -r requirements.txt

# Install octotools in development mode (must be run from octotools directory)
uv pip install -e .
```

To make the timeout setting permanent (optional):

```bash
echo "export UV_HTTP_TIMEOUT=120" >> ~/.bashrc
```

### 5. Test Basic Installation

```bash
# Navigate to the python code generator tool
cd octotools/octotools/tools/python_code_generator

# Run the test tool
python tool.py
```

If successful, you should see the tool's output without any errors.

## Troubleshooting

### Common Issues

1. **Dependency Installation Timeouts**
   - Symptom: Error message about failing to download packages
   - Solution: Set UV_HTTP_TIMEOUT as described above

2. **Directory Structure Issues**
   - Symptom: "No such file or directory" errors
   - Solution: Verify directory structure with `ls -la` or `tree -L 2`
   - Expected structure:
     ```
     octotools/
     └── octotools/
         └── tools/
             └── python_code_generator/
     ```

3. **Missing System Dependencies**
   - Symptom: "command not found" errors
   - Solution: Install parallel using uv:
     ```bash
     uv pip install parallel-python
     ```

4. **Missing Directories**
   - Symptom: "No such file or directory" for results/logs
   - Solution: Create required directories:
     ```bash
     mkdir -p results/octotools
     ```

## Next Steps

After completing installation:
1. Create .env file for API keys
2. Test basic installation
3. Proceed with development setup
