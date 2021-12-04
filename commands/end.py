import sys
from time import time as now

from commands import Command, CommandError
from tasks import Task, TaskError
from utils import date_format, parse_date, parse_timespan, sum_time

class EndCommand(Command):
    def exec(self, tasks: Task, args):
        try:
            amend = True if "amend" in args else False
            name = tasks.last_task["name"]
            start_time = tasks.last_task["start"]

            if amend:
                if "duration" in args:
                    try:
                        duration = parse_timespan(args["duration"])
                    except KeyError as e:
                        raise CommandError(e.message)
                        
                    tasks.end(t=start_time + duration, amend=amend)
                    print(f"Corrected {name}. Time ellapsed: {sum_time(duration)}")
                elif "t" in args:
                    t = parse_date(args["t"])
                    tasks.end(t=t, amend=amend)
                    print(f"Corrected {name}. Ended at: {date_format(t)}")
            else:
                t = now()
                tasks.end(t=t, amend=amend)
                print(f"Ended {name}. Time ellapsed: {sum_time(t - start_time)}")
        except TaskError as e:
            raise CommandError(e.message)
        