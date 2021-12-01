import numpy as np
from commands.command import Command
from datetime import datetime
from tasks import Task
from utils import sum_time

class ListCommand(Command):
    def exec(self, tasks: Task, args) -> Task:

        def row_to_dict(cols, row):
            ret = {}
            for col in cols:
                if isinstance(row[col], float) and np.isnan(row[col]):
                    v = "-"
                elif col == "start" or col == "end":
                    v = datetime.fromtimestamp(row[col]).strftime("%d-%m-%Y %H:%M")
                elif col == "diff":
                    v = sum_time(row[col])
                else:
                    v = str(row[col])
                
                ret[col] = v

            return ret

        def list_general(tasks, cols, n=10, index=False):
            tasks_to_list = tasks.tail(n)[cols]
            if index:
                cols = cols.insert(0, "index")
            lengths = [len(col) for col in cols]
            values = []
            for i, task_to_list in tasks_to_list.iterrows():
                task_to_list["index"] = i
                row = row_to_dict(cols, task_to_list)
                values.append(row)
                for i, col in enumerate(cols):
                    if len(row[col]) > lengths[i]:
                        lengths[i] = len(row[col])

            # headers
            break_line = "".join("".join(["|-" + "-" * l + "-|"]) for l in lengths)
            print(break_line)
            headers = ""
            for i, col in enumerate(cols):
                half = (lengths[i] - len(col)) // 2
                extra = (lengths[i] - len(col)) % 2
                headers += "| " + " " * (half + extra) + col + " " * half + " |"
            print(headers)
            print(break_line)

            for val in values:
                row = ""
                for i, col in enumerate(cols):
                    v = val[col]
                    half = (lengths[i] - len(v)) // 2
                    extra = (lengths[i] - len(v)) % 2
                    row += "| " + " " * (half + extra) + v + " " * half + " |"
                print(row)
            # end
            print(break_line)

        task = args["task"]
        index = "i" in args
        n = args["n"] if "n" in args else 10
        df = tasks.df.copy()
        df["diff"] = df["end"] - df["start"]
        if task is None:
            list_general(df, df.columns, df.shape[0] if n == "all" else n, index=index)
        else:
            df = df.loc[df["name"] == task, :]
            total_time = df["diff"].sum()
            print(f"Total time: {sum_time(total_time)}")
            list_general(df, ["start", "end", "diff"], df.shape[0] if n == "all" else n, index=index)

        return tasks