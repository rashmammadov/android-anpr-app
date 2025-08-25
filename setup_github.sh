#!/bin/bash

# GitHub Setup Script for Android ANPR App
# This script helps you set up GitHub repository and trigger builds

echo "=== GitHub Setup for Android ANPR App ==="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Error: Git not found. Please install Git first."
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "Error: main.py not found. Please run this script from the android_anpr_app directory."
    exit 1
fi

echo "This script will help you set up GitHub repository for automated builds."
echo ""

# Ask for GitHub username
read -p "Enter your GitHub username: " github_username

if [ -z "$github_username" ]; then
    echo "Error: GitHub username is required."
    exit 1
fi

# Ask for repository name
read -p "Enter repository name (default: android-anpr-app): " repo_name
repo_name=${repo_name:-android-anpr-app}

echo ""
echo "Setting up repository: $github_username/$repo_name"
echo ""

# Initialize git repository
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
fi

# Add all files
echo "Adding files to git..."
git add .

# Commit files
echo "Creating initial commit..."
git commit -m "Initial commit: Android ANPR App with full ML capabilities"

# Add remote
echo "Adding GitHub remote..."
git remote add origin "https://github.com/$github_username/$repo_name.git"

# Set main branch
git branch -M main

echo ""
echo "=== Next Steps ==="
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: $repo_name"
echo "   - Make it public (for free GitHub Actions)"
echo "   - Don't initialize with README (we already have files)"
echo ""
echo "2. Push your code to GitHub:"
echo "   git push -u origin main"
echo ""
echo "3. Check GitHub Actions:"
echo "   - Go to: https://github.com/$github_username/$repo_name/actions"
echo "   - The build should start automatically"
echo ""
echo "4. Download APK when build completes:"
echo "   - Click on the completed workflow"
echo "   - Download 'anpr-app-apk' artifact"
echo ""
echo "=== Repository URL ==="
echo "https://github.com/$github_username/$repo_name"
echo ""

# Ask if user wants to push now
read -p "Do you want to push to GitHub now? (y/n): " push_now

if [ "$push_now" = "y" ] || [ "$push_now" = "Y" ]; then
    echo ""
    echo "Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Successfully pushed to GitHub!"
        echo "Check the Actions tab for build progress:"
        echo "https://github.com/$github_username/$repo_name/actions"
    else
        echo ""
        echo "❌ Failed to push to GitHub."
        echo "Please check your GitHub credentials and try again."
    fi
else
    echo ""
    echo "You can push later with:"
    echo "git push -u origin main"
fi

echo ""
echo "=== Full Version Features ==="
echo "✅ YOLOv8 License Plate Detection"
echo "✅ PaddleOCR Text Recognition"
echo "✅ RTSP Stream Processing"
echo "✅ Advanced Plate Tracking"
echo "✅ Corezoid API Integration"
echo "✅ Professional Android UI"
echo ""
echo "Your Android ANPR app is ready for automated builds! 🚀"
