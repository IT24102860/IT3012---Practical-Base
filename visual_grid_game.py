# visual_grid_game.py

import random
import tkinter as tk
from collections import deque

from agent import SearchAgent


class VisualGridHuntGame:
    """A flexible Pacman-style grid environment."""

    def __init__(
        self,
        width=10,
        height=10,
        num_food=10,
        num_opponents=2,
        custom_walls=None
    ):
        self.width = width
        self.height = height

        # Starting position
        self.agent_pos = [0, 0]

        # Starting direction
        self.facing = "Up"


        # ---------------------------------
        # Logical percepts for Lab 05
        # ---------------------------------

        self.has_dust = True
        self.target_visible = True
        self.bloodseeker_missing = False

        # Create walls
        if custom_walls is not None:
            self.walls = set(custom_walls)
        else:
            self.walls = {
                (2, 2),
                (2, 3),
                (5, 5),
                (6, 5),
                (3, 7)
            }

        # -------------------------------------------------
        # Generate food positions
        # -------------------------------------------------

        self.food_positions = set()

        while len(self.food_positions) < num_food:

            fx = random.randint(
                0,
                self.width - 1
            )

            fy = random.randint(
                0,
                self.height - 1
            )

            pos_tuple = (fx, fy)

            if (
                pos_tuple != (0, 0)
                and pos_tuple not in self.walls
            ):
                self.food_positions.add(
                    pos_tuple
                )

        # -------------------------------------------------
        # Generate opponents
        # -------------------------------------------------

        self.opponents = []

        while len(self.opponents) < num_opponents:

            ox = random.randint(
                0,
                self.width - 1
            )

            oy = random.randint(
                0,
                self.height - 1
            )

            op_pos = [ox, oy]

            if (
                tuple(op_pos) != (0, 0)
                and tuple(op_pos) not in self.walls
                and tuple(op_pos)
                not in self.food_positions
            ):
                self.opponents.append(
                    op_pos
                )

        # -------------------------------------------------
        # Create toxic traps
        # -------------------------------------------------

        self.toxic_traps = set()

        while len(self.toxic_traps) < 5:

            tx = random.randint(
                0,
                self.width - 1
            )

            ty = random.randint(
                0,
                self.height - 1
            )

            trap_pos = (tx, ty)

            if (
                trap_pos != (0, 0)
                and trap_pos not in self.walls
                and trap_pos
                not in self.food_positions
            ):
                self.toxic_traps.add(
                    trap_pos
                )

        # Game information
        self.score = 0
        self.steps = 0
        self.collision = False

    # =====================================================
    # GET PERCEPT
    # =====================================================

    def get_percept(self) -> dict:

        x, y = self.agent_pos

        # Coordinate change for each facing direction
        direction_changes = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }

        # Get movement values
        dx, dy = direction_changes[
            self.facing
        ]

        # Calculate position directly ahead
        front_x = x + dx
        front_y = y + dy

        front_pos = (
            front_x,
            front_y
        )

        # Check whether front position
        # is outside the grid
        outside_grid = not (
            0 <= front_x < self.width
            and
            0 <= front_y < self.height
        )

        # Check wall ahead
        wall_ahead = (
            outside_grid
            or
            front_pos in self.walls
        )

        # Check food in current position
        food_here = (
            tuple(self.agent_pos)
            in self.food_positions
        )

        return {
            "wall_ahead": wall_ahead,
            "food_here": food_here,
            "agent_pos":
                tuple(self.agent_pos),

            "food_positions":
                set(self.food_positions),

                "grid_size": (self.width, self.height),
                "walls": list(self.walls),
                "all_food": list(self.food_positions),
            "TargetVisible": self.target_visible,
            " HasDust": self.has_dust,
            "BloodseekerMissing": self.bloodseeker_missing   
        }

    # =====================================================
    # EXECUTE ACTION
    # =====================================================

    def execute_action(
        self,
        action: str
    ):

        self.steps += 1

        # Absolute direction
        if action in [
            "Up",
            "Down",
            "Left",
            "Right"
        ]:
            self.facing = action

        # -------------------------------------------------
        # Turning tables
        # -------------------------------------------------

        left_turn = {
            "Up": "Left",
            "Left": "Down",
            "Down": "Right",
            "Right": "Up"
        }

        right_turn = {
            "Up": "Right",
            "Right": "Down",
            "Down": "Left",
            "Left": "Up"
        }

        # -------------------------------------------------
        # TURN LEFT
        # -------------------------------------------------

        if action == "turn_left":

            self.facing = left_turn[
                self.facing
            ]

            return

        # -------------------------------------------------
        # TURN RIGHT
        # -------------------------------------------------

        if action == "turn_right":

            self.facing = right_turn[
                self.facing
            ]

            return

        # -------------------------------------------------
        # SUCK / COLLECT FOOD
        # -------------------------------------------------

        if action == "suck":

            current_pos = tuple(
                self.agent_pos
            )

            if (
                current_pos
                in self.food_positions
            ):

                self.food_positions.remove(
                    current_pos
                )

                self.score += 20

            return

        # -------------------------------------------------
        # MOVE FORWARD
        # -------------------------------------------------

        if action == "move_forward":

            action = self.facing

        # Keep original Lab 01 actions
        if action in [
            "Up",
            "Down",
            "Left",
            "Right"
        ]:

            self.facing = action

        new_pos = list(
            self.agent_pos
        )

        # -------------------------------------------------
        # Apply movement
        # -------------------------------------------------

        if action == "Up":

            new_pos[1] = min(
                self.height - 1,
                new_pos[1] + 1
            )

        elif action == "Down":

            new_pos[1] = max(
                0,
                new_pos[1] - 1
            )

        elif action == "Left":

            new_pos[0] = max(
                0,
                new_pos[0] - 1
            )

        elif action == "Right":

            new_pos[0] = min(
                self.width - 1,
                new_pos[0] + 1
            )

        # -------------------------------------------------
        # Wall collision
        # -------------------------------------------------

        if (
            tuple(new_pos)
            in self.walls
        ):

            self.score -= 5

        else:

            self.agent_pos = new_pos

        # -------------------------------------------------
        # Toxic trap
        # -------------------------------------------------

        tuple_pos = tuple(
            self.agent_pos
        )

        if (
            tuple_pos
            in self.toxic_traps
        ):

            self.score -= 15

        # -------------------------------------------------
        # Move opponents
        # -------------------------------------------------

        for op in self.opponents:

            move = random.choice(
                [
                    "Up",
                    "Down",
                    "Left",
                    "Right",
                    "Stay"
                ]
            )

            candidate = list(op)

            if (
                move == "Up"
                and
                op[1] < self.height - 1
            ):

                candidate[1] += 1

            elif (
                move == "Down"
                and
                op[1] > 0
            ):

                candidate[1] -= 1

            elif (
                move == "Left"
                and
                op[0] > 0
            ):

                candidate[0] -= 1

            elif (
                move == "Right"
                and
                op[0] < self.width - 1
            ):

                candidate[0] += 1

            # Opponents cannot move
            # through walls
            if (
                tuple(candidate)
                not in self.walls
            ):

                op[:] = candidate

            # Collision with agent
            if (
                op == self.agent_pos
            ):

                self.score -= 50
                self.collision = True

    # =====================================================
    # CHECK END CONDITION
    # =====================================================

    def is_done(self) -> bool:

        return (
            len(self.food_positions) == 0
            or
            self.steps >= 60
            or
            self.collision
        )


