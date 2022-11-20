from Services import TestDatabaseService as Service
from Services import FeedbackService
import random
from unittest import TestCase
import config
import datetime


class FeedbackServiceTest(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database(prototype=True)

    def generate_random_metrics(self):
        num_of_metrics = config.METRIC_COUNT
        metrics = []
        for i in range(0, num_of_metrics):
            metrics.append(random.randrange(1, 5))
        return metrics

    def test_insert_new_feedback(self):
        metrics = self.generate_random_metrics()
        goodcomment = "This is an good example comment"
        badcomment = "This is a bad example comment"
        time = datetime.datetime.strptime("2021-09-11 12:56:21", "%Y-%m-%d %H:%M:%S")
        target = 1
        author = 2
        report = 0
        id = FeedbackService.insert_new_feedback(metrics=metrics, goodcomment=goodcomment, badcomment=badcomment,
                                                 target=target, submitter=author, time=time, prototype=True)
        results = FeedbackService.get_feedback_from_id(id, True)
        self.assertEqual(target, results[0]['target'])
        self.assertEqual(author, results[0]['author'])
        self.assertEqual(str(report), results[0]['report'])
        self.assertEqual(time, results[0]['timesubmitted'])
        self.assertEqual(metrics[0], results[0]['metric1'])
