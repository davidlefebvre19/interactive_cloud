import threading
import time
from rpi_ws281x import Adafruit_NeoPixel, Color
import random
from art import *
import os
import subprocess

# Configuration des LED
PIN = 12
NUM_LEDS = 300
BRIGHTNESS = 255

# CHILL
MIN_BRIGHTNESS = int(BRIGHTNESS * 0.20)  # 20% de la luminosité maximale
HALO_SIZE = 50
DELAY = 0.05

BLUE_DARK = Color(0, 0, MIN_BRIGHTNESS)
BLUE_LIGHT = Color(0, 0, int(BRIGHTNESS * 0.50))  # Bleu clair avec 50% de la luminosité maximale

# RAIN
BRIGHTNESS = 100
FADE_OUT_RATE = 5
#    Couleur de la pluie
RAIN_COLOR = Color(0, 0, 255)

#    Tableaux pour suivre l'état de chaque LED
led_brightness = [0 for _ in range(NUM_LEDS)]
is_raining = [False for _ in range(NUM_LEDS)]

# THUNDER
ZONE_LENGTH = 50  # Longueur de chaque zone
FADE_OUT_RATE_LIGHTNING = 10  # Vitesse du fondu
LIGHTNING_COLOR = Color(255, 255, 0)

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

# Sound config
script_dir = os.path.dirname(os.path.abspath(__file__))
subfolder = 'sounds'

