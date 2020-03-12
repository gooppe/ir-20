import click

from boosearch.index import index_json


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
    "--index", type=click.Path(), required=True, help="Output index file name"
)
@click.option(
    "--target_column",
    type=click.INT,
    default=3,
    help="Index of the indexed column in the json file",
)
@click.option(
    "--buffer_size", type=click.INT, default=10000, help="Indexation buffer size"
)
def index(data, index, target_collumn, buffer_size):
    """Build search index"""
    index_json(data, index, target_collumn, buffer_size)


@click.command()
@click.option(
    "--data",
    type=click.Path(exists=True, file_okay=True),
    required=True,
    help="Data file name",
)
@click.option(
    "--index",
    type=click.Path(exists=True, file_okay=True),
    required=True,
    help="Index file name",
)
@click.argument("query", type=click.STRING)
def search(data, index, query):
    """Search documents"""

    raise NotImplementedError


main.add_command(index)
main.add_command(search)