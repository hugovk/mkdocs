import click
import mkdocs


@click.group()
def cli():
    pass


@cli.command(name="build")
def build():
    m = mkdocs.MkDocs()
    m.build()


@cli.command(name="serve")
def serve():
    m = mkdocs.MkDocs()
    m.serve()
