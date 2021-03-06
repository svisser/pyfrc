
import sys

from .. import sim
from .. import wpilib

def run(run_fn, file_location, enable_pynetworktables=False):
    
    # TODO: do more with this

    if len(sys.argv) == 2 and sys.argv[1] == "--enable-pynetworktables":
        enable_pynetworktables = True

    wpilib.internal.setup_networktables(enable_pynetworktables)
    wpilib.internal.initialize_test()
    myrobot = run_fn()

    # sim parameters
    field_size = (25, 54)
    px_per_ft = 10

    sim_manager = sim.SimManager()
    
    controller = sim.RobotController(myrobot)
    robot_element = sim.RobotElement(controller, px_per_ft) 
    
    sim_manager.add_robot(controller)
    
    controller.run()
    
    ui = sim.SimUI(sim_manager, field_size, px_per_ft)
    ui.field.add_moving_element(robot_element)
    ui.run()

    # once it has finished, try to shut the robot down
    # -> if it can't, then the user messed up
    if not controller.stop():
        print('Error: could not stop the robot code! Check your code')

    return 0
