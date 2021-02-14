from dao.basedao import BaseDAO
from entities.fcm import FCM
from entities.wallet import Wallet


class WalletDAO(BaseDAO):
    __TABLE_NAME = 't_wallet'

    def __init__(self):
        pass

    @classmethod
    def get_wallet_by_id(cls, id):
        sql = "SELECT * FROM {0} where id='{1}'".format(cls.__TABLE_NAME, id)
        wallet = cls._get_item(sql)
        if wallet:
            if wallet['autouse'] == '\x00':
                wallet['autouse'] = False
            elif wallet['autouse'] == '\x01':
                wallet['autouse'] = True
            return Wallet(wallet)
        else:
            raise Exception('No result found')