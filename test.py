#!/usr/bin/python3
from smsproto import SMSProto




def main():
    for i in range(0, 10):
        print("Sent " + str(i + 1) + " message")
        SMSProto.send('+79101234567', "Test SMS message " + str(i + 1))

if __name__ == "__main__":
    main()
