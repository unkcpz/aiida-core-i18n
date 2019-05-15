# AiiDA-l10n

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
