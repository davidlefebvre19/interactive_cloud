from rpi_ws281x import Adafruit_NeoPixel, Color
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 300
BRIGHTNESS = 255
MIN_BRIGHTNESS = int(BRIGHTNESS * 0.20)  # 20% de la luminosité maximale
HALO_SIZE = 50
FADE_STEP = 10  # Pas du fondu en millisecondes
DELAY = 0.05

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def set_background():
    """Allume le fond avec une couleur bleu foncé."""
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

def move_halos(halo_size_1, halo_size_2):
    position_1 = 0
    position_2 = NUM_LEDS // 2  # Démarre le second halo à la moitié de la bande LED

    while True:
        # Éteindre toutes les LEDs avec un fade-out progressif
        for i in range(NUM_LEDS):
            fade_out(i)

        # Allumer les LEDs pour le premier halo avec un fade-in progressif
        for i in range(halo_size_1):
            led_index = (position_1 + i) % NUM_LEDS
            fade_in(led_index)

        # Allumer les LEDs pour le second halo avec un fade-in progressif
        for i in range(halo_size_2):
            led_index = (position_2 + i) % NUM_LEDS
            fade_in(led_index)

        # Mettre à jour l'affichage de la bande LED
        strip.show()
        time.sleep(DELAY)

        # Avancer les positions des halos
        position_1 = (position_1 + 1) % NUM_LEDS
        position_2 = (position_2 + 1) % NUM_LEDS

try:
    halo_size_1 = HALO_SIZE  # Taille du premier halo
    halo_size_2 = HALO_SIZE  # Taille du second halo
    move_halos(halo_size_1, halo_size_2)
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
