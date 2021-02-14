from dao.basedao import BaseDAO


# The Toll Rate Data Access Object handles all interactions with the TollRate table.
from entities.gate import Gate
from entities.tollrate import TollRate


class TollRateDAO(BaseDAO):
    __TABLE_NAME = 't_toll_rates'

    def __init__(self):
        pass

    @classmethod
    def get_rate_by_gate_id_and_vehicle_id(cls, gate_id, vehicle_id):
        sql = "SELECT * FROM {0} where gate_id='{1}' and vehicle_type_id='{2}'".format(cls.__TABLE_NAME, gate_id,
                                                                                       vehicle_id)
        toll_rate = cls._get_item(sql)
        if toll_rate:
            return TollRate(toll_rate)
        else:
            raise Exception('No result found')

    @classmethod
    def get_rate_by_id(cls, id):
        sql = "SELECT * FROM {0} where id={1}".format(cls.__TABLE_NAME, id)
        toll_rate = cls._get_item(sql)
        if toll_rate:
            return TollRate(toll_rate)
        else:
            raise Exception('No result found')

    @classmethod
    def get_rate_by_gate_id(cls, gate_id, vehicle_type_id):
        sql = "SELECT * FROM {0} where gate_id='{1}' and vehicle_type_id='{2}'".format(cls.__TABLE_NAME, gate_id, vehicle_type_id)
        toll_rate = cls._get_item(sql)
        if toll_rate:
            return TollRate(toll_rate)
        else:
            raise Exception('No result found')