# =========================================================
# SIMPLE REFLEX AGENT
# =========================================================

class SimpleReflexAgent:

    """Uses only current percept."""

    def sense_and_act(
        self,
        percept: dict
    ) -> str:

        # Food here
        if percept["food_here"]:

            return "suck"

        # Wall ahead
        if percept["wall_ahead"]:

            return "turn_left"

        # Otherwise move forward
        return "move_forward"


# =========================================================
# MODEL-BASED AGENT
# =========================================================

class ModelBasedAgent:

    """
    Model-based agent using:
    1. Current percept
    2. Previous action
    3. Internal estimated position
    4. Visited cells
    """

    def __init__(self):

        # Cells visited by agent
        self.visited_cells = {
            (0, 0)
        }



        # Internal estimated position
        self.internal_pos = [
            0,
            0
        ]

        # Internal facing direction
        self.facing = "Up"

        # Previous action
        self.last_action = None

        # Previous percept
        self.last_percept = None

    # -----------------------------------------------------

    def turn_left_direction(
        self,
        direction
    ):

        left_turn = {
            "Up": "Left",
            "Left": "Down",
            "Down": "Right",
            "Right": "Up"
        }

        return left_turn[
            direction
        ]

    # -----------------------------------------------------

    def turn_right_direction(
        self,
        direction
    ):

        right_turn = {
            "Up": "Right",
            "Right": "Down",
            "Down": "Left",
            "Left": "Up"
        }

        return right_turn[
            direction
        ]

    # -----------------------------------------------------

    def next_position(
        self,
        position,
        direction
    ):

        x, y = position

        direction_changes = {
            "Up": (0, 1),
            "Down": (0, -1),
            "Left": (-1, 0),
            "Right": (1, 0)
        }

        dx, dy = direction_changes[
            direction
        ]

        return (
            x + dx,
            y + dy
        )

    # -----------------------------------------------------

    def update_state(
        self,
        percept
    ):

        # Previous action was turn left
        if (
            self.last_action
            == "turn_left"
        ):

            self.facing = (
                self.turn_left_direction(
                    self.facing
                )
            )

        # Previous action was turn right
        elif (
            self.last_action
            == "turn_right"
        ):

            self.facing = (
                self.turn_right_direction(
                    self.facing
                )
            )

        # Previous action was move forward
        elif (
            self.last_action
            == "move_forward"
        ):

            if (
                self.last_percept
                is not None
                and
                not self.last_percept[
                    "wall_ahead"
                ]
            ):

                new_pos = (
                    self.next_position(
                        self.internal_pos,
                        self.facing
                    )
                )

                self.internal_pos = [
                    new_pos[0],
                    new_pos[1]
                ]

        # Store visited cell
        self.visited_cells.add(
            tuple(
                self.internal_pos
            )
        )

        # Store current percept
        self.last_percept = (
            percept.copy()
        )

    # -----------------------------------------------------

    def left_position(self):

        left_direction = (
            self.turn_left_direction(
                self.facing
            )
        )

        return self.next_position(
            self.internal_pos,
            left_direction
        )

    # -----------------------------------------------------

    def forward_position(self):

        return self.next_position(
            self.internal_pos,
            self.facing
        )

    # -----------------------------------------------------
    # BFS helper used by previous model-based version
    # -----------------------------------------------------

    @staticmethod
    def shortest_direction(
        start,
        goals,
        walls,
        grid_size
    ):

        width, height = grid_size

        queue = deque(
            [start]
        )

        previous = {
            start: None
        }

        target = None

        while queue:

            current = (
                queue.popleft()
            )

            if current in goals:

                target = current
                break

            x, y = current

            for direction, (
                dx,
                dy
            ) in (

                ("Up", (0, 1)),
                ("Down", (0, -1)),
                ("Left", (-1, 0)),
                ("Right", (1, 0))

            ):

                neighbor = (
                    x + dx,
                    y + dy
                )

                if (
                    0 <= neighbor[0] < width
                    and
                    0 <= neighbor[1] < height
                    and
                    neighbor not in walls
                    and
                    neighbor not in previous
                ):

                    previous[
                        neighbor
                    ] = (
                        current,
                        direction
                    )

                    queue.append(
                        neighbor
                    )

        if (
            target is None
            or
            target == start
        ):

            return None

        # Trace backwards
        # until reaching start
        while (
            previous[target][0]
            != start
        ):

            target = (
                previous[target][0]
            )

        return (
            previous[target][1]
        )

    # -----------------------------------------------------
    # SENSE AND ACT
    # -----------------------------------------------------

    def sense_and_act(
        self,
        percept
    ):

        # If global position information
        # is available, find a route
        if (
            "agent_pos"
            in percept
        ):

            if percept[
                "food_here"
            ]:

                self.last_action = "suck"

                return "suck"

            action = (
                self.shortest_direction(
                    percept[
                        "agent_pos"
                    ],
                    percept[
                        "food_positions"
                    ],
                    percept[
                        "walls"
                    ],
                    percept[
                        "grid_size"
                    ],
                )
            )

            if action is not None:

                self.last_action = action

                return action

        # -------------------------------------------------
        # Fallback model-based logic
        # -------------------------------------------------

        self.update_state(
            percept
        )

        left_pos = (
            self.left_position()
        )

        forward_pos = (
            self.forward_position()
        )

        left_is_visited = (
            left_pos
            in self.visited_cells
        )

        forward_is_visited = (
            forward_pos
            in self.visited_cells
        )

        # Food here
        if percept[
            "food_here"
        ]:

            action = "suck"

        # Wall ahead and
        # left already visited
        elif (
            percept[
                "wall_ahead"
            ]
            and
            left_is_visited
        ):

            action = "turn_right"

        # Wall ahead
        elif percept[
            "wall_ahead"
        ]:

            action = "turn_left"

        # Forward already visited
        elif forward_is_visited:

            action = "turn_right"

        # Otherwise move
        else:

            action = "move_forward"

        self.last_action = action

        return action


