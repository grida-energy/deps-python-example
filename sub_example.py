import paho.mqtt.client as mqtt

def connect_mqtt(url: str, client_id: str, **kwargs) -> mqtt.Client:
    host, port_str = url.split(':')
    port = int(port_str)
    client:mqtt.Client = mqtt.Client(client_id=client_id)
    print(f"Connecting to {host}:{port} with client ID '{client_id}'")
    if 'ca_cert' in kwargs:
        print("Setting up TLS")
        client.tls_set(ca_certs=kwargs['ca_cert'], certfile=kwargs['cert'], keyfile=kwargs['key'],cert_reqs=mqtt.ssl.CERT_REQUIRED)
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected successfully!")
        else:
            print(f"Connection failed with code {rc}")
    client.on_connect = on_connect
    client.on_disconnect = lambda client, userdata, rc: print(f"Disconnected {client}, rc={rc}, userdata={userdata}")
    client.connect(host, port)
    return client


def on_bess_message(topic_prefix: str, client, userdata, msg: mqtt.MQTTMessage):
    import deps.preset.bess.model.v1_pb2 as bess_model
    import deps.vnd.parameter.v1_pb2 as vnd_param_model
    import deps.vnd.alarm.v1_pb2 as vnd_alarm_model

    sub_topic: str = ""
    if msg.topic.startswith(topic_prefix):
        sub_topic = msg.topic[len(topic_prefix):]
    try:
        match sub_topic:
            case "/measure":
                model = bess_model.BessMeasure()
                model.ParseFromString(msg.payload)
                print(f"Received message: {model} on topic {msg.topic}")
            case "/vnd/param-meta":
                model = vnd_param_model.ParamMeta()
                model.ParseFromString(msg.payload)
                print(f"Received message: {model} on topic {msg.topic}")
            case "/vnd/alarm-meta":
                model = vnd_alarm_model.AlarmMeta()
                model.ParseFromString(msg.payload)
                print(f"Received message: {model} on topic {msg.topic}")
            case "/vnd/alarm":
                model = vnd_alarm_model.AlarmData()
                model.ParseFromString(msg.payload)
                print(f"Received message: {model} on topic {msg.topic}")
            case _:
                print(f"Unknown topic suffix: {sub_topic}")
    except Exception as e:
        print(f"Failed to parse message: {e}")
        return
    
def on_station_cast_message(topic_prefix: str,client, userdata, msg: mqtt.MQTTMessage):
    import deps.preset.station_cast.model.v1_pb2 as station_cast_model

    sub_topic: str = ""
    if msg.topic.startswith(topic_prefix):
        sub_topic = msg.topic[len(topic_prefix):]
    try:
        match sub_topic:
            case "/measure":
                model = station_cast_model.Rpc.CastMeasure()
                model.ParseFromString(msg.payload)
                print(f"Received message: {model} on topic {msg.topic}")
            case _:
                print(f"Unknown topic suffix: {sub_topic}")
    except Exception as e:
        print(f"Failed to parse message: {e}")
        return
        
def sub(client: mqtt.Client, topic_prefix: str):
    from functools import partial
    client.subscribe(topic_prefix + "/#")
    client.on_message = partial(on_bess_message, topic_prefix)
    # client.on_message = partial(on_station_cast_message, topic_prefix)

if __name__ == "__main__":
    import os
    import argparse
    from dotenv import load_dotenv

    load_dotenv()

    parser = argparse.ArgumentParser(description="deps-python-example")
    url_default = os.getenv("MQTT_URL")
    parser.add_argument("--url", required=url_default is None, default=url_default, help="mqtt url to connect including port.")
    client_id_default = os.getenv("MQTT_CLIENT_ID", "")
    parser.add_argument("--client_id", default=client_id_default, help="mqtt client id. if use client certificate, this value usually needs to match the certificate's common name.")
    topic_default = os.getenv("MQTT_TOPIC")
    parser.add_argument("--topic", required=topic_default is None, default=topic_default, help="mqtt topic prefix to subscribe.")
    ca_cert_default = os.getenv("MQTT_CA_CERT")
    parser.add_argument("--ca_cert", default=ca_cert_default, help="ca certificate file path. if not provided, connection will be made without tls.")
    cert_default = os.getenv("MQTT_CERT")
    parser.add_argument("--cert", default=cert_default, help="client certificate file path. used with --ca_cert.")
    key_default = os.getenv("MQTT_KEY")
    parser.add_argument("--key", default=key_default, help="client private key file path. used with --ca_cert.")

    args = parser.parse_args()

    print("args:", args.__repr__())

    client = connect_mqtt(args.url, args.client_id, ca_cert=args.ca_cert, cert=args.cert, key=args.key)
    sub(client, args.topic)
    client.loop_forever()
