"""This specially named module makes the package runnable."""

from project import constants
from project.model import Model
from project.ViewController import ViewController


def main() -> None:
    """Entrypoint of simulation."""
    model = Model(constants.CELL_COUNT, constants.CELL_SPEED, constants.INFECTED_COUNT, constants.IMMUNE_COUNT)
    vc = ViewController(model)
    vc.start_simulation()


if __name__ == "__main__":
    main()