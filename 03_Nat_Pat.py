from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info

class CustomTopo(Topo):
    def build(self):

        # Create the switch
        switch1 = self.addSwitch('s1')

        # Create hosts in the first subnet
        host1 = self.addHost('h1', ip='10.0.1.2/24', defaultRoute='via 10.0.1.1')
        host2 = self.addHost('h2', ip='10.0.1.3/24', defaultRoute='via 10.0.1.1')
        host3 = self.addHost('h3', ip='10.0.1.4/24', defaultRoute='via 10.0.1.1')
        
        # Link hosts to switch
        self.addLink(host1, switch1)
        self.addLink(host2, switch1)
        self.addLink(host3, switch1)

        # Create the gateway with two interfaces
        gateway = self.addHost('gw', ip='10.0.1.1/24')  # Interface for the local subnet
        self.addLink(switch1, gateway)

        # Link for the second subnet
        hostWeb = self.addHost('HostWeb', ip='203.0.113.2/24', defaultRoute='via 203.0.113.1') 
        self.addLink(gateway, hostWeb, intfName1='gw-eth1', intfName2='HostWeb-eth0', params1={'ip': '203.0.113.1/24'})

       
def createNetwork():
    topo = CustomTopo()
    net = Mininet(topo=topo)
    
    info('*** Starting network\n')
    net.start()

    info('*** Configuring gateway routing\n')
    gateway = net.get('gw')
    
 
    # Configure the NAT rules
    # Allow traffic from the 10.0.1.0 subnet to be translated to 203.0.113.0
    gateway.cmd('iptables -t nat -A POSTROUTING -s 10.0.1.0/24 -o gw-eth1 -j SNAT --to-source 203.0.113.0')
    
    # Allow related and established connections
    gateway.cmd('iptables -A FORWARD -m state --state RELATED,ESTABLISHED -j ACCEPT')
    gateway.cmd('iptables -A FORWARD -s 10.0.1.0/24 -o gw-eth1 -j ACCEPT')


    info('*** Testing network connectivity\n')

 

    info('*** Running CLI\n')
    CLI(net)

    info('*** Stopping network\n')
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    createNetwork()