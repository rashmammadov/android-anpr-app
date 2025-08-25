"""
Simplified Android ANPR App for Testing
This version doesn't include heavy ML dependencies for initial testing
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

# For Android permissions
if platform == 'android':
    from android.permissions import request_permissions, Permission

class SimpleANPRApp(BoxLayout):
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
        
        # Setup UI
        self.setup_ui()
        
        # Request permissions on Android
        if platform == 'android':
            self.request_android_permissions()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Title
        title_label = Label(text='ANPR Camera App', size_hint_y=0.1, font_size='20sp')
        
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
            request_permissions([
                Permission.CAMERA,
                Permission.WRITE_EXTERNAL_STORAGE,
                Permission.READ_EXTERNAL_STORAGE,
                Permission.INTERNET
            ])
    
    def add_log_entry(self, text):
        """Add entry to the log"""
        timestamp = time.strftime("%H:%M:%S")
        label = Label(text=f"[{timestamp}] {text}", size_hint_y=None, height=30)
        self.log_layout.add_widget(label)
        # Keep only last 50 entries
        if len(self.log_layout.children) > 50:
            self.log_layout.remove_widget(self.log_layout.children[-1])
    
    def simulate_detection(self, stream_name):
        """Simulate license plate detection for testing"""
        import random
        
        # Simulate some license plates
        sample_plates = [
            "10AA123", "20BB456", "30CC789", "40DD012", "50EE345",
            "60FF678", "70GG901", "80HH234", "90II567", "99JJ890"
        ]
        
        while self.is_processing:
            # Simulate detection every 5-15 seconds
            time.sleep(random.uniform(5, 15))
            
            if not self.is_processing:
                break
                
            # Randomly select a plate
            plate = random.choice(sample_plates)
            confidence = random.uniform(0.7, 0.95)
            
            # Log detection
            self.add_log_entry(f"[{stream_name.upper()}] Detected: {plate} (Conf: {confidence:.2f})")
            
            # Send to API
            self.send_to_api(plate, stream_name, confidence, random.randint(1, 1000))
    
    def send_to_api(self, plate_text, stream_name, confidence, track_id):
        """Send detected plate to API"""
        try:
            payload = {
                "plate_number": plate_text,
                "stream": stream_name,
                "confidence": confidence,
                "track_id": track_id,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            response = requests.post(self.api_url, json=payload, timeout=5)
            
            if response.status_code == 200:
                self.add_log_entry(f"✓ API: {plate_text} sent successfully")
            else:
                self.add_log_entry(f"✗ API: Failed to send {plate_text} (Status: {response.status_code})")
                
        except Exception as e:
            self.add_log_entry(f"✗ API: Error sending {plate_text} - {str(e)}")
    
    def toggle_detection(self, instance):
        """Start license plate detection on both streams"""
        if not self.is_processing:
            self.is_processing = True
            self.start_button.text = 'Detection Active'
            self.status_label.text = 'Starting detection...'
            
            # Update RTSP URLs from inputs
            self.rtsp_urls['in'] = self.in_url_input.text
            self.rtsp_urls['out'] = self.out_url_input.text
            
            # Start processing threads (simulated)
            self.in_thread = threading.Thread(target=self.simulate_detection, args=("in",))
            self.out_thread = threading.Thread(target=self.simulate_detection, args=("out",))
            
            self.in_thread.start()
            self.out_thread.start()
            
            self.in_status_label.text = 'IN Stream: Processing'
            self.out_status_label.text = 'OUT Stream: Processing'
            self.add_log_entry("Detection started on both streams (Simulation Mode)")
            self.add_log_entry(f"IN URL: {self.rtsp_urls['in']}")
            self.add_log_entry(f"OUT URL: {self.rtsp_urls['out']}")
    
    def stop_detection(self, instance):
        """Stop license plate detection"""
        self.is_processing = False
        self.start_button.text = 'Start Detection'
        self.status_label.text = 'Detection stopped'
        self.in_status_label.text = 'IN Stream: Disconnected'
        self.out_status_label.text = 'OUT Stream: Disconnected'
        self.add_log_entry("Detection stopped")

class SimpleANPRApp(App):
    def build(self):
        return SimpleANPRApp()

if __name__ == '__main__':
    SimpleANPRApp().run()
