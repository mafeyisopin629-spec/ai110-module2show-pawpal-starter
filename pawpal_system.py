from __future__ import annotations
from dataclasses import dataclass
from typing import List


@dataclass
class Task:
    title: str
    category: str
    due_time: str
    duration: int
    priority: str
    recurring: bool
    completed: bool

    def mark_complete(self) -> None:
        pass

    def update_time(self, new_time: str) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task]

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


class Owner:
    def __init__(self, name: str):
        self.name: str = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass


class Scheduler:
    def __init__(self):
        self.tasks: List[Task] = []

    def sort_tasks(self) -> None:
        pass

    def detect_conflicts(self) -> List[Task]:
        pass

    def generate_daily_plan(self) -> List[Task]:
        pass