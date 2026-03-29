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
        self.pets.append(pet)

    def get_pets(self) -> List["Pet"]:
        return self.pets

    def get_all_tasks(self) -> List["Task"]:
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
        self.tasks.append(task)

    def remove_task(self, task: "Task") -> None:
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List["Task"]:
        return self.tasks


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
        self.completed = True

    def update_time(self, new_time: time) -> None:
        self.due_time = new_time


@dataclass
class Scheduler:
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)

    def load_tasks_from_owner(self, owner: Owner) -> None:
        self.tasks = owner.get_all_tasks()

    def sort_tasks(self) -> List[Task]:
        return sorted(
            self.tasks,
            key=lambda task: (task.due_time, -task.priority.value)
        )

    def detect_conflicts(self) -> List[str]:
        conflicts = []
        sorted_tasks = self.sort_tasks()

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
        return [task for task in self.sort_tasks() if not task.completed]


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