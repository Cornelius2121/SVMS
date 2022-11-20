from Services import TestDatabaseService as Service
from unittest import TestCase
from config import PROTOTYPE_DATABASE


class PrototypeDatabaseSetupTest(TestCase):
    @classmethod
    def setUp(self) -> None:
        Service.setup_prototype_database()


