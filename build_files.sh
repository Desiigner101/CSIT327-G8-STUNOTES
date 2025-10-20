#!/usr/bin/env bash
# Build script for Vercel
set -e

echo "======================================"
echo "Starting build process for Vercel..."
echo "======================================"

# Detect Python executable
if command -v python >/dev/null 2>&1; then
    PY=python
elif command -v python3 >/dev/null 2>&1; then
    PY=python3
else
    echo "ERROR: No python executable found"
    exit 1
fi

echo "Using Python: $PY"
$PY --version

# Upgrade pip
echo "Upgrading pip..."
$PY -m pip install --upgrade pip setuptools wheel

# Install requirements
echo "Installing requirements..."
if [ -f requirements.txt ]; then
    $PY -m pip install -r requirements.txt
else
    echo "ERROR: requirements.txt not found"
    exit 1
fi

# Set Django settings module
export DJANGO_SETTINGS_MODULE=stunotesapp.settings

# Create staticfiles directory if it doesn't exist
mkdir -p staticfiles

# Collect static files
echo "Collecting static files..."
$PY manage.py collectstatic --noinput --clear

# Verify static files were collected
if [ -d staticfiles ]; then
    echo "✓ Static files collected successfully in staticfiles/"
    ls -la staticfiles/
else
    echo "WARNING: staticfiles directory not found"
fi

echo "======================================"
echo "Build complete!"
echo "======================================"