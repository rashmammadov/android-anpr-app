# Android ANPR Camera App

This Android application provides real-time license plate detection using RTSP streams, based on the original `license_plate_cropper.py` logic.

## Features

- **Real-time License Plate Detection**: Uses YOLOv8 model for license plate detection
- **OCR Processing**: PaddleOCR for text recognition from license plates
- **RTSP Stream Support**: Processes live RTSP streams (IN and OUT)
- **Plate Tracking**: Advanced tracking to avoid duplicate detections
- **API Integration**: Sends detected plates to Corezoid API
- **Android UI**: Native Android interface with detection logs

## Prerequisites

### For Development (Building APK)

1. **Linux Environment** (Ubuntu 20.04+ recommended)
   - Windows users can use WSL2
   - macOS users can use Docker

2. **Required Software**:
   - Python 3.8+
   - Java JDK 8
   - Android SDK
   - Android NDK

### For Running on Android Device

- Android 5.0+ (API level 21+)
- Internet connection for RTSP streams
- Camera permission

## Installation & Setup

### Option 1: Build APK (Recommended)

1. **Setup Build Environment**:
   ```bash
   # Install required packages on Ubuntu
   sudo apt update
   sudo apt install -y python3 python3-pip git zip unzip openjdk-8-jdk python3-virtualenv
   
   # Install Android SDK and NDK
   sudo apt install -y android-sdk android-ndk
   ```

2. **Install Buildozer**:
   ```bash
   pip3 install buildozer
   ```

3. **Build the APK**:
   ```bash
   cd android_anpr_app
   buildozer android debug
   ```

4. **Install on Device**:
   ```bash
   # Enable USB debugging on your Android device
   # Connect device via USB
   adb install bin/anprcamera-0.1-arm64-v8a_armeabi-v7a-debug.apk
   ```

### Option 2: Termux (For Testing)

1. **Install Termux** from F-Droid
2. **Install Python and dependencies**:
   ```bash
   pkg update && pkg upgrade
   pkg install python git
   pip install --upgrade pip
   ```

3. **Install required packages**:
   ```bash
   pkg install opencv numpy
   pip install ultralytics torch torchvision pillow paddlepaddle paddleocr requests
   ```

4. **Run the app**:
   ```bash
   cd android_anpr_app
   python main.py
   ```

## Configuration

### RTSP Stream URLs

The app is configured to use these RTSP streams by default:
- **IN Stream**: `rtsp://5.197.60.18:700/chID=1&streamType=main`
- **OUT Stream**: `rtsp://5.197.60.18:700/chID=2&streamType=main`

To change these URLs, edit the `main.py` file:
```python
# RTSP URLs
self.in_rtsp_url = "your_in_stream_url"
self.out_rtsp_url = "your_out_stream_url"
```

### API Configuration

The app sends detected plates to the Corezoid API. To change the API endpoint:
```python
# API configuration
self.api_url = "your_api_endpoint"
```

## Usage

1. **Launch the App**: Open the ANPR Camera app on your Android device
2. **Grant Permissions**: Allow camera, storage, and internet permissions when prompted
3. **Start Detection**: Tap "Start Detection" to begin processing RTSP streams
4. **Monitor Logs**: View detected license plates in the detection log
5. **Stop Detection**: Tap "Stop Detection" to halt processing

## App Structure

```
android_anpr_app/
├── main.py                 # Main application file
├── buildozer.spec         # Buildozer configuration
├── requirements.txt       # Python dependencies
├── license_plate_detector.pt  # YOLOv8 model file
└── README.md             # This file
```

## Key Components

### LicensePlateDetector
- **YOLOv8 Model**: License plate detection
- **PaddleOCR**: Text recognition
- **Plate Tracking**: Duplicate detection prevention
- **API Integration**: Corezoid API communication

### ANPRCamera (UI)
- **Stream Management**: RTSP stream handling
- **Real-time Processing**: Frame-by-frame analysis
- **Detection Logging**: User interface for results
- **Android Integration**: Permissions and platform-specific features

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Ensure all dependencies are installed
   - Check Android SDK/NDK versions
   - Verify Java JDK installation

2. **RTSP Connection Issues**:
   - Check network connectivity
   - Verify RTSP URLs are accessible
   - Ensure firewall allows RTSP traffic

3. **Performance Issues**:
   - Reduce frame processing rate
   - Lower confidence thresholds
   - Use lower resolution streams

4. **Memory Issues**:
   - Close other apps
   - Restart the application
   - Check available device memory

### Debug Mode

Enable debug logging by modifying `buildozer.spec`:
```ini
android.logcat_filters = *:S python:D
```

View logs using:
```bash
adb logcat | grep python
```

## Performance Optimization

### For Better Performance

1. **Model Optimization**:
   - Use quantized models
   - Reduce model input size
   - Use TensorRT optimization

2. **Processing Optimization**:
   - Skip frames (process every Nth frame)
   - Reduce resolution
   - Use hardware acceleration

3. **Memory Management**:
   - Clear detection history periodically
   - Optimize image processing pipeline
   - Use efficient data structures

## Security Considerations

1. **Network Security**:
   - Use HTTPS for API calls
   - Implement authentication
   - Secure RTSP streams

2. **Data Privacy**:
   - Minimize data collection
   - Implement data retention policies
   - Secure local storage

3. **App Permissions**:
   - Request minimal permissions
   - Explain permission usage
   - Implement proper permission handling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs for error messages
3. Create an issue on the repository
4. Contact the development team

## Version History

- **v0.1**: Initial release with RTSP support and basic UI
- Future versions will include additional features and optimizations
