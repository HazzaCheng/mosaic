import unittest
import random

from mosaic.scenario import ListTask, ComplexScenario, ChoiceScenario
class TestScenario(unittest.TestCase):

    def test_call(self):
        arr1 = ["x1_p1", "x1_p2"]
        arr2 = ["x2_p1", "x2_p2"]

        x1 = ListTask(name = "x1", is_ordered=False, tasks = arr1.copy())
        x2 = ListTask(name = "x2", is_ordered=True, tasks = arr2.copy())

        start = ComplexScenario(name = "Model", scenarios=[x1, x2], is_ordered=True)

        assert(start.call() == "Model")
        assert(start.call() == "x1")
        assert(start.call() in ["x1_p1", "x1_p2"])
        assert(start.call() in ["x1_p1", "x1_p2"])
        assert(start.call() == "x2")
        assert(start.call() == "x2_p1")
        assert(start.call() == "x2_p2")

    def test_execute(self):
        arr1 = ["x1_p1"]
        arr2 = ["x2_p1", "x2_p2"]

        x1 = ListTask(name = "x1", is_ordered=False, tasks = arr1.copy())
        x2 = ListTask(name = "x2", is_ordered=True, tasks = arr2.copy())

        start = ComplexScenario(name = "Model", scenarios=[x1, x2], is_ordered=True)

        assert(start.execute("Model") == "Model")
        assert(start.execute("x1") == "x1")
        assert(start.execute("x1_p1") == "x1_p1")
        assert(start.execute("x2") == "x2")
        assert(start.execute("x2_p1") == "x2_p1")
        assert(start.execute("x2_p2") == "x2_p2")

    def test_queue_task(self):
        arr1 = ["x1_p1"]
        arr2 = ["x2_p1", "x2_p2"]

        x1 = ListTask(name = "x1", is_ordered=False, tasks = arr1.copy())
        x2 = ListTask(name = "x2", is_ordered=True, tasks = arr2.copy())

        start = ComplexScenario(name = "Model", scenarios=[x1, x2], is_ordered=True)

        assert(start.queue_tasks() == ["Model"])
        start.call()
        assert(start.queue_tasks() == ["x1", "x2"])
        start.call()
        assert(start.queue_tasks() == ["x1_p1"])
        start.call()
        assert(start.queue_tasks() == ["x2"])
        start.call()
        assert(start.queue_tasks() == ["x2_p1"])

    def test_finished(self):
        arr1 = ["x1_p1", "x1_p2"]
        arr2 = ["x2_p1", "x2_p2"]
        x1 = ListTask(name = "x1", is_ordered=False, tasks = arr1)
        x2 = ListTask(name = "x2", is_ordered=True, tasks = arr2)
        start = ComplexScenario(name = "Model", scenarios=[x1, x2], is_ordered=True)

        for t in range(4):
            start.call()
        assert(x1.finished())

        for t in range(3):
            start.call()
        assert(x2.finished())
        assert(start.finished())

    def test_choice_scenario(self):
        arr1 = ["x1_p1", "x1_p2"]
        arr2 = ["x2_p1", "x2_p2"]
        x1 = ListTask(name = "x1", is_ordered=False, tasks = arr1)
        x2 = ListTask(name = "x2", is_ordered=True, tasks = arr2)
        start = ChoiceScenario(name = "Model", scenarios=[x1, x2])
        assert(start.call() == "Model")
        assert(start.queue_tasks() == ["x1", "x2"])
        start.execute("x2")
        assert(start.call() == "x2_p1")
        assert(start.call() == "x2_p2")
        assert(start.finished())