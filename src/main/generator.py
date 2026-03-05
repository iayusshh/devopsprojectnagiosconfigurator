"""
Nagios Configuration Generator Engine.

Uses Jinja2 templates to render valid Nagios .cfg files from
structured NagiosConfig data models.
"""

from __future__ import annotations

import os
import zipfile
import io
from typing import Dict, List, Optional

from jinja2 import Environment, FileSystemLoader

from src.main.models import NagiosConfig


# Resolve template directory relative to this file
_TEMPLATE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "templates",
    "nagios",
)


class NagiosGenerator:
    """Generates Nagios .cfg configuration files from templates.

    Attributes:
        env: The Jinja2 template environment.
    """

    # Mapping of template file -> output config file
    TEMPLATE_MAP: Dict[str, str] = {
        "hosts.cfg.j2": "hosts.cfg",
        "services.cfg.j2": "services.cfg",
        "contacts.cfg.j2": "contacts.cfg",
        "hostgroups.cfg.j2": "hostgroups.cfg",
        "commands.cfg.j2": "commands.cfg",
    }

    def __init__(self, template_dir: Optional[str] = None):
        """Initialize the generator with a Jinja2 template directory.

        Args:
            template_dir: Path to the directory containing .j2 templates.
                          Defaults to templates/nagios/ relative to project root.
        """
        tpl_dir = template_dir or _TEMPLATE_DIR
        self.env = Environment(
            loader=FileSystemLoader(tpl_dir),
            keep_trailing_newline=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def generate(self, config: NagiosConfig) -> Dict[str, str]:
        """Render all Nagios config files from the given configuration.

        Args:
            config: A fully validated NagiosConfig object.

        Returns:
            Dictionary mapping output filename to rendered content.
        """
        results: Dict[str, str] = {}

        # Map of template name -> context variable name -> data
        context_map = {
            "hosts.cfg.j2": {"hosts": config.hosts},
            "services.cfg.j2": {"services": config.services},
            "contacts.cfg.j2": {
                "contacts": config.contacts,
                "contact_groups": config.contact_groups,
            },
            "hostgroups.cfg.j2": {"hostgroups": config.hostgroups},
            "commands.cfg.j2": {"commands": config.commands},
        }

        for template_name, output_name in self.TEMPLATE_MAP.items():
            ctx = context_map.get(template_name, {})
            # Skip templates with no data
            has_data = any(
                (isinstance(v, list) and len(v) > 0) for v in ctx.values()
            )
            if not has_data:
                continue

            template = self.env.get_template(template_name)
            rendered = template.render(**ctx)
            results[output_name] = rendered

        return results

    def write(self, config: NagiosConfig, output_dir: str) -> List[str]:
        """Generate and write .cfg files to the output directory.

        Args:
            config: A fully validated NagiosConfig object.
            output_dir: Directory to write .cfg files to.

        Returns:
            List of file paths that were written.
        """
        os.makedirs(output_dir, exist_ok=True)
        rendered = self.generate(config)
        written_files: List[str] = []

        for filename, content in rendered.items():
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "w") as f:
                f.write(content)
            written_files.append(filepath)

        return written_files

    def generate_zip(self, config: NagiosConfig) -> bytes:
        """Generate .cfg files and package them into a ZIP archive.

        Args:
            config: A fully validated NagiosConfig object.

        Returns:
            Bytes of the ZIP file.
        """
        rendered = self.generate(config)
        buffer = io.BytesIO()

        with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for filename, content in rendered.items():
                zf.writestr(f"nagios_configs/{filename}", content)

        return buffer.getvalue()
