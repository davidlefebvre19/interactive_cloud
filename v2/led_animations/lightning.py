from rpi_ws281x import *
from art import *
import random
import time

PIN = 12
NUM_LEDS = 300
BRIGHTNESS = 255
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

ZONE_LENGTH = 50  # Longueur de chaque zone
FADE_OUT_RATE_LIGHTNING = 10  # Vitesse du fondu
LIGHTNING_COLOR = Color(255, 255, 0)

def lightning_effect( zone, fade_out_rate):
    """ Créer un effet d'éclair dans une zone spécifique """
    start_led = random.randint(zone * ZONE_LENGTH, (zone + 1) * ZONE_LENGTH - 1)
    end_led = random.randint(start_led, (zone + 1) * ZONE_LENGTH - 1)

    # Premier clignotement
    for i in range(start_led, end_led):
        strip.setPixelColor(i, LIGHTNING_COLOR)
    strip.show()
    time.sleep(0.05)  # Durée du clignotement

    # Éteindre les LEDs
    for i in range(start_led, end_led):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()

    # Deuxième clignotement avec fondu
    for i in range(start_led, end_led):
        strip.setPixelColor(i, LIGHTNING_COLOR)
    strip.show()
    time.sleep(0.05)  # Durée du clignotement

    # Fondu
    for brightness in range(255, 0, -fade_out_rate):
        for i in range(start_led, end_led):
            strip.setPixelColor(i, Color(brightness, brightness, 0))
        strip.show()
        time.sleep(0.01)


def run_thunder():
    print("thunder started")

    while True:
        # Logique pour la gestion des LEDs
        for zone in range(NUM_LEDS // ZONE_LENGTH):
            if random.choice([True, False]):  # 50% de chance d'activer l'éclair
                lightning_effect(zone, FADE_OUT_RATE_LIGHTNING)
        time.sleep(random.uniform(0.1, 0.5))  # Intervalle aléatoire entre les éclairs
        time.sleep(0.1)

if __name__ == "__main__":
    run_thunder()