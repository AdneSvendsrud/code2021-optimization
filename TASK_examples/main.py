#######################################################################################
#    .oooooo.                   .o8              .oooo.     .oooo.     .oooo.     .o  #
#   d8P'  `Y8b                 "888            .dP""Y88b   d8P'`Y8b  .dP""Y88b  o888  #
#  888           .ooooo.   .oooo888   .ooooo.        ]8P' 888    888       ]8P'  888  #
#  888          d88' `88b d88' `888  d88' `88b     .d8P'  888    888     .d8P'   888  #
#  888          888   888 888   888  888ooo888   .dP'     888    888   .dP'      888  #
#  `88b    ooo  888   888 888   888  888    .o .oP     .o `88b  d88' .oP     .o  888  #
#  `Y8bood8P'  `Y8bod8P' `Y8bod88P" `Y8bod8P' 8888888888  `Y8bd8P'  8888888888 o888o  #
#######################################################################################

"""
__        __       _                                 _
\ \      / /  ___ | |  ___   ___   _ __ ___    ___  | |_   ___
 \ \ /\ / /  / _ \| | / __| / _ \ | '_ ` _ \  / _ \ | __| / _ \
  \ V  V /  |  __/| || (__ | (_) || | | | | ||  __/ | |_ | (_) |
   \_/\_/    \___||_| \___| \___/ |_| |_| |_| \___|  \__| \___/
 _   _               _            _    _                    _
| | | |  __ _   ___ | | __  __ _ | |_ | |__    ___   _ __  | |
| |_| | / _` | / __|| |/ / / _` || __|| '_ \  / _ \ | '_ \ | |
|  _  || (_| || (__ |   < | (_| || |_ | | | || (_) || | | ||_|
|_| |_| \__,_| \___||_|\_\ \__,_| \__||_| |_| \___/ |_| |_|(_)

"""

# This is an example script of how to (very simply) solve the given problems

# Import required packages
import numpy as np
import json
import pprint


def parse_json(filepath):
    """
    Function for converting the input JSON, to a dictionary and an array of coordinates
    :param filepath:
        string containing the location of the input-JSON
    :return:
        A tuple, where the first value is an array containing the coordinates of the floor plan, and
        the other a dictionary containing all the rooms to be fitted in the floor
    """

    # Read the JSON file and dump the contents
    with open(filepath, 'r') as input_JSON:
        data = json.load(input_JSON)
        floor_plan = data['planBoundary']
        room_dict = data['rooms']

    # To get a feeling for what our data looks like, let's print the contents
    print(f'Coordinate array:')
    pprint.pprint(floor_plan)
    print('\n')
    print(f'Room dictionary:\n')
    pprint.pprint(room_dict)
    print('\n')
    return floor_plan, room_dict


def brute_force(floor_plan, rooms):
    """
    This is a function demonstrating the possibility of brute-force approach. It will simply return the first possible
    configuration of rooms it can find that satisfies the rules.
    :param floor_plan:
        List containing the coordinates of the floor plan
    :param rooms:
        List containing every room to be fitted into the floor plan
    :return:
        Dictionary containing all the rooms, and their position within the floor plan (i.e. changed anchors)
    """
    # Since we're brute-forcing, we pick out the first room, and fit it into the corner. This corresponds to doing
    # nothing with it since it's anchor is (0, 0). We leave this be, and start with the next
    fitted_rooms = dict()
    fitted_rooms[rooms[0]["id"]] = rooms[0]
    # We need parameters to check if a room fits. So we extract the width and height of the floor plan
    x_values = list(map(lambda e: e["x"], floor_plan))
    min_x_coord = min(x_values)
    max_x_coord = max(x_values)

    fp_width = min_x_coord + max_x_coord

    y_values = list(map(lambda e: e["y"], floor_plan))
    min_y_coord = min(y_values)
    max_y_coord = max(y_values)

    fp_height = min_y_coord + max_y_coord
    # Note than in this most simple solution, the room is a square. This will not always be the case (how do you deal
    # with that?)
    print(f'Width and height of the floor plan: ({fp_width}, {fp_height})\n')

    prev_room = rooms[0]
    for room in rooms:
        room_id = room["id"]
        # If it's the first room, we've already dealt with it, therefore skip it
        if room_id in fitted_rooms:
            continue
        # Try fitting the room to the right of, or below the previous room
        potential_x_anchor = prev_room['anchorTopLeftX'] + prev_room['width']
        potential_y_anchor = prev_room['anchorTopLeftY'] + prev_room['height']
        if potential_x_anchor + room['width'] <= fp_width:
            # Since we have not dealt with the y-anchor, this remains the same
            room['anchorTopLeftX'] = potential_x_anchor
            # Add the room to the fitted rooms
            fitted_rooms[room_id] = room
        elif potential_y_anchor + room['height'] <= fp_height:
            # Do the same, only opposite to the x-anchor
            room['anchorTopLeftY'] = potential_y_anchor
            fitted_rooms[room_id] = room

        prev_room = room
    # If we managed to fit all rooms, then return them. Else we raise an exception
    if len(rooms) == len(fitted_rooms):
        return fitted_rooms
    raise RuntimeError('Did not manage to fit all rooms into the floor plan.')


def validate_solution(floor_plan, rooms):
    print("Add your validation function here")


if __name__ == '__main__':
    floor_plan, rooms = parse_json('./TASK_examples/basic_example_input.json')
    result = brute_force(floor_plan, rooms)
    print('Results of brute-force:\n')
    pprint.pprint(result)
