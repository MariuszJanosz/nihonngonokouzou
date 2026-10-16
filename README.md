# Simple app to visualize the structure of Japanese

This is a simple software to visualize the structure of Japanese.
It treats each word as a node in a directed graph. There is an endge between
words `A` and `B` if and only if `A` appears in the definition of `B`.
We define the importance `I` of a given word as the number of edges
going out of its node; that is `I(A) = #(edges going out of A)`.

## Setup

Run all commands from the repo root directory.

To set up virtual environment for the first time run

```sh
python -m venv .venv
. .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dependencies,dev,dev-tools]"
```

Then for each subsequent time run

```sh
. .venv/bin/activate
```

To set up the environment for the first time run

```sh
cp .env.example .env
nano .env # Here set up your environmental variables
. env.sh
```

Then for each subsequent time run

```sh
. env.sh
```

To set up database run

```sh
./postgresql/start.sh
alembic upgrade head
```

To populate database run

```sh
python -m scripts.get_words_urls
python -m scripts.format_words_urls
python -m scripts.get_dictionary_entry
python -m scripts.dictionary_entries_remove_images
python -m scripts.format_dictionary_entries
python -m scripts.clean_dictionary_entries
python -m postgresql.populate_database dictionary_entries_formated_cleaned.txt
```
