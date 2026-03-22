# EGX-MCP 📈

A **Model Context Protocol (MCP) server** that exposes Egyptian Exchange (EGX) stock market data and live gold prices as AI-callable tools — enabling LLMs like Claude to query real-time and historical Egyptian market data conversationally.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Available Tools](#available-tools)
- [Available Resources](#available-resources)
- [Example Prompts](#example-prompts)
- [Tech Stack](#tech-stack)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- 🔴 **Live & closing stock prices** for EGX-listed companies
- 📊 **Intraday price readings** with 1-minute granularity
- 📅 **Historical price changes** over custom time periods
- 🏆 **Top rising stocks** — both intraday and over a date range
- 🥇 **Live gold prices** across 5 karats (buy & sell)
- 🗓️ **Date utilities** for easy time period calculations
- 🤖 **MCP-compatible** — plug directly into Claude Desktop or any MCP client

---

## Project Structure

```
egx-mcp/
│
├── server.py                   # MCP server entry point — registers all tools and resources
│
└── Domain/
    ├── egx_controller.py       # EGX stock data logic (prices, intraday, risers)
    ├── gold_controller.py      # Gold price scraper
    └── date_parser.py          # Date formatting utility
```

---

## Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) — fast Python package and project manager

## Install `uv` if you haven't already

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/your-username/egx-mcp.git
cd egx-mcp
```

2. **Install dependencies**

```bash
uv sync
```

> This will automatically create a virtual environment and install all dependencies from `pyproject.toml`. Required packages include: `mcp[cli]`, `egxpy`, `requests`, `beautifulsoup4`

---

## Configuration

### Claude Desktop

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "egx-mcp": {
      "command": "uv",
      "args": ["--directory", "/absolute/path/to/egx-mcp", "run", "server.py"]
    }
  }
}
```

---

## Usage

### Running the server directly

```bash
uv run server.py
```

### Using with the MCP CLI

```bash
uv run mcp dev server.py
```

Once connected to a compatible client (e.g., Claude Desktop), you can interact with the server through natural language.

---

## Available Tools

| Tool                     | Description                                                                     |
| ------------------------ | ------------------------------------------------------------------------------- |
| `get_current_time`       | Returns the current local date and time                                         |
| `get_timeperiod_date`    | Calculates a past date given today's date and a number of days                  |
| `get_last_price`         | Returns the last closing price for a given stock ticker                         |
| `get_live_price`         | Returns the live price for a stock (falls back to closing price if unavailable) |
| `get_price_change`       | Returns a list of daily prices between two dates for a given ticker             |
| `get_intraday_readings`  | Returns 1-minute intraday price readings for a stock on a given day             |
| `get_risers_overtime`    | Returns the top N stocks that gained the most over a given period               |
| `get_riser_intraday`     | Returns the top N stocks that gained the most today (intraday)                  |
| `get_current_gold_price` | Returns live buy and sell prices for 5 gold karats                              |

---

## Available Resources

| Resource      | URI               | Description                                                                        |
| ------------- | ----------------- | ---------------------------------------------------------------------------------- |
| EGX Companies | `egx://companies` | Returns the full dictionary of EGX-listed companies mapped to their ticker symbols |

---

## Example Prompts

Once connected to Claude Desktop, try asking:

> _"What is the current price of COMI?"_

> _"Which EGX stocks rose the most this week?"_

> _"Show me the intraday price readings for SWDY today."_

> _"What is today's gold price per karat in Egypt?"_

> _"How has FWRY performed over the last month?"_

> _"What are the top 3 rising stocks today?"_

---

## Tech Stack

| Package                                                                 | Purpose                                       |
| ----------------------------------------------------------------------- | --------------------------------------------- |
| [`uv`](https://docs.astral.sh/uv/)                                      | Fast Python package and project manager       |
| [`mcp`](https://github.com/modelcontextprotocol/python-sdk) / `FastMCP` | MCP server framework                          |
| [`egxpy`](https://pypi.org/project/egxpy/)                              | EGX market data (OHLCV, intraday, historical) |
| `requests`                                                              | HTTP requests for gold price scraping         |
| `beautifulsoup4`                                                        | HTML parsing for gold price data              |

---

## License

This project is licensed under the [MIT License](LICENSE).
