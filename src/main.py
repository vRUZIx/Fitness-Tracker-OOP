import argparse
from models.factory import ObjectFactory
from repository.repository import Repository
from services.scheduler import Scheduler
from services.user_service import UserService
from services.workout_service import WorkoutService
from logging_config import configure_logging


configure_logging()
repo = Repository()


def get_services():
	"""Return service instances bound to the current module-level `repo`.

	This allows tests or callers to replace `main.repo` and have CLI
	functions operate on the substituted repository.
	"""
	return UserService(repo=repo), WorkoutService(repo=repo)


user_service, workout_service = get_services()
scheduler = Scheduler()


def cli_create_user(args):
	user_service, _ = get_services()
	record_id = user_service.create_user(args.username, args.age, height=args.height, weight=args.weight)
	print(f"Created user id={record_id}")


def cli_create_workout(args):
	_, workout_service = get_services()
	record_id = workout_service.create_workout(args.name, args.duration)
	print(f"Created workout id={record_id}")


def cli_list(args):
	user_service, _ = get_services()
	for r in user_service.list_all():
		print(r)


def cli_get(args):
	user_service, _ = get_services()
	r = user_service.read_record(args.id)
	if not r:
		print("Record not found")
		return
	print(r)
	obj = user_service.get_domain_by_id(args.id)
	if obj:
		# attempt to show domain-specific summary
		if hasattr(obj, "get_info"):
			print(obj.get_info())
		elif hasattr(obj, "get_summary"):
			print(obj.get_summary())
		elif hasattr(obj, "burn_info"):
			print(obj.burn_info())


def cli_schedule(args):
	user_service, workout_service = get_services()
	user_obj = user_service.get_domain_by_id(args.user_id)
	workout_obj = workout_service.get_domain_by_id(args.workout_id)
	if not user_obj or not workout_obj:
		print("User or workout not found")
		return

	# Collect strategy kwargs based on strategy type
	strategy_kwargs = {}
	if args.strategy == "simple" and hasattr(args, "met") and args.met is not None:
		strategy_kwargs["met"] = args.met
	elif args.strategy == "constant" and hasattr(args, "rate_per_min") and args.rate_per_min is not None:
		strategy_kwargs["rate_per_min"] = args.rate_per_min

	result = scheduler.schedule_workout(user_obj, workout_obj, strategy=args.strategy, **strategy_kwargs)
	print(result)


# pluggable input function used by interactive mode (can be replaced in tests)
INPUT_FUNC = input


def _prompt(prompt_text, cast=str, required=False, default=None):
	while True:
		try:
			raw = INPUT_FUNC(f"{prompt_text}{' [' + str(default) + ']' if default is not None else ''}: ")
		except EOFError:
			return default
		if raw == "" and default is not None:
			return default
		if raw == "" and not required:
			return None
		try:
			return cast(raw)
		except Exception:
			print(f"Invalid value — expected {cast.__name__}. Please try again.")


def _confirm(prompt_text, default: bool = True) -> bool:
	"""Ask a yes/no confirmation. Returns True for yes.

	default True yields prompt like "[Y/n]", False yields "[y/N]".
	"""
	choices = "[Y/n]" if default else "[y/N]"
	while True:
		try:
			ans = INPUT_FUNC(f"{prompt_text} {choices}: ").strip().lower()
		except EOFError:
			return default
		if ans == "" and default is not None:
			return default
		if ans in ("y", "yes"):
			return True
		if ans in ("n", "no"):
			return False
		print("Please answer 'y' or 'n'.")


