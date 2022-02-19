from myapp.views import auth, database


def load_user(request):

    username, image, localId = None, None, None
    try:
        localId = auth.get_account_info(request.session.get('token', None))
        if localId:
            localId = localId["users"][0]["localId"]
            image = database.child("users").child(localId).child('details').child('image').get().val()
            username = database.child("users").child(localId).child('details').child('name').get().val()
    except:
        pass
    return {'username': username, "user_image": image}
