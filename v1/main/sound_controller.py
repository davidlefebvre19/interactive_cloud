import threading
import pygame
from pydub import AudioSegment
import socket
import time

class SoundController():
    def __init__(self):
        self.stop_signal = threading.Event()
        self.fade_out_duration = 2000  # Durée du fade-out en millisecondes
        self.current_song = None

    def run_music(self, audio_file, duration):
        # Convertir et jouer le fichier audio
        song = AudioSegment.from_file(audio_file)
        pygame.mixer.init(frequency=song.frame_rate)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play(-1)

        start_time = time.time()

        while not self.stop_signal.is_set() and (time.time() - start_time) < duration:
            continue

        # Fade-out
        pygame.mixer.music.fadeout(self.fade_out_duration)

        # Attendre la fin du fade-out avant d'arrêter la musique
        pygame.time.wait(self.fade_out_duration)
        pygame.mixer.music.stop()

    def run_calm(self, duration):
        self.run_music("/home/rpi/wind.mp3", duration)
        self.current_song = None

    def run_raindrop(self, duration):
        self.run_music("/home/rpi/rain.mp3", duration)
        self.current_song = None

    def run_thunder(self, duration):
        self.run_music("/home/rpi/thunder.mp3", duration)
        self.current_song = None

    def stop(self):
        self.stop_signal.set()
        while self.current_song != None:
            time.sleep(0.1)

    def start_music(self, music, duration=20):
        self.stop_signal.clear()
        self.current_song = music

        if music == "calm":
            music_thread = threading.Thread(target=self.run_calm, args=(duration,))
        elif music == "raindrop":
            music_thread = threading.Thread(target=self.run_raindrop, args=(duration,))
        elif music == "thunder":
            music_thread = threading.Thread(target=self.run_thunder, args=(duration,))
        else:
            return
        music_thread.start()

host = '127.0.0.1'
port = 65432
soundController = SoundController()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    while True:
        data = s.recv(1024)
        if not data:
            break

        print(data.decode())
        if len(data.decode().split()) == 2:
            cmd, duration = data.decode().split()
            print("data received : " + cmd + duration)
            duration = int(duration) if duration.isdigit() else None

            # Si "thunder" est reçu, arrêtez l'animation actuelle et démarrez "thunder"
            # Sinon, démarrez "calm" ou "rain" seulement si aucune animation n'est en cours
            if cmd.lower() == 'stop':
                soundController.stop()
            elif cmd.lower() == 'thunder':
                soundController.stop()
                print("thunder sequence started")
                soundController.start_music('thunder', duration)
            elif soundController.current_song is None:
                print(cmd + " sequence started")
                soundController.start_music(cmd.lower(), duration)
            elif soundController.current_song is not None:
                print("sound controller busy with : " + soundController.current_song)



