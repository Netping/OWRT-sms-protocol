from threading import Thread
from threading import Lock
from journal import journal
import ubus
import enum
import time




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

    def send(phonenumber, text):
        SMSProto.__parseConfig()

        message = { 'phone' : phonenumber,
                    'text' : text }

        SMSProto.mutex.acquire()
        SMSProto.task_list.insert(0, message)
        SMSProto.mutex.release()

        if not SMSProto.pollThread:
            SMSProto.pollThread = Thread(target=SMSProto.__poll, args=())
            SMSProto.pollThread.start()

    def __parseConfig():
        #parse config
        if SMSProto.device == device_type.none:
            try:
                ubus.connect()

                confvalues = ubus.call("uci", "get", {"config": "smsprotoconf"})
                for confdict in list(confvalues[0]['values'].values()):
                    if confdict['.type'] == 'info':
                        SMSProto.device = SMSProto.device_type_map[confdict['device']]
            except Exception as e:
                journal.WriteLog(module_name, "Normal", "error", "Can't parse config: " + str(e))
            finally:
                ubus.disconnect()

    def __poll():
        while SMSProto.task_list:
            SMSProto.mutex.acquire()

            message = SMSProto.task_list.pop()
            p = message['phone']
            t = message['text']

            SMSProto.mutex.release()

            if SMSProto.device == device_type.fake_sms:
                time.sleep(2)
                journal.WriteLog(module_name, "Normal", "notice", "Send SMS to " + p 
                                    + " with text '" + t + "'")

        SMSProto.pollThread = None
