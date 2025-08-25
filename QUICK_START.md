# Quick Start Guide - Android ANPR App

## Option 1: Simple Version (Recommended for Testing)

The simple version doesn't include heavy ML dependencies and is perfect for testing the UI and API integration.

### Build Simple Version

1. **Rename the simple version**:
   ```bash
   cd android_anpr_app
   cp main_simple.py main.py
   cp buildozer_simple.spec buildozer.spec
   ```

2. **Build the APK**:
   ```bash
   ./build.sh
   ```

3. **Install on device**:
   ```bash
   adb install bin/anprcamerasimple-0.1-arm64-v8a_armeabi-v7a-debug.apk
   ```

## Option 2: Full Version (With ML)

The full version includes all the original license plate detection logic.

### Prerequisites

- Linux environment (Ubuntu 20.04+ recommended)
- Python 3.8+
- Java JDK 8
- Android SDK and NDK

### Build Full Version

1. **Ensure you have the model file**:
   ```bash
   # The license_plate_detector.pt should already be in the directory
   ls -la license_plate_detector.pt
   ```

2. **Build the APK**:
   ```bash
   ./build.sh
   ```

3. **Install on device**:
   ```bash
   adb install bin/anprcamera-0.1-arm64-v8a_armeabi-v7a-debug.apk
   ```

## Option 3: Termux Testing

For quick testing without building an APK:

1. **Install Termux** from F-Droid
2. **Install dependencies**:
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   pip install kivy requests
   ```

3. **Run the simple version**:
   ```bash
   cd android_anpr_app
   cp main_simple.py main.py
   python main.py
   ```

## Testing the App

1. **Launch the app** on your Android device
2. **Grant permissions** when prompted
3. **Enter RTSP URLs** (or use defaults)
4. **Tap "Start Detection"** to begin
5. **Watch the detection log** for results

## Troubleshooting

### Build Issues
- Ensure you're on Linux or using WSL2/Docker
- Install all required dependencies
- Check internet connection for downloads

### Runtime Issues
- Grant all required permissions
- Check network connectivity
- Verify RTSP URLs are accessible

### Performance Issues
- Use the simple version for testing
- Close other apps to free memory
- Ensure good network connection

## Next Steps

1. **Test the simple version** first
2. **Verify API integration** works
3. **Test with real RTSP streams**
4. **Build the full version** if needed
5. **Optimize for production** use

## Support

- Check the main README.md for detailed documentation
- Review build logs for specific errors
- Test with the simple version first
