
```bash
# Connect to FTP service interactively  
ftp <IP>  
  
# Grab banner / interact manually via raw socket  
nc -nv <IP> 21  
  
# Basic manual interaction with FTP  
telnet <IP> 21  
  
# Upgrade FTP to encrypted FTPS session  
openssl s_client -connect <IP>:21 -starttls ftp  
  
# Recursively download all files using anonymous login  
wget -m ftp://anonymous:anonymous@<IP>
```