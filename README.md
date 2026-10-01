# TeamProject8_M2: Job Finding Agent

CEN 4930, Milestone 2. Team 8: George Stephen and Manuel Rosales.

## Problem

Job seekers waste time scrolling through listings that do not match their
location, schedule, pay, or skills, so this agent lets them describe what
they want in plain English and returns only the jobs that fit.

## What the agent can do right now

- Take a plain English request, such as "a remote part-time job paying at
  least $18 an hour that uses Python."
- Turn it into filters and call the `search_jobs` MCP tool. The tool filters
  by keywords, location, remote, full or part time, minimum hourly pay, and
  skills.
- Summarize the matching jobs, or say clearly that nothing matched, without
  inventing listings.

The agent uses the OpenAI Agents SDK with the `qwen3` model on the course NRP
endpoint. It starts the MCP server (`job_mcp_server.py`) itself over stdio.

## Not implemented yet

- Live job data. The tool searches `jobs.json`, which holds 8 sample listings.
- Conversation memory. Each request is handled on its own.
- Applying to jobs or contacting employers.

## Setup and run

Requires Python 3.10 or newer.

1. Clone the repo and open a terminal in its folder.
2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Create a file named `.env` in the same folder with the NRP values from the
   course:

   ```
   NRP_API_KEY=your_key_here
   NRP_BASE_URL=the_course_nrp_base_url
   ```

4. Run the agent, then type a job search at the `You:` prompt. Type `exit` to
   quit.

   ```
   python job_agent.py
   ```

Test cases with inputs and expected outputs are in `tests/test_cases.md`.

## Known limitations

1. **Sample data only.** The 8 listings are made up and are not real openings.
2. **Loose text matching.** Any single keyword or skill counts as a match, so
   broad searches return loosely related jobs, and synonyms such as "coder"
   for "developer" do not match.
3. **Filter choice depends on the model.** The model picks the search filters,
   so the same request can produce different filters from run to run. The
   rule against inventing jobs is a prompt instruction, not a guarantee.

`mcp` is pinned below 2.0 in `requirements.txt` because version 2 renamed
`FastMCP` and the server will not start with it.
