# Nagios Configuration Generator - Demo Script

## Introduction (1 min)
*   **Greeting:** "Hello everyone, my name is [Your Name], Registration Number [Your Registration Number]."
*   **Project Overview:** "For my DevOps project, I built the Nagios Configuration Generator. It's a tool designed to solve the tedious and error-prone process of manually writing Nagios monitoring configuration files."

## The Problem & Solution (1.5 min)
*   **Problem:** "Normally, defining hosts, services, and contacts in Nagios requires creating multiple `.cfg` files with strict syntax. This doesn't scale well when monitoring 50+ servers."
*   **Solution:** "My tool automates this. It takes simple YAML input—or input from a web form—and uses Jinja2 templates to generate valid, production-ready Nagios configuration files."
*   **Tech Stack:** "The project is built with Python, Flask for the web UI, Click for the CLI, and Pydantic for strict input validation. It's fully containerized with Docker and uses GitHub Actions for CI/CD."

## Live Demo - CLI (2 min)
*   **Show Sample Input:** "First, let's look at `examples/sample_input.yaml`. You can see it clearly defines hosts, services, and contacts."
*   **Run Validation:** Run `python -m src.main.cli validate -i examples/sample_input.yaml`. "The tool validates IPs, hostnames, and email formats."
*   **Run Generation:** Run `python -m src.main.cli generate -i examples/sample_input.yaml -o output/`.
*   **Show Output:** Open `output/hosts.cfg` and `output/services.cfg` to show the generated Nagios syntax.

## Live Demo - Web UI (2.5 min)
*   **Start Server:** Run `docker-compose up -d` or `python -m src.main.cli web`.
*   **Open Browser:** Navigate to `http://localhost:5000`.
*   **Show Form:** "Here is the interactive web UI. We can add a new host dynamically." Fill out a quick host and service definition.
*   **Generate & Download:** Click Generate, show the results page with the syntax highlighting, and click "Download as ZIP".

## CI/CD and DevOps Implementation (2 min)
*   **GitHub Actions:** Show the `.github/workflows/ci.yml` file. Explain the stages: code quality (flake8), testing (pytest), and Docker build.
*   **Docker:** Show the multi-stage `Dockerfile` and `docker-compose.yml` explaining how it drastically reduces image size and makes deployment easy.
*   **Show Pipeline Run:** (Optional) Show a green build passing on GitHub.

## Conclusion (1 min)
*   "This project demonstrated applying DevOps practices (CI/CD, containerization) to solve a real-world infrastructure problem (configuration management)."
*   "Thank you. Are there any questions?"
