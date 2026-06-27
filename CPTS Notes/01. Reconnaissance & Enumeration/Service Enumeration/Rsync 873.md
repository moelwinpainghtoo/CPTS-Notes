
### Check service

```bash
sudo nmap -sV -p 873 <IP>
```

### List shares

```bash
nc -nv <IP> 873
```

```
#list
```

### Enumerate share

```bash
rsync -av --list-only rsync://<IP>/dev
```

### Download files

```bash
rsync -av rsync://<IP>/dev .
```

### SSH over rsync (if required)

```bash
rsync -av -e ssh rsync://<IP>/dev .
```