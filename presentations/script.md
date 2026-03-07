# Nagios Configuration Generator — Speaker Script

> **Total Duration:** ~10–12 minutes  
> **Audience:** DevOps course evaluators / peers  
> **Format:** 16 slides + Live terminal demo + Browser demo  
> **Registration Number:** 23FE10CSE00339

---

## SLIDE 1 — Title Slide

**On Screen:**
- Nagios Configuration Generator
- Automating Infrastructure Monitoring with DevOps
- DevOps Project — Semester 6

### Say This

> "Good morning. I'm Ayush Anand, Registration Number 23FE10CSE00339, and today I'll present my DevOps semester project — the **Nagios Configuration Generator**. This is a Python-based automation tool that solves a real-world infrastructure monitoring challenge using DevOps best practices."

**Duration:** ~20 seconds

---

## SLIDE 2 — Agenda

**On Screen:**
1. Problem Statement
2. Solution Overview
3. Architecture & Tech Stack
4. Core Features
5. Live Demo — CLI
6. Live Demo — Web UI
7. DevOps Pipeline & Infrastructure
8. Testing Strategy
9. Key Results & Metrics
10. Conclusion & Q&A

### Say This

> "Here's what I'll cover. We'll start with the problem, walk through the architecture and features, do a live demo of both the CLI and web interface, then go into the DevOps pipeline, testing, and results."

**Duration:** ~15 seconds

---

## SLIDE 3 — The Problem

**On Screen:**
- Nagios requires **repetitive .cfg files** for every host, service, and contact
- Managing **50+ servers** means **hundreds of lines** of boilerplate
- **Human errors** in syntax cause monitoring failures silently
- **No built-in validation** — mistakes caught only at Nagios reload time
- **Configuration drift** across environments (dev/staging/prod)
- *"One misplaced bracket can leave your entire infrastructure unmonitored."*

### Say This

> "Nagios is a widely-used open-source monitoring tool, but configuring it is incredibly tedious. Every host, service, and contact needs its own `define` block in a `.cfg` file — with exact syntax. If you're managing 50 or 100 servers, that's hundreds of lines of repetitive boilerplate.
>
> The bigger issue is that Nagios has **no built-in validation**. A misplaced bracket or typo won't show an error until you try to reload the Nagios daemon — and by then, your monitoring might silently fail.
>
> So the question becomes: how do we automate this?"

**Duration:** ~45 seconds

---

## SLIDE 4 — The Solution

**On Screen:**
- A **Python-based automation tool** generating production-ready Nagios `.cfg` files
- **Input:** YAML definition or Web Form
- **Output:** Valid `.cfg` files (hosts, services, contacts, hostgroups, commands)
- **Validate** before generating — catch errors instantly
- **Template-driven** — consistent, production-ready output
- **Dual interface** — CLI for automation, Web UI for interactivity

### Say This

> "The answer is the Nagios Configuration Generator. You define your infrastructure in a simple YAML file — hosts, services, contacts — and the tool **validates** your input, then uses **Jinja2 templates** to generate production-ready `.cfg` files.
>
> It offers two interfaces: a **CLI** for scripting and CI/CD, and a **web UI** built with Flask for interactive use. Both share the same engine.
>
> What used to take hours of manual work now takes **under 100 milliseconds**."

**Duration:** ~40 seconds

---

## SLIDE 5 — Tech Stack

**On Screen:**

| Layer | Technology | Purpose |
|---|---|---|
| Language | Python 3.11 | Core application |
| Web | Flask 3.0 | Interactive web interface |
| CLI | Click 8.1 | Command-line interface |
| Validation | Pydantic 2.5 | Data models & validation |
| Templating | Jinja2 3.1 | Config file generation |
| Containerization | Docker | Multi-stage builds |
| Orchestration | Kubernetes | Production deployment |
| CI/CD | Jenkins + GitHub Actions | Automated pipeline |
| Testing | pytest 7.4 | Unit & integration tests |
| Security | Trivy | Container vulnerability scanning |

### Say This

> "Quick stack overview — **Python 3.11** is the core language. **Flask** powers the web UI, **Click** gives us the CLI, **Pydantic** handles validation.
>
> **Jinja2** renders templates. On the DevOps side — **Docker** with multi-stage builds, **Kubernetes** for production, **Jenkins** for CI/CD, **Trivy** for security scanning, and **pytest** for testing."

**Duration:** ~30 seconds

---

## SLIDE 6 — Architecture

**On Screen:**
- **Input Layer** — YAML Input (CLI) + Web Form (Flask)
- **Validation Layer** — Pydantic Models + Standalone Validators
- **Generator Engine** — NagiosGenerator (Jinja2 Templates)
- **Output** — .cfg Files | ZIP Archive | Web Preview
- Flow: `YAML / Web Form → Validation → Jinja2 Engine → .cfg Output`
- 5 config file types: hosts, services, contacts, hostgroups, commands

