from datetime import time, date, timedelta
from pawpal_system import Owner, Pet, Task, Scheduler, Priority


def test_task_completion():
    owner = Owner("Feyi")
    pet = Pet("Bella", "Dog", 3, owner)
    task = Task("Walk", "Exercise", time(8, 0), 30, Priority.HIGH, pet)

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet():
    owner = Owner("Feyi")
    pet = Pet("Bella", "Dog", 3, owner)
    task = Task("Feed", "Food", time(9, 0), 10, Priority.MEDIUM, pet)

    assert len(pet.get_tasks()) == 0
    pet.add_task(task)
    assert len(pet.get_tasks()) == 1


def test_sorting_correctness():
    owner = Owner("Feyi")
    pet = Pet("Bella", "Dog", 3, owner)
    owner.add_pet(pet)

    task1 = Task("Late Task", "Walk", time(10, 0), 20, Priority.MEDIUM, pet)
    task2 = Task("Early Task", "Feed", time(8, 0), 10, Priority.HIGH, pet)
    task3 = Task("Middle Task", "Health", time(9, 0), 15, Priority.LOW, pet)

    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)

    scheduler = Scheduler()
    scheduler.load_tasks_from_owner(owner)

    sorted_tasks = scheduler.sort_by_time()

    assert [task.title for task in sorted_tasks] == [
        "Early Task",
        "Middle Task",
        "Late Task",
    ]


def test_daily_recurring_task_creates_next_day():
    owner = Owner("Feyi")
    pet = Pet("Bella", "Dog", 3, owner)
    owner.add_pet(pet)

    task = Task(
        "Morning Walk",
        "Walk",
        time(8, 0),
        30,
        Priority.HIGH,
        pet,
        recurring="daily",
        due_date=date.today(),
    )
    pet.add_task(task)

    scheduler = Scheduler()
    scheduler.load_tasks_from_owner(owner)

    scheduler.mark_task_complete(task)

    future_tasks = [
        t for t in pet.get_tasks()
        if t.title == "Morning Walk" and not t.completed
    ]

    assert len(future_tasks) == 1
    assert future_tasks[0].due_date == date.today() + timedelta(days=1)


def test_conflict_detection_flags_same_time_tasks():
    owner = Owner("Feyi")
    dog = Pet("Bella", "Dog", 3, owner)
    owner.add_pet(dog)

    task1 = Task(
        "Morning Walk",
        "Walk",
        time(8, 0),
        30,
        Priority.HIGH,
        dog,
        due_date=date.today(),
    )
    task2 = Task(
        "Vet Visit",
        "Health",
        time(8, 0),
        60,
        Priority.HIGH,
        dog,
        due_date=date.today(),
    )

    dog.add_task(task1)
    dog.add_task(task2)

    scheduler = Scheduler()
    scheduler.load_tasks_from_owner(owner)

    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "Morning Walk" in conflicts[0]
    assert "Vet Visit" in conflicts[0]