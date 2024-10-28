import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

def print_graph(net, filename='network_graph.png'):
    G = nx.Graph()
    ip_mapping = {}

    # Add nodes and IP addresses
    for host in net.hosts:
        G.add_node(host.name)
        ip_mapping[host.name] = host.IP()  

    # Add links
    for link in net.links:
        G.add_edge(link.intf1.node.name, link.intf2.node.name)

    # Draw the graph with IP addresses as labels
    pos = nx.spring_layout(G)  # Use a spring layout
    labels = {host.name: f"{host.name}\n({ip_mapping[host.name]})" for host in net.hosts}
    
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold')

    # Save the graph to a file
    plt.savefig(filename)  # Change the filename if needed
    plt.clf()  # Clear the current figure to avoid overlaps
    print(f'*** Network graph saved as {filename}\n')
