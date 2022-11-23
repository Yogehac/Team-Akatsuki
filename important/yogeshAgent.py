from typing import Union
from game_state import GameState
import asyncio
import random
import os
import time

from aka1 import Gameboard as agB


uri = os.environ.get(
    'GAME_CONNECTION_STRING') or "ws://127.0.0.1:3000/?role=agent&agentId=agentId&name=defaultName"

actions = ["up", "down", "left", "right", "bomb", "detonate"]


class Agent():
    def __init__(self):
        self._client = GameState(uri)

        # any initialization code can go here
        self._client.set_game_tick_callback(self._on_game_tick)

        self.boardB = agB()

        loop = asyncio.get_event_loop()
        connection = loop.run_until_complete(self._client.connect())
        tasks = [
            asyncio.ensure_future(self._client._handle_messages(connection)),
        ]
        loop.run_until_complete(asyncio.wait(tasks))

    # returns coordinates of the first bomb placed by a unit
    def _get_bomb_to_detonate(self, unit) -> Union[int, int] or None:
        entities = self._client._state.get("entities")
        bombs = list(filter(lambda entity: entity.get(
            "unit_id") == unit and entity.get("type") == "b", entities))
        bomb = next(iter(bombs or []), None)
        if bomb != None:
            return [bomb.get("x"), bomb.get("y")]
        else:
            return None

    async def _on_game_tick(self, tick_number, game_state):

        # get my units
        my_agent_id = game_state.get("connection").get("agent_id")
        print('****************')
        print(my_agent_id)
        print('****************')
        my_units = game_state.get("agents").get(my_agent_id).get("unit_ids")
        # if my_agent_id == 'a':
        #     my_units = self.boardA.active_agents(my_units)
        # else:
        #     my_units = self.boardB.active_agents(my_units)

        my_units = self.boardB.active_agents(my_units)

        for unit_id in my_units:

            self.boardB.update_board(self._client._state)
            try:
                action, unit_id = self.boardB.AI(
                    unit_id)  # METHOD TO CATCH SPAN
            except Exception as e:
                print('*****In AI******')
                print(e)
                action = None
                print('***********')
           
            if action in ["up", "left", "right", "down"]:
                await self._client.send_move(action, unit_id)
            elif action == "bomb":
                await self._client.send_bomb(unit_id)
            elif action == "detonate":
                bomb_coordinates = self._get_bomb_to_detonate(unit_id)
                if bomb_coordinates != None:
                    x, y = bomb_coordinates
                    await self._client.send_detonate(x, y, unit_id)
            else:
                print(f"Unhandled action: {action} for unit {unit_id}")


def main():
    for i in range(0, 10):
        while True:
            try:
                Agent()
            except:
                time.sleep(5)
                continue
            break


if __name__ == "__main__":
    main()