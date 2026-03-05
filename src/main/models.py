"""
Pydantic data models for Nagios configuration objects.

Each model represents a Nagios configuration directive and can be
serialized from YAML input to render Jinja2 templates.
"""

from __future__ import annotations

import ipaddress
import re
from typing import List, Optional

import yaml
from pydantic import BaseModel, field_validator


class Host(BaseModel):
    """Represents a Nagios host definition."""
    host_name: str
    alias: str
    address: str
    max_check_attempts: int = 5
    check_period: str = "24x7"
    notification_interval: int = 30
    notification_period: str = "24x7"
    check_command: str = "check-host-alive"
    contact_groups: str = "admins"
    hostgroups: Optional[str] = None

    @field_validator("host_name")
    @classmethod
    def validate_hostname(cls, v: str) -> str:
        pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,62}$")
        if not pattern.match(v):
            raise ValueError(
                f"Invalid hostname '{v}': must start with alphanumeric, "
                "contain only alphanumeric/dot/hyphen/underscore, max 63 chars"
            )
        return v

    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        try:
            ipaddress.ip_address(v)
        except ValueError:
            # Allow hostnames as addresses too
            pattern = re.compile(
                r"^[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?"
                r"(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
            )
            if not pattern.match(v):
                raise ValueError(f"Invalid address '{v}': must be IP or hostname")
        return v

    @field_validator("max_check_attempts")
    @classmethod
    def validate_max_checks(cls, v: int) -> int:
        if not 1 <= v <= 100:
            raise ValueError("max_check_attempts must be between 1 and 100")
        return v

    @field_validator("notification_interval")
    @classmethod
    def validate_notif_interval(cls, v: int) -> int:
        if v < 0:
            raise ValueError("notification_interval must be non-negative")
        return v


class Service(BaseModel):
    """Represents a Nagios service definition."""
    host_name: str
    service_description: str
    check_command: str
    max_check_attempts: int = 4
    check_interval: int = 5
    retry_interval: int = 1
    check_period: str = "24x7"
    notification_interval: int = 30
    notification_period: str = "24x7"
    contact_groups: str = "admins"

    @field_validator("check_interval", "retry_interval")
    @classmethod
    def validate_intervals(cls, v: int) -> int:
        if v < 1:
            raise ValueError("Interval must be at least 1")
        return v


class Contact(BaseModel):
    """Represents a Nagios contact definition."""
    contact_name: str
    alias: str
    email: str
    service_notification_period: str = "24x7"
    host_notification_period: str = "24x7"
    service_notification_options: str = "w,u,c,r"
    host_notification_options: str = "d,u,r"
    service_notification_commands: str = "notify-service-by-email"
    host_notification_commands: str = "notify-host-by-email"

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if not pattern.match(v):
            raise ValueError(f"Invalid email '{v}'")
        return v


class ContactGroup(BaseModel):
    """Represents a Nagios contact group definition."""
    contactgroup_name: str
    alias: str
    members: str


class HostGroup(BaseModel):
    """Represents a Nagios hostgroup definition."""
    hostgroup_name: str
    alias: str
    members: str


class Command(BaseModel):
    """Represents a Nagios command definition."""
    command_name: str
    command_line: str


class NagiosConfig(BaseModel):
    """Top-level container holding all Nagios configuration objects."""
    hosts: List[Host] = []
    services: List[Service] = []
    contacts: List[Contact] = []
    contact_groups: List[ContactGroup] = []
    hostgroups: List[HostGroup] = []
    commands: List[Command] = []

    @classmethod
    def from_yaml(cls, path: str) -> "NagiosConfig":
        """Load configuration from a YAML file."""
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    @classmethod
    def from_yaml_string(cls, content: str) -> "NagiosConfig":
        """Load configuration from a YAML string."""
        data = yaml.safe_load(content)
        return cls(**data)

    @classmethod
    def from_dict(cls, data: dict) -> "NagiosConfig":
        """Load configuration from a dictionary."""
        return cls(**data)
