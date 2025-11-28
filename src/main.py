import argparse
import os
import logging
from models.factory import ObjectFactory
from repository.repository import Repository
from services.scheduler import Scheduler
from logging_config import configure_logging

# Will be initialized in main() after parsing CLI options so we can honor --logfile
repo = None
scheduler = None


def cli_create_user(args):
	data = {"username": args.username, "age": args.age}
	if args.height is not None:
		data["height"] = args.height
	if args.weight is not None:
		data["weight"] = args.weight

	record_id = repo.create(data, type_="user")
	print(f"Created user id={record_id}")


def cli_create_workout(args):
	data = {"name": args.name, "duration": args.duration}
	record_id = repo.create(data, type_="workout")
	print(f"Created workout id={record_id}")


def cli_list(args):
	for r in repo.read_all():
		print(r)


def cli_list_schedules(args):
	"""List schedule records in a human readable form."""
	schedules = repo.find_by_type("schedule")
	if not schedules:
		print("No schedules found")
		return
	for s in schedules:
		data = s.get("data", {})
		user_id = data.get("user_id")
		workout_id = data.get("workout_id")
		# Try to resolve ids to summaries
		user = repo.get_object_by_id(user_id) if user_id else None
		workout = repo.get_object_by_id(workout_id) if workout_id else None
		user_summary = user.get_info() if user and hasattr(user, "get_info") else (user_id or "Unknown user")
		workout_summary = workout.get_summary() if workout and hasattr(workout, "get_summary") else (workout_id or "Unknown workout")
		print(f"Schedule id={s.get('id')}: {user_summary} -> {workout_summary}")


def cli_show_schedule(args):
	"""Show a single schedule by id in human readable form."""
	s = repo.read_by_id(args.id)
	if not s or s.get("type") != "schedule":
		print("Schedule not found")
		return
	data = s.get("data", {})
	user_id = data.get("user_id")
	workout_id = data.get("workout_id")
	user = repo.get_object_by_id(user_id) if user_id else None
	workout = repo.get_object_by_id(workout_id) if workout_id else None
	if user and hasattr(user, "get_info"):
		print(user.get_info())
	else:
		print(f"User id: {user_id}")
	if workout and hasattr(workout, "get_summary"):
		print(workout.get_summary())
	else:
		print(f"Workout id: {workout_id}")


def cli_get(args):
	r = repo.read_by_id(args.id)
	if not r:
		print("Record not found")
		return
	print(r)
	obj = repo.get_object_by_id(args.id)
	if obj:
		# attempt to show domain-specific summary
		if hasattr(obj, "get_info"):
			print(obj.get_info())
		elif hasattr(obj, "get_summary"):
			print(obj.get_summary())
		elif hasattr(obj, "burn_info"):
			print(obj.burn_info())


def cli_schedule(args):
	user_obj = repo.get_object_by_id(args.user_id)
	workout_obj = repo.get_object_by_id(args.workout_id)
	if not user_obj or not workout_obj:
		print("User or workout not found")
		return
	print(scheduler.schedule_workout(user_obj, workout_obj))


def cli_update(args):
	"""Update fields on an existing record.
	Provide one or more `--set key=value` arguments. Types are inferred when possible.
	"""
	record = repo.read_by_id(args.id)
	if not record:
		print("Record not found")
		return
	if not args.set:
		print("No updates provided. Use --set key=value")
		return
	updates = {}
	for s in args.set:
		if "=" not in s:
			print(f"Ignoring invalid set value: {s}")
			continue
		k, v = s.split("=", 1)
		k = k.strip()
		v = v.strip()
		# Try to convert to int/float/bool when appropriate
		converted = v
		if v.lower() in ("true", "false"):
			converted = v.lower() == "true"
		else:
			try:
				if "." in v:
					converted = float(v)
				else:
					converted = int(v)
			except ValueError:
				converted = v
		updates[k] = converted
	merged = dict(record.get("data", {}))
	merged.update(updates)
	ok = repo.update(args.id, merged)
	print(f"Updated: {ok}")
	if ok:
		print(repo.read_by_id(args.id))


def cli_delete(args):
	record = repo.read_by_id(args.id)
	if not record:
		print("Record not found")
		return
	if not args.yes:
		confirm = input(f"Delete record id={args.id} type={record.get('type')}? (y/N): ").strip().lower()
		if confirm != "y":
			print("Aborted")
			return
	ok = repo.delete(args.id)
	print(f"Deleted: {ok}")


