# Deployment Process

If all goes well the commands and its responses looks like this:

```
demx8as6@oam.orbit-lab.org$ docker-compose -f smo/common/docker-compose.yml up -d
Creating zookeeper   ... done
Creating identity    ... done
Creating persistence ... done
Creating kafka       ... done
Creating onap-dmaap  ... done

demx8as6@oam.orbit-lab.org$ python smo/common/identity/config.py
Got token!
User leia.organa created!
User r2.d2 created!
User luke.skywalker created!
User jargo.fett created!
User martin.skorupski created!
User demx8as6 created!
User role demx8as6 administration created!
User role jargo.fett supervision created!
User role leia.organa administration created!
User role luke.skywalker provision created!
User role martin.skorupski administration created!
User role r2.d2 administration created!

demx8as6@oam.orbit-lab.org$ docker-compose -f smo/oam/docker-compose.yml up -d
WARNING: Found orphan containers (kafka, persistence, identity, zookeeper, onap-dmaap) for this project. If you removed or renamed this service in your compose file, you can run this command with the --remove-orphans flag to clean it up.
Creating sdnc-web      ... done
Creating sdnr          ... done
Creating ves-collector ... done

demx8as6@oam.orbit-lab.org$ docker-compose -f network/docker-compose.yml up -d
Creating ntsim-ng-o-du-1122     ... done
Creating ntsim-ng-o-ru-fh-11223 ... done
Creating ntsim-ng-o-ru-fh-11221 ... done
Creating ntsim-ng-o-ru-fh-11222 ... done

demx8as6@oam.orbit-lab.org$ docker restart ntsim-ng-o-du-1122
ntsim-ng-o-du-1122

demx8as6@oam.orbit-lab.org$ python network/config.py
Set O-RU-11222 True
Set O-RU-11221 True
Set O-DU-1122 True
Set O-RU-11223 True

demx8as6@oam.orbit-lab.org$
```

# Verification with ODLUX

The ODLUX web application is accessible at port 8453.

```
https://sdnc-web:8453/
```

## Connect

At the 'Connect' page, 4 connections to the simulated network should be in state 'connected'. This validates the secure (TLS) VES:PNF-Registration and NETCONF CallHome onboarding is correctly configured for IPv6.

![Automated onboarding using NETCONF CallHome or VES:PNF-Registration](docs/smo-oam-test-01.png "Automated onboarding using NETCONF CallHome or VES:PNF-Registration")

## Fault

The simulated Network is configured in a way that spontaneous fault messages are send to the SMO using the VES or the NETCONF protocol.

At the 'Fault' page on tab 'Alarm Log' NETCONF and VES fault notification should be visible.

![Fault notification (NETCONF and VES)](docs/smo-oam-test-02.png "Fault notification (NETCONF and VES)")

