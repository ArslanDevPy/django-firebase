from .firebase_config import firebaseConfig
import pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
storage = firebase.storage()
# storage.child("img/admin.jpg").put("admin.jpg")
