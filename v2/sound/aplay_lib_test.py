import subprocess
import os


def play_sound():
    script_dir = os.path.dirname(os.path.abspath(__file__))

    audio_file = os.path.join(script_dir, 'wind_16bit.wav')

    try:
        subprocess.run(['sudo', 'aplay', audio_file], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la lecture du fichier audio : {e}")


if __name__ == "__main__":
    play_sound()
