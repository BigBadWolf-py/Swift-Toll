from datetime import datetime
from entities.baseentity import BaseEntity


class TollRate(BaseEntity):
    """
    Model class for TollRate
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.vehicle_type_id = item.get('vehicle_type_id')
        self.gate_id = item.get('gate_id')
        self.created_on = item.get('created_on', datetime.now())
        self.updated_on = item.get('updated_on', datetime.now())
        self.single_price = item.get('single_price')
        self.return_price = item.get('return_price')
        self.return_applicable = item.get('is_return_applicable')

    @staticmethod
    def get_table():
        return 't_toll_rates'

    def is_return_applicable(self):
        return True if self.return_price else False

    def __repr__(self):
        return 'Model id : {}'.format(self.id)
