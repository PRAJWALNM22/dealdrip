#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies  
npm install

echo "✅ Build completed successfully!"