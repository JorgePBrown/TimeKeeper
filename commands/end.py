import sys
from time import time as now

from commands.command import Command
from tasks import Task, TaskError
from utils import parse_timespan, sum_time

class EndCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        try:
            amend = True if "amend" in args else False
            name = tasks.last_task["name"]
            start_time = tasks.last_task["start"]

            if amend:
                if "duration" in args:
                    try:
                        duration = parse_timespan(args["duration"])
                    except KeyError:
                        sys.exit(1)
                        
                    tasks.end(t=start_time + duration, amend=amend)
                    print(f"Corrected {name}. Time ellapsed: {sum_time(duration)}")
            else:
                t = now()
                tasks.end(t=t, amend=amend)
                print(f"Ended {name}. Time ellapsed: {sum_time(t - start_time)}")
        except TaskError as e:
            print(e.message)
        finally:
            return tasks
        