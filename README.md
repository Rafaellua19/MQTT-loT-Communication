ROBOT PROJECT: TEXT-TO-SPEECH (TTS) GUIDE
Developer: Alan (Text to Speech)
Target Hardware: Raspberry Pi 2 ("Sin Raya") - 10.21.16.120
MQTT Broker: Raspberry Pi 1 ("Rayita") - 10.21.60.231

1. PROJECT OVERVIEW
This module is the "mouth" of the robot. It subscribes to the topic robot/audio/play and waits for JSON messages containing text. Once a message is received, it uses Google TTS to generate audio and plays it through the Raspberry Pi's hardware.

2. REQUIRED FILES
Place these files in your project folder:

gtts_say.py: The main Python script that handles MQTT and speech.

requirements.txt: List of Python dependencies.


.gitignore: To keep the folder clean from temporary files.

3. SYSTEM INSTALLATION
Before running the script, the Raspberry Pi needs specific system tools installed:

Bash
# Update the system and install FFmpeg and ALSA tools
sudo apt update
sudo apt install ffmpeg alsa-utils -y
4. PYTHON SETUP
I am using a virtual environment to keep the project organized. Follow these steps to set it up:

Bash
# Create the virtual environment
python3 -m venv venv

# Activate the environment
source venv/bin/activate

# Install the necessary libraries
pip install gTTS paho-mqtt
5. RUNNING THE MODULE
Make sure the MQTT Broker (Mosquitto) is running on Pi 1. Then, run the script:

Bash
python gtts_say.py
6. MQTT TOPIC & DATA FORMAT
The other teams (LLM/Reasoning) must send messages to my topic using the following format:

Topic: robot/audio/play

Format: JSON

Example Payload:

JSON
{
  "text": "Hello, I am the robot. How can I help you today?",
  "lang": "en",
  "tld": "com"
}
7. MANUAL TESTING
To test if the TTS is working without the rest of the robot, run this command from any terminal connected to the network:

Bash
mosquitto_pub -h 10.21.60.231 -t "robot/audio/play" -m '{"text": "Testing the audio system", "lang": "en", "tld": "com"}'
Summary of requirements.txt content:
Ensure this file exists in your folder with these two lines:

Plaintext
gTTS
paho-mqtt