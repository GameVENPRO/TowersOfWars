
TOKEN = "1623058330:AAGsL076jnv3FIiRHEgJyfumeCmmMiSasHA" #Test
DEV_MODO = True

def Fire():
    from firebase import firebase
    fire = firebase.FirebaseApplication("https://torrerpgbot-default-rtdb.firebaseio.com",None)
    return fire

