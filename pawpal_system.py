from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from datetime import time
from enum import Enum


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    title: str
    category: str
    due_time: time
    duration: int
    priority: Priority
    recurring: bool = False
    completed: bool = False
    pet: 'Pet'

    def mark_complete(self) -> None:
        pass

    def update_time(self, new_time: time) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    owner: 'Owner'

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass

    def get_tasks(self) -> List[Task]:
        pass


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_pets(self) -> List[Pet]:
        pass


@dataclass
class Scheduler:
    tasks: List[Task] = field(default_factory=list)

    def sort_tasks(self) -> None:
        pass

    def detect_conflicts(self) -> List[Task]:
        pass

    def generate_daily_plan(self) -> List[Task]:
        pass


@dataclass
class Scheduler:
    tasks: List[Task] = field(default_factory=list)

    def sort_tasks(self) -> List[Task]:
        pass

    def detect_conflicts(self) -> List[str]:
        pass

    def generate_daily_plan(self) -> List[Task]:
        pass