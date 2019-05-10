import paho.mqtt.client as mqtt
import can 


def on_message(client, userdata, msg):
    bus = can.interface.Bus(channel='can0', bustype='socketcan_native')
    print("user requests id: ", int(msg.payload.decode("utf-8")), hex(int(msg.payload.decode("utf-8"))))
    for frame in bus:

        if frame.arbitration_id == int(msg.payload.decode("utf-8")):

            stringa = "{}: {:02X} {:02X}".format(frame.arbitration_id, frame.data[0], frame.data[1])
            print(stringa)
            client.publish("speaker", stringa)
            break


def on_connect(client, userdata, flags, rc):

    print("Connected with result code " + str(rc))

    print("Client Connesso")


client = mqtt.Client("IlMagnificoLettore")

client.on_connect = on_connect

client.on_message = on_message

client.username_pw_set("Rettorato", "Nucleare")

client.connect("broker.shiftr.io", 1883, 60)

client.subscribe('listener')


client.loop_forever()
