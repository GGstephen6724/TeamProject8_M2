# TeamProjectN_M2 - Job Finding Agent

## Overview

This project is a prototype Job Finding Agent
for CEN 4930 Milestone 2.

The agent uses the course NRP endpoint and the
OpenAI Agents SDK.

It connects to a local MCP server through stdio.

The MCP server exposes a `search_jobs` tool that
searches a small JSON job dataset.

---

## Architecture

User
↓
Job Finding Agent
↓
MCP stdio connection
↓
Job Search MCP Server
↓
search_jobs()
↓
jobs.json
↓
Matching Job Listings
↓
Agent Response

---

## Files

- `job_agent.py`
  AI agent and MCP client

- `job_mcp_server.py`
  MCP server and search_jobs tool

- `jobs.json`
  Prototype job dataset

- `tests/test_cases.md`
  Test cases

- `requirements.txt`
  Python dependencies

---

## Setup

Install dependencies:

pip install -r requirements.txt

Create a `.env` file containing the NRP
values supplied by the course.

---

## Run

python job_agent.py

The agent automatically starts the MCP
server using the course's stdio MCP pattern.

---

## MCP Tool

The MCP server provides:

search_jobs(
    keywords,
    location,
    remote,
    employment_type,
    minimum_salary,
    skills
)

---

## Limitations

This is an educational prototype.

The job database is:

- Small
- Static
- Not a live job board

The prototype does not submit applications
and does not guarantee that a job listing
currently exists.

Users should verify job openings,
compensation, and requirements with the
employer.