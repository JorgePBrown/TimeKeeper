from commands import Command
from tasks import Task


class DebugCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        instructions = args["remainder"]
        for instruction in instructions:
            eval(instruction)
        return super().exec(tasks, args)