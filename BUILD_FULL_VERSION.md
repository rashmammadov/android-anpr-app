# Building the Full Version (With ML) - Android ANPR App

This guide will help you build the complete Android ANPR app with all ML capabilities including YOLOv8 license plate detection and PaddleOCR text recognition.

## 🚀 Quick Start Options

### Option 1: Docker Build (Recommended for macOS)

**Prerequisites:**
- Docker Desktop installed

**Steps:**
```bash
cd android_anpr_app
./docker_build.sh
```

This will:
1. Create a Docker container with all dependencies
2. Build the APK in a Linux environment
3. Output the APK to the `bin/` directory

### Option 2: Native macOS Build

**Prerequisites:**
- Homebrew installed

**Steps:**
```bash
cd android_anpr_app
./setup_macos.sh
# Restart terminal or run: source ~/.zshrc
./build.sh
```

### Option 3: Linux Build (Best Performance)

**Prerequisites:**
- Ubuntu 20.04+ or similar Linux distribution

**Steps:**
```bash
cd android_anpr_app
sudo apt update
sudo apt install -y python3 python3-pip git zip unzip openjdk-8-jdk
pip3 install buildozer cython
./build.sh
```

## 📱 What's Included in the Full Version

### Core Features
- ✅ **YOLOv8 License Plate Detection**: Real-time license plate detection using your trained model
- ✅ **PaddleOCR Text Recognition**: Advanced OCR for reading license plate text
- ✅ **RTSP Stream Processing**: Live processing of IN and OUT RTSP streams
- ✅ **Advanced Plate Tracking**: Prevents duplicate detections with sophisticated tracking
- ✅ **Text Stabilization**: Improves OCR accuracy with multiple frame analysis
- ✅ **Corezoid API Integration**: Sends detected plates to your API endpoint
- ✅ **Android Native UI**: Professional mobile interface with real-time logs

### Technical Components
- **LicensePlateDetector**: Main detection engine with YOLO + PaddleOCR
- **PlateTracker**: Advanced tracking system for duplicate prevention
- **ANPRCamera**: Android UI with stream management and logging
- **API Integration**: Corezoid API communication for detected plates

## 🔧 Build Process Details

### Docker Build Process
1. **Environment Setup**: Creates Ubuntu 20.04 container with all dependencies
2. **Dependency Installation**: Installs Java 8, Android SDK, NDK, and Python packages
3. **APK Building**: Uses buildozer to compile the Python app to Android APK
4. **Output**: Generates APK file in `bin/` directory

### Build Time
- **First Build**: 15-45 minutes (downloads dependencies)
- **Subsequent Builds**: 5-15 minutes (uses cached dependencies)

### APK Size
- **Expected Size**: 50-150 MB (includes ML models and dependencies)
- **Target Devices**: Android 5.0+ (API level 21+)

## 🎯 Configuration Options

### RTSP Stream URLs
Edit `main.py` to change stream URLs:
```python
# RTSP URLs
self.in_rtsp_url = "rtsp://5.197.60.18:700/chID=1&streamType=main"
self.out_rtsp_url = "rtsp://5.197.60.18:700/chID=2&streamType=main"
```

### API Configuration
Change the API endpoint in `main.py`:
```python
# API configuration
self.api_url = "https://www.corezoid.com/api/2/json/public/1714853/0a04e6b3904e3b837ae4c6ba4d8c70a9311a90e7"
```

### Model Configuration
- **Model File**: `license_plate_detector.pt` (YOLOv8 model)
- **Confidence Threshold**: 0.5 (adjustable in code)
- **OCR Confidence**: 0.5 (minimum for text recognition)

## 📊 Performance Optimization

### For Better Performance
1. **Reduce Model Input Size**: Edit YOLO model configuration
2. **Skip Frames**: Process every Nth frame instead of every frame
3. **Lower Resolution**: Use lower resolution RTSP streams
4. **Hardware Acceleration**: Enable GPU acceleration if available

### Memory Management
- **Detection History**: Limited to prevent memory leaks
- **Image Processing**: Optimized pipeline for mobile devices
- **Thread Management**: Proper cleanup of processing threads

## 🚨 Troubleshooting

### Common Build Issues

**Docker Issues:**
```bash
# If Docker build fails
docker system prune -a
./docker_build.sh
```

**macOS Issues:**
```bash
# If native build fails
./setup_macos.sh
source ~/.zshrc
./build.sh
```

**Linux Issues:**
```bash
# Install missing dependencies
sudo apt install -y build-essential python3-dev
pip3 install --upgrade buildozer
```

### Runtime Issues

**APK Installation:**
```bash
# Enable USB debugging on Android device
adb install bin/anprcamera-0.1-arm64-v8a_armeabi-v7a-debug.apk
```

**Permission Issues:**
- Grant camera, storage, and internet permissions
- Check Android device settings

**Network Issues:**
- Verify RTSP URLs are accessible
- Check firewall settings
- Ensure stable internet connection

## 📈 Testing the Full Version

### Pre-deployment Testing
1. **Build Verification**: Ensure APK builds successfully
2. **Installation Test**: Install on test device
3. **Permission Test**: Verify all permissions work
4. **Network Test**: Test RTSP connectivity
5. **API Test**: Verify Corezoid API integration

### Production Deployment
1. **Performance Testing**: Test on target devices
2. **Memory Testing**: Monitor memory usage
3. **Battery Testing**: Check battery consumption
4. **Stability Testing**: Long-running tests
5. **User Acceptance**: Final user testing

## 🔄 Updates and Maintenance

### Updating the App
1. **Code Changes**: Modify `main.py` as needed
2. **Model Updates**: Replace `license_plate_detector.pt`
3. **Rebuild**: Run build process again
4. **Deploy**: Install new APK on devices

### Monitoring
- **Log Analysis**: Review detection logs
- **Performance Monitoring**: Track app performance
- **Error Tracking**: Monitor for crashes or errors
- **API Monitoring**: Check API response times

## 📞 Support

### Getting Help
1. **Check Logs**: Review build and runtime logs
2. **Documentation**: Refer to README.md for details
3. **Troubleshooting**: Use this guide for common issues
4. **Community**: Seek help from Kivy/Buildozer communities

### Debug Mode
Enable debug logging in `buildozer.spec`:
```ini
android.logcat_filters = *:S python:D
```

View logs with:
```bash
adb logcat | grep python
```

## 🎉 Success!

Once you've successfully built and deployed the full version, you'll have:

- ✅ **Real-time license plate detection** on Android devices
- ✅ **Live RTSP stream processing** with dual streams
- ✅ **Advanced ML capabilities** with YOLO and PaddleOCR
- ✅ **Professional Android UI** with detection logging
- ✅ **API integration** for data collection
- ✅ **Production-ready deployment** for your ANPR system

Your Android ANPR app is now ready for production use! 🚀