def cli_update_user(args):
	record = repo.read_by_id(args.id)
	if not record or record.get("type") != "user":
		print("User not found")
		return
	merged = dict(record.get("data", {}))
	if args.username is not None:
		merged["username"] = args.username
	if args.age is not None:
		merged["age"] = args.age
	if args.height is not None:
		merged["height"] = args.height
	if args.weight is not None:
		merged["weight"] = args.weight
	ok = repo.update(args.id, merged)
	print(f"Updated: {ok}")
	if ok:
		print(repo.read_by_id(args.id))


def cli_update_workout(args):
	record = repo.read_by_id(args.id)
	if not record or record.get("type") != "workout":
		print("Workout not found")
		return
	merged = dict(record.get("data", {}))
	if args.name is not None:
		merged["name"] = args.name
	if args.duration is not None:
		merged["duration"] = args.duration
	ok = repo.update(args.id, merged)
	print(f"Updated: {ok}")
	if ok:
		print(repo.read_by_id(args.id))


def build_parser():
	p = argparse.ArgumentParser(description="Fitness Tracker CLI")
	# Global options
	p.add_argument("--logfile", help="Path to logfile. If provided, overrides default logs/fitness_tracker.log")
	sub = p.add_subparsers(dest="cmd")

	cu = sub.add_parser("create-user")
	cu.add_argument("--username", required=True)
	cu.add_argument("--age", type=int, required=True)
	cu.add_argument("--height", type=float)
	cu.add_argument("--weight", type=float)
	cu.set_defaults(func=cli_create_user)

	cw = sub.add_parser("create-workout")
	cw.add_argument("--name", required=True)
	cw.add_argument("--duration", type=int, required=True)
	cw.set_defaults(func=cli_create_workout)

	ls = sub.add_parser("list")
	ls.set_defaults(func=cli_list)

	g = sub.add_parser("get")
	g.add_argument("--id", required=True)
	g.set_defaults(func=cli_get)

	sch = sub.add_parser("schedule")
	sch.add_argument("--user-id", required=True)
	sch.add_argument("--workout-id", required=True)
	sch.set_defaults(func=cli_schedule)

	lsch = sub.add_parser("list-schedules")
	lsch.set_defaults(func=cli_list_schedules)

	ss = sub.add_parser("show-schedule")
	ss.add_argument("--id", required=True)
	ss.set_defaults(func=cli_show_schedule)

	upd = sub.add_parser("update")
	upd.add_argument("--id", required=True)
	upd.add_argument("--set", "-s", action="append", help="Set a field: key=value. Repeat for multiple fields.")
	upd.set_defaults(func=cli_update)

	delp = sub.add_parser("delete")
	delp.add_argument("--id", required=True)
	delp.add_argument("--yes", action="store_true", help="Skip confirmation")
	delp.set_defaults(func=cli_delete)

	uu = sub.add_parser("update-user")
	uu.add_argument("--id", required=True)
	uu.add_argument("--username")
	uu.add_argument("--age", type=int)
	uu.add_argument("--height", type=float)
	uu.add_argument("--weight", type=float)
	uu.set_defaults(func=cli_update_user)

	uw = sub.add_parser("update-workout")
	uw.add_argument("--id", required=True)
	uw.add_argument("--name")
	uw.add_argument("--duration", type=int)
	uw.set_defaults(func=cli_update_workout)

	return p


def main():
	parser = build_parser()
	args = parser.parse_args()
	# Configure logging now that we have CLI options (e.g. --logfile)
	logfile = getattr(args, "logfile", None)
	if logfile:
		# If user provided a full path, split dir/name. If only a name, leave dir default.
		log_dir = os.path.dirname(logfile) or None
		log_name = os.path.basename(logfile)
		configure_logging(level=logging.INFO, log_dir=log_dir, logfile_name=log_name)
	else:
		configure_logging()

	# Initialize repository and services after logging is configured
	global repo, scheduler
	repo = Repository()
	scheduler = Scheduler()
	if not vars(args):
		# no args provided; run default demo
		user = ObjectFactory.create_object("user", "Ruzi", 21)
		workout = ObjectFactory.create_object("workout", "Chest Day", 45)
		print(user.get_info())
		print(workout.get_summary())
		repo.create({"user": user.get_info(), "workout": workout.get_summary()}, type_="demo")
		print("Data Saved:")
		print(repo.read_all())
		print(scheduler.schedule_workout(user, workout))
	else:
		if hasattr(args, "func"):
			args.func(args)


if __name__ == "__main__":
	main()

