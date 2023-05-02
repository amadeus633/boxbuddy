# boxbuddy

# Getting Started

## Before using: 

To simplify use of the "VPN" feature, place your lab_<htb_username>.ovpn file in the same folder as app.py

# FYI
***These instructions assume you are using zsh on Kali Linux. You might need to adjust the steps if needed 

# chatGPT
- to try out the version with chatGPT included, run `python3 gpt.py`
- to use chatGPT you need an OpenAI account and an OpenAI API key, instructions below

## Install OpenAI
- run `pip install openai`
- run `openai --help` to see if it was set up correctly
- if you get an error "command not found":
  - run `export PATH=$PATH:/home/USER/.local/bin` replacing USER with your username
  - check your path with `echo $PATH`

## Add API key
- edit gpt.py file and replace `your_api_key` 
  `openai.api_key = "your_api_key"`
  
