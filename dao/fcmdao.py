from dao.basedao import BaseDAO
from entities.fcm import FCM


class FCMDAO(BaseDAO):
    __TABLE_NAME = 't_fcm'

    def __init__(self):
        pass

    @classmethod
    def get_fcmid_from_user_id(cls, user_id):
        sql = "SELECT * FROM {0} where user_id='{1}'".format(cls.__TABLE_NAME, user_id)
        fcm = cls._get_item(sql)
        if fcm:
            return FCM(fcm)
        else:
            raise Exception('No result found')

    @classmethod
    def get_fcmid_from_id(cls, fcm_id):
        sql = "SELECT * FROM {0} where device_token='{1}'".format(cls.__TABLE_NAME, fcm_id)
        fcm = cls._get_item(sql)
        if fcm:
            return FCM(fcm)
        else:
            raise Exception('No result found')
