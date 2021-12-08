from utils import date_format, parse_date
from commands import Command
from tasks import Task
import time

class StartCommand(Command):
    def exec(self, tasks: Task, args: dict) -> Task:
        task = args["task"]
        amend = "amend" in args
        index = args.get("index", None)
        if index is not None:
            index = int(index)
        t = args.get("t", time.time())
        if isinstance(t, str):
            t = parse_date(t)
        
        task = tasks.start(task, t=t, amend=amend, index=index)

        if amend:
            print(f"Task {task['name']}'s start changed to {date_format(t)}.")
        else:
            print(f"Starting {task['name']}...")

        return tasks