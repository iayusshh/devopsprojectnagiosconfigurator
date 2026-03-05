# User Guide — Nagios Configuration Generator

## Table of Contents
1. [Quick Start](#quick-start)
2. [CLI Usage](#cli-usage)
3. [Web UI Usage](#web-ui-usage)
4. [YAML Input Format](#yaml-input-format)
5. [Generated Output](#generated-output)
6. [Docker Deployment](#docker-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Install
```bash
git clone https://github.com/[username]/devopsprojectnagiosconfigurator.git
cd devopsprojectnagiosconfigurator
pip install -r requirements.txt
```

### Generate configs in 30 seconds
```bash
python -m src.main.cli generate -i examples/sample_input.yaml -o output/
```

This reads the sample YAML file and produces ready-to-use Nagios `.cfg` files in the `output/` directory.

---

## CLI Usage

The CLI is built with [Click](https://click.palletsprojects.com/) and provides three sub-commands.

### `generate` — Generate config files
```bash
python -m src.main.cli generate -i <input.yaml> -o <output_dir>
```

| Flag | Description |
|---|---|
| `-i, --input` | Path to YAML input file (required) |
| `-o, --output` | Directory to write `.cfg` files (required) |
| `--template-dir` | Custom Jinja2 template directory (optional) |

**Example:**
```bash
python -m src.main.cli generate -i examples/sample_input.yaml -o /etc/nagios/conf.d/generated/
```

### `validate` — Validate input without generating
```bash
python -m src.main.cli validate -i <input.yaml>
```

This performs a dry-run, checking that the YAML input is structurally and semantically correct. No files are written.

**Example output:**
```
🔍 Validating: examples/sample_input.yaml
✅ Input is valid!
   Hosts:          4
   Services:       6
   Contacts:       3
   Contact Groups: 2
   Host Groups:    2
   Commands:       2
```

### `web` — Launch the web UI
```bash
python -m src.main.cli web --host 0.0.0.0 --port 5000 --debug
```

| Flag | Description |
|---|---|
| `--host` | Bind address (default: `0.0.0.0`) |
| `--port` | Port (default: `5000`) |
| `--debug` | Enable Flask debug mode |

### `--version`
```bash
python -m src.main.cli --version
```

---

## Web UI Usage

1. **Start the server:**
   ```bash
   python -m src.main.cli web
   ```

2. **Open http://localhost:5000** in your browser.

3. **Add Hosts** — Click "Add Host", fill in hostname, alias, IP address, and contact groups.

4. **Add Services** — Click "Add Service", select the host, description, and check command.

5. **Add Contacts** — Click "Add Contact", fill in name, alias, and email.

6. **Add Contact Groups** — (Optional) Click "Add Group" to create contact groups.

7. **Generate** — Click the "Generate Configuration Files" button.

8. **Review** — The result page shows a preview of each generated `.cfg` file.

9. **Download** — Click "Download as ZIP" to get all files in a single archive.

---

## YAML Input Format

The input file supports the following top-level keys:

### Hosts
```yaml
hosts:
  - host_name: webserver01          # Required, unique hostname
    alias: Production Web Server    # Required, human-readable name
    address: 192.168.1.10           # Required, IP or hostname
    max_check_attempts: 5           # Optional, default: 5
    check_period: 24x7              # Optional, default: 24x7
    notification_interval: 30       # Optional, default: 30 (minutes)
    notification_period: 24x7       # Optional, default: 24x7
    check_command: check-host-alive # Optional, default: check-host-alive
    contact_groups: admins          # Optional, default: admins
    hostgroups: web-servers         # Optional
```

### Services
```yaml
services:
  - host_name: webserver01           # Required
    service_description: HTTP Check  # Required
    check_command: check_http        # Required
    max_check_attempts: 4            # Optional, default: 4
    check_interval: 5                # Optional, default: 5 (minutes)
    retry_interval: 1                # Optional, default: 1 (minutes)
    check_period: 24x7               # Optional
    notification_interval: 30        # Optional
    notification_period: 24x7        # Optional
    contact_groups: admins           # Optional
```

### Contacts
```yaml
contacts:
  - contact_name: admin              # Required
    alias: System Administrator      # Required
    email: admin@example.com         # Required, valid email
    service_notification_period: 24x7
    host_notification_period: 24x7
    service_notification_options: w,u,c,r
    host_notification_options: d,u,r
    service_notification_commands: notify-service-by-email
    host_notification_commands: notify-host-by-email
```

### Contact Groups, Host Groups, Commands
```yaml
contact_groups:
  - contactgroup_name: admins
    alias: Nagios Administrators
    members: admin,devops

hostgroups:
  - hostgroup_name: web-servers
    alias: Web Servers
    members: webserver01,webserver02

commands:
  - command_name: notify-host-by-email
    command_line: /usr/bin/mail -s 'Host Alert' $CONTACTEMAIL$
```

---

## Generated Output

The tool generates up to 5 `.cfg` files:

| File | Contents |
|---|---|
| `hosts.cfg` | All `define host {}` blocks |
| `services.cfg` | All `define service {}` blocks |
| `contacts.cfg` | All `define contact {}` and `define contactgroup {}` blocks |
| `hostgroups.cfg` | All `define hostgroup {}` blocks |
| `commands.cfg` | All `define command {}` blocks |

Files are only generated if the corresponding section has data. For example, if no commands are defined, `commands.cfg` is not created.

### Deploying to Nagios
Copy the generated files to your Nagios config objects directory:
```bash
cp output/*.cfg /usr/local/nagios/etc/objects/
sudo systemctl reload nagios
```

---

## Docker Deployment

### Using Docker Compose (recommended)
```bash
cd infrastructure/docker
docker-compose up --build -d
```

### Using Docker directly
```bash
docker build -t nagiosgen -f infrastructure/docker/Dockerfile .
docker run -p 5000:5000 nagiosgen
```

### Full stack with Nagios server
```bash
cd infrastructure/docker
docker-compose --profile full up --build -d
```
This starts both the generator (port 5000) and a Nagios server (port 8080).

---

## Troubleshooting

| Issue | Solution |
|---|---|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| Port 5000 in use | Use `--port 8000` flag |
| YAML parse error | Check YAML indentation (use 2 spaces) |
| Validation error on address | Ensure IPs are valid (e.g., `192.168.1.10`) |
| Docker build fails | Ensure Docker Desktop is running |
