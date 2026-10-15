# Nmap

Use Nmap to discover reachable hosts and services, then narrow later scans to the ports and protocols that evidence supports. Run scans only against systems in the authorized scope. Save original output so findings can be revisited and reported accurately.

## Quick workflow

1. Discover hosts on the authorized subnet.
2. Scan common TCP ports on each live host.
3. Run a full TCP port scan if the initial results or scope justify it.
4. Fingerprint discovered services and run only relevant NSE checks.
5. Scan UDP separately; UDP results need careful interpretation.
6. Re-scan targeted ports after gaining credentials or discovering new routes.

## Host discovery

```bash
# ARP discovery on a directly connected local Ethernet network
sudo nmap -sn 192.168.1.0/24

# ICMP echo and common TCP discovery probes; use when ARP is unavailable
nmap -sn -PE -PS22,80,443 -PA443 192.168.1.0/24

# When discovery probes are filtered, treat each scoped address as online
nmap -Pn -p 22,80,443 192.168.1.10
```

`-sn` performs host discovery without a port scan. A host that does not answer discovery probes may still be up; filtering, routing, or host firewall rules can cause false negatives. `-Pn` skips discovery and proceeds as though targets are online, so use it against a bounded target list or subnet.

## TCP port discovery

```bash
# Fast initial scan of common TCP ports
sudo nmap -sS --top-ports 1000 -T3 -n -oA scans/host-tcp-top 192.168.1.10

# Scan every TCP port (1-65535)
sudo nmap -sS -p- -T3 -n -oA scans/host-tcp-all 192.168.1.10

# Scan a known port list, including UDP ports in scope
sudo nmap -sS -sU -p T:22,80,443,U:53,161 -sV -oA scans/host-targeted 192.168.1.10

# If raw packet scanning is unavailable, use a TCP connect scan
nmap -sT -p 22,80,443 192.168.1.10
```

A SYN scan (`-sS`) generally requires elevated privileges. A connect scan (`-sT`) uses the operating system's connection call. `-p-` means all TCP ports; it does not include UDP. Add `-p-` only when a full port sweep is appropriate for the time and scope.

## Service and version detection

```bash
# Probe only the ports already found open
sudo nmap -sV -sC -p 22,80,445 192.168.1.10

# Lighter version probes when time or network impact matters
nmap -sV --version-light -p 22,80,445 192.168.1.10

# Recheck a specific service with a relevant script category or script
nmap -p 445 --script smb-os-discovery,smb-enum-shares 192.168.1.10
```

`-sV` probes services for product/version details. `-sC` runs the default NSE script set; scripts can send application requests and some can be intrusive. Review the selected scripts and target authorization before running them. Do not assume a reported version alone proves a vulnerability; validate configuration and exploit preconditions separately.

## UDP scanning

```bash
# Common UDP ports, with service detection
sudo nmap -sU --top-ports 100 -sV -T3 -n -oA scans/host-udp 192.168.1.10

# Target likely infrastructure services
sudo nmap -sU -p 53,67,123,137,161,500,623 -sV 192.168.1.10
```

UDP scans are slower and often return `open|filtered` because UDP services may not reply and ICMP errors may be filtered. Follow up with protocol-aware enumeration; do not report `open|filtered` as confirmed open without corroboration.

## Useful options

| Option | Purpose |
| --- | --- |
| `-p 22,80` | Scan selected ports |
| `-p-` | Scan all TCP ports (1–65535) |
| `-p U:53,161` | Select UDP ports |
| `-sS` / `-sT` | TCP SYN / TCP connect scan |
| `-sU` | UDP scan |
| `-sV` | Service/version detection |
| `-sC` | Default NSE scripts |
| `-Pn` | Skip host discovery |
| `-n` | Disable DNS resolution |
| `-T0`–`-T5` | Timing template; higher values can be less reliable or more disruptive |
| `--reason` | Show why Nmap assigned a state |
| `-oA <prefix>` | Save normal, XML, and grepable output |
| `--open` | Show only open (or potentially open) ports |
| `-iL targets.txt` | Read targets from a file |

Prefer a conservative timing template on fragile or high-latency networks. A fast scan that drops probes can miss services; if results look incomplete, reduce timing and repeat a targeted scan.

## Read the states correctly

- **open**: an application accepted or answered the probe on that port.
- **closed**: the host responded, but no service is listening on that port at scan time.
- **filtered**: Nmap cannot determine whether the port is open because probes are blocked or unanswered.
- **open|filtered**: Nmap cannot distinguish an open silent service from filtering (common with UDP).
- **unfiltered**: the port is reachable, but the selected scan cannot determine whether it is open.

Record the state, protocol, service evidence, and scan context. A service name in the port table can come from a port-number mapping; use `-sV` and application-level checks before treating it as a verified identification.

## Save and revisit results

```bash
mkdir -p scans
sudo nmap -sS --top-ports 1000 -sV -oA scans/192.168.1.10-initial 192.168.1.10

# Readable output
less scans/192.168.1.10-initial.nmap

# Extract open ports from grepable output
awk '/\/open\// {print $2, $3}' scans/192.168.1.10-initial.gnmap
```

Keep the `.nmap`, `.xml`, and `.gnmap` files together. Record the command, date/time, source vantage point, target, and any credentials or route changes that affected a follow-up scan. Update the host/service inventory in [[Reporting]] as evidence is confirmed.

## Common pitfalls

- Scanning only the top ports can miss services on high TCP ports; do a full TCP sweep when justified.
- A failed ping or discovery probe does not prove a host is offline.
- TCP results do not cover UDP; scan UDP as a separate step when in scope.
- Filtered and `open|filtered` states are inconclusive, not proof of an open application.
- Broad NSE wildcards can run many scripts with different behaviors; select scripts deliberately.
- Port-based service labels and version banners are leads. Validate them before choosing an exploit.
- Preserve raw output and avoid reporting a scan as exhaustive if ports, protocols, or reachable network segments were excluded.

## Related notes

- [[01 - Reconnaissance & Enumeration/Service Enumeration/SMB 445|SMB service enumeration]]
- [[01 - Reconnaissance & Enumeration/Service Enumeration/SNMP 161,162 (UDP)|SNMP service enumeration]]
- [[01 - Reconnaissance & Enumeration/Service Enumeration/DNS 53|DNS service enumeration]]
- [[Utilities/Adding hosts file|Manage discovered hostnames locally]]
- [[Reporting|Record discovered hosts and services]]

## Existing quick snippets

### Banner script

```bash
sudo nmap -v <IP> --script banner
```

### Host file generation from authenticated SMB enumeration

```bash
nxc smb <IP> --generate-hosts-file /tmp/hosts.tmp
sudo tee -a /etc/hosts < /tmp/hosts.tmp
rm /tmp/hosts.tmp
```

Review generated entries before appending them, especially when a hostname already exists. See [[Utilities/Adding hosts file]].
