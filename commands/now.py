from commands import Command
from tasks import Task
from utils import sum_time
from time import time as now

class NowCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        ongoing = tasks.ongoing_task
        if ongoing is not None:
            print(f"Current task: {ongoing['name']} - {sum_time(now()-ongoing['start'])}")
        else:
            print("No task being performed right now.")
        return tasks