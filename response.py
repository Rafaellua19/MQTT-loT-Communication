import json
import time
from paho.mqtt import client as mqtt_client
from typing import Optional

BROKER_IP = "10.21.60.231"
PORT = 1883

STT_TOPIC = "robot/speech/text"
LLM_REQUEST_TOPIC = "robot/llm/request"
LLM_RESPONSE_TOPIC = "robot/llm/response"
TTS_TOPIC = "robot/audio/play"

CLIENT_ID = "response_processor"

def create_mqtt_client():
    client = mqtt_client.Client(
        mqtt_client.CallbackAPIVersion.VERSION2,
        client_id=CLIENT_ID
    )

    client.on_connect = on_connect
    client.on_message = on_message

    print(f"Connecting to broker at {BROKER_IP}...")

    client.connect(BROKER_IP, PORT, 60)
    client.loop_start()

    return client

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected with result code {reason_code}")

    client.subscribe(STT_TOPIC)
    client.subscribe(LLM_RESPONSE_TOPIC)

    print(f"Subscribed to: {STT_TOPIC}")
    print(f"Subscribed to: {LLM_RESPONSE_TOPIC}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode("utf-8", errors="replace")

    print(f"[RAW]: {payload}")

    try:

        if topic == STT_TOPIC:
            data = json.loads(payload)
            text = data.get("text", "").strip()

            print(f"[STT Received]: {text}")

            if text:
                client.publish(LLM_REQUEST_TOPIC, text)
                print(f"[Forwarded → LLM]: {text}")

        elif topic == LLM_RESPONSE_TOPIC:
            text = payload.strip()

            print(f"[LLM Response]: {text}")

            if text:
                tts_message = {
                    "text": text,
                    "lang": "en",
                    "tld": "com"
                }

                client.publish(TTS_TOPIC, json.dumps(tts_message))
                print(f"[Forwarded → TTS]: {text}")

    except Exception as e:
        print(f"[Error]: {e}")

def run():
    client = create_mqtt_client()

    print("Response processor running...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutting down...")
        client.disconnect()


if __name__ == "__main__":
    run()
