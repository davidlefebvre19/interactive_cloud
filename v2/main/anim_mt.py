import threading
import time
from rpi_ws281x import Adafruit_NeoPixel, Color
import random

# Configuration des LED
PIN = 12
NUM_LEDS = 300
BRIGHTNESS = 255
MIN_BRIGHTNESS = int(BRIGHTNESS * 0.20)  # 20% de la luminosité maximale
HALO_SIZE = 50
DELAY = 0.05

# Couleurs de bleu
BLUE_DARK = Color(0, 0, MIN_BRIGHTNESS)
BLUE_LIGHT = Color(0, 0, int(BRIGHTNESS * 0.50))  # Bleu clair avec 50% de la luminosité maximale

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

class StoppableThread(threading.Thread):
    def __init__(self, task, stop_event, duration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.task = task
        self.stop_event = stop_event
        self.duration = duration

    def run(self):
        self.task(self.stop_event, self.duration)

##################################### RAIN ###########################################

def set_background():
    """Allume le fond avec une couleur bleu foncé ou bleu clair."""
    for i in range(NUM_LEDS):
        if random.random() < 0.5:
            strip.setPixelColor(i, BLUE_DARK)
        else:
            strip.setPixelColor(i, BLUE_LIGHT)
    strip.show()

def r(stop_event, duration):
    print(f"Animation rain démarrée pour {duration} secondes")
    start_time = time.time()

    position1 = 0
    position2 = NUM_LEDS // 2  # Début de la deuxième moitié de la bande

    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode rain...")
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
    print("Animation rain terminée")

def c(stop_event, duration):
    print(f"Animation chill démarrée pour {duration} secondes")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode chill...")
        time.sleep(1)
    print("Animation chill terminée")

def t(stop_event, duration):
    print(f"Animation thunder démarrée pour {duration} secondes")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode thunder...")
        time.sleep(1)
    print("Animation thunder terminée")