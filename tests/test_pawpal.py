from datetime import time
from pawpal_system import Owner, Pet, Task, Priority


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