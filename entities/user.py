from datetime import datetime
from entities.baseentity import BaseEntity


class User(BaseEntity):
    """
    Model class for User
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.name = item.get('name')
        self.email = item.get('email')
        self.phone = item.get('phone')
        self.last_login_ip = item.get('last_login_ip')
        self.last_login_time = item.get('last_login_time')
        self.created_on = item.get('created_on', datetime.now())
        self.updated_on = item.get('updated_on', datetime.now())
        self.password = item.get('password')
        self.registration_method = item.get('registration_method', 'USUAL')
        self.wallet_id = item.get('wallet_id')
        self.wallet = item.get('wallet')
        self.valid = item.get('valid', False)

    @staticmethod
    def get_table():
        return 't_users'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)