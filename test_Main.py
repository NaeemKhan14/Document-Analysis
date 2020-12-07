from unittest import TestCase
from Main import Main


class TestMain(TestCase):

    def setUp(self):
        self.main_task = Main()


class TestErrors(TestMain):

    def test_invalid_file_format(self):
        self.assertEqual(self.main_task.run_task('requirements.txt', '2a'),
                         'Invalid file format. Only .json files are allowed.')

    def test_invalid_task(self):
        self.assertEqual(self.main_task.run_task('sample_100k_lines.json', '11'),
                         'Invalid or no task ID given. Please use -h for more help.')

    def test_no_doc_id(self):
        self.assertEqual(self.main_task.run_task('sample_100k_lines.json', '2a'),
                         'No document uuid provided. Please use -h for more help.')
