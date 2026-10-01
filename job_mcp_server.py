from mcp.server.fastmcp import FastMCP
import json
from pathlib import Path


# Create MCP server
mcp = FastMCP("Job Search Tools")


# Location of our job database
DATABASE = Path(__file__).with_name(
    "jobs.json"
)


# ------------------------------------------------
# JOB SEARCH TOOL
# ------------------------------------------------

@mcp.tool()
def search_jobs(
    keywords: str = "",
    location: str = "",
    remote: bool = False,
    employment_type: str = "",
    minimum_salary: float = 0,
    skills: str = ""
) -> str:

    """
    Search the prototype job database using
    the user's job preferences.

    keywords:
        Job title or general search terms.

    location:
        Location such as Remote or Fort Myers.

    remote:
        If true, only return remote jobs.

    employment_type:
        Part-time or Full-time.

    minimum_salary:
        Minimum acceptable hourly salary.

    skills:
        Comma-separated skills such as Python, SQL.
    """


    # ------------------------------------------------
    # LOAD DATABASE
    # ------------------------------------------------

    try:

        with DATABASE.open(
            "r",
            encoding="utf-8"
        ) as file:

            jobs = json.load(file)

    except FileNotFoundError:

        return "ERROR: jobs.json was not found."

    except json.JSONDecodeError:

        return "ERROR: jobs.json contains invalid JSON."


    # ------------------------------------------------
    # NORMALIZE INPUT
    # ------------------------------------------------

    keywords = keywords.lower().strip()

    location = location.lower().strip()

    employment_type = (
        employment_type
        .lower()
        .strip()
    )


    requested_skills = [

        skill.strip().lower()

        for skill in skills.split(",")

        if skill.strip()
    ]


    matches = []


    # ------------------------------------------------
    # SEARCH JOBS
    # ------------------------------------------------

    for job in jobs:

        searchable_text = (
            job["title"]
            + " "
            + job["company"]
            + " "
            + " ".join(job["skills"])
        ).lower()


        # Keyword filter
        if keywords:

            keyword_terms = [
                term.strip().lower()
                for term in keywords.split()
                if term.strip()
            ]

            if not any(
                term in searchable_text
                for term in keyword_terms
            ):

                continue


        # Location filter
        if location:

            if location not in job["location"].lower():

                continue


        # Remote filter
        if remote:

            if not job["remote"]:

                continue


        # Employment type filter
        if employment_type:

            if (
                job["employment_type"].lower()
                != employment_type
            ):

                continue


        # Salary filter
        if job["salary_min"] < minimum_salary:

            continue


        # Skills filter
        if requested_skills:

            job_skills = [

                skill.lower()

                for skill in job["skills"]
            ]


            skill_match = any(

                requested in job_skill

                for requested in requested_skills

                for job_skill in job_skills
            )


            if not skill_match:

                continue


        matches.append(job)


    # ------------------------------------------------
    # RETURN RESULTS
    # ------------------------------------------------

    if not matches:

        return (
            "No jobs matched the provided criteria."
        )


    return json.dumps(
        matches,
        indent=2
    )


# ------------------------------------------------
# START MCP SERVER
# ------------------------------------------------

if __name__ == "__main__":

    mcp.run()