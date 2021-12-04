import sys
from time import time as now

from commands import Command, CommandError
from tasks import Task, TaskError
from utils import date_format, parse_date, parse_timespan, sum_time

class EndCommand(Command):
    def exec(self, tasks: Task, args):
        try:
            amend = True if "amend" in args else False
            index = args.get("index", None)
            if isinstance(index, str):
                index = int(index)

            if amend:
                if "duration" in args:
                    try:
                        duration = parse_timespan(args["duration"])
                    except KeyError as e:
                        raise CommandError(e.message)
                    task = tasks.df.loc[index, :]
                    task = tasks.end(t=task['start'] + duration, amend=amend, index=index)
                    print(f"Corrected {task['name']}. Time ellapsed: {sum_time(duration)}")
                elif "t" in args:
                    t = parse_date(args["t"])
                    task = tasks.end(t=t, amend=amend, index=index)
                    print(f"Corrected {task['name']}. Ended at: {date_format(t)}")
            else:
                t = now()
                task = tasks.end(t=t, amend=amend)
                print(f"Ended {task['name']}. Time ellapsed: {sum_time(t - task['start'])}")
        except TaskError as e:
            raise CommandError(e.message)
        