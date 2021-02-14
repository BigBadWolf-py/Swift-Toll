from datetime import datetime
from entities.baseentity import BaseEntity


class TxnGate(BaseEntity):
    """
    Model class for TxnGate
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.booking_id = item.get('booking_id')
        self.gate_id = item.get('gate_id')
        self.amount = item.get('amount')
        self.times_used = item.get('times_used')
        self.valid = item.get('valid')
        self.gate = item.get('gate')
        self.txn_gate_crossing = item.get('txn_gate_crossing')
        self.refunded = item.get('refunded')

    @staticmethod
    def get_table():
        return 't_txn_gates'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)
