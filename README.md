# aiida-core localized documentation

This is the repository serves for the localization of [aiida-core documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/index.html).

Contributions are highly welcome - see below.


## Contributing to the documentation localization through transifex

If you are familar with [AiiDA](https://www.aiida.net/) and would like to contribute to the translation of its documentation, simply

 * go to <https://www.transifex.com/aiidateam/aiida-core/dashboard/> 
 * register for a transifex account there
 * and start translaing. 

Your translations will be merged within days.

Can't find your language? See below.


## How to add support for a new language?

Currently, we support the following languages:

- Chinese(simplified)

To add a new language for the documentation, please request a new language in transifex and open an [issue](https://github.com/unkcpz/aiida-l10n-zh_CN/issues/new/choose).

## How does the localization process work?

The English source of the documentation is uploaded automatically to the transifex platform by 
a github action whenever a new version of aiida-core is released
(see [here](https://github.com/aiidateam/aiida-core/blob/develop/.github/workflows/post-release.yml) for how it works).

The transifex configuration in `.tx/config` maps the documentation to the translation files in this repository, which may need to be updated after a new release.

To do so, install the `transifex-client` by:

```bash
pip install transifex-client
```

To download the newly translated files from transifex:

```bash
tx pull --all
```

Then commit the changes and push to your fork of this repository github. 
The translated documentation is deployed by readthedocs once the `develop` branch of this repository is updated.

The version of the documentation does **NOT** correspond to the `latest` version of the English docs but the last released one i.e. the `stable` version.
This is controlled by the script to fetch the source docs (`aiida-core/docs/source/`) and the source code (for API documentation).
We only fetch the depth=1 branch by:

```bash
git clone --single-branch --branch "$tag" --depth 1 $REMOTE
```
