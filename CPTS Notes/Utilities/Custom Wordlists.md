
# User Wordlist

| Command                                  | Description                                                                                   |
| ---------------------------------------- | --------------------------------------------------------------------------------------------- |
| `username-anarchy Jane Smith > jane.txt` | Generate possible usernames for "Jane Smith"                                                  |
| `username-anarchy -i names.txt`          | Use a file (`names.txt`) with names for input. Can handle space, CSV, or TAB delimited names. |
| `username-anarchy -a --country us`       | Automatically generate usernames using common names from the US dataset.                      |
| `username-anarchy -l`                    | List available username format plugins.                                                       |
| `username-anarchy -f format1,format2`    | Use specific format plugins for username generation (comma-separated).                        |
| `username-anarchy -@ example.com`        | Append `@example.com` as a suffix to each username.                                           |
| `username-anarchy --case-insensitive`    | Generate usernames in case-insensitive (lowercase) format.                                    |

# Password Wordlist

| Command                | Description                                                         |
| ---------------------- | ------------------------------------------------------------------- |
| `cupp -i`              | Generate wordlist based on personal information (interactive mode). |
| `cupp -w profiles.txt` | Generate a wordlist from a predefined profile file.                 |
| `cupp -l`              | Download popular password lists like `rockyou.txt`.                 |

# Password Policy Filtering (grep)

## Requirements
- Minimum length: **6 characters**
- Must include:
  - At least **1 uppercase letter** `[A-Z]`
  - At least **1 lowercase letter** `[a-z]`
  - At least **1 number** `[0-9]`
  - At least **2 special characters** from: `!@#$%^&*`

## Filtering Approach (Linux grep)

We can use `grep` with regular expressions to progressively filter a password list:

```bash
grep -E '^.{6,}$' jane.txt \
| grep -E '[A-Z]' \
| grep -E '[a-z]' \
| grep -E '[0-9]' \
| grep -E '([!@#$%^&*].*){2,}' \
> jane-filtered.txt
```

# Hashcat

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

# Website Hunt (CeWL)

Use to hunt down websites for password.

- https://github.com/digininja/CeWL

```bash
cewl https://www.inlanefreight.com -d 4 -m 6 --lowercase -w inlane.wordlist
```
