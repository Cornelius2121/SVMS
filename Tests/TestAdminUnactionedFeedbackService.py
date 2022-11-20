from Services.Admin import UnactionedFeedbackService as UService
from Services import TestDatabaseService as Service
from unittest import TestCase

class UnactionedFeedbackServiceTest(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database(prototype=True)


    def test_get_all_unactioned_feedback(self):
        results = UService.select_all_unactioned_feedback(prototype=True)
        self.assertEqual(results[0]['Week'], 1)
        self.assertEqual(results[0]['Unactioned Feedback'][0]['target'], "8216850")
        self.assertEqual(results[0]['Unactioned Feedback'][0]['author'], "1425704")


