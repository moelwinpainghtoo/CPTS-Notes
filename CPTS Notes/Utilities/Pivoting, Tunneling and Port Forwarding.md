
# SSH

## Dynamic Port Forwarding

```bash
# Forwarind two local ports 1234 & 8080
ssh -L 1234:localhost:3306 -L 8080:localhost:80 ubuntu@10.129.202.64

# Dynamic port forward
ssh -D 9050 ubuntu@10.129.202.64

netstat -antp | grep 1234
tail -4 /etc/proxychains.conf
```

## Reverse Port Forwarding

```bash
# forward pivothost's port 8080 to local port 8000
ssh -R <InternalIPofPivotHost>:8080:0.0.0.0:8000 ubuntu@<ipAddressofTarget> -vN
```

# Meterpreter

## Ping Sweep

### Meterpreter

```bash
# Perform an ICMP sweep through the Meterpreter pivot session
run post/multi/gather/ping_sweep RHOSTS=172.16.5.0/23
```

### Linux

```bash
# Ping every address in the target subnet from a Linux pivot host
for i in {1..254}; do (ping -c 1 172.16.5.$i | grep "bytes from" &) ; done
```

### Windows

```powershell
# Ping every address in the target subnet from a Windows CMD pivot host
for /L %i in (1 1 254) do ping 172.16.5.%i -n 1 -w 100 | find "Reply"
```

### PowerShell

```powershell
# Ping every address in the target subnet from a PowerShell pivot host
1..254 | % {"172.16.5.$($_): $(Test-Connection -Count 1 -ComputerName 172.16.5.$($_) -Quiet)"}
```

## Configure the Metasploit SOCKS Proxy

```bash
# Select the SOCKS proxy module
use auxiliary/server/socks_proxy

# Set the local SOCKS proxy port
set SRVPORT 9050

# Listen on all local interfaces
set SRVHOST 0.0.0.0

# Configure SOCKS version 4a
set VERSION 4a

# Start the SOCKS proxy as a background job
run

# Need to configure proxychains.conf if needed
```

## Add a Route with AutoRoute Module

```bash
# Select the AutoRoute post-exploitation module
use post/multi/manage/autoroute

# Select the Meterpreter session
set SESSION 1

# Configure Subnet
set SUBNET 172.16.5.0

run
```

```bash
# another way
run autoroute -s 172.16.5.0/23

# Listing active routes
run autoroute -p
```

## Port Forward

```bash

portfwd add -l 3300 -p 3389 -r 172.16.5.19
```