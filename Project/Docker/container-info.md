## Networks definiton
| NAME           | NETWORK IP      | IP RANGE | DESCRIPTION
| internet       | 172.0.0.0/24    | 
| web            | 172.0.254.0/24  | 172.0.254.1 - 172.0.254.254 |
| corpA          | 172.0.254.16/28 | 172.0.254.17 - 172.0.254.30 |
| corpB          | 172.0.254.32/28 | 172.0.254.33 - 172.0.254.46 |
| houseA         | 172.0.254.48/28 | 172.0.254.49 - 172.0.254.62 |
| houseA-private | 192.168.0.0/28  | 192.168.0.1 - 192.168.0.14  |
| houseB         | 172.0.254.64/28 | 172.0.254.65 - 172.0.254.78 |
| houseB-private | 192.168.0.0/28  | 192.168.0.1 - 192.168.0.14  |



| NETWORK         | NAME         | ROLE    | IP                                      | KERNEL         | OS                             | FIREWALL |
|-----------------|--------------|---------|-----------------------------------------|----------------|--------------------------------|----------|
| **web 172.0.254.0/24** |              |         |                                         |                |                                |          |
|                 | main-router  | router  | ETH0: 172.0.254.254 (main-network)       | 6.8.0-39-generic | FRRouting (based on Alpine)   | No       |
|                 |              |         | ETH1: 172.0.0.254 (internet)             |                |                                |          |
|                 | attacker     | attacker| 172.0.254.200                            | 5.15           | Ubuntu 22.04                   | No       |
| **corpA 172.0.1.0/24** |              |         |                                         |                |                                |          |
|                 | sub1-router  | router  | ETH0: 172.0.254.5 (main-network)         | 6.8.0-39-generic | FRRouting (based on Alpine)   | No       |
|                 |              |         | ETH1: 172.0.1.100 (subnet1)              |                |                                |          |
|                 | sub1-ubu12   | zombie  | 172.0.1.12                               | 3.2+           | Ubuntu 12.04                  | No       |
|                 | sub1-ubu14   | victim  | 172.0.1.14                               | 3.13           | Ubuntu 14.04                  | No       |
|                 | sub1-ubu16   | victim  | 172.0.1.16                               | 4.8            | Ubuntu 16.04                  | No       |
|                 | sub1-ubu18   | victim  | 172.0.1.18                               | 4.18           | Ubuntu 18.04                  | No       |
|                 | sub1-ubu20   | victim  | 172.0.1.20                               | 5.4            | Ubuntu 20.04                  | No       |
|                 | sub1-ubu22   | victim  | 172.0.1.22                               | 5.15           | Ubuntu 22.04                  | No       |
| **corpB 172.0.2.0/24** |              |         |                                         |                |                                |          |
|                 | sub2-router  | router  | ETH0: 172.0.254.2 (main-network)         | 6.8.0-39-generic | FRRouting (based on Alpine)   | Yes      |
|                 |              |         | ETH1: 172.0.2.100 (subnet2)              |                |                                |          |
|                 | sub2-ubu12   | zombie  | 172.0.2.12                               | 3.2+           | Ubuntu 12.04                  | No       |
|                 | sub2-ubu14   | victim  | 172.0.2.14                               | 3.13           | Ubuntu 14.04                  | No       |
|                 | sub2-ubu16   | victim  | 172.0.2.16                               | 4.8            | Ubuntu 16.04                  | No       |
|                 | sub2-ubu18   | victim  | 172.0.2.18                               | 4.18           | Ubuntu 18.04                  | No       |
|                 | sub2-ubu20   | victim  | 172.0.2.20                               | 5.4            | Ubuntu 20.04                  | No       |
|                 | sub2-ubu22   | victim  | 172.0.2.22                               | 5.15           | Ubuntu 22.04                  | No       |
