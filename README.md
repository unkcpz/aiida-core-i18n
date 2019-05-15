# AiiDA-l10n-zh_CN
[![Documentation Status](https://readthedocs.org/projects/aiida-l10n-zh_CN/badge/?version=latest)](https://aiida-l10n-zh_CN.readthedocs.io/zh_CN/latest/?badge=latest)

[Transifex](https://www.transifex.com/) is used as translation platform.
The workflow is described as following, to process the translation work of AiiDA documentation.

## Workflow for transifex maintainers

### 0. push `pot` files to transifex

In `aiida_core/docs/` directory,
generate `pot` files:

```sh
$ make gettext
```

Creating `.tx/config` file:

```sh
$ tx init --no-interactive
$ sphinx-intl update-txconfig-resources --pot-dir build/locale --transifex-project-name aiida-documentation
```

*make sure* not to include apidoc which should not be translated in `.tx/config`. (manually remove these lines?)

```sh
$ tx push -s
```

### 1. When docs of source language update

If `.tx/config` is going to be reset to track new `pot` files, runing:

```sh
$ make gettext
$ sphinx-intl update-txconfig-resources --pot-dir build/locale --transifex-project-name aiida-documentation
$ tx push -s
```

*make sure* not to include apidoc which should not be translated in `.tx/config`. (manually remove these lines?)

## Workflow for transifex translators

1. Login to transifex service.
2. Go to AiiDA documentation translation page.
3. Click Request language and fill form.
4. Wait acceptance by transifex AiiDA Docs translation maintainers.
5. (After acceptance) Translate on transifex.

## How to add a new localization to the documentation?

This repository is a template for how to add a new localization.

### 0. Create a github repository 'aiida-l10n-<lang>'

The source code of documentation comes from aiida_core.
Therefore, submodule the `aiida_core` in the new created repository.

```sh
$ git submodule add "https://github.com/aiidateam/aiida_core.git"
$ git submodule init
$ git submodule update
```

You can update submodule by running:

```sh
git submodule foreach git pull
```

The submodule is just a pointer to a particular commit of the submodule's repository. To point to a latest version refer to [Git submodules: Specify a branch/tag](https://stackoverflow.com/questions/1777854/how-can-i-specify-a-branch-tag-when-adding-a-git-submodule). Running:

```sh
aiida-l10n-<lang> $ cd aiida_core
aiida_core $ git checkout develop
aiida_core $ cd ..
aiida-l10n-<lang> $ git add .
aiida-l10n-<lang> $ git commit -m "moved aiida_core to develop"
aiida-l10n-<lang> > git push
```

Copy the source code of docs to current project. Every time when official documentation update, do this to track the latest docs code.

```sh
$ cp -R aiida_core/docs/source ./
```

Because the folder structure is changed, the `conf.py` need to be replaced by conf.py.tmpl:

```sh
cp conf.py.tmpl source/conf.py
```

Creating `.tx/config` file (used for `tx pull`):

```sh
$ tx init --no-interactive
$ sphinx-intl update-txconfig-resources --pot-dir build/locale --transifex-project-name aiida-documentation
```

*make sure* not to include apidoc which should not be translated in `.tx/config`. (manually remove these lines?)

### 1. Request language in transifex

https://www.transifex.com/aiidateam/aiida-documentation/languages/

Getting the `.po` file from transifex platform:

```sh
tx pull -l <lang>
```

### 2. A new localization project is better to include the transltion style guid as following

## Chinese translation style guide(中文翻译指南)
