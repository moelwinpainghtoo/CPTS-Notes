
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

