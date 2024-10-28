import networkx as nx
import matplotlib.pyplot as plt

def print_graph(net, filename='network_graph.png'):
    G = nx.Graph()

    # Add nodes and interfaces with IP addresses
    for host in net.hosts:
        G.add_node(host.name)
        interfaces = host.intfList()  # Get all interfaces of the host
        ip_labels = []
        
        # Create a string of all interfaces and their IPs
        for intf in interfaces:
            ip = intf.IP()
            ip_labels.append(f"{intf.name}: {ip}")  # Add the interface and the IP to the list
        # Use join to create a multiline label
        ip_label_str = "\n".join(ip_labels)
        
        # Set the label for the node, label is the key
        G.nodes[host.name]['label'] = f"{host.name}\n{ip_label_str}"

    # Add links
    for link in net.links:
        G.add_edge(link.intf1.node.name, link.intf2.node.name)

    # Draw the graph with labels
    pos = nx.spring_layout(G)  # Use a spring layout
    labels = {host.name: G.nodes[host.name]['label'] for host in net.hosts}
    
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold')

    # Save the graph to a file
    plt.savefig(filename)  # Change the filename if needed
    plt.clf()  # Clear the current figure to avoid overlaps
    print(f'*** Network graph saved as {filename}\n')
