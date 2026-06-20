
```bash
# Dump SNMP data using community string
snmpwalk -v2c -c <community> <IP>

# Bruteforce SNMP community strings
onesixtyone -c wordlist.txt <IP>
onesixtyone -c /usr/share/seclists/Discovery/SNMP/snmp.txt 10.129.85.144

# Query full SNMP OID tree
braa <community>@<IP>:.1.*
```