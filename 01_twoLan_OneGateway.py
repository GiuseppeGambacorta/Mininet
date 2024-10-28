from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from utils import *


class CustomTopo(Topo):
    def build(self):
    
        switch1 = self.addSwitch('s1')
        host1 = self.addHost('h1', ip='10.0.0.1/24', defaultRoute='via 10.0.0.254')
        host2 = self.addHost('h2', ip='10.0.0.2/24', defaultRoute='via 10.0.0.254')
        self.addLink(host1, switch1)
        self.addLink(host2, switch1)

      
        switch2 = self.addSwitch('s2')
        host3 = self.addHost('h3', ip='10.0.1.1/24', defaultRoute='via 10.0.1.254')
        host4 = self.addHost('h4', ip='10.0.1.2/24', defaultRoute='via 10.0.1.254')
        self.addLink(host3, switch2)
        self.addLink(host4, switch2)

     
        gateway = self.addHost('gw')
        self.addLink(switch1, gateway)  
        self.addLink(switch2, gateway)  


def createNetwork():
    topo = CustomTopo()
    net = Mininet(topo=topo)
    
    info('*** Starting network\n')
    net.start()


    gateway = net.get('gw')
    
    gateway.cmd('ifconfig gw-eth0 10.0.0.254/24')
    gateway.cmd('ifconfig gw-eth1 10.0.1.254/24')
    gateway.cmd('sysctl -w net.ipv4.ip_forward=1')

    
    info('*** Testing network connectivity\n')
    net.pingAll()


    print_graph(net,"network_graph")
    
    info('*** Running CLI\n')
    CLI(net)

   
    
    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()