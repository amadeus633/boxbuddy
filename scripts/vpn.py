import subprocess

def main():
    command = "sudo openvpn lab_<htb_username>.ovpn"

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
    main()
