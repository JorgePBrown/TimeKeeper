from commands.command import Command
from tasks import Task

class NowCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        ongoing = tasks.ongoing_task
        if ongoing is not None:
            print(f"Current task is: {ongoing['name']}")
        else:
            print("No task being performed right now.")
        return tasks