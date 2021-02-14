from datetime import datetime

from entities.baseentity import BaseEntity


class Booking(BaseEntity):
    """
    Model class for Booking
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.vehicle_id = item.get('vehicle_id')
        self.type = item.get('type')
        self.trip_type = item.get('trip_type')
        self.vehicle_no = item.get('vehicle_no')
        self.total_amount = item.get('total_amount')
        self.access_code = item.get('access_code')
        self.valid = item.get('valid', True)
        self.payment_status = item.get('payment_status')
        self.trip_name = item.get('trip_name')
        self.txn_gates = item.get('txn_gates')
        self.created_on = item.get('created_on', datetime.now())
        self.updated_on = item.get('updated_on', datetime.now())

    @staticmethod
    def get_table():
        return 't_booking'

    class PaymentStatus:
        PAID = 'PAID'
        UNPAID = 'UNPAID'

    class Type:
        SINGLE = 'SINGLE'
        MULTI = 'MULTI'

    class TripType:
        ONE_WAY = 'ONE_WAY'
        RETURN = 'RETURN'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)
