# Locust performance tests for the Restful Booker API

Test task for Meteoro Platform - AQA Engineer.

## Project Structure

- `locustfile.py` - Main test script containing:
  - `RestfulBookerUser` class with test scenarios
  - Authentication flow
  - CRUD operations for bookings
- `config.py` - Configuration settings (API host)
- `pyproject.toml` - Python project configuration (contains dependencies)
- `.gitignore` - Git ignore rules
- `requirements.txt` - Dependencies list
- `uv.lock` - Dependency lock file

## Installation

### 1. Install uv

[Documentation for uv](https://github.com/astral-sh/uv)

```sh
pip install uv
```

### 2. Create and activate virtual environment

```sh
uv venv
```

For Windows:

```sh
.venv\Scripts\activate
```

For Linux/macOS:

```sh
source .venv/bin/activate
```

### 3. Install dependencies

Dependencies are installed from pyproject.toml:

```sh
uv sync
```

## Running Tests

### Web Interface

Start Locust with:

```sh
locust -f locustfile.py
```

Then open web interface at <http://localhost:8089>

### Headless

For Windows (PS):

```sh
locust -f .\locustfile.py --headless -u 5 -r 1 --run-time 1m 2>&1 | Tee-Object .\locust_run.log
```

For Linux/macOS:

```sh
locust -f ./locustfile.py --headless -u 5 -r 1 --run-time 1m 2>&1 | tee locust_run.log
```

## Test Scenarios

1. Authentication and token retrieval
2. Creating test booking
3. Getting all bookings
4. Getting specific booking
5. Full booking update
6. Partial booking update
7. Booking deletion

## Configuration

### API Host

Edit `config.py` to change the `HOST` variable if needed.

### Test Parameters

Edit `locustfile.py` to modify:

- Test data
- Task weights
- Wait times between requests

Edit test run parameters:  
`-u` - number of users (peak)  
`-r` - ramp up (users/sec)  
`--run-time` - run time
