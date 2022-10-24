# PySprida

This repository contains a tool to distribute classes to the teacher depending on their preferences and requirements

> If you want to add something to this repo, please submit a PR. Contributions are very welcome.

## How to install (by source)
### Install git
Download and install [Git](https://git-scm.com/downloads) over the installer or your package repository.
### Python environment
Set up a working python environment. [Miniconda](https://docs.conda.io/en/latest/miniconda.html) is the recommended way to create a python environment.

After installing miniconda create an environment:
`conda create --name pySprida`

> For windows users: Open the anaconda prompt to be able to execute commands

Activate an enviroment with:
`conda activate pySprida`

Download the source with: `git clone https://github.com/pbnl/pySprida.git`.
You can update the code by navigating to the repository root and execute `git pull`.

Execute `python -m pip install -r ./requirements.txt` in the project root to install the dependencies.
## How to use
After you have activated the correct environment execute `python main.py` in the project root.
