# The Booking Data Access Object handles all interactions with the Booking table.
from dao.basedao import BaseDAO
from entities.booking import Booking
from service.txngateservice import TxnGateService


class BookingDAO(BaseDAO):
    __TABLE_NAME = 't_booking'

    def __init__(self):
        pass

    @classmethod
    def get_booking_by_code(cls, code):
        sql = "SELECT * FROM {0} where access_code={1}".format(cls.__TABLE_NAME, code)
        booking = cls._get_item(sql)
        if booking:
            return Booking(booking)
        else:
            raise Exception('No booking found for id : {0}'.format(code))

    @classmethod
    def get_booking_by_id(cls, booking_id):
        sql = "SELECT * FROM {0} where id={1}".format(cls.__TABLE_NAME, booking_id)
        booking = cls._get_item(sql)
        if booking:
            if booking['valid'] == '\x00':
                booking['valid'] = False
            elif booking['valid'] == '\x01':
                booking['valid'] = True
            return Booking(booking)
        else:
            raise Exception('No booking found for id : {0}'.format(booking_id))

    @classmethod
    def get_booking_by_vehicle_id(cls, vehicle_id):
        sql = "SELECT * FROM {0} where vehicle_id={1} ORDER BY created_on DESC".format(cls.__TABLE_NAME, vehicle_id)
        bookings = cls._get_items(sql)
        if not bookings:
            return []
        for booking in bookings:
            if booking['valid'] == '\x00':
                booking['valid'] = False
            elif booking['valid'] == '\x01':
                booking['valid'] = True
            booking['trip_name'] = TxnGateService.get_toll_name(booking['id'])
        if bookings:
            return [Booking(booking) for booking in bookings]
        else:
            raise Exception('No booking found for vehicle_id : {0}'.format(vehicle_id))

    @classmethod
    def get_booking_by_vehicle_id_till_midnight(cls, vehicle_id):
        sql = "SELECT * FROM {0} where vehicle_id={1} and day(created_on) = day(now()) ORDER BY created_on DESC LIMIT 1"\
            .format(cls.__TABLE_NAME, vehicle_id)
        bookings = cls._get_items(sql)
        if not bookings:
            return None
        for booking in bookings:
            if booking['valid'] == '\x00':
                booking['valid'] = False
            elif booking['valid'] == '\x01':
                booking['valid'] = True

        return [Booking(booking) for booking in bookings]

    @classmethod
    def get_booking_by_vehicle_id_till_day(cls, vehicle_id):
        sql = "SELECT * FROM {0} where vehicle_id={1} and created_on >= CURDATE() - INTERVAL 1 DAY" \
              " ORDER BY created_on DESC LIMIT 1" \
            .format(cls.__TABLE_NAME, vehicle_id)
        bookings = cls._get_items(sql)
        if not bookings:
            return None
        for booking in bookings:
            if booking['valid'] == '\x00':
                booking['valid'] = False
            elif booking['valid'] == '\x01':
                booking['valid'] = True
        return [Booking(booking) for booking in bookings]


    @classmethod
    def get_booking_by_vehicle_ids(cls, vehicle_ids):
        #sql = "SELECT * FROM {0} where vehicle_id in ({1}) and valid = true and ABS(UNIX_TIMESTAMP(now()) -" \
        #      " UNIX_TIMESTAMP(updated_on)) > 300 ORDER BY created_on DESC LIMIT 1".\
        #    format(cls.__TABLE_NAME, ','.join(str(id) for id in vehicle_ids))
        sql = "SELECT * FROM {0} where vehicle_id in ({1}) and valid = true ORDER BY created_on DESC LIMIT 1". \
            format(cls.__TABLE_NAME, ','.join(str(id) for id in vehicle_ids))
        bookings = cls._get_items(sql)
        if bookings:
            for booking in bookings:
                if booking['valid'] == '\x00':
                    booking['valid'] = False
                elif booking['valid'] == '\x01':
                    booking['valid'] = True
            return [Booking(booking) for booking in bookings]
        else:
            raise Exception('No booking found for vehicle_id : {0}'.format(','.join([str(a) for a in vehicle_ids])))