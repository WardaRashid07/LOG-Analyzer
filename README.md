# Log File Analyzer

A Python tool that parses unstructured pipeline log files using regular expressions, categorizes entries by severity, and produces structured summaries to support pipeline monitoring and error triage.

## Overview

Data pipelines generate continuous log output that mixes informational messages, warnings, and errors in free-text form. This tool reads a plain-text log file line by line, extracts structured fields (timestamp, severity level, source component, and message) using a single regular expression, and produces:

- A count of log entries by severity level (INFO, WARN, ERROR, DEBUG)
- A count of events per hour, based on log timestamps
- A plain-text file containing every ERROR-level entry, for quick triage
- A structured CSV summary of every successfully parsed log line
- A console summary of processing results

Lines that don't match the expected format are treated as malformed: they're logged as a warning and skipped, rather than stopping the run.

## Log Format

The analyzer expects each line to follow this structure:

```
<timestamp> | <level> | <component> | <message>
```

For example:

```
2024-01-15 10:23:45 | INFO  | DataLoader   | File loaded successfully
2024-01-15 10:24:01 | ERROR | Transformer  | Null value found in column: amount
2024-01-15 10:24:30 | WARN  | Validator    | Record count mismatch: expected 1000, got 987
```

Recognized severity levels are `INFO`, `WARN`, `ERROR`, and `DEBUG`.

## Project Structure

```
LogFilerProject/
├── analyzer.py          # Main script: reads, parses, counts, and writes output
├── patterns.py           # Regex pattern(s) defined as named constants
├── data/
│   └── application.log    # Input log file
├── errors.log              # Output: all ERROR-level lines, extracted
├── log_summary.csv          # Output: structured fields for every valid line
├── .gitignore
└── README.md
```

## Requirements

No third-party dependencies — the project relies only on the Python standard library:

- `re` — regular expression parsing
- `csv` — structured CSV output
- `logging` — warnings for malformed lines
- `datetime` — timestamp parsing and hourly aggregation

Python 3.8 or later is recommended.

## Usage

1. Place your log file in the project directory (or update the `path` variable in `analyzer.py` to point to it).
2. Run the script:

```bash
python analyzer.py
```

3. Check the outputs:
   - `log_summary.csv` — one row per valid log entry, with columns `timestamp, level, component, message`
   - `errors.log` — the raw text of every ERROR-level line
   - Console output — total lines processed, valid vs. invalid counts, per-level counts, and per-hour event counts

## How It Works

1. **Read the log line by line.** The file is streamed with a `for` loop rather than loaded fully into memory, so the approach scales to very large log files.
2. **Match each line against a regular expression** (defined in `patterns.py`) that captures the timestamp, level, component, and message as four separate groups.
3. **Skip and log malformed lines.** If a line doesn't match the expected pattern, a warning is logged via Python's `logging` module and the line is skipped — it does not stop processing.
4. **Parse the timestamp** into a `datetime` object using `datetime.strptime`, enabling per-hour aggregation.
5. **Count entries by severity level** as each line is processed.
6. **Count entries per hour**, grouped by the hour portion of each timestamp.
7. **Collect ERROR-level lines** and write them, verbatim, to `errors.log`.
8. **Write every valid line's structured fields** to `log_summary.csv` using Python's `csv` module, which correctly handles messages containing commas.
9. **Print a final summary** to the console: total lines processed, valid and invalid line counts, and counts per severity level.

## Sample Console Output

```
total lines processed  =  2199
total valid lines =  2068   total invalid lines =  131
count per log level:
num of INFO logs = 866, num of warning logs = 359, number of Error logs = 421, number of Debug logs = 422
```

*(Exact figures will vary depending on the input log file.)*

## Notes on Design

- **Regex patterns are isolated in `patterns.py`** so the matching logic can be reused, tested, or modified independently of the parsing script.
- **Malformed-line handling uses Python's `logging` module** rather than raising exceptions, so a single bad line doesn't crash the run.
- **The CSV module, rather than manual string joining, is used for structured output**, since it correctly quotes fields that contain commas — a real case in this dataset (e.g. `"Record count mismatch: expected 1000, got 987"`).

## Possible Extensions

- Detect repeated ERROR entries within a short time window (error spike detection)
- Support multiple, configurable log format patterns
- Archive log entries older than a configurable age
- Generate a simple text-based chart of per-hour error rate

## Author

Warda Rashid
