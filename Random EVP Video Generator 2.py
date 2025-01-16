import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np
import pygame
from threading import Thread
from moviepy.editor import VideoFileClip, concatenate_videoclips
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
    cv2.namedWindow("Random EVP Video Generator", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Random EVP Video Generator", 640, 480)

    # Получение размеров экрана
    screen_width = 1920  # замените на фактическую ширину экрана
    screen_height = 1080  # замените на фактическую высоту экрана

    # Вычисление координат центра окна
    x = (screen_width - 640) // 2
    y = (screen_height - 480) // 2

    # Перемещение окна в центр экрана
    cv2.moveWindow("Random EVP Video Generator", x, y)

    while True:
        # Разделение видео на 1-секундные фрагменты
        video_clips = []
        for start in range(0, int(video_clip.duration), 1):
            end = min(start + 1, video_clip.duration)
            video_clips.append(video_clip.subclip(start, end))

        # Случайное перемешивание видеофрагментов
        random.shuffle(video_clips)

        # Вывод случайного кадра из перемешанных видеофрагментов
        for clip in video_clips:
            for frame in clip.iter_frames():
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Преобразование из BGR в RGB
                cv2.imshow("Random EVP Video Generator", frame)
                if cv2.waitKey(30) & 0xFF == ord('q'):
                    break

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
root.geometry("320x120")  # Установка размера окна

select_button = tk.Button(root, text="Выбрать видео", command=select_video)
select_button.pack()

# Запустить основной цикл интерфейса
root.mainloop()
