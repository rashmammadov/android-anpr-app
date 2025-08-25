"""
Full Android ANPR App with ML Capabilities
This version includes YOLOv8 license plate detection and PaddleOCR text recognition
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
from ultralytics import YOLO
from paddleocr import PaddleOCR
import os

# For Android permissions
if platform == 'android':
    from android.permissions import request_permissions, Permission

class PlateTracker:
    def __init__(self, max_disappeared=30, max_distance=50):
        self.next_object_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared
        self.max_distance = max_distance
        self.text_history = {}
        self.stable_text = {}
        
    def register(self, centroid, text=""):
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.text_history[self.next_object_id] = [text] if text else []
        self.stable_text[self.next_object_id] = text
        self.next_object_id += 1
        
    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]
        if object_id in self.text_history:
            del self.text_history[object_id]
        if object_id in self.stable_text:
            del self.stable_text[object_id]
            
    def update(self, rects, texts):
        if len(rects) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects.copy()
            
        input_centroids = np.array([self._get_centroid(rect) for rect in rects])
        
        if len(self.objects) == 0:
            for i in range(len(input_centroids)):
                self.register(input_centroids[i], texts[i] if i < len(texts) else "")
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())
            
            distances = self._calculate_distances(object_centroids, input_centroids)
            rows = distances.min(axis=1).argsort()
            cols = distances.argmin(axis=1)[rows]
            
            used_rows = set()
            used_cols = set()
            
            for (row, col) in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                    
                if distances[row, col] > self.max_distance:
                    continue
                    
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                
                if col < len(texts) and texts[col]:
                    self.text_history[object_id].append(texts[col])
                    if len(self.text_history[object_id]) > 5:
                        self.text_history[object_id].pop(0)
                    self.stable_text[object_id] = self._get_most_common(self.text_history[object_id])
                
                used_rows.add(row)
                used_cols.add(col)
                
            unused_rows = set(range(len(object_centroids))).difference(used_rows)
            unused_cols = set(range(len(input_centroids))).difference(used_cols)
            
            if len(object_centroids) >= len(input_centroids):
                for row in unused_rows:
                    object_id = object_ids[row]
                    self.disappeared[object_id] += 1
                    if self.disappeared[object_id] > self.max_disappeared:
                        self.deregister(object_id)
            else:
                for col in unused_cols:
                    self.register(input_centroids[col], texts[col] if col < len(texts) else "")
                    
        return self.objects.copy()
    
    def _get_centroid(self, rect):
        x, y, w, h = rect
        return (int(x + w // 2), int(y + h // 2))
    
    def _calculate_distances(self, centroids1, centroids2):
        distances = np.zeros((len(centroids1), len(centroids2)))
        for i, c1 in enumerate(centroids1):
            for j, c2 in enumerate(centroids2):
                distances[i, j] = np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
        return distances
    
    def _get_most_common(self, text_list):
        if not text_list:
            return ""
        from collections import Counter
        return Counter(text_list).most_common(1)[0][0]

class LicensePlateDetector:
    def __init__(self, model_path="license_plate_detector.pt"):
        self.model = YOLO(model_path)
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')
        self.tracker = PlateTracker()
        
    def detect_and_recognize(self, frame):
        results = self.model(frame)
        plates = []
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    
                    # Crop the license plate
                    plate_img = frame[y1:y2, x1:x2]
                    if plate_img.size == 0:
                        continue
                        
                    # OCR on the cropped plate
                    ocr_result = self.ocr.ocr(plate_img, cls=True)
                    if ocr_result and ocr_result[0]:
                        text = ocr_result[0][0][1][0]
                        confidence = ocr_result[0][0][1][1]
                        if confidence > 0.5:  # Filter low confidence results
                            plates.append({
                                'bbox': (x1, y1, x2-x1, y2-y1),
                                'text': text,
                                'confidence': confidence
                            })
        
        return plates

class FullANPRApp(BoxLayout):
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
        
        # Initialize ML components
        self.detector = None
        self.init_ml_components()
        
        # Setup UI
        self.setup_ui()
        
        # Request permissions on Android
        if platform == 'android':
            self.request_android_permissions()
        
    def init_ml_components(self):
        """Initialize ML components"""
        try:
            self.detector = LicensePlateDetector()
            self.log_message("ML components initialized successfully")
        except Exception as e:
            self.log_message(f"Error initializing ML components: {str(e)}")
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = Label(text='ANPR Camera App (Full ML Version)', size_hint_y=0.1, font_size='20sp')
        
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
        
        self.log_message("Started license plate detection")
    
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
            # Process every 10th frame to reduce CPU usage
            if frame_count % 10 == 0 and self.detector:
                try:
                    plates = self.detector.detect_and_recognize(frame)
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
        return FullANPRApp()

if __name__ == '__main__':
    ANPRApp().run()
