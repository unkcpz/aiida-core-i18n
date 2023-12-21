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
@click.argument('po', type=click.Path(exists=True, path_type=pathlib.Path))
@click.option('--max-chars', help='The max characters to translate', default=500, type=int)
@click.option('--override-translation', help='Override the existing translation', is_flag=True, default=False)
@click.option('--override-file', help='Override the existing file', is_flag=True, default=False)
def translate(po: pathlib.Path, max_chars: int, override_translation: bool, override_file: bool):
    """Run the translation to the po file"""
    click.echo(f"Translate the file {po}")

    # read the file
    with open(po, "r") as fh:
        lines = fh.readlines()
        
    # translate the file
    try:
        translated_lines = po_translate(lines, max_chars=max_chars, override=override_translation)
    except RuntimeError:
        click.echo("ERROR: Please set the correct DEEPL_TOKEN environment variable")
        return
    
    # override original file
    out_po = po if override_file else po.with_suffix(".zh.po")
    with open(out_po, "w") as fh:
        fh.write("\n".join(translated_lines))

    click.echo("Done")

@cli.command()
@click.option('-p', '--param', help='which information to show', type=click.Choice(['count', 'limit', 'verbose', 'valiable']), default='verbose')
def status(param: str):
    """Show the status of the api translation limit"""
    import os
    import deepl

    DEEPL_TOKEN = os.environ.get("DEEPL_TOKEN")
    if DEEPL_TOKEN is None:
        click.echo("ERROR: Please set the DEEPL_TOKEN environment variable")
        return

    translator = deepl.Translator(DEEPL_TOKEN)
    
    usage = translator.get_usage()

    if param == 'verbose':
        click.echo(usage)
    elif param == 'count':
        click.echo(usage.character.count)
    elif param == 'limit':
        click.echo(usage.character.limit)
    elif param == 'valiable':
        click.echo(usage.character.limit - usage.character.count)
    
    



if __name__ == '__main__':
    cli()