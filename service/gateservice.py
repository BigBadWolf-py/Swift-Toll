from dao.gatedao import GateDAO
from dao.tollratedao import TollRateDAO
from dao.vehicledao import VehicleDAO
from service import googlemapservice


class GateService():
    @classmethod
    def get_gates_by_location(cls, location, vehicle_type_id):
        gates = googlemapservice.search_nearby_gates(location)
        searched_gates = []
        for gate in gates:
            for g in GateDAO.get_gates_by_name(gate, vehicle_type_id):
                searched_gates.append(g)
        return searched_gates

    @classmethod
    def get_price(cls, gate_id, vehicle_id):
        vehicle = VehicleDAO.get_vehicle_by_id(vehicle_id)
        return TollRateDAO.get_rate_by_gate_id_and_vehicle_id(gate_id, vehicle.vehicle_type)

