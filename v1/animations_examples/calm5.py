from rpi_ws281x import Adafruit_NeoPixel, Color
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 50
BRIGHTNESS = 255
INITIAL_BRIGHTNESS = int(BRIGHTNESS * 0.20)  # 20% de luminosité
HALO_SIZE = 10
FADE_STEP = 5
DELAY = 0.02

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, INITIAL_BRIGHTNESS)
strip.begin()


def set_brightness(pixel_index, brightness):
    """Définit la luminosité d'une LED à un niveau spécifié."""
    strip.setPixelColor(pixel_index, Color(brightness, brightness, brightness))


def initialize_strip():
    """Initialise toute la bande LED à une couleur blanche avec 20 % de luminosité."""
    for i in range(NUM_LEDS):
        set_brightness(i, INITIAL_BRIGHTNESS)
    strip.show()


def move_halo():
    position = 0

    while True:
        # Éteindre la LED à l'arrière du halo avec un fade out
        for i in range(0, HALO_SIZE):
            current_led = (position - i - 1) % NUM_LEDS
            brightness = INITIAL_BRIGHTNESS + i * FADE_STEP
            set_brightness(current_led, max(INITIAL_BRIGHTNESS, brightness - FADE_STEP))
            strip.show()
            time.sleep(DELAY)

        # Allumer la LED à l'avant du halo avec un fade in
        for i in range(0, HALO_SIZE):
            current_led = (position - i) % NUM_LEDS
            brightness = INITIAL_BRIGHTNESS + i * FADE_STEP
            set_brightness(current_led, min(BRIGHTNESS, brightness + FADE_STEP))
            strip.show()
            time.sleep(DELAY)

        # Avancer la position du halo
        position = (position + 1) % NUM_LEDS


try:
    initialize_strip()
    move_halo()
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
