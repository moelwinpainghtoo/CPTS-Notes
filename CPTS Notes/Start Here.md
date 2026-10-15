# CPTS Notes — Start Here

A navigation page for the CPTS study vault. Use the sequence below as a repeatable workflow, then open the topic notes for commands, checks, and attack paths. Keep activity within the scope of an authorized lab or assessment.

## Assessment workflow

1. **Establish scope and record evidence.** Track in-scope hosts, domains, credentials, and constraints. Record commands, timestamps, outputs, and where each lead came from.
2. **Enumerate broadly, then follow evidence.** Start with [[01 - Reconnaissance & Enumeration/NMAP|Nmap]] and [[01 - Reconnaissance & Enumeration/Application Enumeration|application enumeration]]. For each discovered service, use the relevant [[01 - Reconnaissance & Enumeration/Service Enumeration/DNS 53|service enumeration note]]; for HTTP, use [[01 - Reconnaissance & Enumeration/Web Enumeration|web enumeration]]. Revisit scans as new hosts, credentials, or routes appear.
3. **Turn findings into hypotheses.** Identify exposed functionality, versions, trust relationships, and credential reuse. Validate one hypothesis at a time and preserve the request/output that supports it.
4. **Exploit a validated path.** Consult the matching [[02 - Exploitation/Application Exploitation|application]], [[02 - Exploitation/Service Exploitation/SMB|service]], or [[02 - Exploitation/Web Exploitation/SQL Injection|web exploitation]] notes. Capture the exact preconditions and proof of impact.
5. **After foothold, enumerate locally and expand carefully.** Use the [[03 - Post Exploitation/Linux Privilege Escalation|Linux]] or [[03 - Post Exploitation/Windows Privilege Escalation|Windows privilege escalation]] guides. For domain environments, follow [[AD/AD Enumeration & Attack|Active Directory enumeration and attack]] and the [[Methodology/AD/Password Attack|AD password attack workflow]]. Record pivot routes and credential provenance before moving to another host.
6. **Connect steps into a path.** Review [[Methodology/Attack Chains Map|Attack Chains Map]] and the [[Methodology/Web/LFI → Source Code Disclosure → Arbitrary File Upload → File Inclusion → RCE|web attack-chain example]]. Treat each chain as a hypothesis map, not a guaranteed recipe.
7. **Report as you go.** Use [[Reporting]] to capture discovery, exploited hosts, evidence, findings, and remediation while details are fresh.

## Main sections

### Reconnaissance and enumeration

- [[01 - Reconnaissance & Enumeration/NMAP|Nmap]]
- [[01 - Reconnaissance & Enumeration/Application Enumeration|Application Enumeration]]
- [[01 - Reconnaissance & Enumeration/Web Enumeration|Web Enumeration]]
- Service notes: [[01 - Reconnaissance & Enumeration/Service Enumeration/DNS 53|DNS]], [[01 - Reconnaissance & Enumeration/Service Enumeration/FTP 21|FTP]], [[01 - Reconnaissance & Enumeration/Service Enumeration/IMAP, POP3 (143,993,110,995)|IMAP/POP3]], [[01 - Reconnaissance & Enumeration/Service Enumeration/IPMI 623 (UDP)|IPMI]], [[01 - Reconnaissance & Enumeration/Service Enumeration/MSSQL 1433|MSSQL]], [[01 - Reconnaissance & Enumeration/Service Enumeration/MySQL 3306|MySQL]], [[01 - Reconnaissance & Enumeration/Service Enumeration/NetBIOS 137,138,139|NetBIOS]], [[01 - Reconnaissance & Enumeration/Service Enumeration/NFS 111,2049|NFS]], [[01 - Reconnaissance & Enumeration/Service Enumeration/Oracle TNS 1521|Oracle TNS]], [[01 - Reconnaissance & Enumeration/Service Enumeration/R-services 512,513,514|R-services]], [[01 - Reconnaissance & Enumeration/Service Enumeration/RDP 3389|RDP]], [[01 - Reconnaissance & Enumeration/Service Enumeration/RPC 135|RPC]], [[01 - Reconnaissance & Enumeration/Service Enumeration/Rsync 873|Rsync]], [[01 - Reconnaissance & Enumeration/Service Enumeration/SMB 445|SMB]], [[01 - Reconnaissance & Enumeration/Service Enumeration/SMTP 25,587,465|SMTP]], [[01 - Reconnaissance & Enumeration/Service Enumeration/SNMP 161,162 (UDP)|SNMP]], [[01 - Reconnaissance & Enumeration/Service Enumeration/SSH 22|SSH]].