def cli_interactive(_args=None, input_func=None):
	"""Interactive prompt loop. Uses same services beneath the CLI commands."""
	print("=" * 60)
	print("FITNESS TRACKER - Interactive Menu")
	print("=" * 60)
	print("Entering interactive mode. Type the number for an action. Ctrl-C to exit.")
	global INPUT_FUNC
	old_input = INPUT_FUNC
	if input_func is not None:
		INPUT_FUNC = input_func

	history = []
	while True:
		try:
			print("\n" + "=" * 60)
			print("MAIN MENU")
			print("=" * 60)
			print("1)  Create user")
			print("2)  Create workout")
			print("3)  List all records")
			print("4)  Get record by ID")
			print("5)  Update user")
			print("6)  Update workout")
			print("7)  Delete user")
			print("8)  Delete workout")
			print("9)  List users only")
			print("10) List workouts only")
			print("11) Schedule workout")
			print("12) History")
			print("13) Exit")
			print("=" * 60)
			choice = _prompt("Choose action", cast=int, required=True)
			history.append(choice)
			if choice == 1:
				username = _prompt("Username", cast=str, required=True)
				age = _prompt("Age", cast=int, required=True)
				height = _prompt("Height (cm)", cast=float, required=False)
				weight = _prompt("Weight (kg)", cast=float, required=False)
				print(f"About to create user: username={username}, age={age}, height={height}, weight={weight}")
				if _confirm("Proceed with creating this user?", default=True):
					user_service, _ = get_services()
					rid = user_service.create_user(username, age, height=height, weight=weight)
					print(f"Created user id={rid}")
				else:
					print("Creation cancelled.")
			elif choice == 2:
				name = _prompt("Workout name", cast=str, required=True)
				duration = _prompt("Duration (minutes)", cast=int, required=True)
				print(f"About to create workout: name={name}, duration={duration}")
				if _confirm("Proceed with creating this workout?", default=True):
					_, workout_service = get_services()
					rid = workout_service.create_workout(name, duration)
					print(f"Created workout id={rid}")
				else:
					print("Creation cancelled.")
			elif choice == 3:
				# list all records
				records = repo.read_all()
				if not records:
					print("No records found.")
				else:
					print(f"\nTotal records: {len(records)}")
					for r in records:
						print(r)
			elif choice == 4:
				# get record by ID
				rid = _prompt("Record id", cast=str, required=True)
				r = repo.read_by_id(rid)
				if not r:
					print("Record not found — check the id and try again.")
				else:
					print(r)
					obj = repo.get_object_by_id(rid)
					if obj:
						if hasattr(obj, "get_info"):
							print(obj.get_info())
						elif hasattr(obj, "get_summary"):
							print(obj.get_summary())
			elif choice == 5:
				# update user
				user_service, _ = get_services()
				rid = _prompt("User id to update", cast=str, required=True)
				record = user_service.read_record(rid)
				if not record:
					print("User not found.")
					continue
				if record.get("type") != "user":
					print("Record is not a user.")
					continue
				
				current_data = record.get("data", {})
				print(f"\nCurrent values: {current_data}")
				print("Leave blank to keep current value.")
				
				username = _prompt("New username", cast=str, required=False, default=current_data.get("username"))
				age = _prompt("New age", cast=int, required=False, default=current_data.get("age"))
				height = _prompt("New height (cm)", cast=float, required=False, default=current_data.get("height"))
				weight = _prompt("New weight (kg)", cast=float, required=False, default=current_data.get("weight"))
				
				try:
					if user_service.update_user(rid, username=username, age=age, height=height, weight=weight):
						print(f"User {rid} updated successfully.")
					else:
						print("Update failed.")
				except Exception as e:
					print(f"Error updating user: {e}")
			elif choice == 6:
				# update workout
				_, workout_service = get_services()
				rid = _prompt("Workout id to update", cast=str, required=True)
				record = workout_service.read_record(rid)
				if not record:
					print("Workout not found.")
					continue
				if record.get("type") != "workout":
					print("Record is not a workout.")
					continue
				
				current_data = record.get("data", {})
				print(f"\nCurrent values: {current_data}")
				print("Leave blank to keep current value.")
				
				name = _prompt("New workout name", cast=str, required=False, default=current_data.get("name"))
				duration = _prompt("New duration (minutes)", cast=int, required=False, default=current_data.get("duration"))
				
				try:
					if workout_service.update_workout(rid, name=name, duration=duration):
						print(f"Workout {rid} updated successfully.")
					else:
						print("Update failed.")
				except Exception as e:
					print(f"Error updating workout: {e}")
			elif choice == 7:
				# delete user
				user_service, _ = get_services()
				rid = _prompt("User id to delete", cast=str, required=True)
				record = user_service.read_record(rid)
				if not record:
					print("User not found.")
					continue
				if record.get("type") != "user":
					print("Record is not a user.")
					continue
				
				print(f"\nUser to delete: {record}")
				if _confirm("Are you sure you want to delete this user?", default=False):
					try:
						if user_service.delete_user(rid):
							print(f"User {rid} deleted successfully.")
						else:
							print("Delete failed.")
					except Exception as e:
						print(f"Error deleting user: {e}")
				else:
					print("Deletion cancelled.")
			elif choice == 8:
				# delete workout
				_, workout_service = get_services()
				rid = _prompt("Workout id to delete", cast=str, required=True)
				record = workout_service.read_record(rid)
				if not record:
					print("Workout not found.")
					continue
				if record.get("type") != "workout":
					print("Record is not a workout.")
					continue
				
				print(f"\nWorkout to delete: {record}")
				if _confirm("Are you sure you want to delete this workout?", default=False):
					try:
						if workout_service.delete_workout(rid):
							print(f"Workout {rid} deleted successfully.")
						else:
							print("Delete failed.")
					except Exception as e:
						print(f"Error deleting workout: {e}")
				else:
					print("Deletion cancelled.")
			elif choice == 9:
				# list users only
				user_service, _ = get_services()
				users = user_service.list_users()
				if not users:
					print("No users found.")
				else:
					print(f"\nTotal users: {len(users)}")
					for u in users:
						print(u)
			elif choice == 10:
				# list workouts only
				_, workout_service = get_services()
				workouts = workout_service.list_workouts()
				if not workouts:
					print("No workouts found.")
				else:
					print(f"\nTotal workouts: {len(workouts)}")
					for w in workouts:
						print(w)
			elif choice == 11:
				user_id = _prompt("User id", cast=str, required=True)
				workout_id = _prompt("Workout id", cast=str, required=True)
				user_obj = repo.get_object_by_id(user_id)
				workout_obj = repo.get_object_by_id(workout_id)
				if not user_obj or not workout_obj:
					print("User or workout not found — verify ids with the list command.")
					continue
				strat = _prompt("Strategy (none/simple/constant)", cast=str, required=False, default="none")
				strat_name = None
				strat_kwargs = {}
				if strat and strat.lower() in ("simple", "constant"):
					strat_name = strat.lower()
					if strat_name == "simple":
						met = _prompt("MET value (e.g. 5.0)", cast=float, required=False, default=6.0)
						strat_kwargs["met"] = met
					else:
						rate = _prompt("Rate (kcal/min)", cast=float, required=False, default=5.0)
						strat_kwargs["rate_per_min"] = rate
				print(f"About to schedule workout '{getattr(workout_obj, 'name', 'unknown')}' for user '{getattr(user_obj, 'username', 'unknown')}'.")
				if _confirm("Proceed with scheduling?", default=True):
					try:
						result = scheduler.schedule_workout(user_obj, workout_obj, strategy=strat_name, **strat_kwargs)
						print(result)
					except Exception as e:
						print(f"Error scheduling workout: {e}")
				else:
					print("Scheduling cancelled.")
			elif choice == 12:
				# show history
				if not history:
					print("No history yet.")
				else:
					print("\nRecent actions:")
					for i, h in enumerate(history[-20:], start=1):
						print(f"{i}. Action choice: {h}")
			elif choice == 13:
				print("\nExiting interactive mode. Goodbye!")
				break
			else:
				print("Unknown choice. Please select a valid option (1-13).")
		except KeyboardInterrupt:
			print("\nInterrupted. Exiting interactive mode.")
			break
	# restore original input function
	INPUT_FUNC = old_input


