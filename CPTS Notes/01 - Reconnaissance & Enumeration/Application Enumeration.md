
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

# Tomcat

Checklist:
- tomcat:tomcat, admin:admin (try default passwords)
## General Folder Structure

```bash
tomcat/
├── bin/
├── conf/
│   ├── catalina.policy
│   ├── catalina.properties
│   ├── context.xml
│   ├── tomcat-users.xml
│   ├── tomcat-users.xsd
│   └── web.xml
├── lib/
├── logs/
├── temp/
├── webapps/
│   ├── manager/
│   │   ├── images/
│   │   ├── META-INF/
│   │   └── WEB-INF/
│   │       └── web.xml
│   ├── ROOT/
│   │   └── WEB-INF/
│   └── customapp/
│       ├── images/
│       ├── index.jsp
│       ├── META-INF/
│       │   └── context.xml
│       ├── status.xsd
│       └── WEB-INF/
│           ├── web.xml
│           ├── jsp/
│           │   └── admin.jsp
│           ├── lib/
│           │   └── jdbc_drivers.jar
│           └── classes/
│               └── AdminServlet.class
├── work/
│   └── Catalina/
│       └── localhost/
└── temp/
```

## Version Enumeration

> If the server is operating behind a reverse proxy, requesting an invalid page should reveal the server and version.

```bash
# check invalid endpoint
http://app-dev.inlanefreight.local:8080/invalid
curl -s http://app-dev.inlanefreight.local:8080/docs/ | grep Tomcat
```

## Important files to check

```bash
web.xml
# used to allow or disallow access to the `/manager` and `host-manager` admin pages.
tomcat-users.xml
```

## Directory Bruteforce

```bash
gobuster dir -u http://web01.inlanefreight.local:8180/ -w /usr/share/dirbuster/wordlists/directory-list-2.3-small.txt
```

# Jenkins

- Jenkins runs on Tomcat port 8080 by default. It also utilizes port 5000 to attach slave servers.

```bash
# default creds
admin:admin
```

# Splunk

Note: If ssl/http from Nmap result, uses https://host:8000

- The Splunk web server runs by default on port 8000. Nmap scan will also reveal it.
- Splunk has multiple ways of running code, such as server-side Django applications, REST endpoints, scripted inputs, and alerting scripts. A common method of gaining remote code execution on a Splunk server is through the use of a scripted input
## Default Creds

```bash
# username admin
# possible passowrds
changeme
admin
Welcome
Welcome1
Password123
```

## Version Enumeration

```bash
# inspect the page with this keyword (after login)
version": "
```

## CVEs

- https://www.exploit-db.com/exploits/40895
- https://www.cvedetails.com/vulnerability-list/vendor_id-10963/Splunk.html

# PRTG Network Monitor

## CVEs

- CVE-2018-9276 before version 18.2.39

## Default Creds

```bash
prtgadmin:prtgadmin
prtgadmin:Password123
```

## Version Enumeration

```bash
curl -s http://10.129.201.50:8080/index.htm -A "Mozilla/5.0 (compatible; MSIE 7.01; Windows NT 5.0)" | grep version
```

# osTicket

https://www.cvedetails.com/vendor/2292/Osticket.html

1. Identify osTicket: OSTSESSID cookie, “powered by osTicket”, /open.php, /scp/login.php.
2. Create ticket if allowed and check if a temporary internal email/ticket email is assigned.
3. Try scoped leaked credentials from DeHashed against osTicket and other exposed portals.
4. Review tickets for password reset details, standard passwords, VPN info, usernames, and emails.
5. Export/enumerate address book or staff/user emails if access allows.
6. Check detected osTicket version against known issues, especially CVE-2020-24881 SSRF in osTicket 1.14.1.
7. Check closed tickets for credentials harvesting. ***
8. Use email address if the Username is not working. ***
9. Test credential reuse or password spraying only when explicitly authorized.

# GitLab

## Enumeration

```bash
gitlab.company.com
```