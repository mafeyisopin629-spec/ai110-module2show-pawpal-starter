from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from datetime import time, timedelta, datetime
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Owner:
    name: str
    pets: List["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_pets(self) -> List["Pet"]:
        """Return all pets owned."""
        return self.pets

    def get_all_tasks(self) -> List["Task"]:
        """Return all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


@dataclass
class Pet:
    name: str
    species: str
    age: int
    owner: Owner
    tasks: List["Task"] = field(default_factory=list)

    def add_task(self, task: "Task") -> None:
        """Add a task to the pet."""
        self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        """Remove a task from the pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List["Task"]:
        """Return all tasks for this pet."""
        return self.tasks

    def get_pending_tasks(self) -> List["Task"]:
        """Return incomplete tasks for this pet sorted by time."""
        return sorted(
            [task for task in self.tasks if not task.completed],
            key=lambda task: (task.due_time, -task.priority.value)
        )


@dataclass
class Task:
    title: str
    category: str
    due_time: time
    duration: int
    priority: Priority
    pet: Pet
    recurring: bool = False
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.completed = True

    def update_time(self, new_time: time) -> None:
        """Update the task's scheduled time."""
        self.due_time = new_time


@dataclass
class Scheduler:
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.tasks.append(task)

    def load_tasks_from_owner(self, owner: Owner) -> None:
        """Load all tasks from an owner."""
        self.tasks = owner.get_all_tasks()

    def sort_by_time(self) -> List[Task]:
        """Sort tasks by due time and priority."""
        return sorted(
            self.tasks,
            key=lambda task: (task.due_time, -task.priority.value)
        )

    def filter_by_completion(self, completed: bool) -> List[Task]:
        """Return tasks filtered by completion status."""
        return [task for task in self.tasks if task.completed == completed]

    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Return tasks for a specific pet."""
        return [task for task in self.tasks if task.pet.name == pet_name]

    def detect_conflicts(self) -> List[str]:
        """Detect overlapping tasks."""
        conflicts = []
        sorted_tasks = self.sort_by_time()

        for i in range(len(sorted_tasks) - 1):
            current_task = sorted_tasks[i]
            next_task = sorted_tasks[i + 1]

            current_start = datetime.combine(datetime.today(), current_task.due_time)
            current_end = current_start + timedelta(minutes=current_task.duration)
            next_start = datetime.combine(datetime.today(), next_task.due_time)

            if current_end > next_start:
                conflicts.append(
                    f"Conflict between '{current_task.title}' for {current_task.pet.name} "
                    f"and '{next_task.title}' for {next_task.pet.name}"
                )

        return conflicts

    def generate_daily_plan(self) -> List[Task]:
        """Return incomplete tasks in sorted order."""
        return [task for task in self.sort_by_time() if not task.completed]


if __name__ == "__main__":
    owner = Owner("Feyi")
    pet = Pet("Bella", "Dog", 3, owner)
    owner.add_pet(pet)

    task = Task("Morning Walk", "Walk", time(8, 0), 30, Priority.HIGH, pet)
    pet.add_task(task)

    scheduler = Scheduler()
    scheduler.load_tasks_from_owner(owner)

    print("Tasks:")
    for t in scheduler.generate_daily_plan():
        print(f"{t.title} - {t.pet.name} at {t.due_time}")

    print("Conflicts:", scheduler.detect_conflicts())