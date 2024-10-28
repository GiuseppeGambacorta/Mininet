from mininet.net import Mininet
from mininet.topo import Topo
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from utils import *





def createNetwork():
    topo = CustomTopo(n=3)
    net = Mininet(topo=topo)
    
    info('*** Starting network\n')
    net.start()

    info('*** Assigning IP addresses\n')
    net.get('h1').setIP('10.0.0.1/24')
    net.get('h2').setIP('10.0.0.2/24')
    net.get('h3').setIP('10.0.0.3/24')
    
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