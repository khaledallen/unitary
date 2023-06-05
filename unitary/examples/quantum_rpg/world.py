# Copyright 2023 The Unitary Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import Callable, Dict, List, Optional, Sequence, Union

import dataclasses
import unitary.examples.quantum_rpg.encounter as encounter
import unitary.examples.quantum_rpg.item as item
import enum


class Direction(enum.Enum):
    NORTH = "north"
    EAST = "east"
    SOUTH = "south"
    WEST = "west"
    UP = "up"
    DOWN = "down"

    @classmethod
    def parse(cls, s: str) -> Optional["Direction"]:
        """Parses a string as a Direction.

        Allows prefixes, like 'e' to be parsed as EAST.
        """
        if not s:
            return None
        lower_s = s.lower()
        for d in Direction:
            if d.value.startswith(lower_s):
                return d


@dataclasses.dataclass
class Location:
    """Dataclass representing a location in the quantum RPG.

    Attributes:
        label: id of the location so that other rooms can
            refer to it succintly.
        title: Title or short description of the room.
        description: Longer description of the room.
        exits: Mapping from direction to label of the
           adjacent rooms.
        encounter: Sequence of encounters that can be
           visited here.

    """

    label: str
    title: str
    exits: Dict[Direction, str]
    encounters: Optional[List[encounter.Encounter]] = None
    description: Optional[str] = None
    items: Optional[List[item.Item]] = None

    def _exits(self) -> str:
        return ", ".join([ex.value for ex in self.exits]) + "."

    def _item_str(self) -> str:
        if not self.items:
            return ""
        return "\n" + "\n".join([item.description or "" for item in self.items])

    def get_action(self, keyword: str) -> Union[str, Callable]:
        if self.items:
            for item in self.items:
                action = item.get_action(keyword)
                if action:
                    return action
        return None

    def remove_encounter(self, triggered_encounter) -> bool:
        self.encounters.remove(triggered_encounter)

    def __str__(self) -> str:
        return f"{self.title}\n\n{self.description}{self._item_str()}\nExits: {self._exits()}\n"


class World:
    """A list of connected locations that can be traversed.

    The first location is assumed to be the starting location.
    """

    def __init__(self, locations: Sequence[Location]):
        self.locations = {location.label: location for location in locations}
        self.current_location = locations[0]

    def move(self, direction: Direction) -> Optional[Location]:
        """Move to new location in the specified direction.

        If there is no room in that direction, returns None.
        """
        new_location = self.current_location.exits.get(direction, None)
        if new_location is not None:
            self.current_location = self.locations[new_location]
            return self.current_location
        return None
