import time
import numpy as np
import pandas as pd

class TaskError(Exception):
    @property
    def message(self) -> str:
        return self.args[0]

class Task:
    def __init__(self, df=None) -> None:
        self.df = pd.DataFrame(columns=["name", "start", "end"]) if df is None else df

    @property
    def last_task(self):
        return self.df.iloc[-1, :] if self.df.shape[0] > 0 else None

    @property
    def ongoing_task(self):
        last = self.last_task
        if last is not None and np.isnan(last["end"]):
            return last
        else:
            return None

    def from_file(f):
        return Task(pd.read_csv(f))

    def to_file(self, f):
        self.df.to_csv(f, index=False)

    def __str__(self) -> str:
        return str(self.df)

    def list(self, task=None):
        if task is None:
            print(self.df)
        else:
            print(self.df.loc[self.df["name"] == task, ["start", "end"]])

    def tick(self, task=None, t=time.time()):
        if (self.df.shape[0] == 0):
            self.start(task, t)
            return

        last_task = self.df.iloc[-1, :]

        if task is None:
            self.end(t)
        else:
            if last_task["name"] == task:
                self.end(t)
            else:
                try:
                    self.end(t)
                except TaskError:
                    pass

                self.start(task, t)

        return self

    def start(self, task, t=time.time()):
        if task is None:
            raise TaskError("Cannot start a task with no name.")

        if self.df.shape[0] > 0:
            last_task = self.df.iloc[-1, :]
            
            if np.isnan(last_task["end"]):
                if last_task["name"] == task:
                    return self
                else:
                    self.df.at[self.df.shape[0] - 1, "end"] = t
        
        self.df = self.df.append({"name": task, "start": t}, ignore_index=True)

        return self

    def end(self, t=time.time(), amend=False):
        if self.df.shape[0] > 0:
            last_task = self.df.iloc[-1, :]

            if amend:
                if np.isnan(last_task["end"]):
                    raise TaskError("Can't amend unfinished task.")
                else:
                    if t - last_task["start"] < 60:
                        self.df.drop(self.df.index[self.df.shape[0] - 1], inplace=True)
                        raise TaskError("Task with less than one minute not allowed.")
                    else:
                        self.df.at[self.df.shape[0] - 1, "end"] = t
            else:
                if np.isnan(last_task["end"]):
                    if t - last_task["start"] < 60:
                        self.df.drop(self.df.index[self.df.shape[0] - 1], inplace=True)
                        raise TaskError("Task with less than one minute not allowed.")
                    else:
                        self.df.at[self.df.shape[0] - 1, "end"] = t
                else:
                    raise TaskError("No ongoing task.")
            
            return self
        else:
            raise TaskError("No ongoing task.")
    
    def remove(self, index):
        self.df.drop(index=index, inplace=True)
        return self

    def from_date(self, start, ongoing=True):
        df = self.df.loc[self.df["start"] > start, :]
        if not ongoing:
            if np.isnan(df.loc[df.index[-1], "end"]):
                df = df.iloc[0:-1, :]
        return df

    def with_name(self, task):
        return self.df.loc[self.df["name"] == task, :]