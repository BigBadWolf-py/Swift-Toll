######################  SWIFTOLL ENDPOINT ########################

BASE_URL = '/api/v1.0'

###############################################################################################                 BOOKINGS
VALIDATE_BOOKING = BASE_URL + '/validate/booking/:booking_id/gate/:gate_id'
VALIDATE_BEACONS = BASE_URL + '/validate/data/:data/gate/:gate_id'
MAKE_BOOKING = BASE_URL + '/booking'
MAKE_BOOKING_MULTI = BASE_URL + '/booking/multi'
GET_BOOKINGS = BASE_URL + '/bookings/user/:user_id'
GET_BOOKING = BASE_URL + '/bookings/:booking_id'

###############################################################################################                    GATES
GET_GATE = BASE_URL + '/gates/:gate_id'
GET_GATES = BASE_URL + '/gates'
SEARCH_GATE = BASE_URL + '/gates/search'
GET_PRICE = BASE_URL + '/gates/:gate_id/price'

###############################################################################################                TOLL RATE
TOLL_RATE = BASE_URL + '/tollrates'

###############################################################################################                  VEHICLE
REGISTER_VEHICLE = BASE_URL + '/vehicles'
GET_VEHICLES = BASE_URL + '/vehicles/user/:user_id'
DELETE_VEHICLES = BASE_URL + '/vehicles/delete/:vehicle_id'

###############################################################################################             VEHICLE TYPE
VEHICLE_TYPE = BASE_URL + '/vehicles-types'
GET_VEHICLE_TYPES = BASE_URL + '/vehicle/types'

###############################################################################################                    USERS
REGISTER = BASE_URL + '/users'
FORGOT_PASSWORD = BASE_URL + '/forgot-pass/:phone'
LOGIN = BASE_URL + '/login'
CHANGE_PASSWORD = BASE_URL + '/change/password'

###############################################################################################                   WALLET
GET_BALANCE = BASE_URL + '/wallet/balance/user/:user_id'
MAKE_AUTOUSE = BASE_URL + '/wallet/autouse/user/:user_id'

###############################################################################################                      OTP
VALIDATE_OTP = BASE_URL + '/users/:user_id/otp/:otp'


###############################################################################################                      FCM
REGISTER_DEVICE_FCM = BASE_URL + '/register/user/:user_id/fcm/:fcm_id'
