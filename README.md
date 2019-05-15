# AiiDA-l10n
[![Documentation Status](https://readthedocs.org/projects/aiida-zh-cn/badge/?version=latest)](https://aiida-zh-cn.readthedocs.io/zh_CN/latest/?badge=latest)

`--recursive` make sure the submodule `aiida_core` is included.
clone this repository by:

```sh
git clone https://github.com/unkcpz/aiida-l10n-zh.git --recursive
# update submodule to latest one
git submodule foreach git pull
```

```sh
pip install "aiida_core[dev,testing]"
```

```sh
verdi quicksetup
```

```sh
make html
```

To build the documentation in sphinx, from this folder

```sh
  make html
```

This generates a html documentation tree under docs/build/html

You can browse to docs/build/html/index.html to see the documentation
in html format.

.. note:: However, that this requires to have AiiDA already installed
  on your computer (and sphinx installed, too).

  If you received a distribution file, you should already find
  the compiled documentation in docs/build/html/index.html.

.. note:: for a nicer html format, install the Read The Docs theme,

```sh
    sudo pip install sphinx_rtd_theme
```
