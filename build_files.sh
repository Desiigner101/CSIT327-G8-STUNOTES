#!/usr/bin/env bash
# Build script for Vercel: collect static files and prepare dist directory
set -e

# If pip isn't available under the current python, use python -m pip
if command -v python >/dev/null 2>&1; then
	PY=python
elif command -v python3 >/dev/null 2>&1; then
	PY=python3
else
	echo "No python executable found"
	exit 1
fi

# Install requirements locally (Vercel usually installs them automatically)
"$PY" -m pip install --upgrade pip setuptools wheel
if [ -f requirements.txt ]; then
	"$PY" -m pip install -r requirements.txt
fi

# Ensure DJANGO settings module for collectstatic
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-stunotesapp.settings}

# Prepare dist dir expected by vercel
DIST_DIR=staticfiles_build
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Run collectstatic (won't fail if migrations or DB missing if sqlite fallback is present)
"$PY" manage.py collectstatic --noinput || true

# Copy collected static files to dist dir
if [ -d static_cdn ]; then
	cp -a static_cdn/. "$DIST_DIR" || true
fi

# Also copy the app static directory if present
if [ -d static ]; then
	cp -a static/. "$DIST_DIR" || true
fi

echo "Static build complete"
