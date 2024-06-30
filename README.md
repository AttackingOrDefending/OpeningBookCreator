# Opening Book Creator

Chess build tool for filtering PGN files and building polyglot books.

# Installation

## Cloning the project

Open the Miniconda console and clone the project:

`git clone https://github.com/AttackingOrDefending/OpeningBookCreator`

Cd into the cloned folder:

`cd OpeningBookCreator`

## Creating virtual env

Install virtualenv:

`pip install virtualenv`

Create virtual env:

`python -m venv venv`

Activate virtual env:

`venv\Scripts\activate`

## Installing project dependencies

Install project dependencies:

`pip install -r requirements.txt`

# Usage

First run the program with the `-h` switch to display help:

`python create.py -h`

## Create build environment

Create a build environment for a variant (example will use variant antichess):

`python create.py -e antichess --variant antichess`

The `-e` swith's `antcihess` is arbitrary name for the build environment, could be `foo` as well. The `--variant` swith's `antcihess` should be a proper lichess variant key.

This will create a directory structure:

```
envs
  antichess
    zip
    source
    filtered
    book
    config.yml
    filter_logic.py    
```

File `filter_logic.py` is a python code snippet that has access to the [`BasePgnVisitor`](https://github.com/AttackingOrDefending/OpeningBookCreator/blob/main/buildutils.py#L103) instance as `self` and set the boolean variable `self.ok` to indicate whether to include the given game, `True` for including, `False` for excluding (the code can be empty to include all games, this is the default). File `config.yml` is reserved for build configuration, currently should be left empty.

Example filter logic to filter out games less than 2200 rated:

```python
minelo = self.get_min_elo()

if minelo < 2200:
	self.ok = False
```

## Downloading files

The `zip` folder should contain zipped PGN files.

To download the next monthly lichess database run the program with the `--nextlichessdb` switch (you can repeat this several times to download databases for several months).

To download the proof lines from the antichess solution run the program with `--watkins 1000`, `--watkins 10000`, or `--watkins 25000`. A smaller number will create a better opening book, but it will take less time to download.

## Building files

Running the program with `-u` switch will unzip the files in the `zip` folder to the `source` folder. The source folder should contain the source PGN files, you can add your own files here. Running the program with `-f` switch will filter the files in the `source` folder and store the filtered files in the `filtered` folder. Running the program with `-b` switch will build a book from each filtered PGN in the `filtered` folder and store them in the `book` folder. To merge all the books in the `book` folder into one book, use the `-m` switch. The merged book will be stored in a file called `merged.bin` in the build environment's root folder (`envs/antichess/merged.bin` in our example).

This whole build process can be done in one step using the `-a` switch (which encompasses unzip, filter and build book).

The build is incremental. If you want to build from scratch, use the `--force` switch.

# Putting it all together

Activate the build environment, download the next monthly lichess database and build a merged book:

`pipenv run python create.py -e antichess --nextlichessdb -a`

You can repeat this step to include more monthly databases in the build.

# Credits

This project is created on top of [cbuild](https://github.com/lichapibot/cbuild).

# License

Opening Book Creator is licensed under the GPLv3 (or any later version at your option).
cbuild is licensed under the MIT License.
