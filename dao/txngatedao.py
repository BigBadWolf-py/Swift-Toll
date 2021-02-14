from dao.basedao import BaseDAO
# The TxnGate Data Access Object handles all interactions with the TxnGate table.
from dao.gatedao import GateDAO
from entities.txngate import TxnGate


class TxnGateDAO(BaseDAO):
    __TABLE_NAME = 't_txn_gates'

    def __init__(self):
        pass

    @classmethod
    def get_txn_gate_by_gate_id_and_booking_id(cls, booking_id, gate_id):
        sql = "SELECT * FROM {0} where booking_id={1} and gate_id={2} and valid=true".format(cls.__TABLE_NAME,
                                                                                             booking_id, gate_id)
        txn_gates = cls._get_items(sql)
        if txn_gates:
            return [TxnGate(txn_gate) for txn_gate in txn_gates]
        else:
            raise Exception('No gate for booking and gate id {0}, {1}'.format(booking_id, gate_id))

    @classmethod
    def get_all_txn_gate_by_gate_id_and_booking_id(cls, booking_id, gate_id):
        sql = "SELECT * FROM {0} where booking_id={1} and gate_id={2}".format(cls.__TABLE_NAME,
                                                                                             booking_id, gate_id)
        txn_gates = cls._get_items(sql)
        if txn_gates:
            return [TxnGate(txn_gate) for txn_gate in txn_gates]
        else:
            raise Exception('No gate for booking and gate id {0}, {1}'.format(booking_id, gate_id))

    @classmethod
    def get_txn_gate_by_booking_id(cls, booking_id):
        sql = "SELECT * FROM {0} where booking_id={1}".format(cls.__TABLE_NAME, booking_id)
        txn_gates = cls._get_items(sql)
        new_txn_gates = []
        if txn_gates:
            for txn_gate in txn_gates:
                if txn_gate['valid'] == '\x00':
                    txn_gate['valid'] = False
                elif txn_gate['valid'] == '\x01':
                    txn_gate['valid'] = True
                txn_gate['gate'] = GateDAO.get_gate_by_id(txn_gate['gate_id'])
                new_txn_gates.append(TxnGate(txn_gate))
            return new_txn_gates
        else:
            raise Exception('No result found')

    @classmethod
    def get_valid_gates(cls, booking_id):
        sql = "SELECT * FROM {0} where booking_id={1} and valid=true".format(cls.__TABLE_NAME, booking_id)
        txn_gates = cls._get_items(sql)
        if txn_gates:
            return [TxnGate(txn_gate) for txn_gate in txn_gates]
        else:
            raise Exception('No result found')

