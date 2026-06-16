from maze_core import (
    MazeEnvironment,
    Agent,
    FSMController,
    BehaviourTreeController,
    UtilityBasedController
)


def run_simulation(controller_class, runs=1000, max_steps=100):
    success_count = 0
    total_steps = 0
    total_collisions = 0

    for _ in range(runs):
        env = MazeEnvironment()
        controller = controller_class()
        agent = Agent(env, controller)

        while not agent.reached_goal() and agent.steps < max_steps:
            agent.move()

        if agent.reached_goal():
            success_count += 1
            total_steps += agent.steps
        else:
            total_steps += max_steps

        total_collisions += agent.collisions

    success_rate = (success_count / runs) * 100
    average_steps = total_steps / runs
    obstacle_avoidance_rate = 100 - ((total_collisions / (runs * max_steps)) * 100)

    return success_rate, average_steps, obstacle_avoidance_rate


def main():
    controllers = {
        "Finite State Machine": FSMController,
        "Behaviour Tree": BehaviourTreeController,
        "Utility-Based System": UtilityBasedController
    }

    print("Performance Evaluation Results")
    print("-" * 80)
    print(f"{'Controller':<25}{'Success Rate':<18}{'Average Steps':<18}{'Obstacle Avoidance'}")
    print("-" * 80)

    for name, controller in controllers.items():
        success, steps, avoidance = run_simulation(controller)

        print(
            f"{name:<25}"
            f"{success:.2f}%{'':<12}"
            f"{steps:<18.2f}"
            f"{avoidance:.2f}%"
        )


if __name__ == "__main__":
    main()