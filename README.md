# tippy

Raspbian on Raspberry Pi

```bash
$ cd /home/pi && git clone https://github.com/upamune/tippy
$ cd tippy
$ pip3 install -r requirements.txt
$ cp etc/*.service /etc/systemd/system
$ cp etc/nginx.conf /etc/nginx
$ systemctl start tippy
$ systemctl start tippy_arp
$ systemctl restart nginx
```

