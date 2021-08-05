.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 highstreet technologies and others

Docker Enable IPv6
==================

The O-RAN Alliance specifications target the support of IPv6.
To support IPv6 by docker the docker configuration must be modified. 

Please see:
https://docs.docker.com/config/daemon/ipv6/

1. Edit /etc/docker/daemon.json, set the ipv6 key to true and the fixed-cidr-v6 key to your IPv6 subnet. In this example we are setting it to 2001:db8:1::/64.

.. code-block:: json
  :linenos:
  :emphasize-lines: 12,13

  {
      "dns": ["1.1.1.1"],
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

2. Reload the Docker configuration file.

.. code-block:: bash
  :linenos:

  $ systemctl reload docker


