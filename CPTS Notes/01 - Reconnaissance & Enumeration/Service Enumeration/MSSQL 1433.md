### Nmap

```bash
nmap -sV -p 1433 --script ms-sql-info,ms-sql-empty-password,ms-sql-xp-cmdshell,ms-sql-config,ms-sql-ntlm-info,ms-sql-tables,ms-sql-hasdbaccess,ms-sql-dac,ms-sql-dump-hashes <IP>
```

### Metasploit

```bash
use auxiliary/scanner/mssql/mssql_ping
set rhosts <IP>
run
```

### Impacket mssqlclient

```bash
python3 mssqlclient.py <user>@<IP> -windows-auth
```

### Basic Query

```sql
select system_user;
select name from sys.databases;
use master;
select * from information_schema.tables;
```

## Default Databases

- master → system information
- model → template for new databases
- msdb → jobs & scheduling
- tempdb → temporary data
- resource → read-only system objects