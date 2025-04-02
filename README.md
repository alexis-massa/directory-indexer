# Directory Indexer

---

## Development

### Installation & Setup

#### Prerequisites

Ensure you have **Python 3.13** installed.

#### Clone the Repository

#### Install Dependencies

Under Linux

```sh
python -m pip install uv
uv venv .venv --python 3.13
source .venv/bin/activate
uv pip install -r dev-requirements.in
```

Under Windows

```sh
python -m pip install uv
uv venv .venv --python 3.13
.venv\Scripts\activate
uv pip install -r dev-requirements.in
```

---

#### Modify & Test

#### Building the Executable

##### Windows:

```sh
pyinstaller --onefile --noconsole src/
```

##### Linux:

```sh
pyinstaller --onefile src/
```

The resulting binary will be in the `dist/` folder.

### Update CHANGELOG.md

```sh
pip install git-cliff
git-cliff  -u --prepend CHANGELOG.md -t 0.x
```
With `0.x` being the release being worked on

---

## License

This project is licensed under the MIT License.