def cli_update_user(args):
	user_service, _ = get_services()
	try:
		success = user_service.update_user(
			args.id,
			username=args.username,
			age=args.age,
			height=args.height,
			weight=args.weight
		)
		if success:
			print(f"Updated user id={args.id}")
		else:
			print("Update failed")
	except Exception as e:
		print(f"Error: {e}")


def cli_update_workout(args):
	_, workout_service = get_services()
	try:
		success = workout_service.update_workout(
			args.id,
			name=args.name,
			duration=args.duration
		)
		if success:
			print(f"Updated workout id={args.id}")
		else:
			print("Update failed")
	except Exception as e:
		print(f"Error: {e}")


def cli_delete_user(args):
	user_service, _ = get_services()
	try:
		success = user_service.delete_user(args.id)
		if success:
			print(f"Deleted user id={args.id}")
		else:
			print("Delete failed")
	except Exception as e:
		print(f"Error: {e}")


def cli_delete_workout(args):
	_, workout_service = get_services()
	try:
		success = workout_service.delete_workout(args.id)
		if success:
			print(f"Deleted workout id={args.id}")
		else:
			print("Delete failed")
	except Exception as e:
		print(f"Error: {e}")


def cli_list_users(args):
	user_service, _ = get_services()
	users = user_service.list_users()
	if not users:
		print("No users found.")
	else:
		print(f"Total users: {len(users)}")
		for u in users:
			print(u)


