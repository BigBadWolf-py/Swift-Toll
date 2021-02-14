from bottle import route, request
from common import endpoints, validator
from common.routeutils import result, error_handler
from dao.vehicledao import VehicleDAO
from entities.vehicle import Vehicle


@route(endpoints.REGISTER_VEHICLE, method=['POST'])
@error_handler
def register_vehicle():
    """
    sample_data :
    {
        "vehicle_type": "1",
        "vehicle_number": "RJ02-AA-1111",
        "user_id": "1"
    }
    :return:  {'vehicle_id': vehicle_id}
    """
    item = validator.validate_json(request.json, ['user_id', 'vehicle_number', 'vehicle_type'])
    vehicle = Vehicle(item)
    vehicle_id = vehicle.insert()
    return result(data={'vehicle_id': vehicle_id})


@route(endpoints.GET_VEHICLES, method=['GET'])
@error_handler
def get_vehicles(user_id):
    vehicles = VehicleDAO.get_active_vehicle_by_user_id(user_id)
    return result(data=vehicles)


@route(endpoints.DELETE_VEHICLES, method=['GET'])
@error_handler
def delete_vehicles(vehicle_id):
    try:
        vehicle = VehicleDAO.get_vehicle_by_id(vehicle_id)
        vehicle.deleted = True
        vehicle.update(['deleted'])
        return result(data={'deleted': True})
    except:
        return result(data={'deleted': False})

