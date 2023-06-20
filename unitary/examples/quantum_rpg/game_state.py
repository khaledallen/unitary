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

from typing import Dict, List, Optional, Sequence

import io
import sys

import unitary.examples.quantum_rpg.input_helpers as input_helpers
import unitary.examples.quantum_rpg.qaracter as qaracter


_SAVE_DELIMITER = ";"
_DICT_DELIMITER = ":"


class GameState:
    def __init__(
        self,
        party: List[qaracter.Qaracter],
        current_location_label: str = "",
        state_dict: Dict[str, str] = None,
        user_input: Optional[Sequence[str]] = None,
        file: io.IOBase = sys.stdout,
    ):
        self.party = party
        self.current_location_label = current_location_label
        self.state_dict = state_dict or {}
        self.user_input = user_input
        self.get_user_input = input_helpers.get_user_input_function(user_input)
        self.file = file

    @classmethod
    def from_save_file(
        cls,
        save_file: str,
        user_input: Optional[Sequence[str]] = None,
        file: io.IOBase = sys.stdout,
    ) -> "GameState":
        lines = save_file.split(_SAVE_DELIMITER)
        current_location_label = lines[0]
        party: List[qaracter.Qaracter] = []
        num_party = int(lines[1])
        for party_idx in range(2, 2 + num_party):
            party.append(qaracter.Qaracter.from_save_file(lines[party_idx]))
        state_dict = {}
        for line in lines[2 + num_party :]:
            dict_value = line.split(":")
            state_dict[dict_value[0]] = dict_value[1]
        return cls(party, current_location_label, state_dict, user_input, file)

    def to_save_file(self) -> str:
        s = f"{self.current_location_label}{_SAVE_DELIMITER}{len(self.party)}{_SAVE_DELIMITER}"
        for p in self.party:
            s += p.to_save_file() + _SAVE_DELIMITER
        for k, v in self.state_dict.items():
            s += f"{k}{_DICT_DELIMITER}{v}{_SAVE_DELIMITER}"
        return s[:-1]