def cli_list_workouts(args):
	_, workout_service = get_services()
	workouts = workout_service.list_workouts()
	if not workouts:
		print("No workouts found.")
	else:
		print(f"Total workouts: {len(workouts)}")
		for w in workouts:
			print(w)


def build_parser():
	p = argparse.ArgumentParser(description="Fitness Tracker CLI")
	sub = p.add_subparsers(dest="cmd")

	cu = sub.add_parser("create-user", help="Create a new user")
	cu.add_argument("--username", required=True)
	cu.add_argument("--age", type=int, required=True)
	cu.add_argument("--height", type=float)
	cu.add_argument("--weight", type=float)
	cu.set_defaults(func=cli_create_user)

	cw = sub.add_parser("create-workout", help="Create a new workout")
	cw.add_argument("--name", required=True)
	cw.add_argument("--duration", type=int, required=True)
	cw.set_defaults(func=cli_create_workout)

	uu = sub.add_parser("update-user", help="Update an existing user")
	uu.add_argument("--id", required=True)
	uu.add_argument("--username")
	uu.add_argument("--age", type=int)
	uu.add_argument("--height", type=float)
	uu.add_argument("--weight", type=float)
	uu.set_defaults(func=cli_update_user)

	uw = sub.add_parser("update-workout", help="Update an existing workout")
	uw.add_argument("--id", required=True)
	uw.add_argument("--name")
	uw.add_argument("--duration", type=int)
	uw.set_defaults(func=cli_update_workout)

	du = sub.add_parser("delete-user", help="Delete a user")
	du.add_argument("--id", required=True)
	du.set_defaults(func=cli_delete_user)

	dw = sub.add_parser("delete-workout", help="Delete a workout")
	dw.add_argument("--id", required=True)
	dw.set_defaults(func=cli_delete_workout)

	lsu = sub.add_parser("list-users", help="List all users")
	lsu.set_defaults(func=cli_list_users)

	lsw = sub.add_parser("list-workouts", help="List all workouts")
	lsw.set_defaults(func=cli_list_workouts)

	ls = sub.add_parser("list", help="List all records")
	ls.set_defaults(func=cli_list)

	g = sub.add_parser("get", help="Get record by ID")
	g.add_argument("--id", required=True)
	g.set_defaults(func=cli_get)

	sch = sub.add_parser("schedule", help="Schedule a workout for a user")
	sch.add_argument("--user-id", required=True)
	sch.add_argument("--workout-id", required=True)
	sch.add_argument("--strategy", choices=["simple", "constant"], help="Calorie estimation strategy to use")
	sch.add_argument("--met", type=float, help="MET value for the simple strategy (e.g. 5.0)")
	sch.add_argument("--rate-per-min", dest="rate_per_min", type=float, help="Rate (kcal/min) for constant strategy")
	sch.set_defaults(func=cli_schedule)

	it = sub.add_parser("interactive", help="Start interactive menu mode")
	it.set_defaults(func=cli_interactive)

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
		# persist demo using the module-level repo
		repo.create({"user": user.get_info(), "workout": workout.get_summary()}, type_="demo")
		print("Data Saved:")
		print(repo.read_all())
		print(scheduler.schedule_workout(user, workout))
	else:
		if hasattr(args, "func"):
			args.func(args)


if __name__ == "__main__":
	main()