# TeamProject8_M2: Job Finding Agent

CEN 4930, Milestone 2 prototype.

**Team 8:** George Stephen and Manuel Rosales

## Overview

The Job Finding Agent helps a user search for jobs by describing what they
want in plain English, for example "a remote part-time job paying at least
$18 an hour that uses Python." The agent turns that request into structured
filters, calls a job search tool through the Model Context Protocol (MCP),
and explains the matching listings back to the user.

The agent is built with the OpenAI Agents SDK and runs on the course NRP
model endpoint (`qwen3`). The search tool runs in a separate local MCP server
that the agent starts automatically and talks to over stdio.

This is an educational prototype. It searches a small sample dataset, not a
live job board. See [Limitations](#limitations).

## Architecture

```
User (terminal)
   |
   |  natural language request
   v
Job Finding Agent (job_agent.py)
   |  OpenAI Agents SDK, qwen3 on the course NRP endpoint
   |
   |  MCP over stdio (agent starts the server as a subprocess)
   v
Job Search MCP Server (job_mcp_server.py)
   |  FastMCP, exposes the search_jobs tool
   v
jobs.json (8 sample listings)
   |
   |  matching listings as JSON, or "No jobs matched"
   v
Agent summarizes the results for the user
```

1. The user types a request at the `You:` prompt.
2. The model reads the request and decides which `search_jobs` filters to use.
3. The SDK sends the tool call to the MCP server over stdio.
4. The server filters `jobs.json` and returns the matching listings.
5. The model writes a summary of those listings. Its instructions forbid
   inventing jobs, companies, or salaries that the tool did not return.

## Files

| File | Purpose |
|---|---|
| `job_agent.py` | The agent and MCP client. Loads the NRP settings, starts the MCP server, and runs the chat loop. |
| `job_mcp_server.py` | The MCP server and the `search_jobs` tool. |
| `jobs.json` | The sample job dataset (8 listings in Southwest Florida and remote). |
| `tests/test_cases.md` | Test cases with inputs and expected outputs. |
| `requirements.txt` | Python dependencies. |

## Setup

Requires Python 3.10 or newer.

1. Clone the repository and enter it:

   ```
   git clone https://github.com/GGstephen6724/TeamProject8_M2.git
   cd TeamProject8_M2
   ```

2. (Recommended) create a virtual environment:

   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows
   source .venv/bin/activate     # macOS / Linux
   ```

3. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

   `mcp` is pinned below 2.0 on purpose. Version 2 renamed `FastMCP`, and the
   server will not start with it.

4. Create a file named `.env` in the project folder with the NRP values
   supplied by the course:

   ```
   NRP_API_KEY=your_key_here
   NRP_BASE_URL=the_course_nrp_base_url
   ```

   Do not commit `.env`. It contains your API key.

## Run

```
python job_agent.py
```

The agent starts the MCP server for you. You do not need to run
`job_mcp_server.py` separately. Type a job search at the `You:` prompt, or
type `exit` to quit.

Example requests:

- `Find me a remote part-time job paying at least $18 per hour.`
- `Are there any full-time jobs in Fort Myers?`
- `I know Python and SQL. What jobs match my skills?`

## MCP Tool: `search_jobs`

| Parameter | Type | Meaning |
|---|---|---|
| `keywords` | text | Words to look for in the job title, company, or skills. A job matches if any word matches. |
| `location` | text | Part of the location, such as `Fort Myers` or `Remote`. |
| `remote` | true / false | If true, return only remote jobs. |
| `employment_type` | text | `Part-time` or `Full-time`. |
| `minimum_salary` | number | Lowest acceptable starting hourly pay. |
| `skills` | text | Comma separated skills, such as `Python, SQL`. A job matches if it lists any of them. |

Every parameter is optional. Filters are combined, so a job must pass all of
the filters the agent sends. The tool returns the matching listings as JSON,
or the message `No jobs matched the provided criteria.`

## Test Cases

The full test cases are in [`tests/test_cases.md`](tests/test_cases.md).

| # | Input | Expected output |
|---|---|---|
| 1 | Remote part-time job paying at least $18/hr, with Python, SQL, JavaScript, and customer service skills | Remote, part-time jobs paying $18 or more, with relevant skills noted |
| 2 | Full-time IT support job in Fort Myers paying at least $20/hr | Matching Fort Myers positions only, no invented jobs |
| 3 | Remote part-time job paying at least $40/hr | A clear "no matching jobs" answer, no invented jobs |

We checked the `search_jobs` tool itself by calling it through a real MCP
stdio connection with the filters each test needs:

| # | Filters sent to the tool | Tool result |
|---|---|---|
| 1 | remote, Part-time, minimum $18 | IT Help Desk Technician (SunCoast Technology), Junior Web Developer (Coastal Web Group), Data Analyst Intern (Florida Analytics) |
| 2 | Fort Myers, Full-time, minimum $20 | Technical Support Specialist (Gulf Systems) |
| 3 | remote, Part-time, minimum $40 | No jobs matched the provided criteria. |

These results match the expected outputs. A full end to end run through the
model depends on the NRP endpoint, and the filters the model chooses can vary
from run to run (see below).

## Limitations

- **Small, static data.** `jobs.json` has 8 made-up sample listings. It is not
  connected to a live job board, and the listings are not real openings.
- **Simple matching.** Keywords and skills match on plain text. Any one word
  or skill is enough, so a broad search can return loosely related jobs, and
  a synonym (for example "coder" instead of "developer") will not match.
- **Hourly pay only.** Salaries are stored as hourly starting pay. The tool
  does not convert yearly salaries.
- **Model dependent.** The model decides which filters to send. It may pick
  different filters for the same request, or summarize results imperfectly.
  The instructions tell it not to invent jobs, but that is a prompt rule, not
  a guarantee.
- **No memory.** Each request is handled on its own. The agent does not
  remember earlier messages in the session.
- **No applications.** The agent does not apply for jobs, contact employers,
  or check that a listing is still open. Always confirm job details, pay, and
  requirements with the employer.
