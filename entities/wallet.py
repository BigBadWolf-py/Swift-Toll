from datetime import datetime

from entities.baseentity import BaseEntity


class Wallet(BaseEntity):
    """
    Model class for Wallet
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.balance = float(item.get('balance'))
        self.autouse = item.get('autouse')


    @staticmethod
    def get_table():
        return 't_wallet'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)
