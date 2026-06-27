
```bash
IP=10.129.42.195

for host in \  
app.inlanefreight.local \  
dev.inlanefreight.local \
inlanefreight.local  
do  
printf "%s\t%s\n" "$IP" "$host"  
done | sudo tee -a /etc/hosts
```