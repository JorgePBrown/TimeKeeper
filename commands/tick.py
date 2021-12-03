from commands import Command
from tasks import Task

class TickCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        task = args["task"]
        print(f"\nTicking {task}...\n")
        return tasks.tick(task)