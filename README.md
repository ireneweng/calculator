# Calculator
A simple calculator tool with command-line options, a user interface with preference settings, and server support.

## Overview
This is a very basic demo of a PySide widget, originally completed in two weeks for a coding test.

### Requirements
- Python 3
- [Docker](https://www.docker.com/)
- [PySide6](https://pypi.org/project/PySide6/)
- [sympy](https://www.sympy.org/en/index.html) (for testing)

### Package Files
- [`calculate`](calculate): main executable script to launch tool
- [`calculator.py`](calculator.py): module containing the implementation
- [`calculator_ui.py`](calculator_ui.py): module containing the user interface
- [`calculator_log.txt`](calculator_log.txt): default file where logging output is written
- [`client.py`](client.py): module containing client implementation
- [`server.py`](server.py): module containing server implementation
- [`tests.py`](tests.py): module containing test cases to check calculator implementation
- [`/themes`](themes): folder containing css stylesheets for different ui themes

### Notes
- Assumes the input is a correctly formatted arithmetic string
    - No unmatched or empty parentheses
    - Numbers on both sides of an operator (`+-1` or `--1` assumes negative 1)
    - Invalid inputs may still compute, but no guarantee that it's correct
- Does not support parentheses multiplication
    - `(1+2)(3-4)` computes incorrectly
- Does not support exponents
    - `6 ** 7` fails
- Allows parentheses around negatives
    - `6-(-7)*9` is valid
    - `6--7*9` is also valid
- Spaces with negatives may throw errors
    - `6 --7 * 9` computes
    - `6 - -7 * 9` does not
- When server is used with CLI, connection closes after one input
- When server is used with GUI, connection closes when GUI is closed

### Areas of Improvement

- More robust and descriptive error handling for invalid string inputs
    - Be stricter about what is allowed vs. not allowed, e.g. spaces in input
    - Catch "list index out of range" errors and replace with something more useful
- Could use clearer separation of view and controller in the calculator GUI
    - Separate the connection functions into their own class
- Debug and improve input validator on the calculator GUI to only accept digits and math operators
    - Sometimes breaks after certain buttons are pressed, allowing letters to be inserted
- Set dynamic buffer size on server based on size of input from client
- Keep CLI server connection open for multiple inputs without reinitializing each time
    - Could use some sort of escape/exit command
- Add option for user to choose implemention mode, e.g. mine or sympy

## Usage

All commands are run from inside the top-level `calculator` directory.

### Server initialization
    docker compose up --build

Must have Docker set up and logged in already.

### Command-line with local implementation
    ./calculate -i {input string}
    ./calculate -i "(6+7*9)/-2+4+(-10)"

This runs the command-line calculator without connecting to the server.

### Command-line with server
    ./calculate -ip {optional ip address}
    ./calculate -ip "10.8.9.174"

This runs the command-line calculator and attempts to connect to the server.\
If no host is provided, will use ip address "0.0.0.0".

If connection is established, accepts user input like this:

    -> {input}
    -> (6+7*9)/-2+4+(-10)

*Note*: Do not put input in quotes, will already be sent to server as string

### User interface
    ./calculate

This runs the calculator GUI and attempts to connect to the server.\
If the connection fails, will fall back to the local built-in implementation.

Preferences
- Right align: Aligns the numpad to the right and operators to the left
- Reverse order: Sets numpad to start with 0 in top row; default is 0 in bottom row

Themes
- Fun colors for the calculator!
