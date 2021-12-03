from time import time as now

from commands.command import Command
from tasks import Task, TaskError
import re
import sys
from utils import sum_time

class EndCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        try:
            amend = True if "amend" in args else False
            name = tasks.last_task["name"]
            start_time = tasks.last_task["start"]

            if amend:
                if "duration" in args:
                    times = re.findall("[0-9]+[a-z]", args["duration"])
                    duration = 0
                    unit_conversion = {
                        "s": 1,
                        "m": 60,
                        "h": 60 * 60,
                        "d": 60 * 60 * 24
                    }
                    for time in times:
                        value = int(time[0:-1])
                        unit = time[-1]
                        try:
                            duration += value * unit_conversion[unit]
                        except KeyError:
                            print(f"Used time unit {unit}.Available time units are s, m, h, d.")
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
        