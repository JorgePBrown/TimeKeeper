from commands.command import Command
from datetime import datetime
from tasks import Task

class ListCommand(Command):
    def exec(self, tasks: Task, args) -> Task:

        def row_to_dict(cols, row):
            ret = {}
            for col in cols:
                if col == "start" or col == "end":
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

        def sum_time(time):
            ret = ""
            # secs
            #secs = time % 60
            remainder = time // 60
            #ret = f"{int(secs)} seconds" + ret
            if remainder == 0:
                return ret
            # mins
            mins = remainder % 60
            remainder = remainder // 60
            ret = f"{int(mins)} minutes" + ret
            if remainder == 0:
                return ret
            # hours
            hours = remainder % 24
            remainder = remainder // 24
            ret = f"{int(hours)} hours, " + ret
            if remainder == 0:
                return ret
            # days
            days = remainder
            ret = f"{int(days)} days, " + ret

            return ret

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