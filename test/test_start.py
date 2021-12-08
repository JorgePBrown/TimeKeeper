import time
import unittest
import numpy as np
import pandas as pd
import tasks

class StartTests(unittest.TestCase):

    def test_empty(self):
        tim = time.time()
        t = tasks.Task()
        
        t.start("abc", tim)

        self.assertEqual(1, t.df.shape[0])
        row = t.df.iloc[0, :]
        self.assertEqual("abc", row["name"])
        self.assertEqual(tim, row["start"])
        self.assertTrue(np.isnan(row["end"]))

    def test_started_task(self):
        tim = time.time()
        df = pd.DataFrame({"name": ["a", "b"], "start": [1321321312, 3214891875], "end": [237482202, np.nan]})
        t = tasks.Task(df)

        t.start("c", tim)

        self.assertEqual(3, t.df.shape[0])
        row = t.df.iloc[-2, :]
        self.assertEqual("b", row["name"])
        self.assertEqual(3214891875, row["start"])
        self.assertEqual(tim, row["end"])
        row = t.df.iloc[-1, :]
        self.assertEqual("c", row["name"])
        self.assertEqual(tim, row["start"])
        self.assertTrue(np.isnan(row["end"]))

    def test_no_started_task(self):
        tim = time.time()
        df = pd.DataFrame({"name": ["a", "b"], "start": [1321321312, 3214891875], "end": [237482202, 2138716278]})
        t = tasks.Task(df)

        t.start("c", tim)

        self.assertEqual(3, t.df.shape[0])
        row = t.df.iloc[-1, :]
        self.assertEqual("c", row["name"])
        self.assertEqual(tim, row["start"])
        self.assertTrue(np.isnan(row["end"]))

    def test_already_started_task(self):
        tim = time.time()
        df = pd.DataFrame({"name": ["a", "b"], "start": [1321321312, 3214891875], "end": [237482202, np.nan]})
        t = tasks.Task(df)

        t.start("b", tim)

        self.assertEqual(2, t.df.shape[0])
        row = t.df.iloc[-1, :]
        self.assertEqual("b", row["name"])
        self.assertEqual(3214891875, row["start"])
        self.assertTrue(np.isnan(row["end"]))

if __name__ == '__main__':
    unittest.main()