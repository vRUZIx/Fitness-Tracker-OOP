import json
import sys
from models.factory import ObjectFactory
from repository.repository import Repository


def test_cli_create_list_get_and_schedule(tmp_path, capsys):
    # prepare temp data file and replace repo in main
    data_file = tmp_path / "data.json"

    import importlib

    # import main module
    main = importlib.import_module("main")

    # replace the repo with one pointed at temp file
    main.repo = Repository(str(data_file))

    parser = main.build_parser()

    # create user
    args = parser.parse_args([
        "create-user",
        "--username",
        "alice",
        "--age",
        "30",
    ])
    args.func(args)

    # create workout
    args = parser.parse_args([
        "create-workout",
        "--name",
        "Leg Day",
        "--duration",
        "45",
    ])
    args.func(args)

    # read records from repo
    records = main.repo.read_all()
    assert any(r.get("type") == "user" for r in records)
    assert any(r.get("type") == "workout" for r in records)

    # find ids
    user_id = next(r["id"] for r in records if r["type"] == "user")
    workout_id = next(r["id"] for r in records if r["type"] == "workout")

    # list command - capture output
    args = parser.parse_args(["list"])
    args.func(args)

    # get user
    args = parser.parse_args(["get", "--id", user_id])
    args.func(args)

    # schedule
    args = parser.parse_args(["schedule", "--user-id", user_id, "--workout-id", workout_id])
    args.func(args)

    # ensure schedule produced expected string by calling scheduler directly
    user_obj = main.repo.get_object_by_id(user_id)
    workout_obj = main.repo.get_object_by_id(workout_id)
    assert main.scheduler.schedule_workout(user_obj, workout_obj).endswith(workout_obj.name)
