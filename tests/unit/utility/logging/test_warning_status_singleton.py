import unittest

from wavealign.utility.logging.warning_status_singleton import WarningStatusSingleton


class TestWarningStatusSingleton(unittest.TestCase):
    def setUp(self) -> None:
        WarningStatusSingleton._instance = None

    def test_singleton_behavior(self):
        instance1 = WarningStatusSingleton()
        instance2 = WarningStatusSingleton()
        self.assertIs(instance1, instance2)

    def test_initial_state(self):
        instance = WarningStatusSingleton()
        self.assertFalse(instance.get_warning_counts())

    def test_set_warning_counts(self):
        instance = WarningStatusSingleton()
        instance.set_warning_counts()
        self.assertTrue(instance.get_warning_counts())

    def test_singleton_persistence(self):
        instance1 = WarningStatusSingleton()
        instance1.set_warning_counts()
        instance2 = WarningStatusSingleton()
        self.assertTrue(instance2.get_warning_counts())
