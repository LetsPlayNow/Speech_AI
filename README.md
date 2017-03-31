# Speech_AI
[![image](https://habrastorage.org/files/b93/1f4/ed6/b931f4ed6905407f8d8869611c104cec.png)](https://youtu.be/ZziT4nQCjMk)

## Simple speech linguistic AI with Python

It supports almost any natural language. By default it works in russian language.
if you want to change it, please check documentation of libraries below.
It can be done easily in 3 fixes:
* Change comments
* Change language of recognizer and synthesizer and train bot with your language sources (corpus, Twitter, etc.).

Main script is speech_ai.
It recognizes your speech, looking for answer by chatterbot library and replies you with speech synthesized by GTTS library.
Because of Libraries specials, it needs internet connection.

This script uses:
* Python 3
* [Google Text to Speech](https://github.com/pndurette/gTTS)
* [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/)
* [Chatterbot](https://github.com/gunthercox/ChatterBot)
* [PyGame](https://www.pygame.org/lofi.html)


You can use this idea in you video game or maybe with Smart House.  
Enjoy!

## Installation

### Debian-based linux
At first you need to install libraries, listed above.
For this I recommend use of python environments (like conda environments)


```Bash
conda create --name speech_ai
source activate speech_ai
conda install python=3.5

# Install pyaudio
# You can try pip3 command with sudo if errors appears
sudo apt-get install python-pyaudio python3-pyaudio 
pip3 install pyaudio

pip3 install gTTS
pip3 install SpeechRecognition
pip3 install chatterbot
pip3 install pygame
```

### Windows XP and older
In Windows OS we have several methods to install packages:
* We can install [compiler](https://wiki.python.org/moin/WindowsCompilers) suggested for our Python version
* Or we can easily use `Wheel`.  
On windows it's bit difficult to install `pyaudio` and `pygame`. So, easy way to use `Wheel`. 
This package versions for Python 3.4.x, but you can download versions what you need

1. Install Python 3.4.x standalone or in Anaconda
2. Download wheels depending on your architecture (x86 or amd64) and Python version: 
 - [pygame](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pygame)
 - [pyaudio](http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)

3. Install packages (install wheel if you haven't did it yet).
```bash
pip install --upgrade pip
pip install wheel

pip install pygame-1.9.3-cp34-cp34m-win32.whl
pip install PyAudio-0.2.11-cp34-cp34m-win32.whl

pip3 install gTTS
pip3 install SpeechRecognition
pip3 install chatterbot
```
## Run
```
python3 speech_ai.py
```
