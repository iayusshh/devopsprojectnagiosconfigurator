# Design Document — Nagios Configuration Generator

## 1. Overview

The Nagios Configuration Generator is a Python-based tool that automates the creation of Nagios `.cfg` configuration files from structured YAML input or a web form. It eliminates the manual, error-prone process of writing Nagios configurations for large infrastructure environments.

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interface                           │
│                                                                 │
│   ┌──────────────┐              ┌──────────────────────┐        │
│   │  CLI (Click)  │              │  Web UI (Flask)       │        │
│   │  YAML Input   │              │  HTML Form Input      │        │
│   └──────┬───────┘              └──────────┬───────────┘        │
│          │                                  │                    │
│          └──────────┬───────────────────────┘                    │
│                     ▼                                            │
│   ┌─────────────────────────────────────────────────────┐       │
│   │              Validation Layer                        │       │
│   │  validators.py — IP, hostname, email, threshold      │       │
│   │  Pydantic models — Field-level + structural          │       │
│   └─────────────────────┬───────────────────────────────┘       │
│                         ▼                                        │
│   ┌─────────────────────────────────────────────────────┐       │
│   │           NagiosConfig (Pydantic Model)              │       │
│   │  hosts[], services[], contacts[], hostgroups[],      │       │
│   │  contact_groups[], commands[]                        │       │
│   └─────────────────────┬───────────────────────────────┘       │
│                         ▼                                        │
│   ┌─────────────────────────────────────────────────────┐       │
│   │           NagiosGenerator (Jinja2 Engine)            │       │
│   │  ┌────────────────────────────────────────────┐     │       │
│   │  │  Templates:                                 │     │       │
│   │  │  hosts.cfg.j2 → hosts.cfg                   │     │       │
│   │  │  services.cfg.j2 → services.cfg             │     │       │
│   │  │  contacts.cfg.j2 → contacts.cfg             │     │       │
│   │  │  hostgroups.cfg.j2 → hostgroups.cfg         │     │       │
│   │  │  commands.cfg.j2 → commands.cfg             │     │       │
│   │  └────────────────────────────────────────────┘     │       │
│   └─────────────────────┬───────────────────────────────┘       │
│                         ▼                                        │
│   ┌─────────────────────────────────────────────────────┐       │
│   │              Output                                  │       │
│   │  • .cfg files on disk (CLI)                          │       │
│   │  • ZIP download (Web UI)                             │       │
│   │  • In-browser preview (Web UI)                       │       │
│   └─────────────────────────────────────────────────────┘       │
└─────────────────────────────────────────────────────────────────┘
```

## 3. Data Flow

1. **Input** — User provides monitoring data via YAML file (CLI) or web form (Web UI)
2. **Parsing** — YAML is parsed with PyYAML; form data is extracted from Flask `request`
3. **Validation** — Standalone validators pre-check raw data; Pydantic models enforce types and constraints
4. **Model Construction** — Validated data is constructed into a `NagiosConfig` object containing all Nagios object types
5. **Template Rendering** — `NagiosGenerator` loads Jinja2 templates, passes model data as context, renders `.cfg` content
6. **Output** — Rendered configs are written to files (CLI) or returned as in-browser preview + ZIP download (Web UI)

## 4. Key Design Decisions

### 4.1 Pydantic for Validation
We chose Pydantic v2 over manual validation for:
- Declarative field-level validators with clear error messages
- Automatic type coercion (e.g., string to int)
- Easy serialization to/from JSON and dictionaries
- Built-in support for complex nested models

### 4.2 Jinja2 for Templating
Nagios config syntax maps naturally to Jinja2's `{% for %}` loops and `{{ variable }}` interpolation. This keeps the template files readable and closely resembling actual Nagios configs.

### 4.3 Dual Interface (CLI + Web)
The CLI serves automated/scripted workflows (CI/CD pipelines, batch generation), while the Web UI serves interactive use. Both share the same core `NagiosGenerator` engine, ensuring consistent output.

### 4.4 Multi-Stage Docker Build
The Dockerfile uses a multi-stage build to:
1. Install dependencies in a builder stage
2. Copy only the installed packages to a slim runtime image
3. This reduces the final image size from ~900MB to ~150MB

## 5. Module Descriptions

| Module | Responsibility |
|---|---|
| `models.py` | Pydantic data models for Host, Service, Contact, etc. with field validators |
| `validators.py` | Standalone validation functions (IP, hostname, email, threshold, YAML structure) |
| `generator.py` | Jinja2 template rendering engine with file write and ZIP archive support |
| `cli.py` | Click-based CLI with `generate`, `validate`, and `web` sub-commands |
| `web.py` | Flask web application with form handling, generation, and ZIP download routes |
| `config/config.py` | Application-wide configuration constants and defaults |

## 6. Security Considerations

- All user input is validated through Pydantic before template rendering (prevents injection)
- The Jinja2 environment uses `trim_blocks` and `lstrip_blocks` for clean output
- No database is used — the tool is stateless
- Docker container runs as a non-privileged process
- The Flask `secret_key` should be changed in production via environment variables

## 7. Testing Strategy

- **Unit Tests** — Cover models, validators, generator, and CLI using pytest
- **Integration Tests** — End-to-end YAML → .cfg generation
- **CI Smoke Tests** — CLI validate + generate against sample input in the pipeline
- **Docker Tests** — Build image and verify HTTP response in CI
