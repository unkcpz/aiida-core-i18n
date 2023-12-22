# aiida-core documentation i18n (internationalization and localization)

[![codecov](https://codecov.io/gh/unkcpz/aiida-core-i18n/branch/main/graph/badge.svg)](https://codecov.io/gh/unkcpz/aiida-core-i18n)

| Language     | Build status |
| ----------- | ----------- |
| zh_CN (Simplified, China)    | [![Documentation Status](https://readthedocs.org/projects/aiida-core-zh-cn/badge/?version=latest)](https://aiida.readthedocs.io/projects/aiida-core/zh-cn/latest/?badge=latest)  |
| de (German Standard)   | [![Documentation Status](https://readthedocs.org/projects/aiida-core-de/badge/?version=latest)](https://aiida-core-de.readthedocs.io/de/latest/?badge=latest) |


This is the repository that serves for the localization of [aiida-core documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/index.html).
You can also translate online at <https://www.transifex.com/aiidateam/aiida-core/dashboard/> and your changes will be reviewed as soon as possible.


## Contributing to the documentation localization through transifex

If you are familiar with [AiiDA](https://www.aiida.net/) and want to contribute to the localization of its `aiida-core` documentation, 
simply go to <https://www.transifex.com/aiidateam/aiida-core/dashboard/> register a transifex account and start translating there. 
All your changes will be merged within days along with other translation work. 

Can't find your language? Please refer to the subsequent section and we will help you to add one.


## How to add support for a new language?

Now we have the following language supported:

- Chinese (Simplified) - zh_CN
- German - de

To add a new language for the documentation, please request a new language in transifex and open an [issue](https://github.com/unkcpz/aiida-core-i18n/issues/new/choose).

## How the automatic translation works in this repository?

This repository is for synchronization of the translation work from transifex to the aiida-core documentation.
It includes multiple actions to make the translation work automatic and easy to maintain.
The actions are:
- `dependabot.yml` (weekly): to automatically open PR when submodule `aiida-core` is updated.
- `ci-update-pot.yml` (when submodule `aiida-core` is updated): to update the sounce language (English) pot files and create a PR.
- `auto-translate.yml` (monthly or manually): to automatically translate the pot files to other languages and create a PR.
- `push-translate.yml` (when PR is merged): to push the reviewed automatic translation to the transifex and synchronize the metadata of pot files.

## How to test doc build locally

This is basically how we set readthedocs (RTD) to build the docs.

Clone the repo by and the `aiida-core` submodule.

```
git clone - https://github.com/unkcpz/aiida-core-i18n.git
cd aiida-core-i18n
```

Link the translations to the `aiida-core/docs/source`.

```
for lang in $(ls translations); do mkdir -p aiida-core/docs/source/locales/${lang}; done
for lang in $(ls translations); do ln -s -r translations/${lang} aiida-core/docs/source/locales/${lang}/LC_MESSAGES; done
```

Install the dependencies for the sphinx build and the `aiida-core` APIDOC build.

```
pip install -U -e "aiida-core[docs,tests,rest,atomic_tools]"
```

Build it! (Replace the language with the target language you want to build, currently only `zh_CN` and `de` are supported)

```
python -m sphinx -T -E -W --keep-going -b html -d _build/doctrees -D language=zh_CN aiida-core/docs/source/ _build/html
```

The html can be found in `_build` folder.

To clean up the build, you can run

```
# clean up _build
git clean -xfd

# clean up linked translations
cd aiida-core
git clean -xfd
```
