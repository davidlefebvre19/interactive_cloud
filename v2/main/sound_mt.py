import threading
import time
import pygame
from pydub import AudioSegment

fade_out_duration = 2000
class StoppableThread(threading.Thread):
    def __init__(self, task, stop_event, duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = task
        self.stop_event = stop_event
        self.duration = duration

    def run(self):
        self.task(self.stop_event, self.duration)

def run_music(stop_event, audio_file, duration):
    # Convertir et jouer le fichier audio
    song = AudioSegment.from_file(audio_file)
    pygame.mixer.init(frequency=song.frame_rate)
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play(-1)

    start_time = time.time()

    while not stop_event.is_set() and (time.time() - start_time) < duration:
        continue

    # Fade-out
    pygame.mixer.music.fadeout(fade_out_duration)

    # Attendre la fin du fade-out avant d'arrêter la musique
    pygame.time.wait(fade_out_duration)
    pygame.mixer.music.stop()

def c(stop_event, duration):
    run_music(stop_event, "./sounds/wind.mp3", duration)

def r(stop_event, duration):
    run_music(stop_event, "./sounds/rain.mp3", duration)

def t(stop_event, duration):
    run_music(stop_event, "./sounds/thunder.mp3", duration)