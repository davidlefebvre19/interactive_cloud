from rpi_ws281x import Adafruit_NeoPixel, Color
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 50
BRIGHTNESS = 255
DELAY = 0.05

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()


def move_halo(halo_size):
    position = 0

    while True:
        # Éteindre toutes les LEDs
        for i in range(NUM_LEDS):
            strip.setPixelColor(i, Color(0, 0, 0))

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
    halo_size = 10  # Par exemple, un halo de 10 LEDs
    move_halo(halo_size)
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()