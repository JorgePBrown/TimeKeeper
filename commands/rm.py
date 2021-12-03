from commands import Command
from tasks import Task

class RemoveCommand(Command):
    def exec(self, tasks: Task, args) -> Task:

        index = args["remainder"]
        index = map(lambda x: int(x), index)
        tasks.remove(index)

        return tasks
