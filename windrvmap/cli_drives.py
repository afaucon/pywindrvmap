import click
import logging
import windrvmap


@click.group(invoke_without_command=True)
@click.option('-v', '--verbose', type=click.IntRange(min=0, max=2), default=0)
@click.option('--kind',
              type=click.Choice(['all', 'used', 'available', 'unused', 'physical', 'shortcut', 'network', 'local'], case_sensitive=False),
              default='all')
@click.pass_context
def main(ctx, verbose, kind):
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose == 2:
        logging.basicConfig(level=logging.DEBUG)
    
    if ctx.invoked_subcommand is None:
        drives = windrvmap.Drives()
        if kind == 'all':
            click.echo(drives.string_representation(windrvmap.ALL))
        if kind == 'used':
            click.echo(drives.string_representation(windrvmap.USED))
        if kind == 'available' or kind == 'unused':
            click.echo(drives.string_representation(windrvmap.AVAILABLE))
        if kind == 'physical':
            click.echo(drives.string_representation(windrvmap.PHYSICAL))
        if kind == 'shortcut':
            click.echo(drives.string_representation(windrvmap.SHORTCUT))
        if kind == 'network':
            click.echo(drives.string_representation(windrvmap.NETWORK_SHORTCUT))
        if kind == 'local':
            click.echo(drives.string_representation(windrvmap.LOCAL_SHORTCUT))

@main.command()
@click.argument('drive_letter')
@click.argument('path')
def add(drive_letter, path):
    """
    Description to write
    """
    drives = windrvmap.Drives()

    status, message = drives.add(drive_letter, path)
    click.echo(message)

    if status == 'Success':
        config = windrvmap.Config()
        
        _, message = config.add(drive_letter, path)
        click.echo(message)

@main.command()
@click.argument('drive_letter')
def remove(drive_letter):
    """
    Description to write
    """
    drives = windrvmap.Drives()
    status, message = drives.remove(drive_letter)
    click.echo(message)

    if status == 'Success':
        config = windrvmap.Config()
        
        _, message = config.remove(drive_letter)
        click.echo(message)