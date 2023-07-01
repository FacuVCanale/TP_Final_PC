## Required Libraries and File Paths

Here are the required libraries and file paths for the scripts to work as expected:

### Libraries
- time
- random
- argparse
- customtkinter
- os
- PIL
- prettytable
- tabulate
- numpy
- matplotlib
- typing

### File Paths
The following files should be imported for the scripts to work as expected:
- `communication folder`
- `strategy/tpf_CLIFF_intersection.py`: import `distance`
- `strategy/tpf_CLIFF_constants.py`: import all constants
- `strategy/tpf_CLIFF_class_dataAnalyst.py`: import `DataAnalyst`
- `strategy/tpf_CLIFF_class_hiker.py`: import `Hiker`
- `tpf_CLIFF_interface_utils.py`: import `HikersPositionFrame`, `MountainGraphFrame`, `HeatmapFrame`, `ASCIIFrame`, `ScatterFrame`, `Leaderboard`
- `classes/tpf_CLIFF_match.py`: import `Match`
- `classes/tpf_CLIFF_circle_creator.py`: import `Circle`
- `classes/tpf_CLIFF_map.py`: import `Circular_map`

### Execution Instructions
To execute the client only:
1. Execute the server
2. Execute the client   (tpf_CLIFF_strat.py)
    IP and port are given as command line arguments.
        Example:
        python tpf_CLIFF_strat.py --ip 127.0.0.1:8000

To execute the dashboard:
1. Execute the server
2. Execute the client   (tpf_CLIFF_strat.py)
    IP and port are given as command line arguments.
        Example:
        python tpf_CLIFF_strat.py --ip 127.0.0.1:8000
3. Execute the dashboard    (tpf_CLIFF_interface.py)
    IP and port are also given as command line arguments.
        Example:
        python tpf_CLIFF_interface.py --ip 127.0.0.1:8000

These instructions assume that all required libraries and files are properly installed and imported.

