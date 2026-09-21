# quicknote

A simple command-line tool for taking notes. Supports tags, search, and color-coded output.

I built this because I kept losing track of ideas and TODOs across different projects.

## Install

```bash
git clone https://github.com/1Dhyaa/quicknote.git
cd quicknote
```

No dependencies needed, just Python 3.7+.

## Usage

```bash
# add a note
python quicknote.py add "fix the login bug on the server" --tags bug,server

# list all notes
python quicknote.py list

# search notes
python quicknote.py search "login"

# filter by tag
python quicknote.py list --tag server

# delete a note
python quicknote.py delete 3

# mark as done
python quicknote.py done 1
```

## Output

```
 #  Status  Tags           Note                                Created
 1  [ ]     bug, server    fix the login bug on the server     Sep 20, 2026
 2  [x]     idea           try using redis for caching         Sep 19, 2026
 3  [ ]     todo           write tests for the API             Sep 18, 2026
```

## Storage

Notes are saved in `~/.quicknotes.json`. Nothing fancy.

## License

MIT
