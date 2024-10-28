import matplotlib.pyplot as plt
import networkx as nx

def print_graph(net, filename='network_graph.png'):
    G = nx.Graph()
    ip_mapping = {}

    # Aggiungi nodi e indirizzi IP
    for host in net.hosts:
        G.add_node(host.name)
        ip_mapping[host.name] = host.IP()  # Mappa l'host all'IP

    # Aggiungi i collegamenti
    for link in net.links:
        G.add_edge(link.intf1.node.name, link.intf2.node.name)

    # Disegna il grafo con indirizzi IP come etichette
    pos = nx.spring_layout(G)  # Usa un layout a molla
    labels = {host.name: f"{host.name}\n({ip_mapping[host.name]})" for host in net.hosts}
    
    nx.draw(G, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=2000, font_size=10, font_color='black', font_weight='bold')

    # Salva il grafo in un file
    plt.savefig(filename)  # Cambia il nome del file se necessario
    plt.clf()  # Pulisce la figura corrente per evitare sovrapposizioni
    print(f'*** Network graph saved as {filename}\n')
