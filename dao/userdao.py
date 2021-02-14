# The User Data Access Object handles all interactions with the user table.
from dao.basedao import BaseDAO
from dao.walletdao import WalletDAO
from entities.user import User
from entities.vehicle import Vehicle
from entities.wallet import Wallet


class UserDAO(BaseDAO):
    __TABLE_NAME = 't_users'

    def __init__(self):
        pass

    @classmethod
    def validate_user(cls, phone, password):
        sql = "SELECT * FROM {0} where phone='{1}' and password='{2}'".format(cls.__TABLE_NAME, phone, password)
        user = cls._get_item(sql)
        return User(user) if user else None

    @classmethod
    def get_username_from_id(cls, id):
        sql = "SELECT * FROM {0} where id='{1}'".format(cls.__TABLE_NAME, id)
        user = cls._get_item(sql)
        return User(user).name if user else None

    @classmethod
    def get_user_by_id(cls, id):
        sql = "SELECT * FROM {0} where id='{1}'".format(cls.__TABLE_NAME, id)
        user = cls._get_item(sql)
        return User(user) if user else None

    @classmethod
    def get_user_by_phone(cls, phone):
        sql = "SELECT * FROM {0} where phone='{1}'".format(cls.__TABLE_NAME, phone)
        user = cls._get_item(sql)
        return User(user) if user else None

    @classmethod
    def get_wallet_from_user_id(cls, id):
        sql = "SELECT * FROM {0} where id='{1}'".format(cls.__TABLE_NAME, id)
        user = cls._get_item(sql)
        if user:
            wallet_id = User(user).wallet_id
            w = WalletDAO.get_wallet_by_id(wallet_id)
            if w:
                return w
            else:
                return None

