import paho.mqtt.client as mqtt
import can
import json


def on_message(client, userdata, msg):
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    print("user requests id: ", int(msg.payload.decode("utf-8")), hex(int(msg.payload.decode("utf-8"))))
    for frame in bus:

        if frame.arbitration_id == int(msg.payload.decode("utf-8")):
            # stringa = "{}: {:02X} {:02X}".format(frame.arbitration_id, frame.data[0], frame.data[1])
            tH2O = frame.data[0]*256+frame.data[1]
            tOil = frame.data[2]*256+frame.data[3]
            json_dict = {"tH2O": tH2O, "tOil": tOil}
            json_string = json.dumps(json_dict)
            print(json_string)
            client.publish("speaker", json_string)
            break


def on_connect(client, userdata, flags, rc):

    print("Connected with result code " + str(rc))

    print("Client Connesso")


client = mqtt.Client("IlMagnificoLettore")

client.on_connect = on_connect

client.on_message = on_message

# client.username_pw_set("Rettorato", "Nucleare")

# client.connect("broker.shiftr.io", 1883, 160)

client.connect("localhost", 1883, 160)
client.subscribe('listener')


client.loop_forever()
