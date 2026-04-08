# Text Files Merger

## Purpose

Learning and testing base kit for the AHP platform. Demonstrates the minimal structure required for a kit: input resolution via `KIT_INPUTS_FILE`, logging to stdout and file, and writing output to `/tmp/outputs/`.

## What it does

Reads two text files and concatenates them (in order) into a single output file.

## Inputs

Files are resolved from the directory pointed to by `KIT_INPUTS_FILE`.

| Environment variable | Default | Description |
|---|---|---|
| `KIT_INPUTS_FILE` | *(required)* | Path to the input directory |
| `INPUT_1_NAME` | *(required)* | Filename of the first input (injected by platform) |
| `INPUT_2_NAME` | *(required)* | Filename of the second input (injected by platform) |

## Output

A single file `output.txt` written to `/tmp/outputs/`, containing the content of `input1` followed by the content of `input2`.

## Logging

Written to `/tmp/logs/text_files_merger.log` and to stdout.

## Template files

`templates/` contains example inputs and the expected merged output:

- `templates/input1.txt` — first input
- `templates/input2.txt` — second input
- `templates/output.txt` — expected result

## Build & run locally

### With uv

```bash
# Install dependencies (none, but creates .venv)
uv sync

# Run with template inputs
KIT_INPUTS_FILE=templates INPUT_1_NAME=input1.txt INPUT_2_NAME=input2.txt \
  uv run python text_merger/execute.py
```

### With Docker

```bash
# Build
docker build -t text-files-merger .

# Run with template inputs mounted
docker run \
  -e KIT_INPUTS_FILE=/inputs \
  -e INPUT_1_NAME=input1.txt \
  -e INPUT_2_NAME=input2.txt \
  -v $(pwd)/templates:/inputs \
  text-files-merger
```

The merged output will be at `/tmp/outputs/output.txt` inside the container and the log at `/tmp/logs/text_files_merger.log`.
