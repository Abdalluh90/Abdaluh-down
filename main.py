from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.popup import Popup
import yt_dlp
import os

class DownloaderApp(App):
    def build(self):
        self.title = "Video Downloader"

        # الحاوية الرئيسية
        layout = FloatLayout()

        # إدخال رابط الفيديو
        url_label = Label(text="Video URL:",
                          size_hint=(0.3, 0.1),
                          pos_hint={"x": 0.05, "top": 1})
        layout.add_widget(url_label)

        self.url_input = TextInput(hint_text="Enter URL here",
                                   multiline=False,
                                   size_hint=(0.6, 0.1),
                                   pos_hint={"x": 0.35, "top": 1})
        layout.add_widget(self.url_input)

        # اختيار الجودة
        quality_label = Label(text="Choose Quality:",
                              size_hint=(0.3, 0.1),
                              pos_hint={"x": 0.05, "top": 0.85})
        layout.add_widget(quality_label)

        self.quality_spinner = Spinner(
            text="best",
            values=["best", "720p", "1080p"],
            size_hint=(0.6, 0.1),
            pos_hint={"x": 0.35, "top": 0.85},
        )
        layout.add_widget(self.quality_spinner)

        # تحديد مسار الحفظ
        path_label = Label(text="Save Path:",
                           size_hint=(0.3, 0.1),
                           pos_hint={"x": 0.05, "top": 0.7})
        layout.add_widget(path_label)

        self.output_path = TextInput(hint_text="Default: downloads",
                                     multiline=False,
                                     size_hint=(0.6, 0.1),
                                     pos_hint={"x": 0.35, "top": 0.7})
        layout.add_widget(self.output_path)

        # زر اختيار المجلد
        select_folder_btn = Button(
            text="Select Folder",
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0.3, "top": 0.55},
            background_color=(0.2, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
        )
        select_folder_btn.bind(on_press=self.select_folder)
        layout.add_widget(select_folder_btn)

        # زر التحميل
        download_btn = Button(
            text="Download",
            size_hint=(0.4, 0.1),
            pos_hint={"x": 0.3, "top": 0.4},
            background_color=(0, 0.6, 0, 1),
            color=(1, 1, 1, 1),
        )
        download_btn.bind(on_press=self.start_download)
        layout.add_widget(download_btn)

        return layout

    def select_folder(self, instance):
        # نافذة اختيار مجلد
        popup = Popup(
            title="Select Folder",
            content=Label(text="Folder selection not implemented"),
            size_hint=(0.7, 0.5),
        )
        popup.open()

    def start_download(self, instance):
        url = self.url_input.text.strip()
        quality = self.quality_spinner.text.strip()
        output_dir = self.output_path.text.strip() or "downloads"

        if not url:
            self.show_message("Error", "Please enter a video URL!")
            return

        options = {
            'format': quality,
            'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
            'noplaylist': False,
        }

        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                ydl.download([url])
            self.show_message("Success", "Download completed!")
        except Exception as e:
            self.show_message("Error", f"An error occurred: {e}")

    def show_message(self, title, message):
        popup = Popup(
            title=title,
            content=Label(text=message),
            size_hint=(0.7, 0.5),
        )
        popup.open()


if __name__ == "__main__":
    DownloaderApp().run()