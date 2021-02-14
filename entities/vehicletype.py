from datetime import datetime
from entities.baseentity import BaseEntity


class VehicleType(BaseEntity):
    """
    Model class for VehicleType
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.vehicle_name = item.get('vehicle_name')
        self.created_on = item.get('created_on', datetime.now())
        self.updated_on = item.get('updated_on', datetime.now())

    @staticmethod
    def get_table():
        return 't_vehicle_type'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)