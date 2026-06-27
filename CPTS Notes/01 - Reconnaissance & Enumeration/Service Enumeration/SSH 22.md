### Basic connection

```bash
ssh user@<IP>
```

```bash
ssh -v user@<IP>
```

```bash
ssh user@<IP> -o PreferredAuthentications=password
```

---

### SSH key / fingerprint audit

```bash
git clone https://github.com/jtesta/ssh-audit.git
cd ssh-audit
python3 ssh-audit.py <IP>
```