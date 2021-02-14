from dao.txngatecrossingdao import TxnGateCrossingDAO
from dao.txngatedao import TxnGateDAO


class TxnGateService(object):
    @classmethod
    def get_txn_gate_by_booking_id(cls, booking_id):
        txn_gates = TxnGateDAO.get_txn_gate_by_booking_id(booking_id)
        new_txn_gates = []
        ids = []
        for txn_gate in txn_gates:
            if txn_gate.gate_id not in ids:
                ids.append(txn_gate.gate_id)
                new_txn_gates.append(txn_gate)
        return new_txn_gates

    @classmethod
    def get_toll_name(cls, booking_id):
        txn_gates = cls.get_txn_gate_by_booking_id(booking_id)
        if len(txn_gates) == 1:
            return txn_gates[0].gate.name
        else:
            return txn_gates[0].gate.name + ' to ' + txn_gates[len(txn_gates)-1].gate.name

    @classmethod
    def get_toll_name_given_gates(cls, txn_gates):
        if len(txn_gates) == 1:
            return txn_gates[0].gate.name
        else:
            return txn_gates[0].gate.name + ' to ' + txn_gates[len(txn_gates) - 1].gate.name

    @classmethod
    def get_txn_gates_with_crossings(cls, booking_id):
        txn_gates = TxnGateDAO.get_txn_gate_by_booking_id(booking_id)
        new_txn_gates = []
        ids = []
        for txn_gate in txn_gates:
            if txn_gate.gate_id not in ids:
                ids.append(txn_gate.gate_id)
                try:
                    txn_gate.txn_gate_crossing = TxnGateCrossingDAO.get_all_crossings(txn_gate.id)
                except:
                    txn_gate.txn_gate_crossing = None
                new_txn_gates.append(txn_gate)
            else:
                cross = None
                try:
                    cross = TxnGateCrossingDAO.get_all_crossings(txn_gate.id)
                except:
                    pass
                crossings = new_txn_gates[ids.index(txn_gate.gate_id)].txn_gate_crossing
                if not new_txn_gates[ids.index(txn_gate.gate_id)].valid:
                    new_txn_gates[ids.index(txn_gate.gate_id)].valid = txn_gate.valid

                if crossings:
                    if cross:
                        crossings += cross
                else:
                    crossings = cross
                new_txn_gates[ids.index(txn_gate.gate_id)].txn_gate_crossing = crossings
        return new_txn_gates, cls.get_toll_name_given_gates(txn_gates)
