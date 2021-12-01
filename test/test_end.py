import time
import unittest
import numpy as np
import pandas as pd

from .context import src
from src import tasks

class EndTests(unittest.TestCase):

    def test_empty(self):
        t = tasks.Task()

        with self.assertRaises(tasks.TaskError):
            t.end()

        self.assertEqual(0, t.df.shape[0])
        
    def test_started_task(self):
        tim = time.time()
        df = pd.DataFrame({"name": ["a", "b"], "start": [1321321312, 3214891875], "end": [237482202, np.nan]})
        t = tasks.Task(df)

        t.end(tim)

        self.assertEqual(2, t.df.shape[0])
        row = t.df.iloc[-1, :]
        self.assertEqual("b", row["name"])
        self.assertEqual(3214891875, row["start"])
        self.assertEqual(tim, row["end"])

    def test_no_started_task(self):
        tim = time.time()
        df = pd.DataFrame({"name": ["a", "b"], "start": [1321321312, 3214891875], "end": [237482202, 2138716278]})
        t = tasks.Task(df)

        with self.assertRaises(tasks.TaskError):
            t.end(tim)

        self.assertEqual(2, t.df.shape[0])
        row = t.df.iloc[-1, :]
        self.assertEqual("b", row["name"])
        self.assertEqual(3214891875, row["start"])
        self.assertEqual(2138716278, row["end"])

    def test_already_started_task(self):
        tim = time.time()
        df = pd.DataFrame({"name": ["a", "b"], "start": [1321321312, 3214891875], "end": [237482202, np.nan]})
        t = tasks.Task(df)

        t.end(tim)

        self.assertEqual(2, t.df.shape[0])
        row = t.df.iloc[-1, :]
        self.assertEqual("b", row["name"])
        self.assertEqual(3214891875, row["start"])
        self.assertEqual(tim, row["end"])

if __name__ == '__main__':
    unittest.main()