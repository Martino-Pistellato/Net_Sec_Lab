# Docker strusture
In this section, bla bla bla



## Networking
The following paragraph shows the networks, subnets and the routers that compose and creates our network.
### Networks and subnets
| NAME           | NETWORK IP      | IP RANGE                    | DESCRIPTION                    |
|----------------|-----------------|-----------------------------|--------------------------------|
| internet       | 172.0.0.0/24    | 172.0.0.1 - 172.0.0.254     | Bridge for internet connection |
| web            | 172.0.254.0/24  | 172.0.254.1 - 172.0.254.254 | Fake-ISP WAN               |
| corpA          | 172.0.254.16/28 | 172.0.254.17 - 172.0.254.30 | Corporate A subnet             |
| corpB          | 172.0.254.32/28 | 172.0.254.33 - 172.0.254.46 | Corporate B subnet             |
| houseA         | 172.0.254.48/28 | 172.0.254.49 - 172.0.254.62 | House A subnet                 |
| houseA-private | 192.168.0.0/28  | 192.168.0.1 - 192.168.0.14  | House A private network        |
| houseB         | 172.0.254.64/28 | 172.0.254.65 - 172.0.254.78 | House B subnet                 |
| houseB-private | 192.168.2.0/28  | 192.168.2.1 - 192.168.2.14  | House B private network        |

### Routers
The network contains 3 routers, one managing the main network (web) and two simulating a domestic router. 

#### web-router
| INTERFACE | (SUB-)NETWORK  | IP ADDRESS   | 
|-----------|----------------|--------------|
| eth0      | web            | 172.0.254.5  |
| eth1      | internet       | 172.0.0.254  |
| eth2      | corpA          | 172.0.254.29 |
| eth3      | corpB          | 172.0.254.45 |
| eth4      | houseA         | 172.0.254.61 |
| eth5      | houseB         | 172.0.254.77 |

#### housea-router
| INTERFACE | (SUB-)NETWORK  | IP ADDRESS   | 
|-----------|----------------|--------------|
| eth0      | houseB         | 172.0.254.50 |
| eth1      | houseB-private | 192.168.0.2  |

#### houseb-router
| INTERFACE | (SUB-)NETWORK  | IP ADDRESS   | 
|-----------|----------------|--------------|
| eth0      | houseB         | 172.0.254.66 |
| eth1      | houseB-private | 192.168.2.2  |


## Containers (hosts and router)
The following paragraph provides information about the Docker containers inlcluding also some router's details previously omitted. The containers will be grouped by the respective subnet.

### Web network subnet
Docker does not support external gateways. For this reason, the web-router has mutiple IP addresses to let other subnets use web-router as gateway. Those IPs can be safely ignored for our purposes. 
| NAME        | ROLE    | IP          | OPEN PORTS    | OS                  | Kernel |
|-------------|---------|-------------|---------------|---------------------|--------|
| web-router  | router  | 172.0.254.5 |               | FRRouting (Alpine)  | 6.8.0-39-generic    |
| attacker    | attacker| 172.0.254.6 |               | Ubuntu 22.04        | 5.15

### CorpA subnet
CorpA simulates a corporate with the zombie offering a web-server.

| NAME        | ROLE   | IP           | OPEN PORTS    | OS           | Kernel |
|-------------|--------|--------------|---------------|--------------|--------|
| corpa-ubu12 | zombie | 172.0.254.18 | 8081          | Ubuntu 12.04 | 3.2    |
| corpa-ubu14 | victim | 172.0.254.19 |               | Ubuntu 14.04 | 3.13   |
| corpa-ubu16 | victim | 172.0.254.20 |               | Ubuntu 16.04 | 4.5    |
| corpa-ubu18 | victim | 172.0.254.21 |               | Ubuntu 18.04 | 4.15   |
| corpa-ubu20 | victim | 172.0.254.22 |               | Ubuntu 20.04 | 5.4    |
| corpa-ubu22 | victim | 172.0.254.23 |               | Ubuntu 22.04 | 5.15   |

### CorpB subnet
CorpB simulates a corporate without services offerd.

| NAME        | ROLE   | IP           | OPEN PORTS    | OS           | Kernel |
|-------------|--------|--------------|---------------|--------------|--------|
| corpb-ubu12 | zombie | 172.0.254.34 |               | Ubuntu 12.04 | 3.2    |
| corpb-ubu14 | victim | 172.0.254.35 |               | Ubuntu 14.04 | 3.13   |
| corpb-ubu16 | victim | 172.0.254.36 |               | Ubuntu 16.04 | 4.5    |
| corpb-ubu18 | victim | 172.0.254.37 |               | Ubuntu 18.04 | 4.15   |
| corpb-ubu20 | victim | 172.0.254.38 |               | Ubuntu 20.04 | 5.4    |
| corpb-ubu22 | victim | 172.0.254.39 |               | Ubuntu 22.04 | 5.15   |

### HouseA subnet
HouseA has only a router separating the private network from the main one. No ports are exposed

| NAME          | ROLE   | IP           | OPEN PORTS    | OS                  | Kernel |
|---------------|--------|--------------|---------------|---------------------|--------|
| housea-router | router | 172.0.254.50 |               | FRRouting (Alpine) | 6.8.0-39-generic    |

### HouseA private network
This is the private network of HouseA. It's not reacheable form external hosts.
| NAME         | ROLE   | IP          | OPEN PORTS    | OS           | Kernel |
|--------------|--------|-------------|---------------|--------------|--------|
| housea-ubu12 | zombie | 192.168.0.3 |               | Ubuntu 12.04 | 3.2    |
| housea-ubu14 | victim | 192.168.0.4 |               | Ubuntu 14.04 | 3.13   |
| housea-ubu16 | victim | 192.168.0.5 |               | Ubuntu 16.04 | 4.5    |
| housea-ubu18 | victim | 192.168.0.6 |               | Ubuntu 18.04 | 4.15   |
| housea-ubu20 | victim | 192.168.0.7 |               | Ubuntu 20.04 | 5.4    |
| housea-ubu22 | victim | 192.168.0.8 |               | Ubuntu 22.04 | 5.15   |

### HouseB subnet
HouseB has only a router separating the private network from the main one. The port are exposed only for forwarding packets to the zombie. 

| NAME          | ROLE   | IP           | OPEN PORTS    | OS                  | Kernel |
|---------------|--------|--------------|---------------|---------------------|--------|
| housea-router | router | 172.0.254.50 | 8082          | FRRouting (Alpine) | 6.8.0-39-generic    |

### HouseB private network
This is the private network of HouseB. The zombie is reachable from external hosts thanks to port-forwarding.
| NAME         | ROLE   | IP          | OPEN PORTS    | OS           | Kernel |
|--------------|--------|-------------|---------------|--------------|--------|
| houseb-ubu12 | zombie | 192.168.2.3 | 8082          | Ubuntu 12.04 | 3.2    |
| houseb-ubu14 | victim | 192.168.2.4 |               | Ubuntu 14.04 | 3.13   |
| houseb-ubu16 | victim | 192.168.2.5 |               | Ubuntu 16.04 | 4.5    |
| houseb-ubu18 | victim | 192.168.2.6 |               | Ubuntu 18.04 | 4.15   |
| houseb-ubu20 | victim | 192.168.2.7 |               | Ubuntu 20.04 | 5.4    |
| houseb-ubu22 | victim | 192.168.2.8 |               | Ubuntu 22.04 | 5.15   |