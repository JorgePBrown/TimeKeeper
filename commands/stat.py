from commands import Command, CommandError
from tasks import Task
from time import time

from utils import parse_timespan, row_to_dict, table, date_format

class StatCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        [op, timeframe] = args["remainder"][0:2]
        now = time()
        try:
            start = now - parse_timespan(timeframe)
        except AssertionError as e:
            raise CommandError(f"{e.args[0]} Timespan given: {timeframe}") from e
        except KeyError as e:
            raise CommandError("Unavailable unit selected. " + e.args[0]) from e
        df = tasks.from_date(start, ongoing=False)
        df.loc[:, "diff"] = df.loc[:, "end"] - df.loc[:, "start"]

        if op == "avg":
            df.groupby("name").mean()
        elif op == "sum":
            s = df[["name", "diff"]].groupby("name").sum()
            s.reset_index(inplace=True)
            headers = ["name", "total_time"]
            s.rename(columns={"index": "name", "diff": "total_time"}, inplace=True)
            values = [row_to_dict(headers, row) for _, row in s.iterrows()]                
            table(headers, values)
        return super().exec(tasks, args)