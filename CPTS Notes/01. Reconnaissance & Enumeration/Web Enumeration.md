
```table-of-contents
```

# Host File Location
```bash
C:\Windows\System32\drivers\etc\hosts
/etc/hosts
```

```bash

whois domain.com

```


# DNS
## Dig Commands

```bash
# Default A record lookup for a domain
dig domain.com

# Retrieve IPv4 address (A record)
dig domain.com A

# Retrieve IPv6 address (AAAA record)
dig domain.com AAAA

# Find mail servers (MX records)
dig domain.com MX

# Identify authoritative name servers (NS records)
dig domain.com NS

# Retrieve TXT records
dig domain.com TXT

# Retrieve canonical name (CNAME) record
dig domain.com CNAME

# Retrieve start of authority (SOA) record
dig domain.com SOA

# Query using a specific DNS server
dig @1.1.1.1 domain.com

# Show full DNS resolution path (trace from root)
dig +trace domain.com

# Reverse lookup IP to hostname
dig -x 192.168.1.1

# Short output (minimal result)
dig +short domain.com

# Show only answer section
dig +noall +answer domain.com

# Retrieve all DNS records (may be ignored by some servers)
dig domain.com ANY
```


## Subdomain Enumeration

```
curl https://api.hackertarget.com/hostsearch/?q=gempak.com

```

### dnsenum

```bash
dnsenum --enum inlanefreight.com -f /usr/share/seclists/Discovery/DNS/subdomains-top1million-20000.txt -r
```

### DNS zone transfer

```bash
dig axfr @nsztm1.digi.ninja zonetransfer.me
dig axfr inlanefreight.htb @10.129.86.94

# rule
If NS → 127.0.0.1 → ignore → use target IP
```


### Virtual host Fuzzing

```bash
gobuster vhost -u http://<domain_name:8080> -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt --append-domain

ffuf -u https://kobold.htb/ -H "Host: FUZZ.kobold.htb" -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt -ic -fs 154
```

### Certificate Transparency Logs

```bash
curl -s "https://crt.sh/?q=facebook.com&output=json" | jq -r '.[] | select(.name_value | contains("dev")) | .name_value' | sort -u
```


# Finger Printing

```bash
curl -I https://inlanefreight.com

wafw00f inlanefreight.com

nikto -h inlanefreight.com -Tuning b
```

# Crawling
## Well-Known Uri

```bash
# .well-known (Recon)

# Key URIs
/.well-known/openid-configuration  
/.well-known/security.txt  
/.well-known/change-password  
/.well-known/assetlinks.json  
/.well-known/mta-sts.txt  

# Focus
openid-configuration → auth endpoints, jwks, scopes

# Action
curl target/.well-known/<file>
```

## Custom Script for Crawling

```bash
uv venv
uv pip install scrapy

wget -O ReconSpider.zip https://academy.hackthebox.com/storage/modules/144/ReconSpider.v1.2.zip
unzip ReconSpider.zip

uv run python ReconSpider.py http://inlanefreight.com
```

# Search Engine Discovery

```bash
site:example.com "password reset"  
inurl:admin login  
filetype:pdf "confidential report"  
intitle:"index of" /backup  
cache:example.com  
"internal error" site:example.com  
inurl:admin OR inurl:login  
inurl:admin -intext:wordpress
```

# Automated Scan

```bash
./finalrecon.py --headers --whois --url http://inlanefreight.com
```