"""
Integration tests for the Nagios Configuration Generator.
"""
import os
import tempfile
from pathlib import Path

from click.testing import CliRunner

from src.main.cli import generate


def test_end_to_end_generation():
    """
    Test the full generation pipeline from YAML input to final .cfg files.
    This simulates the CLI execution end-to-end and verifies the outputs.
    """
    runner = CliRunner()
    
    # Path to the sample input included in the repository
    sample_input = Path(__file__).parent.parent.parent / "examples" / "sample_input.yaml"
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Run the generate command
        result = runner.invoke(generate, ["-i", str(sample_input), "-o", temp_dir])
        
        # Verify execution succeeded
        assert result.exit_code == 0
        assert "Generated 5 config file(s)" in result.output
        
        # Verify all expected files were created
        expected_files = [
            "hosts.cfg",
            "services.cfg",
            "contacts.cfg",
            "hostgroups.cfg",
            "commands.cfg",
        ]
        
        for file in expected_files:
            file_path = os.path.join(temp_dir, file)
            assert os.path.exists(file_path), f"Expected {file} to be generated"
            
            # Briefly verify content isn't empty
            with open(file_path, "r") as f:
                content = f.read()
                assert len(content) > 50, f"{file} seems suspiciously empty"
                assert "define " in content, f"{file} does not contain valid Nagios definitions"
