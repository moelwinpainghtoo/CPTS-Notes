
# General Web Discovery

```bash
sudo nmap -p 80,443,8000,8080,8180,8888,10000 --open -oA web_discovery -iL scope_list
```

## EyeWitness

```bash
# xml output from nmap
eyewitness --web -x web_discovery.xml -d inlanefreight_eyewitness
```

## Aquatone

```bash
# xml output from nmap
cat web_discovery.xml | ./aquatone -nmap
```

# WordPress

## User Roles

There are five types of users on a standard WordPress installation.

1. Administrator: This user has access to administrative features within the website. This includes adding and deleting users and posts, as well as editing source code.
2. Editor: An editor can publish and manage posts, including the posts of other users.
3. Author: They can publish and manage their own posts.
4. Contributor: These users can write and manage their own posts but cannot publish them.
5. Subscriber: These are standard users who can browse posts and edit their profiles.
## Common Paths

```bash
/robots.txt
/wp-admin
/wp-content
/wp-content/plugins
/wp-content/themes
```

## Version Enumeration

- Enumerate every page to identify installed themes and plugins

```bash
# core version
curl -s http://blog.inlanefreight.local | grep WordPress
# themes
curl -s http://blog.inlanefreight.local/ | grep themes
# plugins
curl -s http://blog.inlanefreight.local/ | grep plugins
```

## User Enumeration

- Check different error responses from login page with different users like admin

## WPScan

```bash
sudo wpscan --url http://blog.inlanefreight.local --enumerate u --api-token <token>
```

# Joomla

## Version Enumeration

```bash
# Check the website is Joomla or not
curl -s http://dev.inlanefreight.local/ | grep Joomla
# Readme Joomla
curl -s http://dev.inlanefreight.local/README.txt | head -n 5

# Paths to check version
media/system/js/
administrator/manifests/files/joomla.xml
plugins/system/cache/cache.xml

curl -s http://dev.inlanefreight.local/administrator/manifests/files/joomla.xml | xmllint --format
```

## droopescan

### Installation

```bash
git clone https://github.com/droope/droopescan.git && \  
cd droopescan && \  
uv venv -p python3.11 .venv && \  
source .venv/bin/activate && \  
uv pip install -r requirements.txt && \  
uv pip install -e . && \  
./droopescan scan --help
```

```bash
droopescan scan joomla --url http://dev.inlanefreight.local/
```

## JoomScan

https://github.com/OWASP/joomscan.git

## Joomlascan

https://github.com/drego85/JoomlaScan

```bash
python2 -m pip install bs4

python2 joomlascan.py -u http://dev.inlanefreight.local
```

## Password Brute

https://github.com/ajnik/joomla-bruteforce.git

```bash
# be patient (no output while scanning)
sudo python3 joomla-brute.py -u http://dev.inlanefreight.local -w /usr/share/metasploit-framework/data/wordlists/http_default_pass.txt -usr admin
```

# Drupal

## Discovery / Footprinting

- `Powered by Drupal` text or Drupal logo
- `CHANGELOG.txt` or `README.txt` files
- Drupal metadata in page source
- Drupal paths such as `/node` in `robots.txt`
## Common Paths

```bash
/robots.txt
/CHANGELOG.txt
/README.txt
/user/login
/user/register
/user/password
/node/1
```

## User Roles

Drupal supports three types of users by default.

1. Administrator: This user has complete control over the Drupal website.
    
2. Authenticated User: These users can log in and perform actions such as adding or editing content depending on their assigned permissions.
    
3. Anonymous: These are regular website visitors. By default, anonymous users are only allowed to read public content.

## Enumeration

```bash
# check website uses drupal 
curl -s http://drupal.inlanefreight.local | grep Drupal

# check version (latest version returns 404)
curl -s http://drupal-acc.inlanefreight.local/CHANGELOG.txt | grep -m2 ""
```

### droopescan

### Installation

```bash
git clone https://github.com/droope/droopescan.git && \  
cd droopescan && \  
uv venv -p python3.11 .venv && \  
source .venv/bin/activate && \  
uv pip install -r requirements.txt && \  
uv pip install -e . && \  
./droopescan scan --help
```

```bash
droopescan scan drupal -u http://drupal.inlanefreight.local
```




