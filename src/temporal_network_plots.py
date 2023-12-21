import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import itertools
import matplotlib.cm as cm
import glob 
import os
import matplotlib as mpl
import umap

def embeddings_to2d(embedding_df):
    """
    input:
    info_embedding_df:  pandas df containing embeddings for each topic in column 'topic_embeddings'
                        and topic label in column "Topic"

    output:
    dictionary mapping topic nr to [x, y] position
    """

    embeddings = np.array(embedding_df['topic_embeddings'])
    embeddings = np.vstack(embeddings[:])
    reducer = umap.UMAP()
    embedding_2d = reducer.fit_transform(embeddings)
    topic_to_position = dict(zip(embedding_df['Topic'], embedding_2d))

    return topic_to_position

def create_temporal_network(trajectory, timestamps, topic_to_pos):
    """
    input: 
    trajectory:         list of visited topics
    timestamps:         list of timestaps corresponding to each topic visit
    topic_to_pos:       dictionary mapping topic nrs to [x, y] positions

    output: temporal network plot

    """

    #make colormap for edges
    norm = mpl.colors.Normalize(vmin=min(timestamps), vmax=max(timestamps))
    cmap = cm.viridis
    m = cm.ScalarMappable(norm=norm, cmap=cmap)
    edge_colours = m.to_rgba(timestamps)
    
    G = nx.MultiDiGraph()
    for topic in np.unique(trajectory):
        G.add_node(topic, position = topic_to_pos[topic])

    for i, (u, v) in enumerate(itertools.pairwise(trajectory)):
        G.add_edge(u, v, colour = edge_colours[i + 1])

    nx.draw(G, pos = nx.get_node_attributes(G, 'position'),
            edge_color = list(nx.get_edge_attributes(G, 'colour').values()),
            node_size = 10, connectionstyle="arc3")
    plt.show()