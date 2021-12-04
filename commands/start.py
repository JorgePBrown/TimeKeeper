from utils import parse_date
from commands import Command
from tasks import Task
import time

class StartCommand(Command):
    def exec(self, tasks: Task, args: dict) -> Task:
        task = args["task"]
        amend = "amend" in args
        index = args.get("i", None)
        t = args.get("t", time.time())
        if isinstance(t, str):
            t = parse_date(t)
        print(f"\nStarting {task}...\n")

        return tasks.start(task, t=t, amend=amend, index=index)