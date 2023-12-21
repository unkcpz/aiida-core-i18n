"""CLI command: to run the translation using click
"""
import click
import pathlib

from aiida_core_i18n import po_translate

@click.group()
def cli():
    """CLI command: to run the translation using click"""
    pass

@cli.command()
@click.option('--po', help='The po file to translate', required=True, type=click.Path(exists=True, path_type=pathlib.Path))
@click.option('--max-chars', help='The max characters to translate', default=500, type=int)
@click.option('--override', help='Override the existing translation', is_flag=True, default=False)
def translate(po: pathlib.Path, max_chars: int, override: bool):
    """Run the translation to the po file"""
    click.echo(f"Translate the file {po}")

    # read the file
    with open(po, "r") as fh:
        lines = fh.readlines()
        
    # translate the file
    translated_lines = po_translate(lines, max_chars=max_chars, override=override)
    print(translated_lines[0:50])

    # override original file
    with open(po, "w") as fh:
        fh.writelines(translated_lines)

@cli.command()
def status():
    """Show the status of the api translation limit"""
    import os
    import deepl

    DEEPL_TOKEN = os.environ.get("DEEPL_TOKEN")
    if DEEPL_TOKEN is None:
        click.echo("ERROR: Please set the DEEPL_TOKEN environment variable")
        return

    translator = deepl.Translator(DEEPL_TOKEN)
    
    usage = translator.get_usage()
    
    print(usage)



if __name__ == '__main__':
    cli()