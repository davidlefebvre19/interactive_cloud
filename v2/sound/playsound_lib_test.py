# import required module
from playsound import playsound
import os

filename = "wind.wav"

chemin_fichier = os.path.join(os.getcwd(), filename)

# for playing note.wav file
playsound(chemin_fichier)
print('playing sound using  playsound')

