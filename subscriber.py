import os
import time
import paho.mqtt.client as mqtt
import json

BROKER_HOST = "10.21.60.231"
BROKER_PORT = 1883
REQUEST_TOPIC = ("robot/llm/request")
RESPONSE_TOPIC = ("robot/llm/response")

CLIENT_ID = os.getenv("CLIENT_ID", "llm_module")

def process_with_llm(text):
    """
    Replace this with real LLM logic (API or local model)
    """
    text = text.lower()

    if "hello" in text:
        return "Hello! How can I help you?"
    elif "your name" in text:
        return "I am your robot assistant."
    elif "time" in text:
        return f"The current time is {time.strftime('%H:%M:%S')}"
    else:
        return f"I understood: {text}"

def on_connect(client, userdata, flags, reason_code, properties=None):
    print(f"Connected to MQTT broker with reason code {reason_code}")
    client.subscribe(REQUEST_TOPIC)
    print(f"Subscribed to topic: {REQUEST_TOPIC}")





def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8", errors="replace")
        data = json.loads(payload)

        user_text = data.get("text", "").strip()

        print(f"[Received]: {user_text}")

        if not user_text:
            return

        response_text = process_with_llm(user_text)

        client.publish(RESPONSE_TOPIC, response_text)

        print(f"[LLM Response]: {response_text}")

    except Exception as e:
        print(f"[Error]: {e}")


client = mqtt.Client(
    client_id=CLIENT_ID,
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

while True:
    try:
        client.connect(BROKER_HOST, BROKER_PORT)
        break
    except Exception as e:
        print(f"Connection error: {e}")
        time.sleep(5)

print("LLM module running...")
client.loop_forever()