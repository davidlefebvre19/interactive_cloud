import time
import board
import neopixel

# Configuration
LED_COUNT = 300          # Number of LED pixels.
LED_PIN = board.D18     # GPIO pin connected to the pixels (18 is PCM_DIN).
LED_BRIGHTNESS = 0.5    # Set to 0 for darkest and 1 for brightest

# Create NeoPixel object
strip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=LED_BRIGHTNESS, auto_write=False)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

def color_cycle(strip, wait_ms=20):
    """Draw color cycle."""
    for j in range(255):
        for i in range(len(strip)):  # Updated this line
            strip[i] = wheel((int(i * 256 / len(strip)) + j) & 255)  # And this line
        strip.show()
        time.sleep(wait_ms/1000.0)

try:
    for i in range(30):
        color_cycle(strip)

    strip.fill((0, 0, 0))
    strip.show()
except KeyboardInterrupt:
    # Turn off all the LEDs when Ctrl+C is pressed
    strip.fill((0, 0, 0))
    strip.show()
