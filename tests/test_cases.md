# M2 Job Finding Agent - Test Cases

## Test 1: Remote part-time technical work

### Input

Find me a remote part-time job paying at least
$18 per hour. I have Python, SQL, JavaScript,
and customer service skills.

### Expected Output

The agent should use the `search_jobs` MCP tool
and return jobs that meet the remote, part-time,
and salary requirements.

The response should identify relevant skills
for each result.

---

## Test 2: Local IT support

### Input

Find me a full-time IT support job in Fort Myers
that pays at least $20 per hour.

### Expected Output

The agent should use the MCP tool and return
matching Fort Myers positions.

The agent should not invent additional positions.

---

## Test 3: No matching results

### Input

Find me a remote part-time job paying at least
$40 per hour.

### Expected Output

The agent should report that no matching jobs
were found.

The agent should not invent a job to satisfy
the request.
