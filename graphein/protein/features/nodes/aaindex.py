from typing import Dict, Tuple

import networkx as nx

from graphein.utils import import_message, protein_letters_3to1_all_caps

try:
    from pyaaisc import Aaindex
except ImportError:
    import_message(
        submodule="graphein.protein.features.nodes.aaindex",
        package="pyaaisc",
        pip_install=True,
    )


def fetch_AAIndex(accession: str) -> Tuple[str, Dict[str, float]]:
    """
    Fetches AAindex1 dictionary from an accession code. The dictionary maps one-letter AA codes to float values

    :param accession: Aaindex1 accession code
    :return: tuple of record titel(str) and dictionary of AA:value mappings
    """
    # Initialise AAindex object and get data
    aaindex = Aaindex()
    record = aaindex.get(accession)

    return record.title, record.index_data


def aaindex1(G: nx.Graph, accession: str) -> nx.Graph:
    """Adds AAIndex1 datavalues for a given accession as node features.
    :param G: nx.Graph protein structure graphein to featurise
    :param accession: AAIndex1 accession code for values to use
    :return: Protein Structure graph with AAindex1 node features added
    """

    title, index_data = fetch_AAIndex(accession)

    # TODO: change to allow for a list of all accession numbers?
    G.graph["aaindex1"] = accession + ": " + title

    if G.graph["config"].granularity == "atom":
        raise NameError(
            "AAIndex features cannot be added to atom granularity graph"
        )

    for n in G.nodes:
        residue = n.split(":")[1]
        residue = protein_letters_3to1_all_caps(residue)

        aaindex = index_data[residue]

        G.nodes[n][f"aaindex1_{accession}"] = aaindex

    return G
