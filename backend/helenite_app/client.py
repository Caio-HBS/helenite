from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def perform_search(query, **kwargs):
    client = get_client()
    results = results = client.multiple_queries(
    [
        {'indexName': 'Helenite_Profile', 'query': query},
        {'indexName': 'Helenite_Post', 'query': query}
    ]
    )
    return results
