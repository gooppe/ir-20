import os

import click
from boosearch.embeddings import export_embeddings_json
from boosearch.index import index_json
from boosearch.search import cli_search


@click.group()
def main():
    pass


@click.command()
@click.option(
    "--data",
    type=click.Path(exists=True, file_okay=True),
    required=True,
    help="Input file name",
)
@click.option(
    "--dump",
    type=click.Path(),
    required=True,
    help="Output dump indexation folder",
)
@click.option(
    "--target_column",
    type=click.INT,
    default=3,
    help="Index of the indexed column in the json file",
)
@click.option(
    "--buffer_size",
    type=click.INT,
    default=10000,
    help="Indexation buffer size",
)
def index(data, dump, target_column, buffer_size):
    """Build search index"""
    os.makedirs(dump, exist_ok=True)

    index_filename = os.path.join(dump, "index.txt")
    index_json(data, index_filename, target_column, buffer_size)

    embeddings_filename = os.path.join(dump, "embeddings.pth")
    export_embeddings_json(data, embeddings_filename, target_column)


@click.command()
@click.option(
    "--data",
    type=click.Path(exists=True, file_okay=True),
    required=True,
    help="Data file name",
)
@click.option(
    "--dump",
    type=click.Path(exists=True, file_okay=True),
    required=True,
    help="Indexation dump folder",
)
@click.option(
    "--results", type=click.INT, default=5, help="Number of search results",
)
@click.argument("query", type=click.STRING)
def search(data, dump, results, query):
    """Search documents"""
    cli_search(query, dump, data, results)


main.add_command(index)
main.add_command(search)
