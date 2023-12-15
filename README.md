# Ntfy Path Observer

A simple Python script which observes newly created files in a directory and
send its contents to a [ntfy](https://github.com/binwiederhier/ntfy) server.

## Usage

```shell
export OBSERVER_PATH='/path/to/observe'

export NTFY_USER='username'
export NTFY_PASS='password'
export NTFY_URL='https://ntfy.example.com/topic'

./observe.py
```
