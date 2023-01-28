"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from math import sqrt
from project import constants
from math import sin, cos, pi

time_list: List[int] = []
infected_count: List[int] = []
immune_count: List[int] = []

__author__ = "730389244"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def distance(self, point2: Point) -> float:
        """Finds distance between two cells."""
        value_1: float = (point2.x - self.x) ** 2
        value_2: float = (point2.y - self.y) ** 2
        distance: float = sqrt(value_1 + value_2)
        return distance

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)


class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = constants.VULNERABLE

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.

    def tick(self) -> None:
        """Sets a tick for simulation."""
        self.location = self.location.add(self.direction)
        if self.sickness > constants.VULNERABLE and self.sickness < constants.RECOVERY_PERIOD:
            self.sickness += 1
        elif self.sickness >= constants.RECOVERY_PERIOD:
            self.immunize()

    def color(self) -> str:
        """Return the color representation of a cell."""
        vulnerable = self.is_vulnerable()
        infected = self.is_infected()
        immune = self.is_immune()
        if vulnerable:
            return "gray"
        elif immune:
            return "blue"
        elif infected:
            return "red"
        else:
            return "gray"

    def contract_disease(self) -> None:
        """Makes the cell take in the disease."""
        self.sickness = constants.INFECTED
    
    def is_vulnerable(self) -> bool:
        """Is the cell vulnerable."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False

    def is_infected(self) -> bool:
        """Is the cell infected."""
        if self.sickness > 0 and self.sickness < constants.RECOVERY_PERIOD:
            return True
        else:
            return False

    def is_immune(self) -> bool:
        """Is the cell immune."""
        if self.sickness == constants.IMMUNE or self.sickness >= constants.RECOVERY_PERIOD:
            return True
        else:
            return False

    def contact_with(self, cell_2: Cell) -> None:
        """Checks if cell came into contact w others."""
        if cell_2.is_vulnerable() and self.is_infected():
            cell_2.contract_disease()
        if cell_2.is_infected() and self.is_vulnerable():
            self.contract_disease()

    def immunize(self) -> None:
        """Makes the cell immune."""
        self.sickness = constants.IMMUNE


class Model:
    """The state of the simulation."""
    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, infected: int, immune: int = 0):
        """Initialize the cells with random locations and directions."""
        self.population = []
        if infected <= 0 or immune < 0:
            raise ValueError()
        if infected >= cells or immune >= cells:
            raise ValueError()
        for i in range(0, cells - (infected - immune)):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
        for i in range(0, infected):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            Celli: Cell = Cell(start_loc, start_dir)
            Celli.sickness = constants.INFECTED
            self.population.append(Celli)
        for i in range(0, immune):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            Celly: Cell = Cell(start_loc, start_dir)
            Celly.sickness = constants.IMMUNE
            self.population.append(Celly)

    def check_contacts(self) -> None:
        """Checks to see if any cells are touching."""
        for cell1 in self.population:
            cell_location: Point = cell1.location
            for cell2 in self.population:
                if cell2.location.distance(cell_location) < constants.CELL_RADIUS:
                    cell1.contact_with(cell2)
                    cell1.direction.x *= -1
                    cell1.direction.y *= -1
                    cell2.direction.x *= -1
                    cell2.direction.y *= -1

    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        self.check_contacts()
        time_list.append(self.time)
        infected: int = 0
        immune: int = 0
        for cell in self.population:
            cell.tick()
            if cell.sickness == constants.IMMUNE:
                immune += 1
            elif cell.sickness != constants.VULNERABLE:
                infected += 1
            self.enforce_bounds(cell)
        immune_count.append(immune)
        infected_count.append(infected)

    def random_location(self) -> Point:
        """Generate a random location."""
        # TODO
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        # TODO
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1
    
    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        i: int = 0
        for cell in self.population:
            infected = cell.is_infected()
            if infected:
                i += 1
        if i == 0:
            return True
        else:
            return False