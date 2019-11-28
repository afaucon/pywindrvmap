# drive list
# drive add G C:\data\ertms
# drive add G \\nafrayu\Volume_1
# drive remove G

import click
import logging
import windrvmap

@click.group()
@click.option('-v', '--verbose', type=click.IntRange(min=0, max=2), default=0)
def drive_cli(verbose):
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose == 2:
        logging.basicConfig(level=logging.DEBUG)

@drive_cli.command()
@click.option('--kind',
              type=click.Choice(['all', 'used', 'available', 'unused', 'netuse', 'subst', 'physical'], case_sensitive=False),
              default='all')
def list(kind):
    """
    Description to write
    """
    if kind == 'all':
        drives = windrvmap.Drives(windrvmap.ALL)
    if kind == 'used':
        drives = windrvmap.Drives(windrvmap.USED_ONLY)
    if kind == 'available' or kind == 'unused':
        drives = windrvmap.Drives(windrvmap.AVAILABLE_ONLY)
    if kind == 'netuse':
        drives = windrvmap.Drives(windrvmap.USED_BY_NETUSE_ONLY)
    if kind == 'subst':
        drives = windrvmap.Drives(windrvmap.USED_BY_SUBST_ONLY)
    if kind == 'physical':
        drives = windrvmap.Drives(windrvmap.PHYSICAL_ONLY)
    click.echo(str(drives))

@drive_cli.command()
@click.argument('drive_letter')
@click.argument('path')
def add(drive_letter, path):
    """
    Description to write
    """
    _, message = windrvmap.add(drive_letter, path)
    click.echo(message)

@drive_cli.command()
@click.argument('drive_letter')
def remove(drive_letter):
    """
    Description to write
    """
    _, message = windrvmap.remove(drive_letter)
    click.echo(message)


if __name__ == "__main__":
    drive_cli()  # pylint: disable=no-value-for-parameter; Reason: @click.command decorator edits the function parameters, but pylint does not know this since it does not run the code.