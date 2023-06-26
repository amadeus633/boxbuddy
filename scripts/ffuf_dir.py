#!/usr/bin/python

import sys
import subprocess
import sh

def main(targetdomain):
    command_template = "ffuf -u http://domain/FUZZ -w wordlists/directories.txt -mc 200,403 -fc 8161"
    command = command_template.replace('domain', targetdomain)
    
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        exit_code = process.poll()
        if exit_code != 0:
            print(f"The command exited with code {exit_code}")

    except Exception as e:
        print(f"An error occurred while executing the command: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        targetdomain = sys.argv[1]
        main(targetdomain)
    else:
        print("No IP address provided.")
        sys.exit(1)
