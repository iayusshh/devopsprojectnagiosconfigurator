"""
Unit tests for the CLI module using Click's test runner.
"""

import os
import tempfile

from click.testing import CliRunner

from src.main.cli import cli


class TestCLIValidate:
    """Tests for the 'validate' sub-command."""

    def test_validate_valid_file(self):
        runner = CliRunner()
        yaml_content = """
hosts:
  - host_name: testhost
    alias: Test
    address: 10.0.0.1
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()
            result = runner.invoke(cli, ["validate", "-i", f.name])
        os.unlink(f.name)
        assert result.exit_code == 0
        assert "valid" in result.output.lower()

    def test_validate_invalid_yaml(self):
        runner = CliRunner()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write("hosts:\n  - host_name: @invalid\n    address: @@@\n")
            f.flush()
            result = runner.invoke(cli, ["validate", "-i", f.name])
        os.unlink(f.name)
        # Should fail due to invalid hostname/address
        assert result.exit_code != 0

    def test_validate_nonexistent_file(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["validate", "-i", "/nonexistent/file.yaml"])
        assert result.exit_code != 0


class TestCLIGenerate:
    """Tests for the 'generate' sub-command."""

    def test_generate_produces_files(self):
        runner = CliRunner()
        yaml_content = """
hosts:
  - host_name: clihost
    alias: CLI Host
    address: 10.10.10.1
services:
  - host_name: clihost
    service_description: Ping
    check_command: check_ping
contacts:
  - contact_name: admin
    alias: Admin
    email: admin@test.com
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as f:
            f.write(yaml_content)
            f.flush()
            with tempfile.TemporaryDirectory() as outdir:
                result = runner.invoke(cli, ["generate", "-i", f.name, "-o", outdir])
                assert result.exit_code == 0
                assert "Generated" in result.output
                # Check files were created
                files = os.listdir(outdir)
                assert len(files) > 0
                assert any(f.endswith(".cfg") for f in files)
        os.unlink(f.name)

    def test_generate_with_sample_input(self):
        runner = CliRunner()
        sample_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "examples",
            "sample_input.yaml",
        )
        if os.path.exists(sample_path):
            with tempfile.TemporaryDirectory() as outdir:
                result = runner.invoke(cli, ["generate", "-i", sample_path, "-o", outdir])
                assert result.exit_code == 0
                files = os.listdir(outdir)
                assert "hosts.cfg" in files
                assert "services.cfg" in files
                assert "contacts.cfg" in files


class TestCLIVersion:
    """Test the --version flag."""

    def test_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "1.0.0" in result.output
