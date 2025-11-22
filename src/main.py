import argparse
from models.factory import ObjectFactory
from repository.repository import Repository
from services.scheduler import Scheduler
from logging_config import configure_logging


configure_logging()
repo = Repository()
scheduler = Scheduler()


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


def build_parser():
	p = argparse.ArgumentParser(description="Fitness Tracker CLI")
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

	return p


def main():
	parser = build_parser()
	args = parser.parse_args()
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