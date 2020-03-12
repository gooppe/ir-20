import click


@click.group()
def main():
    pass


@click.command()
@click.option(
    "--it", type=click.Choice(["json"]), default="json", help="Input data type"
)
@click.option(
    "--input", type=click.Path(exists=True), required=True, help="Input file name"
)
@click.option(
    "--output", type=click.Path(), required=True, help="Output index file name"
)
def index(it, input, output):
    """Build search index"""

    raise NotImplementedError


@click.command()
@click.argument("index_file", type=click.Path(exists=True, file_okay=True))
@click.argument("query", type=click.STRING)
def search(index_file, query):
    """Search documents"""

    raise NotImplementedError


main.add_command(index)
main.add_command(search)
