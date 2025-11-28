import os
import sys
import json
import argparse
import logging

# Ensure src is importable when running from repo root
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from logging_config import configure_logging
from repository.repository import Repository

# Parse a minimal set of CLI args (allow --logfile) before starting interactive menu
_argp = argparse.ArgumentParser(add_help=False)
_argp.add_argument("--logfile", help="Path to logfile for quick_manage (optional)")
_known, _rest = _argp.parse_known_args()
if _known.logfile:
    log_dir = os.path.dirname(_known.logfile) or None
    log_name = os.path.basename(_known.logfile)
    configure_logging(level=logging.INFO, log_dir=log_dir, logfile_name=log_name)
    # Compute the effective logfile path to show the user
    if os.path.dirname(_known.logfile):
        effective_logfile = os.path.abspath(_known.logfile)
    else:
        project_root = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
        effective_logfile = os.path.join(project_root, 'logs', log_name)
    print(f"Logging to: {effective_logfile}")
else:
    configure_logging()
    # Default logfile path used by configure_logging()
    project_root = os.path.abspath(os.path.join(SCRIPT_DIR, '..'))
    print(f"Logging to: {os.path.join(project_root, 'logs', 'fitness_tracker.log')}")

repo = Repository()


def list_all():
    records = repo.read_all()
    print(json.dumps(records, indent=2, ensure_ascii=False))


def list_schedules():
    schedules = repo.find_by_type("schedule")
    if not schedules:
        print("No schedules found")
        return
    for s in schedules:
        data = s.get("data", {})
        user_id = data.get("user_id")
        workout_id = data.get("workout_id")
        user = repo.get_object_by_id(user_id) if user_id else None
        workout = repo.get_object_by_id(workout_id) if workout_id else None
        user_summary = user.get_info() if user and hasattr(user, "get_info") else (user_id or "Unknown user")
        workout_summary = workout.get_summary() if workout and hasattr(workout, "get_summary") else (workout_id or "Unknown workout")
        print(f"Schedule id={s.get('id')}: {user_summary} -> {workout_summary}")


def get_record():
    rid = input("Record id: ").strip()
    if not rid:
        print("No id provided")
        return
    r = repo.read_by_id(rid)
    if not r:
        print("Record not found")
        return
    print(json.dumps(r, indent=2, ensure_ascii=False))
    obj = repo.get_object_by_id(rid)
    if obj:
        if hasattr(obj, "get_info"):
            print(obj.get_info())
        elif hasattr(obj, "get_summary"):
            print(obj.get_summary())


def create_user():
    username = input("Username: ").strip()
    if not username:
        print("Username required")
        return
    age = input("Age (int): ").strip()
    try:
        age_val = int(age)
    except Exception:
        print("Invalid age")
        return
    height = input("Height (optional, float): ").strip()
    weight = input("Weight (optional, float): ").strip()
    data = {"username": username, "age": age_val}
    if height:
        try:
            data["height"] = float(height)
        except Exception:
            print("Ignoring invalid height")
    if weight:
        try:
            data["weight"] = float(weight)
        except Exception:
            print("Ignoring invalid weight")
    rid = repo.create(data, type_="user")
    print(f"Created user id={rid}")


def create_workout():
    name = input("Workout name: ").strip()
    if not name:
        print("Name required")
        return
    duration = input("Duration (minutes, int): ").strip()
    try:
        dur = int(duration)
    except Exception:
        print("Invalid duration")
        return
    rid = repo.create({"name": name, "duration": dur}, type_="workout")
    print(f"Created workout id={rid}")


def update_user():
    rid = input("User id: ").strip()
    r = repo.read_by_id(rid)
    if not r or r.get("type") != "user":
        print("User not found")
        return
    data = dict(r.get("data", {}))
    print("Press Enter to keep current value")
    username = input(f"Username [{data.get('username')}]: ").strip()
    age = input(f"Age [{data.get('age')}]: ").strip()
    height = input(f"Height [{data.get('height', '')}]: ").strip()
    weight = input(f"Weight [{data.get('weight', '')}]: ").strip()
    if username:
        data['username'] = username
    if age:
        try:
            data['age'] = int(age)
        except Exception:
            print("Invalid age input; keeping existing")
    if height:
        try:
            data['height'] = float(height)
        except Exception:
            print("Invalid height; keeping existing")
    if weight:
        try:
            data['weight'] = float(weight)
        except Exception:
            print("Invalid weight; keeping existing")
    ok = repo.update(rid, data)
    print(f"Updated: {ok}")
    if ok:
        print(repo.read_by_id(rid))


