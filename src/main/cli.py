"""
Click-based CLI for the Nagios Configuration Generator.

Provides commands:
  - generate: Read YAML input, produce .cfg files
  - validate: Dry-run validation of YAML input
  - web: Launch the Flask web UI
"""

import sys
from typing import Optional

import click
import yaml

from src.main.models import NagiosConfig
from src.main.generator import NagiosGenerator
from src.main.validators import validate_yaml_input


@click.group()
@click.version_option(version="1.0.0", prog_name="nagiosgen")
def cli():
    """Nagios Configuration Generator — Generate valid .cfg files from YAML input."""
    pass


@cli.command()
@click.option(
    "-i", "--input", "input_file",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="Path to the YAML input file.",
)
@click.option(
    "-o", "--output", "output_dir",
    required=True,
    type=click.Path(),
    help="Directory to write generated .cfg files to.",
)
@click.option(
    "--template-dir",
    default=None,
    type=click.Path(exists=True),
    help="Custom Jinja2 template directory (optional).",
)
def generate(input_file: str, output_dir: str, template_dir: Optional[str]):
    """Generate Nagios .cfg files from a YAML input file."""
    click.echo(f"📖 Reading input from: {input_file}")

    try:
        with open(input_file, "r") as f:
            raw_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        click.echo(f"❌ YAML parse error: {e}", err=True)
        sys.exit(1)

    # Pre-validate
    valid, errors = validate_yaml_input(raw_data)
    if not valid:
        click.echo("❌ Validation errors:", err=True)
        for err in errors:
            click.echo(f"   • {err}", err=True)
        sys.exit(1)

    # Build config model
    try:
        config = NagiosConfig.from_dict(raw_data)
    except Exception as e:
        click.echo(f"❌ Configuration error: {e}", err=True)
        sys.exit(1)

    # Generate files
    generator = NagiosGenerator(template_dir)
    written = generator.write(config, output_dir)

    click.echo(f"\n✅ Generated {len(written)} config file(s) in: {output_dir}")
    for path in written:
        click.echo(f"   📄 {path}")


@cli.command()
@click.option(
    "-i", "--input", "input_file",
    required=True,
    type=click.Path(exists=True, readable=True),
    help="Path to the YAML input file to validate.",
)
def validate(input_file: str):
    """Validate a YAML input file without generating configs."""
    click.echo(f"🔍 Validating: {input_file}")

    try:
        with open(input_file, "r") as f:
            raw_data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        click.echo(f"❌ YAML parse error: {e}", err=True)
        sys.exit(1)

    # Pre-validate structure
    valid, errors = validate_yaml_input(raw_data)
    if not valid:
        click.echo("❌ Validation errors:", err=True)
        for err in errors:
            click.echo(f"   • {err}", err=True)
        sys.exit(1)

    # Full model validation
    try:
        config = NagiosConfig.from_dict(raw_data)
    except Exception as e:
        click.echo(f"❌ Model validation error: {e}", err=True)
        sys.exit(1)

    click.echo("✅ Input is valid!")
    click.echo(f"   Hosts:          {len(config.hosts)}")
    click.echo(f"   Services:       {len(config.services)}")
    click.echo(f"   Contacts:       {len(config.contacts)}")
    click.echo(f"   Contact Groups: {len(config.contact_groups)}")
    click.echo(f"   Host Groups:    {len(config.hostgroups)}")
    click.echo(f"   Commands:       {len(config.commands)}")


@cli.command()
@click.option("--host", default="0.0.0.0", help="Host to bind to.")
@click.option("--port", default=5000, type=int, help="Port to listen on.")
@click.option("--debug", is_flag=True, help="Enable Flask debug mode.")
def web(host: str, port: int, debug: bool):
    """Launch the Flask web UI."""
    click.echo(f"🌐 Starting Nagios Config Generator Web UI on {host}:{port}")
    from src.main.web import app
    app.run(host=host, port=port, debug=debug)


if __name__ == "__main__":
    cli()
