import time
import random
from rpi_ws281x import Adafruit_NeoPixel, Color

# Configuration des LED
PIN = 12
NUM_LEDS = 300
BRIGHTNESS = 255
MIN_BRIGHTNESS = int(BRIGHTNESS * 0.20)  # 20% de la luminosité maximale
HALO_SIZE = 50
DELAY = 0.05

# Couleurs de bleu
BLUE_DARK = Color(0, 0, MIN_BRIGHTNESS)
BLUE_LIGHT = Color(0, int(BRIGHTNESS * 0.70), int(BRIGHTNESS * 0.70))  # Cyan clair
# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def set_background():
    """Allume le fond avec une couleur bleu foncé ou bleu clair."""
    for i in range(NUM_LEDS):
        if random.random() < 0.5:
            strip.setPixelColor(i, BLUE_DARK)
        else:
            strip.setPixelColor(i, BLUE_LIGHT)
    strip.show()

def move_halo(halo_size1, halo_size2):
    position1 = 0
    position2 = NUM_LEDS // 2  # Début de la deuxième moitié de la bande

    while True:
        # Allumer le fond avec une couleur bleu foncé ou bleu clair
        set_background()

        # Allumer le premier halo
        for i in range(halo_size1):
            led_index = (position1 + i) % NUM_LEDS
            strip.setPixelColor(led_index, Color(BRIGHTNESS, BRIGHTNESS, BRIGHTNESS))

        # Allumer le deuxième halo
        for i in range(halo_size2):
            led_index = (position2 + i) % NUM_LEDS
            strip.setPixelColor(led_index, Color(BRIGHTNESS, BRIGHTNESS, BRIGHTNESS))

        # Mettre à jour l'affichage de la bande LED
        strip.show()
        time.sleep(DELAY)

        # Avancer les positions des halos
        position1 = (position1 + 1) % NUM_LEDS
        position2 = (position2 + 1) % NUM_LEDS

try:
    halo_size1 = HALO_SIZE  # Taille du premier halo
    halo_size2 = HALO_SIZE  # Taille du deuxième halo (par exemple, la moitié de la taille du premier)
    move_halo(halo_size1, halo_size2)
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
