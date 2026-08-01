import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402


def build_figure(raw_trans_to_sub, transformator_to_every, all_priority_queues, hour):
    """Draw the grid topology with the computed load on every substation-transformer line."""
    graph = nx.DiGraph()

    for transformer, substation in raw_trans_to_sub.items():
        graph.add_edge(substation, transformer)

    for transformer, consumers in transformator_to_every.items():
        for consumer in consumers:
            graph.add_edge(transformer, consumer)

    for weight, substation, transformer in all_priority_queues[hour]:
        graph[substation[0]][transformer]['weight'] = weight

    pos = nx.spring_layout(graph, seed=42, k=1.5, iterations=50)

    figure, ax = plt.subplots(figsize=(14, 9))

    node_colors = [
        '#f4a261' if node.startswith('transformer')
        else '#2a9d8f' if node.startswith('substation')
        else '#a8dadc'
        for node in graph.nodes()
    ]

    nx.draw_networkx_nodes(graph, pos, node_size=700, node_color=node_colors, edgecolors='black', ax=ax)
    nx.draw_networkx_edges(graph, pos, width=1, alpha=0.7, edge_color='grey', arrows=True, arrowsize=12, ax=ax)
    nx.draw_networkx_labels(graph, pos, font_size=9, font_weight='bold', ax=ax)

    edge_labels = {
        (source, target): f'{graph[source][target]["weight"]:.2f}'
        for source, target in graph.edges()
        if 'weight' in graph[source][target]
    }
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='#e63946', font_size=9, ax=ax)

    ax.set_title(f"Grid load at hour {hour}: substations, transformers and consumers", fontsize=14)
    ax.axis('off')
    figure.tight_layout()

    return figure


def visual(raw_trans_to_sub, transformator_to_every, all_priority_queues, hour):
    """Render the grid topology to a window (kept for standalone use)."""
    build_figure(raw_trans_to_sub, transformator_to_every, all_priority_queues, hour)
    plt.show()