### Exploitation

- [[02 - Exploitation/Application Exploitation|Application exploitation]]
- Service exploitation: [[02 - Exploitation/Service Exploitation/DNS|DNS]], [[02 - Exploitation/Service Exploitation/FTP|FTP]], [[02 - Exploitation/Service Exploitation/MySQL & MSSQL|MySQL and MSSQL]], [[02 - Exploitation/Service Exploitation/RDP|RDP]], [[02 - Exploitation/Service Exploitation/SMB|SMB]], [[02 - Exploitation/Service Exploitation/SMTP|SMTP]].
- Web exploitation: [[02 - Exploitation/Web Exploitation/Command Injection|Command Injection]], [[02 - Exploitation/Web Exploitation/File Inclusion|File Inclusion]], [[02 - Exploitation/Web Exploitation/File Upload|File Upload]], [[02 - Exploitation/Web Exploitation/HTTP Verb Tempering|HTTP Verb Tampering]], [[02 - Exploitation/Web Exploitation/IDOR|IDOR]], [[02 - Exploitation/Web Exploitation/Login Brute Force|Login Brute Force]], [[02 - Exploitation/Web Exploitation/SQL Injection|SQL Injection]], [[02 - Exploitation/Web Exploitation/XSS|XSS]], [[02 - Exploitation/Web Exploitation/XXE|XXE]].

### Post-exploitation, directory services, and operations

- [[03 - Post Exploitation/Linux Privilege Escalation|Linux privilege escalation]] · [[03 - Post Exploitation/Windows Privilege Escalation|Windows privilege escalation]]
- [[AD/AD Enumeration & Attack|AD Enumeration & Attack]] · [[AD/Notes|AD Notes]] · [[Methodology/AD/Password Attack|AD Password Attack]]
- [[C2/Sliver|Sliver]]
- Utilities: [[Utilities/Adding hosts file|hosts file]], [[Utilities/Credential Hunting|credential hunting]], [[Utilities/Custom Wordlists|custom wordlists]], [[Utilities/File Transfer|file transfer]], [[Utilities/Metasploit|Metasploit]], [[Utilities/Password Attack|password attacks]], [[Utilities/Pivoting, Tunneling and Port Forwarding|pivoting and tunneling]], [[Utilities/Shells|shells]], [[Utilities/SQLMap|SQLMap]], [[Utilities/Web Proxies|web proxies]], [[Utilities/Windows AV|Windows AV]].

### Methodology and reporting

- [[Methodology/Attack Chains Map|Attack Chains Map]]
- Enumeration chains: [[Methodology/Enumeration/NFS → SMB → RDP → MSSQL → ADMIN|NFS → SMB → RDP → MSSQL]], [[Methodology/Enumeration/SNMP → IMAP,POP3 → SSH → MySQL|SNMP → IMAP/POP3 → SSH → MySQL]]
- [[Methodology/Web/LFI → Source Code Disclosure → Arbitrary File Upload → File Inclusion → RCE|LFI to RCE chain]]
- [[Reporting|Reporting Structure]]

## Study and lab notes

The vault also contains [[Lab 01 - Formatted.docx|Lab 01 - Formatted]] (Word document). For each lab, capture the initial clue, enumeration decisions, validated exploit path, privilege escalation, proof, and one lesson to reuse. Prefer concise, reproducible steps over command dumps without context.

