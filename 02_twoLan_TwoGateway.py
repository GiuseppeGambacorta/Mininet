from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from utils import *

class CustomTopo(Topo):
    def build(self):
        # Rete 1
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1', ip='10.0.1.2/24', defaultRoute='via 10.0.1.1')
        host2 = self.addHost('h2', ip='10.0.1.3/24', defaultRoute='via 10.0.1.1')
        self.addLink(host1, switch1)
        self.addLink(host2, switch1)

        # Rete 2 
        switch2 = self.addSwitch('s2')
        host3 = self.addHost('h3', ip='10.0.2.2/24', defaultRoute='via 10.0.2.1') 
        host4 = self.addHost('h4', ip='10.0.2.3/24', defaultRoute='via 10.0.2.1')
        self.addLink(host3, switch2)
        self.addLink(host4, switch2)

        # Gateway 1
        gateway1 = self.addHost('gw1', ip='10.0.1.1/24')
        self.addLink(switch1, gateway1)

        # Gateway 2
        gateway2 = self.addHost('gw2', ip='10.0.2.1/24')
        self.addLink(switch2, gateway2)

        # Link tra i due gateway
        self.addLink(gateway1, gateway2, intfName1='gw1-eth1', intfName2='gw2-eth1', params1={'ip': '10.0.0.1/30'}, params2={'ip': '10.0.0.2/30'})

def createNetwork():
    topo = CustomTopo()
    net = Mininet(topo=topo)
    
    info('*** Starting network\n')
    net.start()

    info('*** Configuring gateway routing\n')
    gateway1 = net.get('gw1')
    gateway2 = net.get('gw2')

    gateway1.cmd('sysctl -w net.ipv4.ip_forward=1')
    gateway2.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Configura il routing sui gateway
    gateway1.cmd('ip route add 10.0.2.0/24 via 10.0.0.2')
    gateway2.cmd('ip route add 10.0.1.0/24 via 10.0.0.1')

    info('*** Testing network connectivity\n')
    net.pingAll()
    print_graph(net, "network_graph")

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()