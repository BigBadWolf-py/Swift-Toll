from datetime import datetime

from entities.baseentity import BaseEntity


class Gate(BaseEntity):
    """
    Model class for Gate
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.unique_id = item.get('unique_id')
        self.name = item.get('name')
        self.email = item.get('email')
        self.phone = item.get('phone')
        self.password = item.get('password')
        self.lat = item.get('lat')
        self.lng = item.get('lng')
        self.address = item.get('address')
        self.created_on = item.get('created_on', datetime.now())
        self.updated_on = item.get('updated_on', datetime.now())
        self.last_login_time = item.get('last_login_time')
        self.max_usage = item.get('max_usage')
        self.toll_rate = item.get('toll_rate')
        self.expiry_time = item.get('expiry_time')
        if item.get('tags'):
            self.tags = [i.strip() for i in item.get('tags').split(',')]
        else:
            self.tags = []

    @staticmethod
    def get_table():
        return 't_gates'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)
