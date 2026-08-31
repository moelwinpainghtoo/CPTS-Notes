
## nexura.htb Attack Chain

### 1. DMZ01 → Initial Access

- Only SSH open
- Generated username wordlist from `Betty Jayde` via `username-anarchy`
- Hydra brute-force → `jbetty:Texas123!@#`

### 2. FILE01 → Credential Discovery

- Found `hwilliam:dealer-screwed-gym1` in `jbetty`'s `.bash_history`
- SMB enumeration → READ/WRITE on `HR` share
- Downloaded `Employee-Passwords_OLD.psafe3` → cracked with `john` (`michaeljackson`)
- Opened pwsafe vault → `bdavid:caramel-cigars-reply1`

### 3. JUMP01 → Privilege Escalation

- RDP as `bdavid` → ran mimikatz (`sekurlsa::logonpasswords`)
- Dumped `stom:calves-warp-learning1` from LSASS
- `stom` = **Domain Admin**

### 4. DC01 → Domain Compromise

- DCSync via `nxc --ntds` as `stom`
- Dumped Administrator NTLM hash → `36e09e1e6ade94d63fbcab5e5b8d6d23`
- **Domain fully compromised**

---

```
jbetty → hwilliam → bdavid → stom (DA) → Administrator
DMZ01  →  FILE01  →  JUMP01           →  DC01
```