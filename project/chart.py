from project import constants
from project.model import Model
from project.ViewController import ViewController
from typing import Dict, List
from project.model import time_list, infected_count, immune_count
import matplotlib.pyplot as plt
import sys


def main() -> None:
    """Entrypoint of simulation."""
    args: Dict[str, str] = read_args()
    model = Model(int(sys.argv[1]), constants.CELL_SPEED, int(sys.argv[2]), int(sys.argv[3]))
    vc = ViewController(model)
    vc.start_simulation()
    chart_data()
    
def read_args() -> Dict[str, str]:
    """Check for valid CLI arguments and return them in a dictionary."""
    if len(sys.argv) != 4:
        print("Usage: python -m projects.pj02 [TOTAL] [INFECTED] [IMMUNE]")
        exit()
    return {
        "total": sys.argv[1],
        "infected": sys.argv[2],
        "immune": sys.argv[3]
    }

def chart_data() -> None:
    """Creates chart w two lines, one for infected, one for immune."""
    plt.ylabel("Cell Total")
    plt.xlabel("Time")
    plt.title("Contagion Simulation")
    plt.plot(time_list, infected_count)
    plt.plot(time_list, immune_count)
    plt.show()

if __name__ == "__main__":
    main()