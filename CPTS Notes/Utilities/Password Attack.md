
# Tools

## John The Ripper

```bash
locate *2john*
```

### Single Crack Mode

Uses username, home directory, and GECOS information to generate password candidates, then applies common password-modification rules to crack the hash.

```bash
john --single passwd
```

### Wordlist Mode

```bash
john --wordlist=<wordlist_file> <hash_file>
```

### Incremental mode

Generates password candidates dynamically using statistical patterns and character combinations, making it more effective than random brute force but slower and resource-intensive.

```bash
john --incremental <hash_file>
```

### Identify Hash Format

```bash
hashid -j 193069ceb0461e1d40d216e32c79c70
```

## Hashcat

### Hash Identification

```bash
hashcat --help

# identify hash
hashid -m '$1$FNr44XZC$wQxY6HHLrgrGX0e1195k.1'

# rule file location
ls -l /usr/share/hashcat/rules
```

### Apply Rule

```bash
hashcat -a 0 -m 0 1b0556a75770563578569ae21392630c /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule
```

### Mask attack

| Symbol | Charset                             |
| ------ | ----------------------------------- |
| ?l     | abcdefghijklmnopqrstuvwxyz          |
| ?u     | ABCDEFGHIJKLMNOPQRSTUVWXYZ          |
| ?d     | 0123456789                          |
| ?h     | 0123456789abcdef                    |
| ?H     | 0123456789ABCDEF                    |
| ?s     | «space»!"#$%&'()*+,-./:;<=>?@[]^_`{ |
| ?a     | ?l?u?d?s                            |
| ?b     | 0x00 - 0xff                         |
```bash
hashcat -a 3 -m 0 1e293d6912d074c0fd15844d803400dd '?u?l?l?l?l?d?s'
```

## Creating Custom Wordlist

- https://hashcat.net/wiki/doku.php?id=rule_based_attack

```bash
cat custom.rule

:
c
so0
c so0
sa@
c sa@
c sa@ so0
$!
$! c
$! so0
$! sa@
$! c so0
$! c sa@
$! so0 sa@
$! c so0 sa@
```

```bash
hashcat --force password.list -r custom.rule --stdout | sort -u > mut_password.list
```

### CeWL

- https://github.com/digininja/CeWL

```bash
cewl https://www.inlanefreight.com -d 4 -m 6 --lowercase -w inlane.wordlist
```