import importlib

from repository.repository import Repository


def test_cli_schedule_with_simple_strategy(tmp_path, capsys):
    data_file = tmp_path / "data.json"

    # import main and swap repo to temp file
    main = importlib.import_module("main")
    main.repo = Repository(str(data_file))

    parser = main.build_parser()

    # create user and workout
    args = parser.parse_args(["create-user", "--username", "sam", "--age", "25", "--weight", "70"])
    args.func(args)
    args = parser.parse_args(["create-workout", "--name", "Run", "--duration", "30"])
    args.func(args)

    records = main.repo.read_all()
    user_id = next(r["id"] for r in records if r["type"] == "user")
    workout_id = next(r["id"] for r in records if r["type"] == "workout")

    # schedule with simple strategy and MET parameter
    args = parser.parse_args([
        "schedule",
        "--user-id",
        user_id,
        "--workout-id",
        workout_id,
        "--strategy",
        "simple",
        "--met",
        "5.0",
    ])
    args.func(args)
    captured = capsys.readouterr()
    assert "Estimated calories" in captured.out


def test_cli_schedule_with_constant_strategy(tmp_path, capsys):
    data_file = tmp_path / "data.json"

    main = importlib.import_module("main")
    main.repo = Repository(str(data_file))
    parser = main.build_parser()

    args = parser.parse_args(["create-user", "--username", "lee", "--age", "29", "--weight", "80"])
    args.func(args)
    args = parser.parse_args(["create-workout", "--name", "Walk", "--duration", "20"])
    args.func(args)

    records = main.repo.read_all()
    user_id = next(r["id"] for r in records if r["type"] == "user")
    workout_id = next(r["id"] for r in records if r["type"] == "workout")

    args = parser.parse_args([
        "schedule",
        "--user-id",
        user_id,
        "--workout-id",
        workout_id,
        "--strategy",
        "constant",
        "--rate-per-min",
        "4.0",
    ])
    args.func(args)
    captured = capsys.readouterr()
    assert "Estimated calories" in captured.out
