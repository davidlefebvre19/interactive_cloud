from rpi_ws281x import Adafruit_NeoPixel, Color

# Configuration des LED
PIN = 12
NUM_LEDS = 50
BRIGHTNESS = 255
DELAY = 0.05

try:
    # Initialisation de la bande de LEDs
    strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
    strip.begin()
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()