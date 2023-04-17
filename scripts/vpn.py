import subprocess, sys

def main(vpnfile):

    vpnfile = vpnfile.replace(';','')
    command = f"sudo openvpn {vpnfile}"

    try:
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.strip())

        exit_code = process.poll()
        if exit_code != 0:
            print("The command exited with code {exit_code}")

    except Exception as e:
        print("An error occurred while executing the command: {e}")
    

if __name__ == "__main__":
    n = sys.argv[1]
    main(n)
