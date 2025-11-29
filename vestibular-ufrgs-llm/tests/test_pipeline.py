import unittest
from src.pipeline import process_test

class TestPipeline(unittest.TestCase):

    def test_process_test(self):
        # Assuming the function returns a dictionary with questions and answers
        pdf_path = 'path/to/test.pdf'  # Replace with actual path for testing
        expected_output = {
            "question_1": "answer_1",
            "question_2": "answer_2",
            # Add more expected questions and answers as needed
        }
        
        result = process_test(pdf_path)
        
        self.assertEqual(result, expected_output)

if __name__ == '__main__':
    unittest.main()