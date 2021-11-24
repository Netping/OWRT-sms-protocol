import click
import sys
from smsproto import SMSProto




@click.command()
@click.option('-p', '--phone', required=True, help='Set phone number for send SMS')
@click.option('-t', '--text', required=True, help='SMS text')
def main(phone, text):
    """Send SMS with text to phone number"""
    ret = SMSProto.send(phone, text, False)
    sys.exit(ret)
