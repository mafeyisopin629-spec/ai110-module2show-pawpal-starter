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

    # Create tasks (out of order intentionally)
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

    # ===== EXISTING OUTPUT =====
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

    # ===== NEW: PHASE 4 STEP 2 TESTS =====
    print("\n=== ALL TASKS SORTED ===")
    for t in scheduler.sort_by_time():
        print(t.title, t.due_time)

    print("\n=== INCOMPLETE TASKS ===")
    for t in scheduler.filter_by_completion(False):
        print(t.title)

    print("\n=== TASKS FOR BELLA ===")
    for t in scheduler.filter_by_pet("Bella"):
        print(t.title)


if __name__ == "__main__":
    main()