import click
import logging
import windrvmap


@click.group(invoke_without_command=True)
@click.option('-v', '--verbose', type=click.IntRange(min=0, max=2), default=0)
@click.pass_context
def main(ctx, verbose):
    if verbose == 0:
        logging.basicConfig(level=logging.WARNING)
    if verbose == 1:
        logging.basicConfig(level=logging.INFO)
    if verbose == 2:
        logging.basicConfig(level=logging.DEBUG)
    
    if ctx.invoked_subcommand is None:
        drives_cfg = windrvmap.Config()
        click.echo(str(drives_cfg))
        
@main.command()
@click.argument('source')
@click.argument('destination')
def add(source, destination):
    """
    Description to write
    """
    drives_cfg = windrvmap.Config()
    _, message = drives_cfg.add(source, destination)
    click.echo(message)
        
@main.command()
@click.argument('source')
def remove(source):
    """
    Description to write
    """
    drives_cfg = windrvmap.Config()
    _, message = drives_cfg.remove(source)
    click.echo(message)
        
@main.command()
def apply():
    """
    Description to write
    """
    # Recovering the mapping
    configured_mapping = windrvmap.Config().mapping

    # Recovering the current mapping situration
    drives = windrvmap.Drives()

    # Trying to remap according to the configuration
    for drive_letter in configured_mapping:
        _, _ = drives.remove(drive_letter)
        _, _ = drives.add(drive_letter, configured_mapping[drive_letter])

    # Recovering the new mapping situration
    drives = windrvmap.Drives()

    # Detecting what succeeded and what failed
    success_mappings = {}
    failed_mappings = {}
    for drive_letter in configured_mapping:
        drive = drives.drive(drive_letter)
        if drive.is_shortcut() and drive.get_shortcut() == configured_mapping[drive_letter]:
            success_mappings[drive_letter] = drive.get_shortcut()
        else:
            failed_mappings[drive_letter] = configured_mapping[drive_letter]

    # Displaying the result for the user
    if len(list(success_mappings)) + len(list(failed_mappings)) == 0:
        click.echo('No mapping configured')
    else:
        if len(list(success_mappings)) > 0:
            click.echo('Applied mapping:')
            str2disp = ""
            for drive_letter in success_mappings:
                str2disp = str2disp + '{} --> {}\n'.format(drive_letter, success_mappings[drive_letter])
            click.echo(str2disp[:-1])
        if len(list(failed_mappings)) > 0:
            click.echo('Failed mapping:')
            str2disp = ""
            for drive_letter in failed_mappings:
                str2disp = str2disp + '{} --> {}\n'.format(drive_letter, failed_mappings[drive_letter])
            click.echo(str2disp[:-1])
   