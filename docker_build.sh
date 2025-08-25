#!/bin/bash

# Docker Build Script for Android ANPR App
# This script builds the APK using Docker to avoid macOS compatibility issues

echo "=== Docker Android ANPR App Build Script ==="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Error: Docker not found. Please install Docker Desktop first."
    echo "Download from: https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the android_anpr_app directory."
    exit 1
fi

# Check if model file exists
if [ ! -f "license_plate_detector.pt" ]; then
    echo "Error: license_plate_detector.pt not found. Please copy it to this directory."
    exit 1
fi

echo "Building Docker image..."
docker build -t android-anpr-builder .

if [ $? -ne 0 ]; then
    echo "Error: Docker build failed."
    exit 1
fi

echo ""
echo "Running build in Docker container..."
echo "This may take 15-45 minutes depending on your system and internet connection."
echo ""

# Run the build in Docker
docker run --rm -v $(pwd)/bin:/app/bin android-anpr-builder

# Check if build was successful
if [ -f "bin/anprcamera-0.1-arm64-v8a_armeabi-v7a-debug.apk" ]; then
    echo ""
    echo "=== Build Successful! ==="
    echo "APK location: bin/anprcamera-0.1-arm64-v8a_armeabi-v7a-debug.apk"
    echo ""
    echo "To install on your device:"
    echo "1. Enable USB debugging on your Android device"
    echo "2. Connect your device via USB"
    echo "3. Run: adb install bin/anprcamera-0.1-arm64-v8a_armeabi-v7a-debug.apk"
    echo ""
    echo "Or transfer the APK file to your device and install manually."
else
    echo ""
    echo "=== Build Failed! ==="
    echo "Check the Docker logs above for errors."
    exit 1
fi
