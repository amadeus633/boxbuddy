# boxbuddy

## Getting Started

- You can start the app 2 different ways 
  1) running `python3 app.py` without python virtual environment
  2) using a virtual environment 
      `python3 -m venv venv`
      `source venv/bin/activate`
      `pip install -r requirements.txt `
    - now you should be able to start while keeping your virtual environment activated
    - if you don't want to enter the virtual environment every time you start BoxBuddy, there is a bash script `run_app.sh` to use the script:
      `chmod +x run_app.sh`
      `./run_app.sh`


## Before using: 

To simplify use of the "VPN" feature, place your lab_[htb_username].ovpn file in the same folder as app.py

# FYI
***These instructions assume you are using zsh on Kali Linux. You might need to adjust the steps if needed 


# Using the chatGPT feature

## Add API key
- edit gpt.py file and replace `your_api_key` 
  `openai.api_key = "your_api_key"`
- if you get an error "command not found":
  - run `export PATH=$PATH:/home/USER/.local/bin` replacing USER with your username
  - check your path with `echo $PATH`
  
