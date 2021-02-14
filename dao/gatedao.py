from dao.basedao import BaseDAO


# The Gate Data Access Object handles all interactions with the Gate table.
from dao.tollratedao import TollRateDAO
from entities.gate import Gate


class GateDAO(BaseDAO):
    __TABLE_NAME = 't_gates'

    def __init__(self):
        pass

    @classmethod
    def get_gate_by_id(cls, id):
        sql = "SELECT * FROM {0} where id='{1}'".format(cls.__TABLE_NAME, id)
        gate = cls._get_item(sql)
        if gate:
            return Gate(gate)
        else:
            raise Exception('No gate found for id : {0}'.format(id))

    @classmethod
    def get_gates_by_tags(cls, tag, vehicle_type_id):
        sql = "SELECT * FROM {0} where tags like '%{1}%'".format(cls.__TABLE_NAME, tag)
        gates = cls._get_items(sql)
        if gates:
            gtes = []
            for gate in gates:
                g = Gate(gate)
                toll_r = TollRateDAO.get_rate_by_gate_id(gate['id'], vehicle_type_id)
                if toll_r:
                    toll_r.return_applicable = toll_r.is_return_applicable()
                g.toll_rate = toll_r
                gtes.append(g)
            return gtes
        else:
            raise Exception('No result found!!')

    @classmethod
    def get_gates_by_name(cls, tag, vehicle_type_id):
        sql = "SELECT * FROM {0} where name like '%{1}%'".format(cls.__TABLE_NAME, tag)
        gates = cls._get_items(sql)
        if gates:
            gtes = []
            for gate in gates:
                g = Gate(gate)
                toll_r = TollRateDAO.get_rate_by_gate_id(gate['id'], vehicle_type_id)
                if toll_r:
                    toll_r.return_applicable = toll_r.is_return_applicable()
                g.toll_rate = toll_r
                gtes.append(g)
            return gtes
        else:
            raise Exception('No result found!!')

    @classmethod
    def get_gates(cls, vehicle_type_id):
        sql = "SELECT * FROM {0}".format(cls.__TABLE_NAME)
        gates = cls._get_items(sql)
        if gates:
            gtes = []
            for gate in gates:
                g = Gate(gate)
                toll_r = TollRateDAO.get_rate_by_gate_id(gate['id'], vehicle_type_id)
                if toll_r:
                    toll_r.return_applicable = toll_r.is_return_applicable()
                g.toll_rate = toll_r
                gtes.append(g)
            return gtes
        else:
            raise Exception('No result found!!')
