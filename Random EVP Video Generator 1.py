import tkinter as tk
from tkinter import filedialog
import numpy as np
import pygame
from threading import Thread
from PIL import Image, ImageTk
from moviepy.editor import VideoFileClip
import random

video_clip = None
audio_clip = None

def load_video(video_path):
    global video_clip, audio_clip
    video_clip = VideoFileClip(video_path)
    audio_clip = video_clip.audio

def play_sound():
    global audio_clip
    sample_rate = 44100
    pygame.mixer.init(frequency=sample_rate, size=-16, channels=1)

    while True:
        start_time = random.uniform(0, audio_clip.duration - 1)
        end_time = min(start_time + 1, audio_clip.duration)  # 1-секундный фрагмент

        audio_segment = audio_clip.subclip(start_time, end_time)
        audio_segment_array = audio_segment.to_soundarray(fps=sample_rate)

        sound = (audio_segment_array * 32767).astype(np.int16)
        pygame.mixer.Sound(buffer=sound.tobytes()).play()

        pygame.time.delay(1000)  # Пауза на 1 секунду перед воспроизведением следующего

def display_random_frame():
    if video_clip:
        start_time = random.uniform(0, video_clip.duration - 1)
        frame = video_clip.get_frame(start_time)

        # Преобразование массива в изображение PIL
        frame_image = Image.fromarray(frame)

        # Изменение размера изображения, чтобы оно подходило под canvas
        frame_image = frame_image.resize((640, 480), Image.LANCZOS)  # Масштабируем изображение с использованием LANCZOS
        frame_photo = ImageTk.PhotoImage(frame_image)

        # Обновление canvas с новым изображением
        canvas.create_image(0, 0, anchor=tk.NW, image=frame_photo)
        canvas.image = frame_photo  # Сохранение ссылки на изображение, чтобы избежать сборки мусора

    # Запланировать обновление через 1000 мс (1 секунда)
    canvas.after(1000, display_random_frame)

def start_audio_and_video(video_path):
    load_video(video_path)
    Thread(target=play_sound, daemon=True).start()  # Запуск звука в отдельном потоке
    display_random_frame()  # Запуск отображения случайных кадров

def select_video():
    file_path = filedialog.askopenfilename(title="Выберите видео файл")  
    if file_path:
        start_audio_and_video(file_path)

# Создание графического интерфейса
root = tk.Tk()
root.title("Random EVP Video Generator")

canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

select_button = tk.Button(root, text="Выбрать видео", command=select_video)
select_button.pack()

# Запустить основной цикл интерфейса
root.mainloop()
