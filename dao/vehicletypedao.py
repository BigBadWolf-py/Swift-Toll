# The Vehicle Tyep Data Access Object handles all interactions with the vehicle type table.
from dao.basedao import BaseDAO
from entities.vehicle import Vehicle
from entities.vehicletype import VehicleType


class VehicleTypeDAO(BaseDAO):
    __TABLE_NAME = 't_vehicle_type'

    def __init__(self):
        pass

    @classmethod
    def get_vehicle_types(cls):
        sql = "SELECT * FROM {0}".format(cls.__TABLE_NAME)
        vehicle_types = cls._get_items(sql)
        if vehicle_types:
            return [VehicleType(item) for item in vehicle_types]
        else:
            raise Exception('No result found')

    @classmethod
    def get_vehicle_types_by_id(cls, id):
        sql = "SELECT * FROM {0} where id={1}".format(cls.__TABLE_NAME, id)
        vehicle_types = cls._get_item(sql)
        if vehicle_types:
            return VehicleType(vehicle_types)
        else:
            raise Exception('No result found')

