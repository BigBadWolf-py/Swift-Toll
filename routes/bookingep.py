# -*- coding: utf-8 -*-
from threading import Thread

import bottle
from bottle import route, request
from common import endpoints, validator
from common.routeutils import result, error_handler
from dao.bookingdao import BookingDAO
from dao.fcmdao import FCMDAO
from dao.gatedao import GateDAO
from dao.userdao import UserDAO
from dao.vehicledao import VehicleDAO
from dao.walletdao import WalletDAO
from entities.booking import Booking
from service.FCMService import FCMService
from service.bookingservice import BookingService
from service.smsservice import SMSService
from service.txngateservice import TxnGateService


@route(endpoints.GET_BOOKINGS)
@error_handler
def get_bookings_by_user_id(user_id):
    if not user_id:
        raise Exception('Parameters user_id not present')

    vehicles = VehicleDAO.get_vehicle_by_user_id(user_id)
    books = []
    for vehicle in vehicles:
        bks = BookingDAO.get_booking_by_vehicle_id(vehicle.id)
        for b in bks:
            b.vehicle_no = vehicle.vehicle_number
            books.append(b)
    return result(data=books)


@route(endpoints.GET_BOOKING)
@error_handler
def get_booking_by_id(booking_id):
    if not booking_id:
        raise Exception('Parameters booking_id not present')
    booking = BookingDAO.get_booking_by_id(booking_id)
    booking.vehicle_no = VehicleDAO.get_vehicle_by_id(booking.vehicle_id).vehicle_number
    try:
        booking.txn_gates, booking.trip_name = TxnGateService.get_txn_gates_with_crossings(booking_id)
    except Exception as e:
        print e
    return result(data=booking)

"""
@route(endpoints.VALIDATE_BOOKING)
@error_handler
def validate_booking(booking_id, gate_id):
    if not booking_id or not gate_id:
        raise Exception('Parameters booking id or gate_id not present')
    try:
        BookingService.validate_booking(booking_id, gate_id)
        return bottle.HTTPResponse(status=200, body=result(data={'valid': True}))
    except Exception as e:
        print e[0]
        return bottle.HTTPResponse(status=500, body=result(data={'valid': False}))
"""


def get_booking_validated_message(user_id, gate_id):
    user = UserDAO.get_user_by_id(user_id)
    gate = GateDAO.get_gate_by_id(gate_id)
    wallet = WalletDAO.get_wallet_by_id(user.wallet_id)
    msg = 'Dear {0}, Thanks for visiting {1}. Available credits Rs. {2}'.format(user.name, gate.name, wallet.balance)
    return msg, user


@route(endpoints.VALIDATE_BEACONS)
@error_handler
def validate_beacons(data, gate_id):
    if not data or not gate_id:
        raise Exception('Parameters booking id or gate_id not present')
    try:
        user_id = data
        if not user_id:
            raise Exception("No suitable beacons found!!")
        booking_id, valid_gate_id = BookingService.validate_booking_by_user_id(user_id, gate_id)
        try:
            fcm = FCMDAO.get_fcmid_from_user_id(user_id)
            FCMService.send_notification(fcm.device_token, booking_id, gate_id)
        except Exception as e:
            print e
            print 'FCM Failed'
        msg, user = get_booking_validated_message(user_id, gate_id)
        Thread(target=SMSService.sendSMS, args=(msg, user.phone)).start()

        return bottle.HTTPResponse(status=200, body=result(data={'valid': True, 'username': UserDAO.get_username_from_id(user_id)}))
    except Exception as e:
        if 'No booking found for vehicle_id' in e.args[0] or 'No gate for booking and gate id' in e.args[0]:
            try:
                user = UserDAO.get_user_by_id(data)
                if WalletDAO.get_wallet_by_id(user.wallet_id).autouse:
                    vehicles = VehicleDAO.get_vehicle_by_user_id(data)
                    if vehicles:
                        book = {
                            "vehicle_id": vehicles[0].id,
                            "type": "SINGLE",
                            "trip_type": "ONE_WAY",
                            "gate_id": gate_id,
                            "payment_status": "PAID"
                        }
                        BookingService.make_booking_for_swiftpay(Booking(book), gate_id, vehicles)
                        booking_id, valid_gate_id = BookingService.validate_booking_by_user_id(data, gate_id)
                        try:
                            fcm = FCMDAO.get_fcmid_from_user_id(data)
                            FCMService.send_notification(fcm.device_token, booking_id, gate_id)
                        except:
                            print 'FCM Failed'
                        msg, user = get_booking_validated_message(data, gate_id)
                        Thread(target=SMSService.sendSMS, args=(msg, user.phone)).start()

                        return bottle.HTTPResponse(status=200, body=result(
                            data={'valid': True, 'username': user.name}))
            except Exception as e:
                print e
                return bottle.HTTPResponse(status=500, body=result(data={'valid': False}))
        return bottle.HTTPResponse(status=500, body=result(data={'valid': False}))


