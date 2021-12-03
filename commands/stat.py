from commands.command import Command
from tasks import Task
from time import time

from utils import parse_timespan, row_to_dict, table, date_format

class StatCommand(Command):
    def exec(self, tasks: Task, args) -> Task:
        [op, timeframe] = args["remainder"][0:2]
        now = time()
        start = now - parse_timespan(timeframe)
        print("DATE:", date_format(start))
        df = tasks.from_date(start, ongoing=False)
        df["diff"] = df["end"] - df["start"]

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