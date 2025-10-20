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

# Clean up any existing static files
rm -rf staticfiles/

# Create fresh staticfiles directory
mkdir -p staticfiles

# Install any static-related requirements
$PY -m pip install whitenoise

# Collect static files
echo "Collecting static files..."
export DJANGO_SETTINGS_MODULE=stunotesapp.settings
$PY manage.py collectstatic --noinput

# Verify static files were collected
if [ -d staticfiles ]; then
    echo "✓ Static files collected successfully in staticfiles/"
    echo "Contents of staticfiles directory:"
    ls -la staticfiles/
    echo "Contents of staticfiles/notes/js directory:"
    ls -la staticfiles/notes/js/ || echo "JS directory not found"
else
    echo "WARNING: staticfiles directory not found"
fi

echo "Build complete!"