def update_workout():
    rid = input("Workout id: ").strip()
    r = repo.read_by_id(rid)
    if not r or r.get("type") != "workout":
        print("Workout not found")
        return
    data = dict(r.get("data", {}))
    print("Press Enter to keep current value")
    name = input(f"Name [{data.get('name')}]: ").strip()
    duration = input(f"Duration [{data.get('duration')}]: ").strip()
    if name:
        data['name'] = name
    if duration:
        try:
            data['duration'] = int(duration)
        except Exception:
            print("Invalid duration; keeping existing")
    ok = repo.update(rid, data)
    print(f"Updated: {ok}")
    if ok:
        print(repo.read_by_id(rid))


def delete_record():
    rid = input("Record id to delete: ").strip()
    if not rid:
        print("No id provided")
        return
    r = repo.read_by_id(rid)
    if not r:
        print("Record not found")
        return
    confirm = input(f"Delete id={rid} type={r.get('type')}? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Aborted")
        return
    ok = repo.delete(rid)
    print(f"Deleted: {ok}")


def schedule_workout():
    user_id = input("User id: ").strip()
    workout_id = input("Workout id: ").strip()
    user = repo.read_by_id(user_id)
    workout = repo.read_by_id(workout_id)
    if not user or user.get('type') != 'user':
        print("User not found")
        return
    if not workout or workout.get('type') != 'workout':
        print("Workout not found")
        return
    rid = repo.create({"user_id": user_id, "workout_id": workout_id}, type_='schedule')
    print(f"Scheduled id={rid}")


def show_templates():
    examples = [
        ("Create user",
         "python main.py create-user --username Ali --age 30 --height 180 --weight 75"),
        ("Create workout",
         "python main.py create-workout --name \"Leg Day\" --duration 60"),
        ("List all records",
         "python main.py list"),
        ("Get record by id",
         "python main.py get --id <record_id>"),
        ("Update user (typed)",
         "python main.py update-user --id <user_id> --username NewName --height 175"),
        ("Update workout (typed)",
         "python main.py update-workout --id <workout_id> --duration 65"),
        ("Generic update using --set",
         "python main.py update --id <id> --set age=31 --set extra=val"),
        ("Delete (interactive)",
         "python main.py delete --id <id>"),
        ("Delete (no prompt)",
         "python main.py delete --id <id> --yes"),
        ("Schedule workout",
         "python main.py schedule --user-id <user_id> --workout-id <workout_id>"),
        ("Run interactive quick manager",
         "python scripts/quick_manage.py")
    ]
    print("\nCommand templates (copy & paste into PowerShell). Replace <...> with actual ids:\n")
    for title, cmd in examples:
        print(f"- {title}:\n    {cmd}\n")


MENU = [
    ("List all records", list_all),
    ("List schedules (readable)", list_schedules),
    ("Show command templates (copy/paste)", None),
    ("Get record by id", get_record),
    ("Create user", create_user),
    ("Create workout", create_workout),
    ("Update user", update_user),
    ("Update workout", update_workout),
    ("Delete record", delete_record),
    ("Schedule workout", schedule_workout),
    ("Exit", None),
]


def main():
    while True:
        print("\nQuick Manage Menu:")
        for i, (label, _) in enumerate(MENU, start=1):
            print(f" {i}. {label}")
        choice = input("Choose an option: ").strip()
        if not choice.isdigit():
            print("Invalid choice")
            continue
        idx = int(choice) - 1
        if idx < 0 or idx >= len(MENU):
            print("Invalid choice")
            continue
        if MENU[idx][1] is None:
            # Special case: templates entry at fixed position
            if MENU[idx][0].startswith("Show command templates"):
                show_templates()
                continue
            print("Bye")
            break
        try:
            MENU[idx][1]()
        except Exception as e:
            print(f"Error executing action: {e}")


if __name__ == '__main__':
    main()
