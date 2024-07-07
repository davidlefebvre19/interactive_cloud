from rpi_ws281x import Adafruit_NeoPixel, Color
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 300
BRIGHTNESS = 255
MIN_BRIGHTNESS = int(BRIGHTNESS * 0.20)  # 20% de la luminosité maximale
HALO_SIZE = 10
FADE_STEP = 10  # Pas du fondu en millisecondes
DELAY = 0.05

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def set_background():
    """Allume le fond avec une couleur bleu foncé et 20% de luminosité."""
    for i in range(NUM_LEDS):
        strip.setPixelColor(i, Color(0, 0, MIN_BRIGHTNESS))
    strip.show()

def fade_in(pixel_index):
    """Effet de fade-in pour une LED spécifique."""
    current_color = strip.getPixelColor(pixel_index)
    current_brightness = (current_color & 0xff0000) >> 16  # Extrait la composante rouge comme luminosité

    for brightness in range(current_brightness, BRIGHTNESS + 1, FADE_STEP):
        strip.setPixelColor(pixel_index, Color(brightness, brightness, brightness))
        strip.show()
        time.sleep(DELAY)

def fade_out(pixel_index):
    """Effet de fade-out pour une LED spécifique."""
    current_color = strip.getPixelColor(pixel_index)
    current_brightness = (current_color & 0xff0000) >> 16  # Extrait la composante rouge comme luminosité

    for brightness in range(current_brightness, MIN_BRIGHTNESS - 1, -FADE_STEP):
        strip.setPixelColor(pixel_index, Color(brightness, brightness, brightness))
        strip.show()
        time.sleep(DELAY)

def move_halo(halo_size):
    position = 0

    while True:
        # Éteindre toutes les LEDs avec un fade-out progressif
        for i in range(NUM_LEDS):
            fade_out(i)

        # Allumer les LEDs pour le halo actuel avec un fade-in progressif
        for i in range(halo_size):
            led_index = (position + i) % NUM_LEDS
            fade_in(led_index)

        # Mettre à jour la bande LED
        strip.show()
        time.sleep(DELAY)

        # Avancer la position du halo
        position = (position + 1) % NUM_LEDS

try:
    halo_size = 10  # Par exemple, un halo de 10 LEDs
    move_halo(halo_size)
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()