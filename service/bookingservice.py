from common import utils
from dao.bookingdao import BookingDAO
from dao.gatedao import GateDAO
from dao.tollratedao import TollRateDAO
from dao.txngatecrossingdao import TxnGateCrossingDAO
from dao.txngatedao import TxnGateDAO
from dao.userdao import UserDAO
from dao.vehicledao import VehicleDAO
from entities.booking import Booking
from entities.gate import Gate
from entities.txngate import TxnGate
from entities.txngatecrossing import TxnGateCrossing
from service.gateservice import GateService


class BookingService:
    """
    Service class for Booking Model
    """
    def __init__(self):
        pass
    """
    @classmethod
    def validate_booking(cls, booking_id, gate_id):
        # Important method :P
        booking = BookingDAO.get_booking_by_code(booking_id)
        txn_gates = TxnGateDAO.get_txn_gate_by_gate_id_and_booking_id(booking.id, gate_id)
        gate = GateDAO.get_gate_by_id(gate_id)
        tollrate = TollRateDAO.get_rate_by_gate_id_and_vehicle_id(gate_id, booking.vehicle_id)
        if booking.TripType.ONE_WAY:
            txn_gates[0].times_used += 1
            txn_gates[0].valid = False
            # Updates the txn gate
            txn_gates[0].update(['times_used', 'valid'])
            TxnGateCrossing({'txn_id': txn_gates[0].id}).insert()
        elif booking.TripType.RETURN:
            if tollrate.is_return_applicable():
                crossing = TxnGateCrossingDAO.get_first_crossing(txn_gates[0].id)
                if gate.expiry_time == 'DAY':
                    if not utils.within_a_same_day(crossing.created_on):
                        txn_gates[0].valid = False
                        txn_gates[0].update(['valid'])
                        raise Exception('Booking expired')
                elif gate.expiry_time == 'MIDNIGHT':
                    if not utils.under_midnight(crossing.created_on):
                        txn_gates[0].valid = False
                        txn_gates[0].update(['valid'])
                        raise Exception('Booking expired')

                TxnGateCrossing({'txn_id': txn_gates[0].id}).insert()
                txn_gates[0].times_used += 1
                if gate.max_usage == txn_gates[0].times_used:
                    txn_gates[0].valid = False
                txn_gates[0].update(['times_used', 'valid'])
            else:
                txn_gates[0].times_used += 1
                txn_gates[0].valid = False
                # Updates the txn gate
                txn_gates[0].update(['times_used', 'valid'])
                TxnGateCrossing({'txn_id': txn_gates[0].id}).insert()
        try:
            TxnGateDAO.get_valid_gates(booking_id)
        except:
            booking.valid = False
            booking.update(['valid'])
        return booking_id
        """

    @classmethod
    def validate_booking_by_user_id(cls, user_id, gate_id):
        vehicles = VehicleDAO.get_vehicle_by_user_id(user_id)
        bookings = BookingDAO.get_booking_by_vehicle_ids([vehicle.id for vehicle in vehicles])
        booking_id = bookings[0].access_code
        # Important method :P
        booking = bookings[0]
        txn_gates = TxnGateDAO.get_txn_gate_by_gate_id_and_booking_id(booking.id, gate_id)
        gate = GateDAO.get_gate_by_id(gate_id)
        tollrate = TollRateDAO.get_rate_by_gate_id_and_vehicle_id(gate_id, VehicleDAO.get_vehicle_by_id(booking.vehicle_id).vehicle_type)
        valid_gate_id = ''
        if booking.TripType.ONE_WAY == booking.trip_type:
            txn_gates[0].times_used += 1
            txn_gates[0].valid = False
            valid_gate_id = txn_gates[0].gate_id
            # Updates the txn gate
            txn_gates[0].update(['times_used', 'valid'])
            TxnGateCrossing({'txn_id': txn_gates[0].id}).insert()
        elif booking.TripType.RETURN == booking.trip_type:
            if tollrate.is_return_applicable():
                if txn_gates[0].times_used == 0:
                    pass
                else:
                    crossing = TxnGateCrossingDAO.get_first_crossing(txn_gates[0].id)
                    if gate.expiry_time == 'DAY':
                        if not utils.within_a_same_day(crossing.created_on):
                            txn_gates[0].valid = False
                            txn_gates[0].update(['valid'])
                            raise Exception('Booking expired')
                    elif gate.expiry_time == 'MIDNIGHT':
                        if not utils.under_midnight(crossing.created_on):
                            txn_gates[0].valid = False
                            txn_gates[0].update(['valid'])
                            raise Exception('Booking expired')

                TxnGateCrossing({'txn_id': txn_gates[0].id}).insert()
                txn_gates[0].times_used += 1
                valid_gate_id = txn_gates[0].gate_id
                if gate.max_usage:
                    if gate.max_usage == txn_gates[0].times_used:
                        txn_gates[0].valid = False
                txn_gates[0].update(['times_used', 'valid'])
            else:
                txn_gates[0].times_used += 1
                txn_gates[0].valid = False
                valid_gate_id = txn_gates[0].gate_id
                # Updates the txn gate
                txn_gates[0].update(['times_used', 'valid'])
                TxnGateCrossing({'txn_id': txn_gates[0].id}).insert()
        try:
            txn_gates = TxnGateDAO.get_valid_gates(booking.id)
            valid = False
            for txn_gate in txn_gates:
                crossing = TxnGateCrossingDAO.get_first_crossing(txn_gate.id)
                if txn_gate.expiry_time == 'DAY':
                    if not utils.within_a_same_day(crossing.created_on):
                        txn_gate.valid = False
                        txn_gate.update(['valid'])
                    else:
                        valid = True
                elif txn_gate.expiry_time == 'MIDNIGHT':
                    if not utils.under_midnight(crossing.created_on):
                        txn_gate.valid = False
                        txn_gate.update(['valid'])
                    else:
                        valid = True
            if not valid:
                booking.valid = False
                booking.update(['valid'])
        except:
            booking.valid = False
            booking.update(['valid'])
        return booking_id, valid_gate_id

    @classmethod
    def make_booking_for_swiftpay(cls, book, gate_id, vehicles):
        gate = GateDAO.get_gate_by_id(gate_id)
        if gate.expiry_time == 'DAY':
            booking = BookingDAO.get_booking_by_vehicle_id_till_day(vehicles[0].id)
        elif gate.expiry_time == 'MIDNIGHT':
            booking = BookingDAO.get_booking_by_vehicle_id_till_midnight(vehicles[0].id)
        if not booking:
            return cls.make_booking(book, gate_id)
        booking = booking[0]
        txn_gate = None
        try:
            txn_gate = TxnGateDAO.get_all_txn_gate_by_gate_id_and_booking_id(booking.id, gate_id)[0]
        except:
            return cls.make_booking(book, gate_id)

        if gate.max_usage:
            if txn_gate.times_used >= gate.max_usage:
                return cls.make_booking(book, gate_id)

        tollrate = GateService.get_price(gate_id, booking.vehicle_id)

        if booking.trip_type == Booking.TripType.RETURN:
            if not tollrate.is_return_applicable():
                return cls.make_booking(book, gate_id)


        # Updating booking
        booking.trip_type = Booking.TripType.RETURN
        booking.valid = True

        vehicle = VehicleDAO.get_vehicle_by_id(booking.vehicle_id)
        wallet = UserDAO.get_wallet_from_user_id(vehicle.user_id)

        if tollrate.is_return_applicable():
            balance = int(tollrate.return_price) - int(booking.total_amount)
            booking.total_amount = tollrate.return_price
            txn_gate.valid = True
            txn_gate.amount = tollrate.return_price
            txn_gate.update(['valid', 'amount'])
            wallet.balance -= float(balance)
        else:
            txn_gate = TxnGate({
                'gate_id': gate_id,
                'times_used': 0,
                'valid': True,
                'refunded': False
            })
            txn_gate.booking_id = booking.id
            txn_gate.amount = tollrate.single_price
            txn_gate.insert()
            booking.total_amount = int(booking.total_amount) + int(tollrate.single_price)
            wallet.balance -= float(tollrate.single_price)
        booking.update(['trip_type', 'valid', 'total_amount'])
        wallet.update(['balance'])
        return booking.id, booking.access_code

    @classmethod
    def make_booking(cls, booking, gate_id):
        tollrate = GateService.get_price(gate_id, booking.vehicle_id)
        txn_gate = TxnGate({
            'gate_id': gate_id,
            'times_used': 0,
            'valid': True,
            'refunded': False
        })
        booking_id = None
        booking.access_code = utils.get_access_code()
        if booking.trip_type == Booking.TripType.ONE_WAY:
            booking.total_amount = tollrate.single_price
            booking_id = booking.insert()
            txn_gate.booking_id = booking_id
            txn_gate.amount = booking.total_amount
            txn_gate.insert()

        elif booking.trip_type == Booking.TripType.RETURN:
            if tollrate.is_return_applicable():
                booking.total_amount = tollrate.return_price
                booking_id = booking.insert()
                txn_gate.booking_id = booking_id
                txn_gate.amount = booking.total_amount
                txn_gate.insert()
            else:
                booking.total_amount = 2 * tollrate.single_price
                booking_id = booking.insert()
                txn_gate.booking_id = booking_id
                txn_gate.amount = tollrate.single_price
                # Inserted two times because return in not applicable so the same txn in replicated.
                txn_gate.insert()
                txn_gate.insert()
        vehicle = VehicleDAO.get_vehicle_by_id(booking.vehicle_id)
        wallet = UserDAO.get_wallet_from_user_id(vehicle.user_id)
        wallet.balance -= float(booking.total_amount)
        wallet.update(['balance'])
        return booking_id, booking.access_code

    @classmethod
    def make_booking_multi(cls, booking, gate_ids):
        tollrates = []
        txn_gates = []
        for gate_id in gate_ids:
            txn_gates.append(TxnGate({
                'gate_id': gate_id,
                'times_used': 0,
                'valid': True,
                'refunded': False
            }))
            tollrates.append(GateService.get_price(gate_id, booking.vehicle_id))

        booking.access_code = utils.get_access_code()
        booking_price = 0
        new_txn_gates = []
        for i, txn_gate in enumerate(txn_gates):
            if booking.trip_type == Booking.TripType.ONE_WAY:
                booking_price += tollrates[i].single_price
                txn_gate.amount = tollrates[i].single_price
                new_txn_gates.append(txn_gate)

            elif booking.trip_type == Booking.TripType.RETURN:
                if tollrates[i].is_return_applicable():
                    booking_price += tollrates[i].return_price
                    txn_gate.amount = tollrates[i].return_price
                    new_txn_gates.append(txn_gate)
                else:
                    booking_price += 2 * tollrates[i].single_price
                    txn_gate.amount = tollrates[i].single_price
                    # Inserted two times because return in not applicable so the same txn in replicated.
                    new_txn_gates.append(txn_gate)
                    new_txn_gates.append(txn_gate)
        booking.total_amount = booking_price
        booking_id = booking.insert()
        for txn_gate in new_txn_gates:
            txn_gate.booking_id = booking_id
            txn_gate.insert()
        vehicle = VehicleDAO.get_vehicle_by_id(booking.vehicle_id)
        wallet = UserDAO.get_wallet_from_user_id(vehicle.user_id)
        wallet.balance -= float(booking.total_amount)
        wallet.update(['balance'])
        return booking_id, booking.access_code