# =========================================================
# GUI
# =========================================================

class GridGameGUI:

    """Tkinter GUI for grid game."""

    def __init__(
        self,
        root,
        width=10,
        height=10,
        num_food=12,
        num_opponents=2,
        walls=None
    ):

        self.root = root

        self.root.title(
            "IT3012 - Scalable Multi-Agent Grid Hunt"
        )

        # Create environment
        self.env = VisualGridHuntGame(
            width=width,
            height=height,
            num_food=num_food,
            num_opponents=num_opponents,
            custom_walls=walls
        )

        # Create agents
        self.simple_agent = (
            SimpleReflexAgent()
        )

        self.model_agent = (
            ModelBasedAgent()
        )


        self.search_agent = SearchAgent()
        self.search_agent.active_algo = 'AStar'

        # Canvas size
        max_canvas_dim = 450

        self.cell_size = max(
            20,
            min(
                max_canvas_dim
                // self.env.width,

                max_canvas_dim
                // self.env.height
            )
        )

        canvas_w = (
            self.env.width
            * self.cell_size
        )

        canvas_h = (
            self.env.height
            * self.cell_size
        )

        self.canvas = tk.Canvas(
            root,
            width=canvas_w,
            height=canvas_h,
            bg="white"
        )

        self.canvas.pack()

        # Score label
        self.label = tk.Label(
            root,
            text="Score: 0 | Steps: 0",
            font=(
                "Arial",
                14
            )
        )

        self.label.pack(
            pady=10
        )

        # Start button
        self.btn = tk.Button(
            root,
            text="Start Simulation",
            command=self.run_loop,
            font=(
                "Arial",
                12
            ),
            bg="#000066",
            fg="white"
        )

        self.btn.pack(
            pady=5
        )

        self.draw_grid()

    # =====================================================
    # DRAW GRID
    # =====================================================

    def draw_grid(self):

        self.canvas.delete(
            "all"
        )

        # Draw cells
        for x in range(
            self.env.width
        ):

            for y in range(
                self.env.height
            ):

                x1 = (
                    x
                    * self.cell_size
                )

                y1 = (
                    (
                        self.env.height
                        - 1
                        - y
                    )
                    * self.cell_size
                )

                x2 = (
                    x1
                    + self.cell_size
                )

                y2 = (
                    y1
                    + self.cell_size
                )

                if (
                    (x, y)
                    not in self.env.walls
                ):

                    color = "#f1f5f9"

                else:

                    color = "#64748b"

                self.canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=color,
                    outline="#cbd5e1"
                )

                # Wall text
                if (
                    self.cell_size >= 40
                    and
                    (x, y)
                    in self.env.walls
                ):

                    self.canvas.create_text(
                        x1
                        + self.cell_size / 2,

                        y1
                        + self.cell_size / 2,

                        text="W",
                        fill="white",

                        font=(
                            "Arial",
                            8,
                            "bold"
                        )
                    )

        # -------------------------------------------------
        # Draw toxic traps
        # -------------------------------------------------

        for tx, ty in (
            self.env.toxic_traps
        ):

            cx = (
                tx
                * self.cell_size
                + self.cell_size / 2
            )

            cy = (
                (
                    self.env.height
                    - 1
                    - ty
                )
                * self.cell_size
                + self.cell_size / 2
            )

            r = (
                self.cell_size
                * 0.25
            )

            self.canvas.create_polygon(
                cx,
                cy - r,

                cx - r,
                cy + r,

                cx + r,
                cy + r,

                fill="purple",
                outline="black"
            )

        # -------------------------------------------------
        # Draw food
        # -------------------------------------------------

        for fx, fy in (
            self.env.food_positions
        ):

            offset = (
                self.cell_size
                * 0.25
            )

            x1 = (
                fx
                * self.cell_size
                + offset
            )

            y1 = (
                (
                    self.env.height
                    - 1
                    - fy
                )
                * self.cell_size
                + offset
            )

            self.canvas.create_oval(
                x1,
                y1,

                x1
                + self.cell_size
                * 0.5,

                y1
                + self.cell_size
                * 0.5,

                fill="#f59e0b",
                outline="#d97706"
            )

        # -------------------------------------------------
        # Draw opponents
        # -------------------------------------------------

        for ox, oy in (
            self.env.opponents
        ):

            offset = (
                self.cell_size
                * 0.2
            )

            x1 = (
                ox
                * self.cell_size
                + offset
            )

            y1 = (
                (
                    self.env.height
                    - 1
                    - oy
                )
                * self.cell_size
                + offset
            )

            self.canvas.create_rectangle(
                x1,
                y1,

                x1
                + self.cell_size
                * 0.6,

                y1
                + self.cell_size
                * 0.6,

                fill="#990000",
                outline="#7a0000"
            )

        # -------------------------------------------------
        # Draw agent
        # -------------------------------------------------

        ax, ay = (
            self.env.agent_pos
        )

        offset = (
            self.cell_size
            * 0.15
        )

        x1 = (
            ax
            * self.cell_size
            + offset
        )

        y1 = (
            (
                self.env.height
                - 1
                - ay
            )
            * self.cell_size
            + offset
        )

        self.canvas.create_oval(
            x1,
            y1,

            x1
            + self.cell_size
            * 0.7,

            y1
            + self.cell_size
            * 0.7,

            fill="#000066",
            outline="#1e3a8a"
        )

    # =====================================================
    # RUN SIMULATION
    # =====================================================

    def run_loop(self):

        self.btn.config(
            state="disabled"
        )

        def step():

            if not self.env.is_done():

                percept = (
                    self.env.get_percept()
                )

                action = self.search_agent.sense_and_act(percept)
                

                print(
                        "Algorithm:", self.search_agent.active_algo,
                        "Action:", action,
                        "Position:", self.env.agent_pos,
                        "Remaining Plan:", self.search_agent.plan
                    )

                self.env.execute_action(
                    action
                )

                self.draw_grid()

                self.label.config(
                    text=(
                        f"Score: "
                        f"{self.env.score}"
                        f" | Steps: "
                        f"{self.env.steps}"
                        f" | Action: "
                        f"{action}"
                    )
                )

                self.root.after(
                    250,
                    step
                )

            else:

                if self.env.collision:

                    end_text = (
                        "Collision! "
                        "Game Over! "
                        f"Final Score: "
                        f"{self.env.score}"
                    )

                else:

                    end_text = (
                        "Finished! "
                        f"Final Score: "
                        f"{self.env.score}"
                    )

                self.label.config(
                    text=end_text
                )

                self.btn.config(
                    state="normal"
                )

        step()


# =========================================================
# MAIN PROGRAM
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = GridGameGUI(
        root,
        width=12,
        height=12,
        num_food=15,
        num_opponents=0
    )

    root.mainloop()