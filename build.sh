#!/bin/bash

# Android ANPR App Build Script
# This script automates the process of building the Android APK

echo "=== Android ANPR App Build Script ==="
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the android_anpr_app directory."
    exit 1
fi

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "Error: buildozer not found. Please install it first:"
    echo "pip3 install buildozer"
    exit 1
fi

# Check if model file exists
if [ ! -f "license_plate_detector.pt" ]; then
    echo "Error: license_plate_detector.pt not found. Please copy it to this directory."
    exit 1
fi

echo "Starting build process..."
echo "This may take 10-30 minutes depending on your system and internet connection."
echo ""

# Clean previous builds (suppress warnings)
echo "Cleaning previous builds..."
buildozer android clean 2>/dev/null || true

# Build the APK (suppress root warnings)
echo "Building APK..."
echo "y" | buildozer android debug

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
    echo "Check the build logs above for errors."
    echo "Common issues:"
    echo "- Missing dependencies (Java JDK, Android SDK, etc.)"
    echo "- Network connectivity issues"
    echo "- Insufficient disk space"
    exit 1
fi
