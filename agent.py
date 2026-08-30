# agent.py

import random
from collections import deque
import heapq
import math

# =========================================================
# OLD / EXISTING AGENT
# =========================================================

class GreedyGridAgent:
    """A simple agent that moves around the grid."""

    def __init__(self):
        self.actions_pool = [
            "Up",
            "Down",
            "Left",
            "Right"
        ]

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


# =========================================================
# LAB 03 - SEARCH AGENT
# =========================================================

class SearchAgent:

    # -----------------------------------------------------
    # STEP 1.3 - INITIAL SETTINGS
    # -----------------------------------------------------

    def __init__(self):

        # Store the complete route
        self.plan = []

        # Select which search algorithm to use
        self.active_algo = "BFS"


    def manhattan_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        distance = abs(x1 - x2) + abs(y1 - y2)

        return distance
    
    def euclidean_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal

        distance = math.sqrt(
            (x1 - x2) ** 2 +
            (y1 - y2) ** 2
        )

        return distance


    # =====================================================
    # STEP 1.2 - BFS
    # =====================================================

    def bfs_search(
        self,
        start,
        goal,
        grid_size,
        walls
    ):

        width, height = grid_size

        # Possible movements
        directions = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }

        # BFS uses a FIFO Queue
        frontier = deque()

        # Store:
        # (current_state, path)
        frontier.append(
            (start, [])
        )

        # Remember discovered states
        reached = {start}

        while frontier:

            # BFS takes the FIRST item
            current_state, path = (
                frontier.popleft()
            )

            # Goal reached
            if current_state == goal:
                return path

            x, y = current_state

            # Try Up, Down, Left, Right
            for action, (dx, dy) in directions.items():

                next_state = (
                    x + dx,
                    y + dy
                )

                next_x, next_y = next_state

                # Check grid boundary
                inside_grid = (
                    0 <= next_x < width
                    and
                    0 <= next_y < height
                )

                # Use only valid new states
                if (
                    inside_grid
                    and next_state not in walls
                    and next_state not in reached
                ):

                    # Mark as reached
                    reached.add(
                        next_state
                    )

                    # Add the new action
                    # to the existing path
                    new_path = (
                        path + [action]
                    )

                    # Add to the back
                    # of the BFS queue
                    frontier.append(
                        (
                            next_state,
                            new_path
                        )
                    )

        # No path found
        return []


    # =====================================================
    # STEP 1.2 - DFS
    # =====================================================

    def dfs_search(
        self,
        start,
        goal,
        grid_size,
        walls
    ):

        width, height = grid_size

        directions = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }

        # DFS uses a Stack
        frontier = []

        frontier.append(
            (start, [])
        )

        reached = {start}

        while frontier:

            # DFS takes the LAST item
            current_state, path = (
                frontier.pop()
            )

            # Goal reached
            if current_state == goal:
                return path

            x, y = current_state

            for action, (dx, dy) in directions.items():

                next_state = (
                    x + dx,
                    y + dy
                )

                next_x, next_y = next_state

                inside_grid = (
                    0 <= next_x < width
                    and
                    0 <= next_y < height
                )

                if (
                    inside_grid
                    and next_state not in walls
                    and next_state not in reached
                ):

                    reached.add(
                        next_state
                    )

                    new_path = (
                        path + [action]
                    )

                    frontier.append(
                        (
                            next_state,
                            new_path
                        )
                    )

        # No path found
        return []


    # =====================================================
    # STEP 1.2 - UCS
    # =====================================================

    def ucs_search(
        self,
        start,
        goal,
        grid_size,
        walls
    ):
        


        width, height = grid_size

        directions = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }

        # UCS uses a Priority Queue
        frontier = []

        # Store:
        # (cost, current_state, path)
        heapq.heappush(
            frontier,
            (
                0,
                start,
                []
            )
        )

        reached = set()

        while frontier:

            # Get the lowest-cost item
            cost, current_state, path = (
                heapq.heappop(
                    frontier
                )
            )

            # Already explored
            if current_state in reached:
                continue

            # Mark current state
            # as explored
            reached.add(
                current_state
            )

            # Goal reached
            if current_state == goal:
                return path

            x, y = current_state

            for action, (dx, dy) in directions.items():

                next_state = (
                    x + dx,
                    y + dy
                )

                next_x, next_y = next_state

                inside_grid = (
                    0 <= next_x < width
                    and
                    0 <= next_y < height
                )

                if (
                    inside_grid
                    and next_state not in walls
                    and next_state not in reached
                ):

                    # Every movement costs 1
                    new_cost = (
                        cost + 1
                    )

                    new_path = (
                        path + [action]
                    )

                    heapq.heappush(
                        frontier,
                        (
                            new_cost,
                            next_state,
                            new_path
                        )
                    )

        # No path found
        return []
    
    

    def astar_search(
            self,
            start_pos,
            goal_pos,
            walls,
            grid_size,
            heuristic_type='manhattan'
        ):

        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)

        walls = set(tuple(wall) for wall in walls)

        width, height = grid_size

        # Choose heuristic
        def get_heuristic(position):

            if heuristic_type == 'euclidean':
                return self.euclidean_distance(
                    position,
                    goal_pos
                )

            return self.manhattan_distance(
                position,
                goal_pos
            )

        # Priority queue
        priority_queue = []

        # Reached positions
        reached_states = set()

        # Starting costs
        start_g = 0
        start_h = get_heuristic(start_pos)
        start_f = start_g + start_h

        # Format:
        # (f_cost, g_cost, current_pos, path_taken)
        heapq.heappush(
            priority_queue,
            (
                start_f,
                start_g,
                start_pos,
                []
            )
        )

        # Possible movements
        moves = [
            ('Up', (0, 1)),
            ('Down', (0, -1)),
            ('Left', (-1, 0)),
            ('Right', (1, 0))
        ]

        while priority_queue:

            f_cost, g_cost, current_pos, path_taken = \
                heapq.heappop(priority_queue)

            # Goal reached
            if current_pos == goal_pos:
                return path_taken

            # Already processed
            if current_pos in reached_states:
                continue

            reached_states.add(current_pos)

            # Check neighbours
            for action, (dx, dy) in moves:

                x, y = current_pos

                new_x = x + dx
                new_y = y + dy

                new_pos = (new_x, new_y)

                # Check grid boundary
                inside_grid = (
                    0 <= new_x < width
                    and 0 <= new_y < height
                )

                # Check wall
                not_wall = new_pos not in walls

                # Check reached
                not_reached = new_pos not in reached_states

                if (
                    inside_grid
                    and not_wall
                    and not_reached
                ):

                    # g(n)
                    new_g = g_cost + 1

                    # h(n)
                    new_h = get_heuristic(new_pos)

                    # f(n) = g(n) + h(n)
                    new_f = new_g + new_h

                    # Add action to path
                    new_path = path_taken + [action]

                    heapq.heappush(
                        priority_queue,
                        (
                            new_f,
                            new_g,
                            new_pos,
                            new_path
                        )
                    )

        # No path found
        return []



    


    # =====================================================
    # STEP 1.3 - EXECUTE OFFLINE PLAN
    # =====================================================

    def sense_and_act(
        self,
        percept
    ):

        # -------------------------------------------------
        # 1. If agent is standing on food,
        #    collect the food.
        # -------------------------------------------------

        if percept["food_here"]:

            # Previous route is finished
            self.plan = []

            return "suck"


        # -------------------------------------------------
        # 2. If there is no existing plan,
        #    create a new plan.
        # -------------------------------------------------

        if not self.plan:

            # Current agent location
            start = percept[
                "agent_pos"
            ]

            # All available food positions
            foods = percept[
                "all_food"
            ]

            # No food remaining
            if not foods:
                return None


            # ---------------------------------------------
            # 3. Find the closest food
            # ---------------------------------------------

            goal = min(
                foods,
                key=lambda food:
                    abs(
                        food[0]
                        - start[0]
                    )
                    +
                    abs(
                        food[1]
                        - start[1]
                    )
            )


            # ---------------------------------------------
            # 4. Get environment information
            # ---------------------------------------------

            grid_size = percept[
                "grid_size"
            ]

            walls = set(
                percept["walls"]
            )


            # ---------------------------------------------
            # 5. Run selected algorithm
            # ---------------------------------------------

            if self.active_algo == "BFS":

                self.plan = (
                    self.bfs_search(
                        start,
                        goal,
                        grid_size,
                        walls
                    )
                )

            elif self.active_algo == "DFS":

                self.plan = (
                    self.dfs_search(
                        start,
                        goal,
                        grid_size,
                        walls
                    )
                )

            elif self.active_algo == "UCS":

                self.plan = (
                    self.ucs_search(
                        start,
                        goal,
                        grid_size,
                        walls
                    )
                )

            
            elif self.active_algo == 'AStar':

                if not self.plan:

                    current_pos = tuple(percept['agent_pos'])
                    grid_size = tuple(percept['grid_size'])
                    walls = percept['walls']
                    remaining_food = percept['all_food']

                    if remaining_food:

                        # Find closest food using Manhattan distance
                        goal_pos = min(
                            remaining_food,
                            key=lambda food:
                                self.manhattan_distance(
                                    current_pos,
                                    tuple(food)
                                )
                        )

                        goal_pos = tuple(goal_pos)

                        # Create A* plan
                        self.plan = self.astar_search(
                            current_pos,
                            goal_pos,
                            walls,
                            grid_size,
                            heuristic_type='manhattan'
                        )

                # Execute next action
                if self.plan:
                    return self.plan.pop(0)

            else:

                raise ValueError(
                    "Unknown search algorithm: "
                    + self.active_algo
                )


            # ---------------------------------------------
            # Useful output for observation
            # ---------------------------------------------

            print(
                "Algorithm:",
                self.active_algo,

                "| Start:",
                start,

                "| Goal:",
                goal,

                "| Plan:",
                self.plan
            )


        # -------------------------------------------------
        # 6. Execute ONE action from the plan
        # -------------------------------------------------

        if self.plan:

            return self.plan.pop(0)


        # No available action
        return None
    
if __name__ == "__main__":

    agent = SearchAgent()

    start = (0, 0)
    goal = (3, 4)

    print("Manhattan Distance:",
          agent.manhattan_distance(start, goal))

    print("Euclidean Distance:",
          agent.euclidean_distance(start, goal))
