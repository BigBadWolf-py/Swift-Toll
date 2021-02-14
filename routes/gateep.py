from bottle import route, request
from datetime import datetime

from common import endpoints, utils, validator
from common.routeutils import result, error_handler
from dao.gatedao import GateDAO
from dao.tollratedao import TollRateDAO
from entities.gate import Gate
from entities.tollrate import TollRate
from service.gateservice import GateService


@route(endpoints.SEARCH_GATE)
@error_handler
def search_gates():
    if request.query.type == 'keyword':
        tag = request.query.tag
        vehicle_type_id = request.query.vehicle_type_id
        return result(data=GateDAO.get_gates_by_tags(tag, vehicle_type_id))
    elif request.query.type == 'nearby':
        vehicle_type_id = request.query.vehicle_type_id
        location = request.query.location
        if not location:
            raise Exception('Location not present')
        location = utils.get_location(location)
        return result(data=GateService.get_gates_by_location(location, vehicle_type_id))


@route(endpoints.GET_GATES)
@error_handler
def search_gates():
    vehicle_type_id = request.query.vehicle_type_id
    return result(data=GateDAO.get_gates(vehicle_type_id))


@route(endpoints.GET_PRICE)
@error_handler
def get_rate_of_gate(gate_id):
    if request.query.vehicle_type:
        res = TollRateDAO.get_rate_by_gate_id_and_vehicle_id(gate_id, request.query.vehicle_type)
        return_applicable = True
        if not res.return_price:
            return_applicable = False
        rate = {
            'gate_id': gate_id,
            'vehicle_type_id': request.query.vehicle_type,
            'single_price':  res.single_price,
            'return_price': res.return_price,
            'return_applicable': return_applicable
        }
        return result(data=rate)


@route(endpoints.GET_GATES, method=['POST'])
@error_handler
def create_gate():
    """
    sample_data :
    {
        "name": "CAR",
        "phone": "**********",
        "email": "***@**.com",
        "password": "*****",
        "lat": "12.121",
        "lng": "25.3453",
        "address": "Gurgaon",
        "max_usage": "2",
        "tags": "gurgaon, gurugram",
        "expiry_time": "DAY"
    }
    :return:  {'gate_id': gate_id}
    """
    item = validator.validate_json(request.json, ['name', 'phone', 'email', 'password', 'lat', 'lng', 'address',
                                                  'expiry_time'])
    gate = Gate(item)
    gate_id = gate.insert()
    return result(data={'gate_id': gate_id})


@route(endpoints.GET_GATES, method=['PUT'])
@error_handler
def update_gate():
    """
    sample_data :
    {
        "id": 1,
        "name": "CAR",
        "phone": "**********",
        "email": "***@**.com",
        "password": "*****",
        "lat": "12.121",
        "lng": "25.3453",
        "address": "Gurgaon",
        "max_usage": "2",
        "tags": "gurgaon, gurugram",
        "expiry_time": "DAY"
    }
    """
    try:
        item = validator.validate_json(request.json, ['id', 'name', 'phone', 'email', 'password', 'lat',
                                                      'lng', 'address', 'expiry_time'])
        gate = GateDAO.get_gate_by_id(item['id'])
        gate.name = item['name']
        gate.phone = item['phone']
        gate.email = item['email']
        gate.password = item['password']
        gate.lat = item['lat']
        gate.lng = item['lng']
        gate.address = item['address']
        gate.tags = item['tags']
        gate. expiry_time = item['expiry_time']
        gate.max_usage = item['max_usage']
        gate.updated_on = datetime.now()
        gate.update(['name', 'phone', 'email', 'password', 'lat', 'lng', 'address', 'expiry_time', 'max_usage', 'tags'])
        return result(data={'updated': True})
    except:
        return result(data={'updated': False})


@route(endpoints.TOLL_RATE, method=['POST'])
@error_handler
def create_toll_rate():
    """
    sample_data :
    {
        "vehicle_type_id": 1,
        "gate_id": 4,
        "single_price": 25,
        "return_price": 40,
    }
    :return:  {'toll_rate_id': toll_rate_id}
    """
    item = validator.validate_json(request.json, ['vehicle_type_id', 'gate_id', 'single_price'])
    toll_rate = TollRate(item)
    toll_rate_id = toll_rate.insert()
    return result(data={'toll_rate_id': toll_rate_id})


@route(endpoints.TOLL_RATE, method=['PUT'])
@error_handler
def update_toll_rate():
    """
    sample_data :
    {
        "id": 1,
        "vehicle_type_id": 1,
        "gate_id": 4,
        "single_price": 25,
        "return_price": 40,
    }
    """
    try:
        item = validator.validate_json(request.json, ['id', 'vehicle_type_id', 'gate_id', 'single_price'])
        tollrate = TollRateDAO.get_rate_by_id(item['id'])
        tollrate.vehicle_type_id = item['vehicle_type_id']
        tollrate.gate_id = item['gate_id']
        tollrate.single_price = item['single_price']
        tollrate.return_price = item['return_price']
        tollrate.updated_on = datetime.now()
        tollrate.update(['vehicle_type_id', 'gate_id', 'single_price', 'return_price'])
        return result(data={'updated': True})
    except:
        return result(data={'updated': False})
