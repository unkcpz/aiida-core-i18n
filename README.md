# aiida-core i18n localization documentation

[![codecov](https://codecov.io/gh/unkcpz/aiida-core-i18n/branch/main/graph/badge.svg)](https://codecov.io/gh/unkcpz/aiida-core-i18n)

This is the repository serves for the localization of [aiida-core documentation](https://aiida.readthedocs.io/projects/aiida-core/en/latest/index.html).
You can also translate online at <https://www.transifex.com/aiidateam/aiida-core/dashboard/> and your changes will be reviewed as soon as possible.


## Contributing to the documentation localization through transifex

If you are familar with [AiiDA](https://www.aiida.net/) and want to contribute to the localization of its aiida-core documentation, 
simply go to <https://www.transifex.com/aiidateam/aiida-core/dashboard/> register a transifex account and start translaing there. 
All your change will be merged within days along with others translation work. 

Can't find your language? Please refer to the subsequent section and we will help you to add one.


## How to add support for a new language?

Now we have following language supported:

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
