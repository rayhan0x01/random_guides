import gi.repository.GLib
import dbus, re, json, requests, codecs, sys, logging
from dbus.mainloop.glib import DBusGMainLoop

logging.basicConfig(level = logging.INFO)
codecs.register_error("strict", codecs.ignore_errors)

dup_msg = ""

def slack_notify(msgTitle, msgData):
    url = "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
    slack_data = {
        "text": msgTitle,
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "From: {}\n\n{}".format(msgTitle,msgData)
                }
            }
        ]
    }
    byte_length = str(sys.getsizeof(slack_data))
    headers = {'Content-Type': "application/json", 'Content-Length': byte_length}
    try:
        response = requests.post(url, data=json.dumps(slack_data), headers=headers, timeout=20)
    except Exception as e:
        logging.exception("Well this happened while sending out the slack notification:")

def notifications(bus, message):
    global dup_msg
    args_list = message.get_args_list()
    if len(args_list) > 4: # the chrome notification for my website X seems to have 7 items in args_list but idk if it's a fixed amount so..
        msgTitle = args_list[3] # the notification title
        if "New message from" in msgTitle: # matching a substring to make sure this is the notification I am looking for
            msgData = args_list[4] # the notification description
            if msgData == dup_msg:
                return # whenever a notification comes, I get 2 message object of it so ignoring the later
            # logging.info("From : {}\nMessage: {}\nSending out the slack notification...".format(msgTitle,msgData))
            slack_notify(msgTitle, msgData)
            dup_msg = msgData


DBusGMainLoop(set_as_default=True)

bus = dbus.SessionBus()
bus.add_match_string_non_blocking("eavesdrop=true, interface='org.freedesktop.Notifications', member='Notify'")
bus.add_message_filter(notifications)

mainloop = gi.repository.GLib.MainLoop()
mainloop.run()