class StoppableThread(threading.Thread):
    def __init__(self, task, stop_event, duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = task
        self.stop_event = stop_event
        self.duration = duration

    def run(self):
        self.task(self.stop_event, self.duration)

def fade_to_black(strip, steps=50, delay=0.05):
    # Réduction progressive de la luminosité
    for step in range(steps):
        for i in range(strip.numPixels()):
            # Récupère la couleur actuelle de chaque LED
            current_color = strip.getPixelColor(i)
            r = (current_color >> 16) & 0xFF
            g = (current_color >> 8) & 0xFF
            b = current_color & 0xFF

            # Réduit progressivement les composantes RGB
            new_r = max(0, int(r * (steps - step) / steps))
            new_g = max(0, int(g * (steps - step) / steps))
            new_b = max(0, int(b * (steps - step) / steps))

            # Applique la nouvelle couleur avec luminosité réduite
            strip.setPixelColor(i, Color(new_r, new_g, new_b))
        strip.show()
        time.sleep(delay)

    # S'assurer que tout est bien éteint à la fin
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

########################################### CHILL

def set_background():
    """Allume le fond avec une couleur bleu foncé ou bleu clair."""
    for i in range(NUM_LEDS):
        if random.random() < 0.5:
            strip.setPixelColor(i, BLUE_DARK)
        else:
            strip.setPixelColor(i, BLUE_LIGHT)
    strip.show()


def c(stop_event, duration):
    print(f"Animation chill démarrée pour {duration} secondes")
    start_time = time.time()

    position1 = 0
    position2 = NUM_LEDS // 2  # Début de la deuxième moitié de la bande

    audio_file = os.path.join(script_dir, subfolder, "wind_16bit.wav")

    process = subprocess.Popen(['sudo', 'aplay', audio_file])
    while not stop_event.is_set() and (time.time() - start_time) < duration:

        print("LED strip en mode chill...")
        if stop_event.is_set():
            print("STOP EVENT SET IN RAIN THREAD")
        else:
            print("stop_event not set in rain thread")
        # Allumer le fond avec une couleur bleu foncé ou bleu clair
        set_background()

        # Allumer le premier halo
        for i in range(HALO_SIZE):
            led_index = (position1 + i) % NUM_LEDS
            strip.setPixelColor(led_index, Color(BRIGHTNESS, BRIGHTNESS, BRIGHTNESS))

        # Allumer le deuxième halo
        for i in range(HALO_SIZE):
            led_index = (position2 + i) % NUM_LEDS
            strip.setPixelColor(led_index, Color(BRIGHTNESS, BRIGHTNESS, BRIGHTNESS))

        # Mettre à jour l'affichage de la bande LED
        strip.show()
        time.sleep(DELAY)

        # Avancer les positions des halos
        position1 = (position1 + 1) % NUM_LEDS
        position2 = (position2 + 1) % NUM_LEDS
    fade_to_black(strip)
    strip.show()
    process.terminate()
    process.wait()
    print("Animation chill terminée")


########################################### RAIN

def update_leds(strip):
    """ Mettre à jour l'état de la bande LED """
    for i in range(NUM_LEDS):
        if led_brightness[i] > 0:
            led_brightness[i] = max(led_brightness[i] - FADE_OUT_RATE, 0)
            strip.setPixelColor(i, Color(0, 0, led_brightness[i]))
            if led_brightness[i] == 0:
                is_raining[i] = False
        else:
            strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()


def rain_drop(strip):
    """ Créer une goutte de pluie """
    start_led = random.randint(0, strip.numPixels() - 1)
    if not is_raining[start_led]:
        led_brightness[start_led] = 255  # Luminosité maximale pour commencer
        is_raining[start_led] = True


def r(stop_event, duration):
    print(f"Animation rain démarrée pour {duration} secondes")
    start_time = time.time()

    audio_file = os.path.join(script_dir, subfolder, "rain_16bit.wav")

    process = subprocess.Popen(['sudo', 'aplay', audio_file])

    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode rain... ")
        if stop_event.is_set():
            print("STOP EVENT SET IN RAIN THREAD")
        else:
            print("stop_event not set in rain thread")
        rain_drop(strip)
        update_leds(strip)
        time.sleep(0.1)
    fade_to_black(strip)
    strip.show()
    process.terminate()
    process.wait()
    print("Animation rain terminée")


########################################### LIGHTNING

def lightning_effect(zone, fade_out_rate):
    """ Créer un effet d'éclair dans une zone spécifique """
    start_led = random.randint(zone * ZONE_LENGTH, (zone + 1) * ZONE_LENGTH - 1)
    end_led = random.randint(start_led, (zone + 1) * ZONE_LENGTH - 1)

    # Premier clignotement
    for i in range(start_led, end_led):
        strip.setPixelColor(i, LIGHTNING_COLOR)
    strip.show()
    time.sleep(0.05)  # Durée du clignotement

    # Éteindre les LEDs
    for i in range(start_led, end_led):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

    # Deuxième clignotement avec fondu
    for i in range(start_led, end_led):
        strip.setPixelColor(i, LIGHTNING_COLOR)
    strip.show()
    time.sleep(0.05)  # Durée du clignotement

    # Fondu
    for brightness in range(255, 0, -fade_out_rate):
        for i in range(start_led, end_led):
            strip.setPixelColor(i, Color(brightness, brightness, 0))
        strip.show()
        time.sleep(0.01)


def t(stop_event, duration):
    print(f"Animation thunder démarrée pour {duration} secondes")
    start_time = time.time()

    audio_file = os.path.join(script_dir, subfolder, "thunder_16bit.wav")

    process = subprocess.Popen(['sudo', 'aplay', audio_file])

    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode thunder...")
        if stop_event.is_set():
            print("STOP EVENT SET IN RAIN THREAD")
        else:
            print("stop_event not set in rain thread")
        for zone in range(NUM_LEDS // ZONE_LENGTH):
            if random.choice([True, False]):  # 50% de chance d'activer l'éclair
                lightning_effect(zone, FADE_OUT_RATE_LIGHTNING)
        time.sleep(random.uniform(0.1, 0.5))  # Intervalle aléatoire entre les éclairs
        time.sleep(0.1)
    fade_to_black(strip)
    strip.show()
    process.terminate()
    print("Animation thunder terminée")
