import sys
from repository.repository import Repository
import main


def test_main_default_demo(tmp_path, monkeypatch, capsys):
    datafile = tmp_path / "data.json"
    repo = Repository(str(datafile))
    # replace the module-level repo with a tmp repository to avoid touching project files
    monkeypatch.setattr(main, "repo", repo)
    # ensure get_services() will bind to the new repo when called
    monkeypatch.setattr(main, "user_service", main.get_services()[0])
    monkeypatch.setattr(main, "workout_service", main.get_services()[1])
    monkeypatch.setattr(sys, "argv", ["prog"])

    # Ensure parse_args() yields an empty Namespace so main() executes the default demo branch
    import argparse

    class DummyParser:
        def parse_args(self):
            return argparse.Namespace()

    monkeypatch.setattr(main, "build_parser", lambda: DummyParser())

    # call main which should take the default demo branch when no args provided
    main.main()

    # some environments capture stdout differently; focus on verifying persistence
    records = repo.read_all()
    assert records, "Expected demo records to be persisted to the temporary repo"
    assert records[0]["type"] == "demo"
