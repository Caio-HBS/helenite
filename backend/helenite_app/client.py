from algoliasearch_django import algolia_engine


def get_client():
    """
    Returns the Algolia-Django built-in client.
    """

    return algolia_engine.client


def get_index(index_name):
    """
    Initializes the specified index on the Algolia servers.

    Args:
        - index_name: the name of the index as specified when indexing new models.
    """

    client = get_client()
    index = client.init_index(index_name)
    return index


def perform_search(query, index="Helenite_Profile", **kwargs):
    """
    Reaches for the Algolia servers for the perform the actual serach.

    Args:
        - query: the query specified by the user;
        - index: the index specified by the user (defaults to "Helenite_Profile").
    """

    index = get_index(index)
    results = index.search(query)
    return results
