import bluetooth

serverMACAddress = 'XX:XX:XX:XX:XX:XX'  # Remplacez par l'adresse MAC de votre Raspberry Pi
port = 3  # Port utilisé pour la connexion Bluetooth, peut nécessiter un ajustement
size = 1024

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((serverMACAddress, port))

# Envoi d'une commande manuelle
sock.send("commande manuelle")

sock.close()