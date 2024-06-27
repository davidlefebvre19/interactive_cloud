from rpi_ws281x import *
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 17
BRIGHTNESS = 255
HALO_SIZE = 3  # Taille de chaque halo
FADE_RATE = 5  # Vitesse du fondu
DELAY = 0.05   # Délai entre chaque mise à jour d'animation

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def set_halo_brightness(strip, start_led, halo_size, brightness):
    """ Régle la luminosité d'un halo de LEDs. """
    for i in range(start_led, start_led + halo_size):
        if 0 <= i < strip.numPixels():
            strip.setPixelColor(i, Color(brightness, brightness, brightness))
    strip.show()

try:
    current_led = 0
    brightness = 0
    increasing = True  # Direction du fondu (augmentation ou diminution)

    while True:
        set_halo_brightness(strip, current_led, HALO_SIZE, brightness)

        # Mise à jour de la luminosité pour le fondu
        if increasing:
            brightness += FADE_RATE
            if brightness >= BRIGHTNESS:
                brightness = BRIGHTNESS
                increasing = False
        else:
            brightness -= FADE_RATE
            if brightness <= 0:
                brightness = 0
                increasing = True
                current_led = (current_led + 1) % NUM_LEDS  # Déplacer le halo

        time.sleep(DELAY)

except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()