### Say This

> "Here's the data flow. Input comes from either the CLI as a YAML file, or through the web form. It passes through a **validation layer** — Pydantic models enforce constraints like valid IP addresses, RFC-compliant hostnames, and proper email formats.
>
> Once validated, the data goes into the **NagiosGenerator** — our Jinja2 template engine — which renders five output types: hosts, services, contacts, hostgroups, and commands.
>
> Output can be written to disk, previewed in the browser, or downloaded as a ZIP."

**Duration:** ~40 seconds

---

## SLIDE 7 — Core Feature: Input Validation

**On Screen:**
- IP addresses — regex + format check
- Hostnames — RFC-compliant, max 63 chars
- Email addresses — proper format validation
- Thresholds — range validation (1–100)
- Required fields — structural completeness
- Sample: `host_name: webserver01 | address: 192.168.1.10 | max_check_attempts: 5`
- **Catch errors before deployment** — validation runs before any file is generated

### Say This

> "Here's what the YAML input looks like. You define hosts with their hostname, alias, IP, and monitoring parameters. The tool validates every field:
>
> - IP addresses checked against proper format
> - Hostnames RFC-compliant — alphanumeric, max 63 characters
> - Email format validation
> - Numeric thresholds range-checked (1–100)
>
> If anything is wrong, you get a clear error **before** any files are generated. Fail fast."

**Duration:** ~35 seconds

---

## SLIDE 8 — Core Feature: Template Engine

**On Screen:**
- **Jinja2 Templates → Nagios Config**
- Template (`hosts.cfg.j2`): loops over hosts, fills in fields
- Generated Output (`hosts.cfg`): `define host { host_name webserver01 … }`
- 5 template types: hosts, services, contacts, hostgroups, commands
- Consistent, production-ready Nagios syntax every time

### Say This

> "Generation happens through Jinja2 templates. The template loops over hosts and fills in fields. The output mirrors Nagios syntax exactly, so the output is **immediately deployable** to a Nagios server.
>
> We have five template types: hosts, services, contacts, hostgroups, and commands. We only generate files that have data — no empty files."

**Duration:** ~25 seconds

---

## SLIDE 9 — Core Feature: Dual Interface

**On Screen:**
- **CLI — For Scripting & Automation**
  - `$ python -m src.main.cli validate -i examples/sample_input.yaml`
  - `$ python -m src.main.cli generate -i sample_input.yaml -o output/`
- **Web UI — For Interactive Use**
  - `$ python -m src.main.cli web --port 5000`
  - Add hosts, services, contacts via dynamic forms
  - Preview generated configs in-browser
  - Download as ZIP archive

### Say This

> "Two interfaces, same engine. The CLI has three commands: `validate` for dry-run checks, `generate` for file output, and `web` to launch the Flask server.
>
> The web UI is for interactive use — dynamic forms for adding monitoring objects, in-browser preview, and ZIP download.
>
> Let me show you both in action."

**Duration:** ~15 seconds — **transition to live demo**

---

## LIVE DEMO — CLI

### Pre-Demo Checklist
- [ ] Terminal open in project directory
- [ ] Virtual environment activated
- [ ] `examples/sample_input.yaml` present

### Step 1 — Show the input
```bash
cat examples/sample_input.yaml
```
> "Here's our sample input — 4 hosts, 6 services, 3 contacts. A small but realistic infrastructure."

### Step 2 — Validate (dry run)
```bash
python -m src.main.cli validate -i examples/sample_input.yaml
```
> "First, validate. It reports the input is valid — 4 hosts, 6 services, 3 contacts. No files generated — pure validation."

### Step 3 — Generate configs
```bash
python -m src.main.cli generate -i examples/sample_input.yaml -o output/
```
> "Now generate. Under a second — 5 config files."

### Step 4 — Inspect output
```bash
cat output/hosts.cfg
cat output/services.cfg
```
> "Here's `hosts.cfg` — proper Nagios `define host` blocks. Production-ready."

**Duration:** ~2 minutes

---

## LIVE DEMO — Web UI

### Pre-Demo Checklist
- [ ] Docker running OR Flask server ready
- [ ] Browser open at `http://localhost:5000`

### Step 1 — Start server
```bash
python -m src.main.cli web --port 5000
```

### Step 2 — Add a host
- Hostname: `webserver01` | Alias: `Production Web Server`
- Address: `192.168.1.10` | Contact Groups: `admins`

### Step 3 — Add a service
- Host: `webserver01` | Description: `HTTP Check` | Command: `check_http`

### Step 4 — Add a contact
- Name: `admin` | Alias: `System Administrator` | Email: `admin@example.com`

