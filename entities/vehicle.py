from datetime import datetime
from entities.baseentity import BaseEntity


class Vehicle(BaseEntity):
    """
    Model class for Vehicle
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.vehicle_type = item.get('vehicle_type')
        self.vehicle_name = item.get('vehicle_name')
        self.vehicle_number = item.get('vehicle_number')
        self.user_id = item.get('user_id')
        self.deleted = item.get('deleted', False)
        self.nickname = item.get('nickname')
        self.created_on = item.get('created_on', datetime.now())
        self.updated_on = item.get('updated_on', datetime.now())

    @staticmethod
    def get_table():
        return 't_vehicle'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)