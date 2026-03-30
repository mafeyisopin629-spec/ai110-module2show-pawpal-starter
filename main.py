from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def main():
    owner = Owner("Feyi")

    dog = Pet("Bella", "Dog", 3, owner)
    cat = Pet("Milo", "Cat", 2, owner)

    owner.add_pet(dog)
    owner.add_pet(cat)

    task1 = Task("Morning Walk", "Walk", time(8, 0), 30, Priority.HIGH, dog, recurring="daily")
    task2 = Task("Feed Cat", "Feeding", time(9, 0), 10, Priority.MEDIUM, cat)
    task3 = Task("Vet Visit", "Health", time(8, 0), 60, Priority.HIGH, dog, recurring="weekly")

    dog.add_task(task1)
    dog.add_task(task3)
    cat.add_task(task2)

    scheduler = Scheduler()
    scheduler.load_tasks_from_owner(owner)

    print("\n=== TODAY'S SCHEDULE ===")
    for task in scheduler.generate_daily_plan():
        print(f"{task.due_date} {task.due_time} | {task.pet.name} | {task.title} ({task.category})")

    print("\n=== MARKING RECURRING TASK COMPLETE ===")
    scheduler.mark_task_complete(task1)

    print(f"Completed: {task1.title} on {task1.due_date}")

    print("\n=== UPDATED TASK LIST ===")
    for task in scheduler.sort_by_time():
        status = "Done" if task.completed else "Pending"
        print(f"{task.due_date} {task.due_time} | {task.pet.name} | {task.title} | {status} | recurring={task.recurring}")

    print("\n=== CONFLICTS ===")
    conflicts = scheduler.detect_conflicts()

    if conflicts:
        for c in conflicts:
            print("⚠️", c)
    else:
        print("No conflicts 🎉")


if __name__ == "__main__":
    main()