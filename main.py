from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def main():
    # Create owner
    owner = Owner("Feyi")

    # Create pets
    dog = Pet("Bella", "Dog", 3, owner)
    cat = Pet("Milo", "Cat", 2, owner)

    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks (at least 3, different times)
    task1 = Task("Morning Walk", "Walk", time(8, 0), 30, Priority.HIGH, dog)
    task2 = Task("Feed Cat", "Feeding", time(9, 0), 10, Priority.MEDIUM, cat)
    task3 = Task("Vet Visit", "Health", time(8, 15), 60, Priority.HIGH, dog)

    # Add tasks to pets
    dog.add_task(task1)
    dog.add_task(task3)
    cat.add_task(task2)

    # Scheduler
    scheduler = Scheduler()
    scheduler.load_tasks_from_owner(owner)

    # Print schedule nicely
    print("\n=== TODAY'S SCHEDULE ===")
    for task in scheduler.generate_daily_plan():
        print(f"{task.due_time} | {task.pet.name} | {task.title} ({task.category})")

    # Print conflicts
    conflicts = scheduler.detect_conflicts()
    print("\n=== CONFLICTS ===")
    if conflicts:
        for c in conflicts:
            print(c)
    else:
        print("No conflicts 🎉")


if __name__ == "__main__":
    main()