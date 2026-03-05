"""
Input validation utilities for Nagios configuration data.

Provides standalone validation functions used by both the CLI and web UI
for pre-checking user input before it reaches the Pydantic models.
"""

import ipaddress
import re
from typing import List, Tuple


def validate_ip_address(address: str) -> Tuple[bool, str]:
    """Validate an IP address string.

    Returns:
        Tuple of (is_valid, error_message).
    """
    try:
        ipaddress.ip_address(address)
        return True, ""
    except ValueError:
        return False, f"'{address}' is not a valid IP address"


def validate_hostname(hostname: str) -> Tuple[bool, str]:
    """Validate a hostname string.

    Returns:
        Tuple of (is_valid, error_message).
    """
    pattern = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._-]{0,62}$")
    if not pattern.match(hostname):
        return False, (
            f"'{hostname}' is not a valid hostname. "
            "Must start with alphanumeric, max 63 chars."
        )
    return True, ""


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate an email address string.

    Returns:
        Tuple of (is_valid, error_message).
    """
    pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    if not pattern.match(email):
        return False, f"'{email}' is not a valid email address"
    return True, ""


def validate_address(address: str) -> Tuple[bool, str]:
    """Validate an address that can be either IP or hostname.

    Returns:
        Tuple of (is_valid, error_message).
    """
    ip_valid, _ = validate_ip_address(address)
    if ip_valid:
        return True, ""

    host_valid, _ = validate_hostname(address)
    if host_valid:
        return True, ""

    return False, f"'{address}' is neither a valid IP address nor a valid hostname"


def validate_threshold(value: int, min_val: int, max_val: int,
                       field_name: str) -> Tuple[bool, str]:
    """Validate a numeric threshold is within range.

    Returns:
        Tuple of (is_valid, error_message).
    """
    if not min_val <= value <= max_val:
        return False, f"'{field_name}' must be between {min_val} and {max_val}, got {value}"
    return True, ""


def validate_check_period(period: str) -> Tuple[bool, str]:
    """Validate a Nagios time period name.

    Returns:
        Tuple of (is_valid, error_message).
    """
    valid_periods = ["24x7", "workhours", "nonworkhours", "never"]
    if period not in valid_periods:
        return False, (
            f"'{period}' is not a recognized time period. "
            f"Valid options: {', '.join(valid_periods)}"
        )
    return True, ""


def validate_yaml_input(data: dict) -> Tuple[bool, List[str]]:
    """Validate a complete YAML input dictionary.

    Returns:
        Tuple of (is_valid, list_of_error_messages).
    """
    errors: List[str] = []

    # Check required top-level keys
    valid_keys = {"hosts", "services", "contacts", "contact_groups",
                  "hostgroups", "commands"}
    unknown_keys = set(data.keys()) - valid_keys
    if unknown_keys:
        errors.append(f"Unknown top-level keys: {', '.join(unknown_keys)}")

    # Validate hosts
    for i, host in enumerate(data.get("hosts", [])):
        if "host_name" not in host:
            errors.append(f"Host #{i + 1}: missing 'host_name'")
        if "address" not in host:
            errors.append(f"Host #{i + 1}: missing 'address'")
        elif "address" in host:
            valid, msg = validate_address(host["address"])
            if not valid:
                errors.append(f"Host #{i + 1}: {msg}")

    # Validate services
    for i, svc in enumerate(data.get("services", [])):
        if "host_name" not in svc:
            errors.append(f"Service #{i + 1}: missing 'host_name'")
        if "service_description" not in svc:
            errors.append(f"Service #{i + 1}: missing 'service_description'")
        if "check_command" not in svc:
            errors.append(f"Service #{i + 1}: missing 'check_command'")

    # Validate contacts
    for i, contact in enumerate(data.get("contacts", [])):
        if "contact_name" not in contact:
            errors.append(f"Contact #{i + 1}: missing 'contact_name'")
        if "email" not in contact:
            errors.append(f"Contact #{i + 1}: missing 'email'")
        elif "email" in contact:
            valid, msg = validate_email(contact["email"])
            if not valid:
                errors.append(f"Contact #{i + 1}: {msg}")

    return len(errors) == 0, errors
