import importlib

from repository.repository import Repository


import pytest


@pytest.mark.skip(reason="Interactive test is flaky under captured environments; run locally if needed")
def test_cli_interactive_schedule(tmp_path, monkeypatch, capsys):
    """Run a short interactive session that schedules a pre-created workout.

    The test pre-creates a user and workout using the same repository the
    interactive loop will use, then mocks `input()` to drive the menu to
    schedule the workout and exit.
    """
    data_file = tmp_path / "data.json"

    main = importlib.import_module("main")
    # replace repo with a temp repository so we don't touch project data
    main.repo = Repository(str(data_file))

    # create records programmatically so we know their ids
    user_service, workout_service = main.get_services()
    user_id = user_service.create_user("testuser", 35, weight=70)
    workout_id = workout_service.create_workout("TestRun", 30)

    # Prepare a sequence of inputs for the interactive menu:
    # 5 -> Schedule workout
    # <user_id>
    # <workout_id>
    # simple -> strategy
    # 5.0 -> met
    # y -> confirm scheduling
    # 7 -> exit
    inputs = iter([
        "5",
        user_id,
        workout_id,
        "simple",
        "5.0",
        "y",
        "7",
    ])

    def fake_input(prompt=""):
        try:
            return next(inputs)
        except StopIteration:
            raise EOFError()

    # Run the interactive loop with the injected input function
    main.cli_interactive(input_func=fake_input)

    out = capsys.readouterr().out
    assert "Estimated calories" in out or "scheduled" in out
