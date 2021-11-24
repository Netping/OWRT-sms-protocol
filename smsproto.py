from threading import Thread
from threading import Lock
from journal import journal
import ubus
import enum
import time
import random




module_name = 'SMS Protocol'

class device_type(enum.Enum):
    none = 0
    fake_sms = 1
    gsm_sms = 2

class SMSProto:
    task_list = []
    device = device_type.none
    device_type_map = { 'Fake_SMS' : device_type.fake_sms, 
                        'GSM_SMS' : device_type.gsm_sms }

    mutex = Lock()
    pollThread = None

    def send(phonenumber, text, threadSend=True):
        SMSProto.__parseConfig()

        message = { 'phone' : phonenumber,
                    'text' : text }

        if threadSend:
            SMSProto.mutex.acquire()
            SMSProto.task_list.insert(0, message)
            SMSProto.mutex.release()

            if not SMSProto.pollThread:
                SMSProto.pollThread = Thread(target=SMSProto.__poll, args=())
                SMSProto.pollThread.start()
        else:
            return SMSProto.__sendSMS(phonenumber, text)

        return 0

    def __parseConfig():
        #parse config
        if SMSProto.device == device_type.none:
            try:
                ubus.connect()

                confvalues = ubus.call("uci", "get", {"config": "smsprotoconf"})
                for confdict in list(confvalues[0]['values'].values()):
                    if confdict['.type'] == 'globals':
                        SMSProto.device = SMSProto.device_type_map[confdict['device']]
            except Exception as e:
                journal.WriteLog(module_name, "Normal", "error", "Can't parse config: " + str(e))
            finally:
                ubus.disconnect()

    def __sendSMS(phone, text):
        ret = 0

        try:
            if SMSProto.device == device_type.fake_sms:
                if random.randint(1, 10) < 4: #fail
                    time.sleep(5)
                    journal.WriteLog(module_name, "Normal", "error", "Send SMS to " + phone 
                                        + " failed")
                else: # success
                    time.sleep(2)
                    journal.WriteLog(module_name, "Normal", "notice", "Send SMS to " + phone 
                                        + " with text '" + text + "'")
        except Exception as e:
            journal.WriteLog(module_name, "Normal", "error", "Can't send SMS: " + str(e))
            ret = -1

        return ret

    def __poll():
        random.seed()

        while SMSProto.task_list:
            SMSProto.mutex.acquire()

            message = SMSProto.task_list.pop()
            p = message['phone']
            t = message['text']

            SMSProto.mutex.release()

            SMSProto.__sendSMS(p, t)

        SMSProto.pollThread = None
