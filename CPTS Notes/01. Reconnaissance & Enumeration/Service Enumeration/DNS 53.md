
```bash
# Query nameservers for domain
dig ns <domain> @<ns>

# Retrieve all DNS records
dig any <domain> @<ns>

# Attempt zone transfer (full DNS dump)
dig axfr <domain> @<ns>

# Reverse Lookup
dig -x <IP>

# Automated DNS enumeration and subdomain brute-force
dnsenum --dnsserver <ns> --enum -p 0 -s 0 -o out.txt -f wordlist.txt <domain>

# Manual subdomain brute-force loop
for sub in $(cat wordlist.txt); do dig $sub.<domain> @<ns>; done
```