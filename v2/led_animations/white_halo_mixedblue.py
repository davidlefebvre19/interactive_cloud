from rpi_ws281x import Adafruit_NeoPixel, Color
import time
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
BLUE_LIGHT = Color(0, 0, int(BRIGHTNESS * 0.50))  # Par exemple, un bleu clair avec 50% de la luminosité maximale

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def set_background():
    """Allume le fond avec une couleur bleu foncé ou bleu clair."""
    for i in range(NUM_LEDS):
        if random.random() < 0.5:  # 50% de chances d'utiliser le bleu foncé
            strip.setPixelColor(i, BLUE_DARK)
        else:
            strip.setPixelColor(i, BLUE_LIGHT)
    strip.show()

def move_halo(halo_size):
    position = 0

    while True:
        # Allumer le fond avec une couleur bleu foncé ou bleu clair
        set_background()

        # Allumer les LEDs pour le halo actuel
        for i in range(halo_size):
            led_index = (position + i) % NUM_LEDS
            strip.setPixelColor(led_index, Color(BRIGHTNESS, BRIGHTNESS, BRIGHTNESS))

        # Mettre à jour l'affichage de la bande LED
        strip.show()
        time.sleep(DELAY)

        # Avancer la position du halo
        position = (position + 1) % NUM_LEDS

try:
    halo_size = HALO_SIZE  # Par exemple, un halo de 50 LEDs
    move_halo(halo_size)
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
