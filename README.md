# COL334 Assignment 1
Networks Assignment - Network Analysis

## Traceroute Script

- **Requirements** - Python 3.5+
- **Call Format** - _python traceroute.py \<destinationIP/hostname\>_
- **Options** - We have implemented the following options:  
    1. **-4** : enforces IPv4 addresses.   
        e.g. - python traceroute.py -4 www.google.com
    2. **-6** : enforces IPv6 addresses.  
    e.g. - python traceroute.py -6 www.google.com
    3. **-m** : Specify max hops to be taken while tracing. Default value is 30. Value must be between 0 and 255.  
    e.g. - python traceroute.py -m 255 www.google.com
    4. **-q** : Specify the number of packets to be sent while tracing. Default value if 3.  
    e.g. - python traceroute.py -q 5 www.google.com