from commands import Command
from tasks import Task
from utils import table, row_to_dict

class ListCommand(Command):
    def exec(self, tasks: Task, args) -> Task:

        def list_general(tasks, cols, n=10, index=False):
            tasks_to_list = tasks.tail(n)[cols]
            if index:
                cols = cols.insert(0, "index")
            values = []
            for i, task_to_list in tasks_to_list.iterrows():
                task_to_list["index"] = i
                row = row_to_dict(cols, task_to_list)
                values.append(row)

            table(cols, values)

        # args
        task = args["task"]
        index = "i" in args
        n = args["n"] if "n" in args else 10

        if task is None:
            df = tasks.df.copy()
            df["diff"] = df["end"] - df["start"]
            list_general(df, df.columns, df.shape[0] if n == "all" else n, index=index)
        else:
            df = tasks.with_name(task)
            df = df.drop(columns="name")
            df["diff"] = df["end"] - df["start"]
            list_general(df, df.columns, df.shape[0] if n == "all" else n, index=index)

        return tasks