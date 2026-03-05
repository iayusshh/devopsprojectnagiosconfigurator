"""
Unit tests for the validators module.
"""

from src.main.validators import (
    validate_ip_address,
    validate_hostname,
    validate_email,
    validate_address,
    validate_threshold,
    validate_check_period,
    validate_yaml_input,
)


class TestValidateIPAddress:
    def test_valid_ipv4(self):
        valid, msg = validate_ip_address("192.168.1.1")
        assert valid is True

    def test_valid_ipv4_localhost(self):
        valid, msg = validate_ip_address("127.0.0.1")
        assert valid is True

    def test_valid_ipv6(self):
        valid, msg = validate_ip_address("::1")
        assert valid is True

    def test_invalid_ip(self):
        valid, msg = validate_ip_address("999.999.999.999")
        assert valid is False

    def test_empty_string(self):
        valid, msg = validate_ip_address("")
        assert valid is False

    def test_hostname_not_ip(self):
        valid, msg = validate_ip_address("webserver01")
        assert valid is False


class TestValidateHostname:
    def test_valid_hostname(self):
        valid, msg = validate_hostname("webserver01")
        assert valid is True

    def test_valid_fqdn(self):
        valid, msg = validate_hostname("web.example.com")
        assert valid is True

    def test_valid_with_hyphens(self):
        valid, msg = validate_hostname("my-server-01")
        assert valid is True

    def test_invalid_starts_with_hyphen(self):
        valid, msg = validate_hostname("-invalid")
        assert valid is False

    def test_invalid_too_long(self):
        valid, msg = validate_hostname("a" * 64)
        assert valid is False

    def test_invalid_special_chars(self):
        valid, msg = validate_hostname("server@01")
        assert valid is False


class TestValidateEmail:
    def test_valid_email(self):
        valid, msg = validate_email("admin@example.com")
        assert valid is True

    def test_valid_email_with_dots(self):
        valid, msg = validate_email("first.last@domain.co.uk")
        assert valid is True

    def test_invalid_no_at(self):
        valid, msg = validate_email("notanemail")
        assert valid is False

    def test_invalid_no_domain(self):
        valid, msg = validate_email("user@")
        assert valid is False


class TestValidateAddress:
    def test_valid_ip(self):
        valid, msg = validate_address("10.0.0.1")
        assert valid is True

    def test_valid_hostname(self):
        valid, msg = validate_address("myserver")
        assert valid is True

    def test_invalid_both(self):
        valid, msg = validate_address("@@@")
        assert valid is False


class TestValidateThreshold:
    def test_within_range(self):
        valid, msg = validate_threshold(5, 1, 10, "test")
        assert valid is True

    def test_at_min(self):
        valid, msg = validate_threshold(1, 1, 10, "test")
        assert valid is True

    def test_at_max(self):
        valid, msg = validate_threshold(10, 1, 10, "test")
        assert valid is True

    def test_below_min(self):
        valid, msg = validate_threshold(0, 1, 10, "test")
        assert valid is False

    def test_above_max(self):
        valid, msg = validate_threshold(11, 1, 10, "test")
        assert valid is False


class TestValidateCheckPeriod:
    def test_valid_24x7(self):
        valid, msg = validate_check_period("24x7")
        assert valid is True

    def test_valid_workhours(self):
        valid, msg = validate_check_period("workhours")
        assert valid is True

    def test_invalid_period(self):
        valid, msg = validate_check_period("allday")
        assert valid is False


class TestValidateYamlInput:
    def test_valid_input(self):
        data = {
            "hosts": [{"host_name": "test", "address": "10.0.0.1"}],
            "services": [{"host_name": "test", "service_description": "HTTP", "check_command": "check_http"}],
            "contacts": [{"contact_name": "admin", "email": "admin@test.com"}],
        }
        valid, errors = validate_yaml_input(data)
        assert valid is True
        assert len(errors) == 0

    def test_missing_host_name(self):
        data = {"hosts": [{"address": "10.0.0.1"}]}
        valid, errors = validate_yaml_input(data)
        assert valid is False
        assert any("host_name" in e for e in errors)

    def test_missing_address(self):
        data = {"hosts": [{"host_name": "test"}]}
        valid, errors = validate_yaml_input(data)
        assert valid is False
        assert any("address" in e for e in errors)

    def test_invalid_address(self):
        data = {"hosts": [{"host_name": "test", "address": "@@@"}]}
        valid, errors = validate_yaml_input(data)
        assert valid is False

    def test_unknown_keys(self):
        data = {"hosts": [], "unknown_key": []}
        valid, errors = validate_yaml_input(data)
        assert valid is False
        assert any("Unknown" in e for e in errors)

    def test_missing_service_fields(self):
        data = {"services": [{"host_name": "test"}]}
        valid, errors = validate_yaml_input(data)
        assert valid is False

    def test_invalid_contact_email(self):
        data = {"contacts": [{"contact_name": "admin", "email": "bademail"}]}
        valid, errors = validate_yaml_input(data)
        assert valid is False

    def test_empty_input(self):
        data = {}
        valid, errors = validate_yaml_input(data)
        assert valid is True
