#!/usr/bin/env python
# -----------------------------------------------------------------------------
# {ZmFudG9tSA==: "Open the vault of knowledge"}
# -----------------------------------------------------------------------------
# filename    : IPaddr.py
# created on  : 2020-07-11 14:22:01 UTC
# updated on  : 2020-07-16 00:55:42 UTC
# description : IP addressing
# dependencies: python3
# -----------------------------------------------------------------------------

import sys

class IPaddr:
    def __init__(self, ip):
        self.ip = ip.split('/')[0]
        self.cidr = int(ip.split('/')[-1])
        self.ip_lst = [x for x in self.ip.split('.')]

    #[λ] IP => Binary
    def ip2bin(self):
        '''
        Returns:
            List of 4 octets of the IP address in binary form.
        '''
        ip_bin_lst = [format(int(item), '08b') for item in self.ip_lst]
        # print(f'ip_bin_lst is {ip_bin_lst}')
        return ip_bin_lst

    @property
    def ip_bin(self):
        '''
        Returns:
            String of the IP address in binary form. 
        '''
        ip_bin = '.'.join([str(x) for x in self.ip2bin()])
        # print(f'ip_bin is {ip_bin}')
        return ip_bin

    #[λ] CIDR + submask
    def cidr2submask(self):
        '''
        Returns:
            String representing the submask, without dot notation.

        Usage:
            For further submask manipulation.
        '''
        sub = ''
        for i in range (self.cidr):
            sub = sub + '1'
        for i in range(32-self.cidr):
            sub = sub + '0'
        return sub

    @property
    def host_bits(self, sub=None):
        '''
        Returns:
            Integer representing the host bits of the submask.
        '''
        sub = self.cidr2submask()
        return sub.count('0')

    def submask2bin(self):
        '''
        Returns:
            List of 4 octets of the submask in binary form.
        '''
        sub = self.cidr2submask()
        submask_bin_lst = [sub[i:i + 8] for i in range(0, len(sub), 8)]
        # print(f'submask_bin_lst is {submask_bin_lst}')
        return submask_bin_lst

    @property
    def submask_bin(self):
        '''
        Returns:
            String of submask in binary form.
        '''
        submask_bin = '.'.join(self.submask2bin())
        return submask_bin

    def submask2dec(self):
        '''
        Returns:
            List of submask in decimal form.
        '''
        submask_lst = [int(i, 2) for i in self.submask2bin()]
        # print(f'submask_lst is {submask_lst}')
        return submask_lst

    @property
    def submask(self):
        '''
        Returns:
            String of submask in decimal form.
        '''
        submask = '.'.join([str(x) for x in self.submask2dec()])
        # print(f'submask is {submask}')
        return submask

    #[λ] Magic number and interesting octet.
    def _magic_num(self):
        '''
        Returns:
             Tuple containing the interesting octet and the magic number.
        '''

        for idx, octet in reversed(list(enumerate(self.submask2dec()))):
            if octet != 0:
                return (idx, 256 - octet)

    def _range_octet(self):

        idx, interesting_octet = self._magic_num()
        lower = [x for x in range(0, int(self.ip_lst[idx]) + 1, interesting_octet)][-1]
        upper = lower + interesting_octet - 1
        return (lower, upper)

    #[λ] Network ID
    def network_id_lst(self):
        '''
        Returns:
            Network ID as a list.
        '''
        network_id_lst = self.ip_lst.copy()
        interesting_octet = self._magic_num()[0]
        network_id_lst[interesting_octet] = self._range_octet()[0]
        for o in range(interesting_octet + 1, 4):
            network_id_lst[o] = 0
        # print(f'network_id_lst is {network_id_lst}')
        return network_id_lst

    @property
    def network(self):
        '''
        Returns:
            String of the Network ID.
        '''
        network = '.'.join(str(x) for x in self.network_id_lst())        
        return network

    #[λ] Broadcast ID
    def broadcast_id_lst(self):
        '''
        Returns:
            Broadcast ID as a list.
        '''
        broadcast_id_lst = self.ip_lst.copy()
        interesting_octet = self._magic_num()[0]
        broadcast_id_lst[interesting_octet] = self._range_octet()[1]
        for o in range(interesting_octet + 1, 4):
            broadcast_id_lst[o] = 255
        return broadcast_id_lst

    @property
    def broadcast(self):
        '''
        Returns:
            Broadcast ID as a string.
        '''
        broadcast = '.'.join(str(x) for x in self.broadcast_id_lst())
        return broadcast

    #[λ] Useful Hosts
    def useful_hosts(self):
        return (2 ** self.host_bits) - 2

    def info(self):
        '''
        Returns:
            Display multiple information retrieved from the IP address.
        '''
        print(f"{'IP address ':.<20} {self.ip}/{self.cidr}")
        print(f"{'IP (binary) ':.<20} {self.ip_bin}")
        print()
        print(f"{'Submask ':.<20} {self.submask}")
        print(f"{'Submask (binary) ':.<20} {self.submask_bin}")
        print(f"{'Network/Host bits ':.<20} {self.cidr}/{self.host_bits}")
        print()
        print(f"{'Network ID ':.<20} {self.network}")
        print(f"{'Broadcast ID ':.<20} {self.broadcast}")
        print(f"{'Useful Hosts ':.<20} {self.useful_hosts()}")

def main():
    if len(sys.argv) == 2:
        ip = sys.argv[1]
        net = IPaddr(ip)
        net.info()
    else:
        print('[λ] Usage:\n    IPaddr.py <ip address/cidr>\n    ex: IPaddr.py 192.168.0.1/24')
        sys.exit(1)
        
if __name__ == "__main__":
    # net = IPaddr('172.16.16.0/22')
    # net = IPaddr('150.150.0.0/30')
    # net = IPaddr('192.168.0.68/26')
    # net = IPaddr('192.168.0.68/24')
    # net = IPaddr('10.42.37.45/22')
    # net.info()
    main()

# ZmluOmZpbGU=
