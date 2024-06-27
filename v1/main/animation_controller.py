import threading
import numpy as np
import usb.core
from art import *
import random
from rpi_ws281x import *
import time
import socket
import subprocess# Sound

# FIFO arrays for db values
avg_db = np.zeros(30)
inst_db = np.zeros(6)

class AnimationController:


    def __init__(self):
        # Multithreading vars
        self.current_animation = None
        self.stop_signal = threading.Event()
        # GPIO and LEDSTRIP(rpi_ws281x) vars
        self.PIN = 12
        self.NUM_LEDS = 17
        self.BRIGHTNESS = 255
        self.strip = Adafruit_NeoPixel(self.NUM_LEDS, self.PIN, 800000, 10, False, self.BRIGHTNESS)
        self.strip.begin()
        # Calm
        self.FADE_STEP = 5  # Incrément pour le fondu
        self.NOMBRE_HALO = 5
        self.HALO_SIZE = 7
        self.DELAY = 0.001
        # Raindrop
        self.FADE_OUT_RATE = 5
        self.RAIN_COLOR = Color(0, 0, 255)
        self.led_brightness = [0 for _ in range(self.NUM_LEDS)]
        self.is_raining = [False for _ in range(self.NUM_LEDS)]
        # Thunder
        self.ZONE_LENGTH = 50  # Longueur de chaque zone
        self.FADE_OUT_RATE_LIGHTNING = 10  # Vitesse du fondu
        self.LIGHTNING_COLOR = Color(255, 255, 0)

    ################################################### CALM #################################

    def fade_to_brightness(self,led_index, target_brightness):
        # Récupérer la couleur actuelle et extraire la composante de luminosité
        current_color = self.strip.getPixelColor(led_index)
        current_brightness = (current_color & 0xff0000) >> 16  # Extrait la composante rouge comme luminosité

        while current_brightness != target_brightness:
            if current_brightness < target_brightness:
                current_brightness = min(current_brightness + self.FADE_STEP, target_brightness)
            else:
                current_brightness = max(current_brightness - self.FADE_STEP, target_brightness)

            self.strip.setPixelColor(led_index, Color(current_brightness, current_brightness, current_brightness))
            self.strip.show()
            time.sleep(0.01)

    def move_halo(self, duration):
        positions = [-self.HALO_SIZE] * self.NOMBRE_HALO  # Positions initiales des halos
        start_time = time.time()
        while time.time() - start_time < duration and not self.stop_signal.is_set():
            print("calm : " + str(duration - (time.time() - start_time)))
            # Parcourir chaque halo
            for i in range(self.NOMBRE_HALO):
                # Position actuelle du halo
                current_position = positions[i]

                # Éteindre les LEDs derrière le halo
                for j in range(self.HALO_SIZE):
                    led_to_turn_off = (current_position + j - self.HALO_SIZE) % self.NUM_LEDS
                    self.fade_to_brightness(led_to_turn_off, 0)

                # Mettre à jour la position du halo
                positions[i] = (positions[i] + 1) % self.NUM_LEDS

                # Allumer les LEDs pour le halo actuel
                for j in range(self.HALO_SIZE):
                    led_to_light = (positions[i] + j) % self.NUM_LEDS
                    self.fade_to_brightness(led_to_light, self.BRIGHTNESS)
            # Mettre à jour l'affichage de la bande LED
            self.strip.show()
            if self.stop_signal.is_set():
                print("stop signal received by calm!")
                break
            time.sleep(self.DELAY)

    def run_calm(self, duration):
        print("calm thread started")
        self.move_halo(duration)
        print("calm thread over")
        self.current_animation = None
        #while time.time() - start_time < duration and not self.stop_signal.is_set():
        #    self.move_halo()

    ######################## RAINDROP ######################################################

    def update_leds(self):
        """ Mettre à jour l'état de la bande LED """
        for i in range(self.NUM_LEDS):
            if self.led_brightness[i] > 0:
                self.led_brightness[i] = max(self.led_brightness[i] - self.FADE_OUT_RATE, 0)
                self.strip.setPixelColor(i, Color(0, 0, self.led_brightness[i]))
                if self.led_brightness[i] == 0:
                    self.is_raining[i] = False
            else:
                self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

    def rain_drop(self):
        """ Créer une goutte de pluie """
        start_led = random.randint(0, self.strip.numPixels() - 1)
        if not self.is_raining[start_led]:
            self.led_brightness[start_led] = 255  # Luminosité maximale pour commencer
            self.is_raining[start_led] = True

    def run_raindrop(self, duration):
        start_time = time.time()

        while time.time() - start_time < duration and not self.stop_signal.is_set():
            # Logique pour la gestion des LEDs
            print("run raindrop")
            self.rain_drop()
            self.update_leds()
            time.sleep(0.1)
        self.current_animation = None



    ######################## THUNDER ######################################################

    def lightning_effect(self, zone, fade_out_rate):
        """ Créer un effet d'éclair dans une zone spécifique """
        start_led = random.randint(zone * self.ZONE_LENGTH, (zone + 1) * self.ZONE_LENGTH - 1)
        end_led = random.randint(start_led, (zone + 1) * self.ZONE_LENGTH - 1)

        # Premier clignotement
        for i in range(start_led, end_led):
            self.strip.setPixelColor(i, self.LIGHTNING_COLOR)
        self.strip.show()
        time.sleep(0.05)  # Durée du clignotement

        # Éteindre les LEDs
        for i in range(start_led, end_led):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

        # Deuxième clignotement avec fondu
        for i in range(start_led, end_led):
            self.strip.setPixelColor(i, self.LIGHTNING_COLOR)
        self.strip.show()
        time.sleep(0.05)  # Durée du clignotement

        # Fondu
        for brightness in range(255, 0, -fade_out_rate):
            for i in range(start_led, end_led):
                self.strip.setPixelColor(i, Color(brightness, brightness, 0))
            self.strip.show()
            time.sleep(0.01)

    def run_thunder(self, duration):
        print("thunder thread started")

        start_time = time.time()

        while time.time() - start_time < duration and not self.stop_signal.is_set():
            # Logique pour la gestion des LEDs
            print("thunder : " + str(duration - (time.time() - start_time)))
            for zone in range(self.NUM_LEDS // self.ZONE_LENGTH):
                if random.choice([True, False]):  # 50% de chance d'activer l'éclair
                    self.lightning_effect(self.strip, zone, self.FADE_OUT_RATE_LIGHTNING)
            time.sleep(random.uniform(0.1, 0.5))  # Intervalle aléatoire entre les éclairs
            time.sleep(0.1)
        self.current_animation = None

    ######################## CONTROL ######################################################

    def start_animation(self, animation, duration=20):
        self.stop_signal.clear()  # Réinitialiser le signal d'arrêt pour la prochaine animation
        self.current_animation = animation  # Mise à jour de l'animation en cours

        # Lancer la nouvelle animation dans un thread séparé
        if animation == 'calm':
            animation_thread = threading.Thread(target=self.run_calm, args=(duration,))
        elif animation == 'raindrop':
            animation_thread = threading.Thread(target=self.run_raindrop, args=(duration,))
        elif animation == 'thunder':
            animation_thread = threading.Thread(target=self.run_thunder, args=(duration,))
        else:
            return
        animation_thread.start()

    def stop_current_animation(self):
        #if self.current_animation is not None:
        self.stop_signal.set()  # Signal pour arrêter l'animation actuelle
        while self.current_animation != None:
            time.sleep(0.1)
        # Éteindre toutes les LEDs à la fin
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()

host = '127.0.0.1'
port = 65432
animationController = AnimationController()

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
                animationController.stop_current_animation()
            elif cmd.lower() == 'thunder':
                animationController.stop_current_animation()
                print("thunder sequence started")
                animationController.start_animation('thunder', duration)
            elif animationController.current_animation is None:
                print(cmd + " sequence started")
                animationController.start_animation(cmd.lower(), duration)
            elif animationController.current_animation is not None:
                print("animation controller busy with : " + animationController.current_animation)



