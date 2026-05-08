Project structure:

stt/
├── script.py
├── vendor/
└── models/
    └── vosk-model-small-en-us-0.15/
        ├── am/
        ├── conf/
        ├── graph/
        └── ivector/
_____________________________________________________________________________
Install system packages:

mkdir -p vendor
python3 -m pip install --target ./vendor sounddevice vosk openwakeword numpy
sudo ldconfig
______________________________________________________________________________
Install Python packages locally:

sudo apt update
sudo apt install python3-pip libportaudio2 portaudio19-dev unzip wget
sudo ldconfig
______________________________________________________________________________
Download the Vosk model:

mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
cd ..
_______________________________________________________________________________
List input devices, then use whichever you get or want:

PYTHONPATH=./vendor python3 - <<'PY'
import sounddevice as sd
for i, dev in enumerate(sd.query_devices()):
if dev["max_input_channels"] > 0:
print(i, dev["name"], "inputs=", dev["max_input_channels"])
PY
______________________________________________________________________________
Run the script:
(Example using microphone device 1)

python3 script.py \
--vosk-model ./models/vosk-model-small-en-us-0.15 \
--device 1 \
--sample-rate 48000 \
--wakeword-name alexa \