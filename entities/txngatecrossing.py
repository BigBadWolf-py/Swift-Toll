from datetime import datetime
from entities.baseentity import BaseEntity


class TxnGateCrossing(BaseEntity):
    """
    Model class for TxnGateCrossing
    """
    def __init__(self, item=None):
        self.id = item.get('id')
        self.txn_id = item.get('txn_id')
        self.created_on = item.get('created_on', datetime.now())

    @staticmethod
    def get_table():
        return 't_txn_gate_crossing'

    def __repr__(self):
        return 'Model id : {}'.format(self.id)
