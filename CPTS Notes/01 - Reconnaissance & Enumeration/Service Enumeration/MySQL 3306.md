## Enumeration Commands

### Nmap

```bash
nmap -p3306 -sV -sC <IP>
nmap -p3306 --script mysql* <IP>
```

### MySQL Client

```bash
mysql -u <user> -p<password> -h <IP> -ssl=0
```

### Basic Queries

```sql
show databases;
use <database>;
show tables;
select * from <table>;
describe users;                     # show columns
select version();
```

---

## Dangerous Settings

|Setting|Description|
|---|---|
|user|Defines which system user runs the MySQL service|
|password|Password stored in configuration (plaintext risk)|
|admin_address|Defines IP for administrative access|
|debug|Enables verbose debugging output|
|sql_warnings|Displays warnings that may leak information|
|secure_file_priv|Controls import/export file operations|

---

## File Locations

```bash
/etc/mysql/mysql.conf.d/mysqld.cnf
```