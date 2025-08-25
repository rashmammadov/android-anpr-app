#!/bin/bash

# macOS Setup Script for Android ANPR App
# This script installs the required dependencies for building Android APKs on macOS

echo "=== macOS Android Build Setup ==="
echo ""

# Check if Homebrew is installed
if ! command -v brew &> /dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "Installing Java JDK 8..."
brew install openjdk@8

# Set JAVA_HOME
echo "Setting JAVA_HOME..."
echo 'export JAVA_HOME=/opt/homebrew/opt/openjdk@8' >> ~/.zshrc
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> ~/.zshrc
source ~/.zshrc

# Install Android SDK
echo "Installing Android SDK..."
brew install android-sdk

# Set ANDROID_HOME
echo "Setting ANDROID_HOME..."
echo 'export ANDROID_HOME=/opt/homebrew/share/android-sdk' >> ~/.zshrc
echo 'export PATH=$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools:$PATH' >> ~/.zshrc
source ~/.zshrc

# Install Android NDK
echo "Installing Android NDK..."
brew install android-ndk

# Set ANDROID_NDK_HOME
echo "Setting ANDROID_NDK_HOME..."
echo 'export ANDROID_NDK_HOME=/opt/homebrew/share/android-ndk' >> ~/.zshrc
source ~/.zshrc

echo ""
echo "=== Setup Complete! ==="
echo "Please restart your terminal or run: source ~/.zshrc"
echo ""
echo "Then you can build the APK with: ./build.sh"
