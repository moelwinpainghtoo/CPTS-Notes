
# SSH

## Dynamic Port Forwarding

```bash
# Forwarind two local ports 1234 & 8080
ssh -L 1234:localhost:3306 -L 8080:localhost:80 ubuntu@10.129.202.64

# Dynamic port forward
ssh -D 9050 ubuntu@10.129.202.64

netstat -antp | grep 1234
tail -4 /etc/proxychains.conf
```

## Reverse Port Forwarding

```bash
# forward pivothost's port 8080 to local port 8000
ssh -R <InternalIPofPivotHost>:8080:0.0.0.0:8000 ubuntu@<ipAddressofTarget> -vN
```


# Meterpreter

