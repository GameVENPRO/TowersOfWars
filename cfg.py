
TOKEN = "1925318172:AAEz1PlQeCN8S2DVMHZ7QINm_oyTjlA9nRA"  # Beta
# TOKEN = "1623058330:AAGsL076jnv3FIiRHEgJyfumeCmmMiSasHA" #TorreRPG

DEV_MODO = True


def Fire():
    from firebase import firebase
    fire = firebase.FirebaseApplication(
        "https://torrerpgbot-default-rtdb.firebaseio.com", None)
    return fire
