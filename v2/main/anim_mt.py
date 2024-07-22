import threading
import time
from rpi_ws281x import Adafruit_NeoPixel, Color
import random

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
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    print("Animation rain terminée")

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
    print(f"Animation chill démarrée pour {duration} secondes")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode chill...")
        rain_drop(strip)
        update_leds(strip)
        time.sleep(0.1)
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    print("Animation chill terminée")

def t(stop_event, duration):
    print(f"Animation thunder démarrée pour {duration} secondes")
    start_time = time.time()
    while not stop_event.is_set() and (time.time() - start_time) < duration:
        print("LED strip en mode thunder...")
        time.sleep(1)
    print("Animation thunder terminée")