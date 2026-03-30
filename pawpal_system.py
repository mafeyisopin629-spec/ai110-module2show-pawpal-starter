from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from datetime import time, timedelta, datetime, date
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
    recurring: str = "none"   # none, daily, weekly
    completed: bool = False
    due_date: date = field(default_factory=date.today)

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
        """Sort tasks by due date, due time, and priority."""
        return sorted(
            self.tasks,
            key=lambda task: (task.due_date, task.due_time, -task.priority.value)
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

        for current_task, next_task in zip(sorted_tasks, sorted_tasks[1:]):
            if current_task.due_date != next_task.due_date:
                continue

            current_end = datetime.combine(
                current_task.due_date, current_task.due_time
            ) + timedelta(minutes=current_task.duration)
            next_start = datetime.combine(
                next_task.due_date, next_task.due_time
            )

            if current_end > next_start:
                conflicts.append(
                    f"Conflict between '{current_task.title}' for {current_task.pet.name} "
                    f"and '{next_task.title}' for {next_task.pet.name}"
                )

        return conflicts

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task complete and create the next recurring task if needed."""
        task.mark_complete()

        if task.recurring == "daily":
            next_date = task.due_date + timedelta(days=1)
        elif task.recurring == "weekly":
            next_date = task.due_date + timedelta(weeks=1)
        else:
            return

        new_task = Task(
            title=task.title,
            category=task.category,
            due_time=task.due_time,
            duration=task.duration,
            priority=task.priority,
            pet=task.pet,
            recurring=task.recurring,
            completed=False,
            due_date=next_date,
        )

        task.pet.add_task(new_task)
        self.tasks.append(new_task)

    def generate_daily_plan(self) -> List[Task]:
        """Return incomplete tasks in sorted order."""
        return [task for task in self.sort_by_time() if not task.completed]

    def mark_task_complete(self, task: Task) -> None:
        """Mark a task complete and create the next recurring task if needed."""
        task.mark_complete()

        if task.recurring == "daily":
            next_date = task.due_date + timedelta(days=1)
        elif task.recurring == "weekly":
            next_date = task.due_date + timedelta(weeks=1)
        else:
            return

        new_task = Task(
            title=task.title,
            category=task.category,
            due_time=task.due_time,
            duration=task.duration,
            priority=task.priority,
            pet=task.pet,
            recurring=task.recurring,
            completed=False,
            due_date=next_date,
        )

        task.pet.add_task(new_task)
        self.tasks.append(new_task)

    def generate_daily_plan(self) -> List[Task]:
        """Return incomplete tasks in sorted order."""
        return [task for task in self.sort_by_time() if not task.completed]