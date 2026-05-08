import json
import os
import tempfile
from paho.mqtt import client as mqtt_client
from gtts import gTTS

# --- Configuration for the Robot Team ---
# We use the IP address of Raspberry Pi 1 (Rayita) as the brain
BROKER_IP = "10.21.60.231" 
PORT = 1883
# My topic is where the LLM team will send the text they want me to say. They should use this exact topic when they publish their messages.
TOPIC = "robot/audio/play" 
# Audio quality setting for the Raspberry Pi
SAMPLE_RATE = 24000 

def say(text, lang="en", tld="com"):
    # This function takes the text and turns it into sound
    text = text.strip()
    if not text:
        return

    # Create temporary files so we don't fill up the Raspberry Pi memory
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
        mp3_path = f.name

    wav_path = mp3_path[:-4] + ".wav"

    try:
        # Use Google to create the voice file (needs internet!)
        tts = gTTS(text=text, lang=lang, tld=tld)
        tts.save(mp3_path)

        # We use FFmpeg to change the format so the Pi can play it clearly
        # It changes it to 24kHz Mono
        convert_command = f'ffmpeg -loglevel error -y -i "{mp3_path}" -ar {SAMPLE_RATE} -ac 1 "{wav_path}"'
        result = os.system(convert_command)
        
        if result != 0:
            print("Error: Make sure ffmpeg is installed!")
            return

    # Play the sound through the speakers (hardware device 2,0)
        os.system(f'aplay "{wav_path}"')

    finally:
        # Clean up the temp files after playing
        for file_path in (mp3_path, wav_path):
            if os.path.exists(file_path):
                os.remove(file_path)

# --- MQTT Setup ---

def on_message(client, userdata, msg):
    # This runs every time the LLM team sends us a message
    try:
        # The team sends data in JSON format, so we decode it here
        payload = json.loads(msg.payload.decode("utf-8", errors="replace"))
        
        # Get the text from the JSON. The team should use the key "text"
        message_text = payload.get("text", "")
        # If they want a different language or accent, they can send these too
        language = payload.get("lang", "en")
        accent = payload.get("tld", "com")
        
        if message_text:
            print(f"[Robot Speaking]: {message_text}")
            say(message_text, lang=language, tld=accent)
            
    except Exception as e:
        print(f"I couldn't read the message: {e}")

# Create the MQTT client
client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
client.on_message = on_message

# Connect to the Broker (Rayita)
print(f"Connecting to the broker at {BROKER_IP}...")
client.connect(BROKER_IP, PORT, 60)

# Subscribe to my specific topic
client.subscribe(TOPIC)
print(" ▄█▀▀▀▄█                           ▀██                            █▀▀██▀▀█ █▀▀██▀▀█  ▄█▀▀▀▄█  ")
print(" ██▄▄  ▀  ▄▄▄ ▄▄▄    ▄▄▄▄   ▄▄▄▄    ██  ▄▄    ▄▄▄▄  ▄▄▄ ▄▄           ██       ██     ██▄▄  ▀  ")
print("  ▀▀███▄   ██▀  ██ ▄█▄▄▄██ ▀▀ ▄██   ██ ▄▀   ▄█▄▄▄██  ██▀ ▀▀          ██       ██      ▀▀███▄  ")
print("▄     ▀██  ██    █ ██      ▄█▀ ██   ██▀█▄   ██       ██      ████    ██       ██    ▄     ▀██ ")
print("█▀▄▄▄▄█▀   ██▄▄▄▀   ▀█▄▄▄▀ ▀█▄▄▀█▀ ▄██▄ ██▄  ▀█▄▄▄▀ ▄██▄            ▄██▄     ▄██▄   █▀▄▄▄▄█▀  ")
print("{*}Created By: Onassis Monzalvo,Steban Ramirez,Adrian Larenas,Illich Estrada")
print(f"{{+}} Waiting for responses on topic: {TOPIC}")

# Keep the program running forever
client.loop_forever()

#How To Start The Connection

#Python
#cd /home/raspberrypi/tts-proj
#Create the environment
#python3 -m venv venv
# Activate it
#source venv/bin/activate

#Mosquitto
#Start it and make sure it runs on every boot
#sudo systemctl enable mosquitto
#sudo systemctl start mosquitto

#Check if it is running (it should say "active (running)")
#sudo systemctl status mosquitto

#mosquitto_pub -h localhost -t "home/voice" -m '{"message": "The message you are going to run", "lang": "en", "tld": "com"}'