from tasks import Task

class Command:
    def __init__(self, help=None) -> None:
        self.help = help

    def exec(self, tasks: Task, args):
        pass

class HelpCommand(Command):
    def exec(self, tasks, args):
        print("-h, --help ------------------ for help")
        print("-t <task>, --task <task> ---- for clocking in or out on a task")
        print("-l -------------------------- to list tasks")
        print()
        return tasks

class CommandError(Exception):
    @property
    def message(self) -> str:
        return self.args[0]
       