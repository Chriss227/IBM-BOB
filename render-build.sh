#!/usr/bin/env bash
# Render build script

set -o errexit  # Exit on error

echo "Python version:"
python --version

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install --no-cache-dir -r requirements-prod.txt

echo "Build complete!"