### Step 5 — Generate & Download
> "Click generate — here's the preview. Download as ZIP — ready to deploy."

**Duration:** ~2.5 minutes

---

## SLIDE 10 — DevOps: Docker & Containerization

**On Screen:**
- Stage 1 (Builder): python:3.11-slim → install dependencies
- Stage 2 (Runtime): minimal image, copy only built artifacts
- Final image: **~150 MB** vs ~900 MB single-stage (83% reduction)
- Health check every 30s | Gunicorn (2 workers)
- `docker-compose up -d` (Generator only)
- `docker-compose --profile full up -d` (Generator + Nagios)

### Say This

> "The application is containerized with a **multi-stage Docker build**. First stage installs dependencies, second copies only what's needed.
>
> Final image goes from ~900 MB down to **~150 MB** — an 83% reduction. Health check every 30 seconds, production server is **Gunicorn** with 2 workers.
>
> Docker Compose gives us **one-command deployment**. The `full` profile spins up a Nagios server reading generated configs through a shared volume."

**Duration:** ~55 seconds

---

## SLIDE 11 — DevOps: CI/CD Pipeline

**On Screen:**
- Lint → Build → Test → Scan → Deploy Staging → Deploy Production
- Checkout / Code Quality (flake8) / Build (Docker) / Test (pytest)
- Security Scan (Trivy) / Deploy Staging (auto) / Deploy Production (manual gate)
- [!] Zero high-severity vulnerabilities allowed

### Say This

> "The Jenkins pipeline automates quality assurance. **flake8** checks code quality, Docker builds the image, **pytest** runs tests, and a smoke test verifies the CLI.
>
> **Trivy** scans for vulnerabilities. Staging deploys automatically; production requires **manual approval**. Every commit goes through the same pipeline — no shortcuts."

**Duration:** ~35 seconds

---

## SLIDE 12 — Testing Strategy

**On Screen:**
- **Unit Tests (12+):** Generator output, file creation, ZIP validity, Nagios syntax
- **Integration Tests:** YAML → validate → generate → verify files
- **Smoke Tests:** CLI commands in CI/CD pipeline
- Key: `test_end_to_end_generation()` — asserts exit code 0, 5 files generated
- **Coverage: 85%+** (target: 80%)

### Say This

> "Testing is first-class. **12+ unit tests** cover generator output, file creation, ZIP validity, and Nagios syntax. The **integration test** runs the full pipeline — YAML to files — and verifies everything.
>
> In CI, **smoke tests** ensure CLI commands execute without errors. Coverage is over **85%**, above our 80% target."

**Duration:** ~25 seconds

---

## SLIDE 13 — Results & Metrics

**On Screen:**

| Metric | Target | Achieved |
|---|---|---|
| Config generation time | < 1 second | **~100 ms** |
| Docker build time | < 2 minutes | **~45 seconds** |
| Docker image size | < 200 MB | **~150 MB** |
| Test coverage | > 80% | **85%+** |
| Config file types | 5 | **5** |

### Say This

> "Numbers — config generation is **~100 ms**, Docker image is **~150 MB**, build time is **45 seconds**, test coverage over **85%**.
>
> This demonstrates Infrastructure as Code, CI/CD with quality gates, optimized containerization, and automation over manual processes."

**Duration:** ~30 seconds

---

## SLIDE 14 — Project Structure

**On Screen:**
```
nagiosconfigurator/
├── src/main/          cli.py, generator.py, models.py, validators.py, web.py
├── templates/nagios/  Jinja2 .cfg.j2 template files
├── infrastructure/    Docker, Kubernetes, Terraform configs
├── pipelines/         Jenkinsfile CI/CD pipeline definition
├── tests/             Unit + integration test suites
├── examples/          Sample YAML input files
└── output/            Generated .cfg files (runtime)
```

### Say This

> "`src/main/` has our five core modules. `templates/nagios/` has Jinja2 templates. `infrastructure/` holds Docker and Kubernetes configs. `pipelines/` has the Jenkinsfile. And `tests/` has our test suites."

**Duration:** ~15 seconds

---

## SLIDE 15 — Key Takeaways

**On Screen:**
- Automation eliminates manual errors in monitoring config
- Validation-first design catches mistakes before deployment
- Dual interfaces serve both automation and interactive needs
- DevOps pipeline ensures quality at every stage
- Containerization makes deployment consistent and portable

### Say This

> "To wrap up — **automation eliminates manual errors**. **Validation-first design** catches mistakes early. **Dual interfaces** serve both automation and interactive needs. The **DevOps pipeline** enforces quality at every stage. And **containerization** makes deployment consistent everywhere."

**Duration:** ~25 seconds

---

## SLIDE 16 — Thank You / Q&A

### Say This

> "That concludes my presentation. Thank you for your time. I'm happy to take any questions."



---
