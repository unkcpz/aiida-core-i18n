# AiiDA-l10n-zh_CN
[![Documentation Status](https://readthedocs.org/projects/aiida-core-zh-cn/badge/?version=latest)](https://aiida-core-zh-cn.readthedocs.io/zh_CN/latest/?badge=latest)

[Transifex](https://www.transifex.com/) is used as translation platform.
The workflow is described as following, to process the translation work of AiiDA documentation.

## Workflow for transifex translators

1. Login to transifex service.
2. Go to AiiDA documentation translation page.
3. Click Request language and fill form.
4. Wait acceptance by transifex AiiDA Docs translation maintainers.
5. (After acceptance) Translate on transifex.

## How to add a new localization to the documentation?

This repository is a template for how to add a new localization.

### 0. Create a github repository 'aiida-l10n-\<lang\>'

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

*make sure* not to include apidoc which should not be translated in `.tx/config`.

## Retrieve translated files from transifex

Translators can directly translate the documentation in transifex, enter from:
https://www.transifex.com/aiidateam/aiida-core/translate/#zh_CN

Every time when the maintainer of the i18n repository feels its a proper time to update the translated documentation, he can pull the translated `.po` file from transifex and update the documentation through sphinx-doc.

Getting the `.po` file from transifex platform:

```sh
tx pull -l <lang>
```

### 2. A new localization project is better to include the transltion style guid as following

## Chinese translation style guide(中文翻译指南)

```text
process: 例程。目的是区别linux的进程和广义的流程的概念，是AiiDA中一个特有的基础概念。
provenance: 可验证性。表示了数据和流程是可以重复并可以追踪来源过程的。
provenance graph: 可验证性图。AiiDA生成的有可验证性的图结构。
calculation: 算例。
calculation job: 算例任务。
calculation function: 算例函数。
workflow: 工作流。
workflow function: 工作流函数。
workchain: 工作链。

...
```

## When original documentation updated

UPDATE the source code:

```bash
$ sh update_source.sh
```
This will update the source code so that the API doc is always latest.
Meanwhile, this command will update the `requirements_for_rtd.txt` in order to sync the file with official repository.

The content in transfix will automatically updated by github action.
