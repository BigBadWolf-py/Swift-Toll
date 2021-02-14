from pyfcm import FCMNotification

from dao.bookingdao import BookingDAO
from dao.fcmdao import FCMDAO
from dao.gatedao import GateDAO
from entities.fcm import FCM


class FCMService:

    @classmethod
    def register_device(cls, user_id, fcm_id):
        item = {'user_id': user_id, 'device_token': fcm_id}
        try:
            fcm = FCMDAO.get_fcmid_from_user_id(user_id)
            fcm.device_token = fcm_id
            fcm.update(['device_token'])
        except:
            fcm = FCM(item)
            fcm.insert()

    @classmethod
    def send_notification(cls, reg_id, booking_id, gate_id):
        push_service = FCMNotification(api_key="AAAAcBpJG8E:APA91bHrp_Ldu1AuNvknp22vav0pVS7V2Qmy7wxhe1oqpoHtuhswminRdrM1V"
                                               "HNEl2nJEY75KBYZ8f-qzlDikTn53PC4D0TMNpd5DtjZlCaIE1x0OYdOQL14__uTELORPAldfeGQng_8")
        registration_id = reg_id
        gate = GateDAO.get_gate_by_id(gate_id)
        message_title = "Swiftoll"
        message_body = "Thanks for visiting {0}".format(gate.name)
        print message_body
        result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title,
                                                   message_body=message_body)