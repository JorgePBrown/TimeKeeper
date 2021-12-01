from commands.command import Command
from tasks import Task, TaskError
import re
import sys

class EndCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        try:
            print("\nEnding last task...\n")
            amend = True if "amend" in args else False

            if amend:
                if "duration" in args:
                    start_time = tasks.last_task["start"]
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
            else:
                tasks.end(amend=amend)
        except TaskError as e:
            print(e.message)
        finally:
            return tasks
        