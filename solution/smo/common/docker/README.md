# Docker configuration

To support IPv6 the docker configuration must be modified. 

Please see:
https://docs.docker.com/config/daemon/ipv6/

1. Edit /etc/docker/daemon.json, set the ipv6 key to true and the fixed-cidr-v6 key to your IPv6 subnet. In this example we are setting it to 2001:db8:1::/64.


```
{
  "registry-mirrors": [
      "https://nexus3.o-ran-sc.org:10002", 
      "https://nexus3.onap.org:10001"
  ],
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  },
  "ipv6": true,
  "fixed-cidr-v6": "2001:db8:1::/64"
}
```

2. Reload the Docker configuration file.

```
$ systemctl reload docker
```