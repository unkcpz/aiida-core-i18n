"""CLI command: to run the translation using click
"""
import click
import pathlib

from aiida_core_i18n import po_translate, get_env_deepl_token

@click.group(context_settings={"help_option_names": ["-h", "--help"]})
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
@click.option('-p', '--param', help='which information to show', type=click.Choice(['count', 'limit', 'verbose', 'avail']), default='verbose')
def status(param: str):
    """Show the status of the api translation limit"""
    from aiida_core_i18n import deepl_status

    try:
        click.echo(deepl_status(param))
    except ValueError as exc:
        click.echo(f"ERROR: {exc}")

@cli.command()
@click.argument('string', type=str)
@click.option('--target-lang', help='The target language', default='ZH', type=str)
@click.option('--post-processing/--no-post-processing', help='Do post processing', default=True, type=bool)
def deepl(string: str, target_lang: str, post_processing: bool):
    """Translate the string"""
    from aiida_core_i18n import translate
    
    # print the initial string
    click.echo(f"Input: \n\t{string}")

    # translate the string
    res = translate(string, target_lang=target_lang, post_processing=post_processing)
    click.echo(f"Output: \n\t{res}")
    

if __name__ == '__main__':
    cli()