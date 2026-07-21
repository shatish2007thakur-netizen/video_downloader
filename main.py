import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import threading
import yt_dlp

class DownloaderLayout(BoxLayout):
    def __init__(self, **kwargs):
        super(DownloaderLayout, self).__init__(orientation='vertical', padding=20, spacing=15, **kwargs)

        self.add_widget(Label(text="Universal Video Downloader", font_size='20sp', size_hint_y=None, height=40))

        self.add_widget(Label(text="Video URL Enter Karein:", size_hint_y=None, height=20))
        self.url_input = TextInput(multiline=False, size_hint_y=None, height=40)
        self.add_widget(self.url_input)

        self.status_label = Label(text="Status: Ready to download", font_size='14sp', size_hint_y=None, height=30)
        self.add_widget(self.status_label)

        self.download_btn = Button(text="Download Video", size_hint_y=None, height=50, background_color=(0.3, 0.7, 0.3, 1))
        self.download_btn.bind(on_press=self.start_download)
        self.add_widget(self.download_btn)

    def update_status(self, text, color=(1, 1, 1, 1)):
        def _update(dt):
            self.status_label.text = text
            self.status_label.color = color
        Clock.schedule_once(_update)

    def start_download(self, instance):
        url = self.url_input.text.strip()
        if not url:
            self.update_status("Error: Valid URL dalein!", color=(1, 0, 0, 1))
            return

        self.download_btn.disabled = True
        self.update_status("Fetching info...", color=(1, 0.5, 0, 1))
        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, video_url):
        save_path = "/sdcard/Download" if os.path.exists("/sdcard/Download") else "."

        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            
            self.update_status("Download Complete! Check Downloads folder", color=(0, 1, 0, 1))
            def clear_input(dt): self.url_input.text = ""
            Clock.schedule_once(clear_input)

        except Exception as e:
            self.update_status(f"Error: {str(e)[:30]}...", color=(1, 0, 0, 1))

        finally:
            def enable_btn(dt): self.download_btn.disabled = False
            Clock.schedule_once(enable_btn)

class VideoDownloaderApp(App):
    def build(self):
        return DownloaderLayout()

if __name__ == '__main__':
    VideoDownloaderApp().run()
