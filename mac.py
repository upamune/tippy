import requests
import json
import os
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from scapy.all import *
from models import Device
import schedule

# SET YOUR CONFIG
slack_endpoint = ""
interval_minutes = 10
ip = "192.168.0.*"
dsn = 'sqlite:///tippy.sqlite'

store = {}

def get_mac_addresses():
    l, _ = arping(ip)
    mac_addresses = [ i[1].hwsrc for i in l.res ]
    return mac_addresses

def get_all_devices():
    engine = create_engine(dsn, echo=True)
    metadata = MetaData()
    metadata.bind = engine

    Session = sessionmaker(bind=engine)
    session = Session()

    devices = session.query(Device).all()
    session.close_all()

    return devices

def filter_exist_devices(addresses, devices):
    exist_devices = []
    for device in devices:
        if device.mac_address.lower() in addresses:
            exist_devices.append(device)
    return exist_devices

def calc_diff(exist_members):
    sorted_members = sorted(exist_members)

    key = "members"
    raw_data = store.get(key)
    if not raw_data or raw_data == "":
        store[key] = json.dumps(sorted_members)
        return {
            "new": sorted_members,
            "stay": sorted_members,
            "old": []
        }
    last_members = json.loads(raw_data)
    if not last_members:
        store[key] = json.dumps(sorted_members)
        return {
            "new": sorted_members,
            "stay": sorted_members,
            "old": []
        }

    if set(sorted_members) == set(last_members):
        return {
            "new": [],
            "stay": sorted_members,
            "old": []
        }

    store[key] = json.dumps(sorted_members)
    return {
        "new": list(set(sorted_members) - set(last_members)),
        "stay": sorted_members,
        "old": list(set(last_members) - set(sorted_members))
    }

def notify_slack(slack_endpoint, exist_devices):
    members = [ device.name for device in exist_devices ]
    calced_member_dict = calc_diff(members)
    if len(calced_member_dict["old"]) == 0 and len(calced_member_dict["new"]) == 0:
        return

    text = ""
    if not len(calced_member_dict["stay"]) == 0:
        text += "部屋にいるのは\n%s\nじゃ\n" % ("\n".join(calced_member_dict["stay"]))

    if not len(calced_member_dict["old"]) == 0:
        text += "\nいなくなったのは\n%s\nじゃ\n" % ("\n".join(calced_member_dict["old"]))

    if not len(calced_member_dict["new"]) == 0:
        text += "\n新しくきたのは\n%s\nじゃ\n" % ("\n".join(calced_member_dict["new"]))

    if text == "" :
        return

    requests.post(slack_endpoint, data = json.dumps({
        "text": text
    }))

    return


def job():
    addresses = get_mac_addresses()
    devices = get_all_devices()
    exist_devices = filter_exist_devices(addresses, devices)
    notify_slack(slack_endpoint, exist_devices)

if __name__ == "__main__":
    job()
    schedule.every(interval_minutes).minutes.do(job)
    while True:
        schedule.run_pending()

