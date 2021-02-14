# The Vehicle Data Access Object handles all interactions with the vehicle table.
from dao.basedao import BaseDAO
from dao.vehicletypedao import VehicleTypeDAO
from entities.vehicle import Vehicle


class VehicleDAO(BaseDAO):
    __TABLE_NAME = 't_vehicle'

    def __init__(self):
        pass

    @classmethod
    def get_vehicle_by_id(cls, id):
        sql = "SELECT * FROM {0} where id='{1}'".format(cls.__TABLE_NAME, id)
        vehicle = cls._get_item(sql)
        if vehicle:
            return Vehicle(vehicle)
        else:
            raise Exception('No vehicle found for id : {0}'.format(id))

    @classmethod
    def get_vehicle_by_user_id(cls, user_id):
        sql = "SELECT * FROM {0} where user_id='{1}'".format(cls.__TABLE_NAME, user_id)
        vehicles = cls._get_items(sql)
        modi_vehicles = []
        if vehicles:
            for vehicle in vehicles:
                vehicle['vehicle_name'] = VehicleTypeDAO.get_vehicle_types_by_id(vehicle['vehicle_type']).vehicle_name
                modi_vehicles.append(Vehicle(vehicle))
            return modi_vehicles
        else:
            raise Exception('No vehicle found for user_id : {0}'.format(user_id))

    @classmethod
    def get_active_vehicle_by_user_id(cls, user_id):
        sql = "SELECT * FROM {0} where user_id='{1}' and deleted=False".format(cls.__TABLE_NAME, user_id)
        vehicles = cls._get_items(sql)
        modi_vehicles = []
        if vehicles:
            for vehicle in vehicles:
                vehicle['vehicle_name'] = VehicleTypeDAO.get_vehicle_types_by_id(vehicle['vehicle_type']).vehicle_name
                modi_vehicles.append(Vehicle(vehicle))
            return modi_vehicles
        else:
            raise Exception('No vehicle found for user_id : {0}'.format(user_id))

