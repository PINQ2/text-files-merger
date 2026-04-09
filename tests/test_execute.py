import pytest
from pathlib import Path

from text_merger.execute import main


def _make_inputs(tmp_path, file1="hello\n", file2="world\n"):
    """Write two input files and return the dir path as string."""
    (tmp_path / "file1.txt").write_text(file1)
    (tmp_path / "file2.txt").write_text(file2)
    return str(tmp_path)


class TestInputNameEnvVars:
    def test_merges_two_files(self, tmp_path, monkeypatch):
        input_dir = _make_inputs(tmp_path)
        monkeypatch.setenv("KIT_INPUTS_FILE", input_dir)
        monkeypatch.setenv("INPUT_1_NAME", "file1.txt")
        monkeypatch.setenv("INPUT_2_NAME", "file2.txt")
        main()
        result = (Path("/tmp/outputs") / "output.txt").read_text()
        assert result == "hello\nworld\n"

    def test_missing_input_1_name_crashes(self, tmp_path, monkeypatch):
        monkeypatch.setenv("KIT_INPUTS_FILE", str(tmp_path))
        monkeypatch.delenv("INPUT_1_NAME", raising=False)
        monkeypatch.setenv("INPUT_2_NAME", "file2.txt")
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_empty_input_1_name_crashes(self, tmp_path, monkeypatch):
        monkeypatch.setenv("KIT_INPUTS_FILE", str(tmp_path))
        monkeypatch.setenv("INPUT_1_NAME", "")
        monkeypatch.setenv("INPUT_2_NAME", "file2.txt")
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_missing_input_2_name_crashes(self, tmp_path, monkeypatch):
        monkeypatch.setenv("KIT_INPUTS_FILE", str(tmp_path))
        monkeypatch.setenv("INPUT_1_NAME", "file1.txt")
        monkeypatch.delenv("INPUT_2_NAME", raising=False)
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_empty_input_2_name_crashes(self, tmp_path, monkeypatch):
        monkeypatch.setenv("KIT_INPUTS_FILE", str(tmp_path))
        monkeypatch.setenv("INPUT_1_NAME", "file1.txt")
        monkeypatch.setenv("INPUT_2_NAME", "")
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1

    def test_missing_kit_inputs_file_crashes(self, monkeypatch):
        """Existing KIT_INPUTS_FILE guard still works."""
        monkeypatch.delenv("KIT_INPUTS_FILE", raising=False)
        monkeypatch.setenv("INPUT_1_NAME", "file1.txt")
        monkeypatch.setenv("INPUT_2_NAME", "file2.txt")
        with pytest.raises(SystemExit) as exc_info:
            main()
        assert exc_info.value.code == 1
