from models.factory import ObjectFactory
from repository.repository import Repository
from services.scheduler import Scheduler


repo = Repository()
scheduler = Scheduler()


user = ObjectFactory.create_object("user", "Ruzi", 21)
workout = ObjectFactory.create_object("workout", "Chest Day", 45)


print(user.get_info())
print(workout.get_summary())


repo.create({
"user": user.get_info(),
"workout": workout.get_summary()
})


print("Data Saved:")
print(repo.read_all())


print(scheduler.schedule_workout(user, workout))