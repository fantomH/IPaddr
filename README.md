# IPaddr
A simple python script to display IP, network ID, broadcast ID and subnetmask information.

Did this as a learning exercise will studying network IP addressing.

## Steps to find information manually
Given an IP, for example 10.42.37.12/22, we first need to find the submask in binary.

The submask can be calculated by adding as many 1 as the CIDR notation number and completing the 32 bits with 0.

In our example, submask is 11111111  11111111  11111100  00000000, which is 255,255,252,0 in dot notation.

The interesting octet would be the third one (252).

Finding the Network ID and Broadcast can be achieve by getting the magic number like so: 256 - 252 = 4.

Create a list starting with the magic number, adding the magic number until pass the number representing the interesting octet of the IP address (in our case 37): 4, 8, 12, 16, 20, 24, 28, 32, 36, 40.

The netwokd ID will be obtained by changing the interesting octet of the IP address by the second to last number of our list (36) and the next octets by 0.

The broadcast ID is given by modifying the interesting octet of the IP address with the last number of the list -1 and filling the next octets by 255.

Finally, the usable IPs are calculated by multiplying the magic number and the next octets (in our example 4 * 256) - 2, since the first and last IPs are reserved for the Network and the Broadcast.

In summary:
```
                    10.42.37.12/22
submask is 1111 1111  1111 1111  1111 1100  0000 0000
              255        255        252         0
                                256 - 252 =4
        4, 8, 12, 16, 20, 24, 28, 32, 36, 40
                                      ------
10 bits = 1022 usable IPs
NETWORK: 10.42.36.0
BROADCAST: 10.42.39.255
```

## Using IPaddr.py
In the terminal simply provide an IP address with the CIDR suffix.

```
$ python IPaddr.py 192.168.0.1/24
IP address ......... 192.168.0.1/24
IP (binary) ........ 11000000.10101000.00000000.00000001

Submask ............ 255.255.255.0
Submask (binary) ... 11111111.11111111.11111111.00000000
Network/Host bits .. 24/8

Network ID ......... 192.168.0.0
Broadcast ID ....... 192.168.0.255
Useful Hosts ....... 254
```

## Requirements and Portability
I wrote IPaddr.py using Python 3.8, but uses basic functions, so should work fine on older versions.
For the same reason, it worked as intended on Linux and Windows.
