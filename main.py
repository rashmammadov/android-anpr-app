"""
Android ANPR App - Lightweight Version
This version uses basic OpenCV for initial testing and can be upgraded with ML later
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import threading
import time
import requests
import cv2
import numpy as np
import os

# For Android permissions
if platform == 'android':
    from android.permissions import request_permissions, Permission

class SimplePlateDetector:
    def __init__(self):
        # Simple contour-based detection for testing
        self.min_area = 1000
        self.max_area = 50000
        
    def detect_plates(self, frame):
        """Simple plate detection using contour analysis"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        plates = []
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if self.min_area < area < self.max_area:
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / float(h)
                
                # License plates typically have aspect ratio between 2.0 and 5.0
                if 2.0 < aspect_ratio < 5.0:
                    plates.append({
                        'bbox': (x, y, w, h),
                        'text': f"PLATE_{len(plates)+1}",
                        'confidence': 0.8
                    })
        
        return plates

class ANPRApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        
        # Initialize components
        self.is_processing = False
        self.rtsp_urls = {
            'in': "rtsp://5.197.60.18:700/chID=1&streamType=main",
            'out': "rtsp://5.197.60.18:700/chID=2&streamType=main"
        }
        
        # API configuration
        self.api_url = "https://www.corezoid.com/api/2/json/public/1714853/0a04e6b3904e3b837ae4c6ba4d8c70a9311a90e7"
        
        # Initialize detector
        self.detector = SimplePlateDetector()
        
        # Setup UI
        self.setup_ui()
        
        # Request permissions on Android
        if platform == 'android':
            self.request_android_permissions()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = Label(text='ANPR Camera App (Lightweight)', size_hint_y=0.1, font_size='20sp')
        
        # Status labels
        self.status_label = Label(text='Ready to start', size_hint_y=0.05)
        self.in_status_label = Label(text='IN Stream: Disconnected', size_hint_y=0.05)
        self.out_status_label = Label(text='OUT Stream: Disconnected', size_hint_y=0.05)
        
        # RTSP URL inputs
        url_layout = BoxLayout(orientation='vertical', size_hint_y=0.2)
        url_layout.add_widget(Label(text='RTSP URLs:', size_hint_y=0.3))
        
        self.in_url_input = TextInput(
            text=self.rtsp_urls['in'],
            hint_text='IN Stream URL',
            size_hint_y=0.35
        )
        self.out_url_input = TextInput(
            text=self.rtsp_urls['out'],
            hint_text='OUT Stream URL',
            size_hint_y=0.35
        )
        url_layout.add_widget(self.in_url_input)
        url_layout.add_widget(self.out_url_input)
        
        # Control buttons
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.start_button = Button(text='Start Detection', size_hint_y=1)
        self.start_button.bind(on_press=self.toggle_detection)
        self.stop_button = Button(text='Stop Detection', size_hint_y=1)
        self.stop_button.bind(on_press=self.stop_detection)
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        
        # Detection log
        self.log_label = Label(text='Detection Log:', size_hint_y=0.05)
        self.log_scroll = ScrollView(size_hint_y=0.4)
        self.log_layout = GridLayout(cols=1, size_hint_y=None)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        self.log_scroll.add_widget(self.log_layout)
        
        # Add widgets
        self.add_widget(title_label)
        self.add_widget(self.status_label)
        self.add_widget(self.in_status_label)
        self.add_widget(self.out_status_label)
        self.add_widget(url_layout)
        self.add_widget(button_layout)
        self.add_widget(self.log_label)
        self.add_widget(self.log_scroll)
        
    def request_android_permissions(self):
        """Request necessary permissions on Android"""
        if platform == 'android':
            permissions = [
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.INTERNET,
                Permission.ACCESS_NETWORK_STATE
            ]
            request_permissions(permissions)
    
    def log_message(self, message):
        """Add message to log"""
        timestamp = time.strftime("%H:%M:%S")
        log_text = f"[{timestamp}] {message}"
        
        def update_log():
            label = Label(text=log_text, size_hint_y=None, height=30)
            self.log_layout.add_widget(label)
            # Keep only last 50 messages
            if len(self.log_layout.children) > 50:
                self.log_layout.remove_widget(self.log_layout.children[-1])
        
        Clock.schedule_once(lambda dt: update_log(), 0)
    
    def toggle_detection(self, instance):
        """Toggle detection on/off"""
        if not self.is_processing:
            self.start_detection()
        else:
            self.stop_detection()
    
    def start_detection(self):
        """Start license plate detection"""
        if self.is_processing:
            return
            
        self.is_processing = True
        self.status_label.text = 'Detection running...'
        self.start_button.text = 'Stop Detection'
        
        # Update RTSP URLs
        self.rtsp_urls['in'] = self.in_url_input.text
        self.rtsp_urls['out'] = self.out_url_input.text
        
        # Start processing threads
        self.in_thread = threading.Thread(target=self.process_stream, args=('in',))
        self.out_thread = threading.Thread(target=self.process_stream, args=('out',))
        
        self.in_thread.daemon = True
        self.out_thread.daemon = True
        
        self.in_thread.start()
        self.out_thread.start()
        
        self.log_message("Started license plate detection (Lightweight Mode)")
    
    def stop_detection(self, instance=None):
        """Stop license plate detection"""
        self.is_processing = False
        self.status_label.text = 'Detection stopped'
        self.start_button.text = 'Start Detection'
        self.in_status_label.text = 'IN Stream: Disconnected'
        self.out_status_label.text = 'OUT Stream: Disconnected'
        self.log_message("Stopped license plate detection")
    
    def process_stream(self, stream_type):
        """Process RTSP stream for license plate detection"""
        url = self.rtsp_urls[stream_type]
        cap = cv2.VideoCapture(url)
        
        if not cap.isOpened():
            self.log_message(f"Failed to open {stream_type.upper()} stream")
            return
        
        self.log_message(f"Connected to {stream_type.upper()} stream")
        
        # Update status
        if stream_type == 'in':
            self.in_status_label.text = 'IN Stream: Connected'
        else:
            self.out_status_label.text = 'OUT Stream: Connected'
        
        frame_count = 0
        while self.is_processing:
            ret, frame = cap.read()
            if not ret:
                self.log_message(f"Failed to read frame from {stream_type.upper()} stream")
                break
            
            frame_count += 1
            # Process every 30th frame to reduce CPU usage
            if frame_count % 30 == 0:
                try:
                    plates = self.detector.detect_plates(frame)
                    for plate in plates:
                        text = plate['text']
                        confidence = plate['confidence']
                        self.log_message(f"{stream_type.upper()}: {text} (conf: {confidence:.2f})")
                        
                        # Send to API
                        self.send_to_api(text, stream_type)
                        
                except Exception as e:
                    self.log_message(f"Error processing {stream_type.upper()} frame: {str(e)}")
        
        cap.release()
        self.log_message(f"Disconnected from {stream_type.upper()} stream")
    
    def send_to_api(self, plate_text, stream_type):
        """Send detected plate to API"""
        try:
            data = {
                "plate_number": plate_text,
                "stream_type": stream_type,
                "timestamp": time.time()
            }
            
            response = requests.post(self.api_url, json=data, timeout=5)
            if response.status_code == 200:
                self.log_message(f"API: Successfully sent {plate_text}")
            else:
                self.log_message(f"API: Failed to send {plate_text} (status: {response.status_code})")
                
        except Exception as e:
            self.log_message(f"API: Error sending {plate_text}: {str(e)}")

class ANPRApp(App):
    def build(self):
        return ANPRApp()

if __name__ == '__main__':
    ANPRApp().run()
