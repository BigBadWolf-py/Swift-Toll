from dao.basedao import BaseDAO
# The Toll Rate Data Access Object handles all interactions with the TollRate table.
from entities.txngatecrossing import TxnGateCrossing


class TxnGateCrossingDAO(BaseDAO):
    __TABLE_NAME = 't_txn_gate_crossing'

    def __init__(self):
        pass

    @classmethod
    def get_first_crossing(cls, txn_id):
        sql = "SELECT * FROM {0} where txn_id={1} ORDER BY created_on ASC LIMIT 1".format(cls.__TABLE_NAME, txn_id)
        gate_crossing = cls._get_item(sql)
        if gate_crossing:
            return TxnGateCrossing(gate_crossing)
        else:
            raise Exception('No result found')

    @classmethod
    def get_all_crossings(cls, txn_id):
        sql = "SELECT * FROM {0} where txn_id={1}".format(cls.__TABLE_NAME, txn_id)
        crossings = cls._get_items(sql)
        if crossings:
            return [TxnGateCrossing(item) for item in crossings]
        else:
            raise Exception('No result found')