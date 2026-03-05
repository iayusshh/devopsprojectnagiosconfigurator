"""
Unit tests for the Nagios Configuration Generator engine.
"""

import os
import tempfile

import pytest

from src.main.models import NagiosConfig, Host, Service, Contact, ContactGroup, HostGroup, Command
from src.main.generator import NagiosGenerator


@pytest.fixture
def sample_config():
    """Create a sample NagiosConfig for testing."""
    return NagiosConfig(
        hosts=[
            Host(
                host_name="webserver01",
                alias="Web Server 01",
                address="192.168.1.10",
                contact_groups="admins",
            ),
            Host(
                host_name="dbserver01",
                alias="Database Server",
                address="192.168.1.20",
                max_check_attempts=3,
                notification_interval=15,
                contact_groups="admins,dba-team",
            ),
        ],
        services=[
            Service(
                host_name="webserver01",
                service_description="HTTP Check",
                check_command="check_http",
            ),
            Service(
                host_name="dbserver01",
                service_description="MySQL Status",
                check_command="check_tcp",
                check_interval=3,
            ),
        ],
        contacts=[
            Contact(
                contact_name="admin",
                alias="System Administrator",
                email="admin@example.com",
            ),
        ],
        contact_groups=[
            ContactGroup(
                contactgroup_name="admins",
                alias="Nagios Admins",
                members="admin",
            ),
        ],
        hostgroups=[
            HostGroup(
                hostgroup_name="web-servers",
                alias="Web Servers",
                members="webserver01",
            ),
        ],
        commands=[
            Command(
                command_name="notify-host-by-email",
                command_line="/usr/bin/mail -s 'Host Alert' $CONTACTEMAIL$",
            ),
        ],
    )


@pytest.fixture
def generator():
    """Create a NagiosGenerator instance."""
    return NagiosGenerator()


class TestNagiosGenerator:
    """Tests for the NagiosGenerator class."""

    def test_generate_returns_dict(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert isinstance(result, dict)

    def test_generate_produces_hosts_cfg(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "hosts.cfg" in result

    def test_generate_produces_services_cfg(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "services.cfg" in result

    def test_generate_produces_contacts_cfg(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "contacts.cfg" in result

    def test_generate_produces_hostgroups_cfg(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "hostgroups.cfg" in result

    def test_generate_produces_commands_cfg(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "commands.cfg" in result

    def test_hosts_cfg_contains_define_host(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "define host {" in result["hosts.cfg"]

    def test_hosts_cfg_contains_host_name(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "webserver01" in result["hosts.cfg"]
        assert "dbserver01" in result["hosts.cfg"]

    def test_hosts_cfg_contains_address(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "192.168.1.10" in result["hosts.cfg"]
        assert "192.168.1.20" in result["hosts.cfg"]

    def test_services_cfg_contains_define_service(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "define service {" in result["services.cfg"]

    def test_services_cfg_contains_check_command(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "check_http" in result["services.cfg"]
        assert "check_tcp" in result["services.cfg"]

    def test_contacts_cfg_contains_define_contact(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "define contact {" in result["contacts.cfg"]
        assert "admin@example.com" in result["contacts.cfg"]

    def test_contacts_cfg_contains_contactgroup(self, generator, sample_config):
        result = generator.generate(sample_config)
        assert "define contactgroup {" in result["contacts.cfg"]

    def test_write_creates_files(self, generator, sample_config):
        with tempfile.TemporaryDirectory() as tmpdir:
            written = generator.write(sample_config, tmpdir)
            assert len(written) > 0
            for filepath in written:
                assert os.path.isfile(filepath)

    def test_write_files_not_empty(self, generator, sample_config):
        with tempfile.TemporaryDirectory() as tmpdir:
            written = generator.write(sample_config, tmpdir)
            for filepath in written:
                assert os.path.getsize(filepath) > 0

    def test_generate_zip_returns_bytes(self, generator, sample_config):
        zip_bytes = generator.generate_zip(sample_config)
        assert isinstance(zip_bytes, bytes)
        assert len(zip_bytes) > 0

    def test_generate_zip_is_valid_zip(self, generator, sample_config):
        import zipfile
        import io
        zip_bytes = generator.generate_zip(sample_config)
        buffer = io.BytesIO(zip_bytes)
        assert zipfile.is_zipfile(buffer)

    def test_empty_config_produces_no_files(self, generator):
        config = NagiosConfig()
        result = generator.generate(config)
        assert len(result) == 0

    def test_config_with_only_hosts(self, generator):
        config = NagiosConfig(
            hosts=[Host(host_name="testhost", alias="Test", address="10.0.0.1")]
        )
        result = generator.generate(config)
        assert "hosts.cfg" in result
        assert "services.cfg" not in result


class TestNagiosConfigFromYaml:
    """Tests for loading NagiosConfig from YAML."""

    def test_from_yaml_string(self):
        yaml_content = """
hosts:
  - host_name: testhost
    alias: Test Host
    address: 10.0.0.1
services:
  - host_name: testhost
    service_description: Ping
    check_command: check_ping
"""
        config = NagiosConfig.from_yaml_string(yaml_content)
        assert len(config.hosts) == 1
        assert config.hosts[0].host_name == "testhost"
        assert len(config.services) == 1

    def test_from_yaml_file(self):
        yaml_content = """
hosts:
  - host_name: filehost
    alias: File Host
    address: 172.16.0.1
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()
            config = NagiosConfig.from_yaml(f.name)
        os.unlink(f.name)
        assert len(config.hosts) == 1
        assert config.hosts[0].address == "172.16.0.1"
