from models.user import UserModel


def authenticate(username,password):
    user = UserModel.find_by_username(username)
    if user and user.password == password:
        return user
        
def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)


    
"""username_mapping = {'bob': {
        'id' : 1 ,
        'username': 'bob',
        'password': 'asdf'
    }
}

userid_mapping = { 1 : {
        'id' : 1 ,
        'username': 'bob',
        'password': 'asdf'
    }
}
"""