from commands.command import Command
from tasks import Task

class StartCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        task = args["task"]
        print(f"\nStarting {task}...\n")
        return tasks.start(task)