@route(endpoints.MAKE_BOOKING, method=['POST'])
@error_handler
def make_booking_single():
    """
    sample_data :
    {
        "vehicle_id": "1",
        "type": "SINGLE",
        "trip_type": "ONE_WAY",
        "gate_id": "1",
        "payment_status": "PAID"
    }
    :return:  {'booking_id': booking_id}
    """
    item = validator.validate_json(request.json, ['vehicle_id', 'type', 'trip_type', 'gate_id', 'payment_status'])
    booking_id, access_code = BookingService.make_booking(Booking(item), item['gate_id'])
    return result(data={'booking_id': access_code})


@route(endpoints.MAKE_BOOKING_MULTI, method=['POST'])
@error_handler
def make_booking_multi():
    """
    sample_data :
    {
        "vehicle_id": "1",
        "type": "SINGLE",
        "trip_type": "ONE_WAY",
        "gate_ids": ["1","2","3"],
        "payment_status": "PAID"
    }
    :return:  {'booking_id': booking_id}
    """
    item = validator.validate_json(request.json, ['vehicle_id', 'type', 'trip_type', 'gate_ids', 'payment_status'])
    booking_id, access_code = BookingService.make_booking_multi(Booking(item), item['gate_ids'])
    return result(data={'booking_id': access_code})


def get_nearest_bookingid(data):
    """
    format == OK+DISISOK+DISC:00000000:00000000000000000000000000000000:0000000000:5A29F9AC09AD:-063
    OK+DISC:00000000:00000000000000000000000000000000:0000000000:E0ACCB7E4239:-060OK+DISCE
    """
    data = data.replace('OK+DISIS', '')
    data = data.replace('OK+DISCE', '')
    beacons = [d.strip() for d in data.split('OK+DISC:') if d.strip()]
    booking_ids = {}
    if not beacons:
        return None
    for beacon in beacons:
        if beacon.split(':')[0] == '00000000':
            continue
        booking_ids.update({beacon.split(':')[2][5:]:beacon.split(':')[4]})
    if not booking_ids:
        return None
    nearest_beacon_id = booking_ids.keys()[0]
    nearest_beacon_rssi = booking_ids.values()[0]
    for key, value in booking_ids.iteritems():
        if value < nearest_beacon_rssi:
            nearest_beacon_id = key
            nearest_beacon_rssi = abs(int(value))
    return nearest_beacon_id


def get_nearest_userid(data):
    """
    format == OK+DISISOK+DISC:00000000:00000000000000000000000000000000:0000000000:5A29F9AC09AD:-063
    OK+DISC:00000000:00000000000000000000000000000000:0000000000:E0ACCB7E4239:-060OK+DISCE
    """
    data = data.replace('OK+DISIS', '')
    data = data.replace('OK+DISCE', '')
    beacons = [d.strip() for d in data.split('OK+DISC:') if d.strip()]
    booking_ids = {}
    if not beacons:
        return None
    for beacon in beacons:
        if beacon.split(':')[0] == '00000000':
            continue
        booking_ids.update({beacon.split(':')[1]: beacon.split(':')[4]})
    if not booking_ids:
        return None
    nearest_beacon_id = booking_ids.keys()[0]
    nearest_beacon_rssi = booking_ids.values()[0]
    for key, value in booking_ids.iteritems():
        if value < nearest_beacon_rssi:
            nearest_beacon_id = key
            nearest_beacon_rssi = abs(int(value))
    return nearest_beacon_id

d = """
OK+DISISOK+DISC:00000000:00000000000000000000000000000000:0000000000:5A29F9AC09AD:-063
    OK+DISC:12345678:00000000000000000000000000000000:0000012345:E0ACCB7E4239:-060OK+DISCE
"""
#print validate_beacons('B0702880A295A8ABF734031A98A512DE', '4')