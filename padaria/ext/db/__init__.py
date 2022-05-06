import pyrebase

config  = {"apiKey": "AIzaSyADCXTTdeLa7zYLM8cUz-P1Ri95KE5XWBY",
                  'authDomain': "padaria-46670.firebaseapp.com",
                  'databaseURL': "https://padaria-46670-default-rtdb.firebaseio.com",
                  'projectId': "padaria-46670",
                  'storageBucket': "padaria-46670.appspot.com",
                  'messagingSenderId': "171323091831",
                  'appId': "1:171323091831:web:a3b1b715c520fc151ccf72",
                  'measurementId': "G-K98SED68KQ" }
firebase = pyrebase.initialize_app(config)

def db():
    return firebase.database()

def auth():
    return  firebase.auth()

def storage():
    return firebase.storage()

