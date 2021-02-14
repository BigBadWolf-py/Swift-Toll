from datetime import datetime

from entities.baseentity import BaseEntity


class FCM(BaseEntity):
    """
    Model class for FCM
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.user_id = item.get('user_id')
        self.device_token = item.get('device_token')
        self.created_on = item.get('created_on', datetime.now())
        self.updated_on = item.get('updated_on', datetime.now())

    @staticmethod
    def get_table():
        return 't_fcm'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)
