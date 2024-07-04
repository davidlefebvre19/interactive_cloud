from rpi_ws281x import Adafruit_NeoPixel, Color
import time

# Configuration des LED
PIN = 12
NUM_LEDS = 50
BRIGHTNESS = 255
HALO_SIZE = 7
DELAY = 0.05
NUM_HALOS = 5

# Initialisation de la bande de LEDs
strip = Adafruit_NeoPixel(NUM_LEDS, PIN, 800000, 10, False, BRIGHTNESS)
strip.begin()

def set_halo(position, size, color):
    """Allume les LEDs pour créer un halo lumineux."""
    for i in range(size):
        led_index = (position + i) % NUM_LEDS
        strip.setPixelColor(led_index, color)

def clear_halo(position, size):
    """Éteint les LEDs derrière le halo."""
    for i in range(size):
        led_index = (position + i) % NUM_LEDS
        strip.setPixelColor(led_index, Color(0, 0, 0))

def move_halos():
    # Initialisation des positions des halos de manière équidistante
    positions = [i * (NUM_LEDS // NUM_HALOS) for i in range(NUM_HALOS)]

    while True:
        # Éteindre les LEDs derrière les halos précédents
        for position in positions:
            clear_halo(position, HALO_SIZE)

        # Mettre à jour les positions des halos
        for i in range(NUM_HALOS):
            positions[i] = (positions[i] + 1) % NUM_LEDS

        # Vérifier que les halos ne se chevauchent pas
        for i in range(NUM_HALOS):
            for j in range(i + 1, NUM_HALOS):
                if abs(positions[i] - positions[j]) < HALO_SIZE:
                    if positions[i] < positions[j]:
                        positions[j] = (positions[i] + HALO_SIZE) % NUM_LEDS
                    else:
                        positions[i] = (positions[j] + HALO_SIZE) % NUM_LEDS

        # Allumer les LEDs pour les nouveaux halos
        for position in positions:
            set_halo(position, HALO_SIZE, Color(BRIGHTNESS, BRIGHTNESS, BRIGHTNESS))

        # Mettre à jour l'affichage de la bande LED
        strip.show()
        time.sleep(DELAY)

try:
    move_halos()
except KeyboardInterrupt:
    # Éteindre toutes les LEDs à l'arrêt du programme
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()