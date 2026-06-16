import random
import time
import os

MAZE = [
    "##########",
    "#S...#...#",
    "#.#.#.#..#",
    "#.#...#..#",
    "#.#####..#",
    "#........#",
    "#..#######",
    "#........#",
    "#...#..G.#",
    "##########"
]

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class MazeEnvironment:
    def __init__(self):
        self.grid = [list(row) for row in MAZE]
        self.start = self.find_position("S")
        self.goal = self.find_position("G")

    def find_position(self, symbol):
        for r, row in enumerate(self.grid):
            for c, value in enumerate(row):
                if value == symbol:
                    return (r, c)

    def is_valid(self, position):
        r, c = position
        return self.grid[r][c] != "#"

    def get_neighbours(self, position):
        neighbours = []
        for dr, dc in DIRECTIONS:
            new_pos = (position[0] + dr, position[1] + dc)
            if self.is_valid(new_pos):
                neighbours.append(new_pos)
        return neighbours

    def distance_to_goal(self, position):
        return abs(position[0] - self.goal[0]) + abs(position[1] - self.goal[1])


class Agent:
    def __init__(self, env, controller):
        self.env = env
        self.controller = controller
        self.position = env.start
        self.steps = 0
        self.collisions = 0
        self.visited = set()

    def move(self):
        next_pos = self.controller.decide(self)

        if self.env.is_valid(next_pos):
            self.position = next_pos
            self.visited.add(next_pos)
        else:
            self.collisions += 1

        self.steps += 1

    def reached_goal(self):
        return self.position == self.env.goal


class FSMController:
    def __init__(self):
        self.state = "exploring"

    def decide(self, agent):
        env = agent.env
        neighbours = env.get_neighbours(agent.position)

        if env.distance_to_goal(agent.position) <= 3:
            self.state = "reaching_goal"
        elif len(neighbours) <= 2:
            self.state = "avoiding_obstacle"
        else:
            self.state = "exploring"

        if self.state == "reaching_goal":
            return min(neighbours, key=env.distance_to_goal)

        unvisited = [n for n in neighbours if n not in agent.visited]

        if unvisited and random.random() < 0.75:
            return min(unvisited, key=env.distance_to_goal)

        return random.choice(neighbours)


class BehaviourTreeController:
    def decide(self, agent):
        if self.goal_near(agent):
            return self.move_to_goal(agent)

        if self.obstacle_near(agent):
            return self.avoid_obstacle(agent)

        return self.explore(agent)

    def goal_near(self, agent):
        return agent.env.distance_to_goal(agent.position) <= 4

    def obstacle_near(self, agent):
        return len(agent.env.get_neighbours(agent.position)) <= 2

    def move_to_goal(self, agent):
        neighbours = agent.env.get_neighbours(agent.position)
        return min(neighbours, key=agent.env.distance_to_goal)

    def avoid_obstacle(self, agent):
        neighbours = agent.env.get_neighbours(agent.position)
        unvisited = [n for n in neighbours if n not in agent.visited]
        return random.choice(unvisited) if unvisited else random.choice(neighbours)

    def explore(self, agent):
        neighbours = agent.env.get_neighbours(agent.position)
        unvisited = [n for n in neighbours if n not in agent.visited]

        if unvisited and random.random() < 0.8:
            return min(unvisited, key=agent.env.distance_to_goal)

        return random.choice(neighbours)


class UtilityBasedController:
    def decide(self, agent):
        env = agent.env
        neighbours = env.get_neighbours(agent.position)

        best_position = None
        best_utility = -9999

        for position in neighbours:
            goal_score = -env.distance_to_goal(position) * 4
            visited_penalty = -6 if position in agent.visited else 4
            safety_score = len(env.get_neighbours(position)) * 2

            utility = goal_score + visited_penalty + safety_score

            if utility > best_utility:
                best_utility = utility
                best_position = position

        return best_position


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def show_agent(env, agent, controller_name):
    clear_screen()
    print(f"Controller: {controller_name}")
    print(f"Step: {agent.steps}")
    print()

    for r, row in enumerate(env.grid):
        line = ""
        for c, cell in enumerate(row):
            if (r, c) == agent.position:
                line += "A"
            else:
                line += cell
        print(line)

    time.sleep(0.25)


def run_demo(controller_class, controller_name, max_steps=80):
    env = MazeEnvironment()
    controller = controller_class()
    agent = Agent(env, controller)

    while not agent.reached_goal() and agent.steps < max_steps:
        show_agent(env, agent, controller_name)
        agent.move()

    show_agent(env, agent, controller_name)

    if agent.reached_goal():
        print(f"\n{controller_name} reached the goal in {agent.steps} steps.")
    else:
        print(f"\n{controller_name} did not reach the goal.")

    input("\nPress Enter to exit...")

