# aiida-core localized documentation

This is the repository serves for the localization of [aiida-core documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/index.html).
You can also translate online at <https://www.transifex.com/aiidateam/aiida-core/dashboard/> and your changes will be merged within days.

The 

## Contributing to the documentation localization through transifex

If you are familar with [AiiDA](https://www.aiida.net/) and want to contribute to the localization of its aiida-core documentation, 
simply go to <https://www.transifex.com/aiidateam/aiida-core/dashboard/> register a transifex account and start translaing there. 
All your change will be merged within days along with others translation work. 

Can't find your language? Please refer to the subsequent section and we will help you to add one.

## How this localization process works?

The source of documentation (english) will automatically upload to the transifex by 
a github action (check https://github.com/aiidateam/aiida-core/blob/develop/.github/workflows/post-release.yml if you are interested in how it works) when the new version release. 
The transifex configuration in `.tx/config` is set to map to the translated files for which should be update in the repository.
All you required is `transifex-client`, you can install it by:

```bash
pip install transifex-client
```

To download the newly translated files from transifex:

```bash
tx pull --all
```

The remote transifex contains the po files from the latest branch of `aiida-core` doc.

Update the submodule `aiida-core` repo so the latest API doc will match with the latest branch of `aiida-core` (a bug in aiida-core `post-release` workflow that the it is not checkout to the latest commit of the `main` branch).

```bash
git submodule update --remote
```

Push to the remote repo and `ReadTheDocs` will compile the doc automatically.

## How to add support for a new language?

Now we have following language supported:

- Chinese(simplified)

To add a new language for the documentation, please request a new language in transifex and open an [issue](https://github.com/unkcpz/aiida-l10n-zh_CN/issues/new/choose).


### New 

- auto update .tx/config and open PR.