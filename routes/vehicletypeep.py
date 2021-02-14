from bottle import route, request
from datetime import datetime

from common import endpoints, validator
from common.routeutils import result, error_handler
from dao.vehicletypedao import VehicleTypeDAO
from entities.vehicletype import VehicleType


@route(endpoints.GET_VEHICLE_TYPES, method=['GET'])
@error_handler
def get_vehicle_types():
    vehicle_types = VehicleTypeDAO.get_vehicle_types()
    return result(data=vehicle_types)


@route(endpoints.VEHICLE_TYPE, method=['POST'])
@error_handler
def register_vehicle_type():
    """
    sample_data :
    {
        "vehicle_name": "CAR"
    }
    :return:  {'vehicle_id': vehicle_id}
    """
    item = validator.validate_json(request.json, ['vehicle_name'])
    vehicle_type = VehicleType(item)
    vehicle_type_id = vehicle_type.insert()
    return result(data={'vehicle_type_id': vehicle_type_id})


@route(endpoints.VEHICLE_TYPE, method=['PUT'])
@error_handler
def update_vehicle_type():
    """
    sample_data :
    {
        "id": 1,
        "vehicle_name": "CAR"
    }
    """
    item = validator.validate_json(request.json, ['id', 'vehicle_name'])
    try:
        vehicle_type = VehicleTypeDAO.get_vehicle_types_by_id(item['id'])
        vehicle_type.vehicle_name = item['vehicle_name']
        vehicle_type.updated_on = datetime.now()
        vehicle_type.update(['vehicle_name', 'updated_on'])
        return result(data={'updated': True})
    except:
        return result(data={'updated': False})
