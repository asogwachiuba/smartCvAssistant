import unittest
from content_selector import parse_items

class TestParseItems(unittest.TestCase):

    def test_with_comma(self):
        raw = ["Python, Java, SQL"]
        expected = ["Python", "Java", "SQL"]
        self.assertEqual(parse_items(raw, ","), expected)
        
    def test_with_multiple_symbols(self):
        raw = ["Python, Java . Help \n Me | I am ! tired , SQL"]
        expected = ["Python", "Java . Help \n Me | I am ! tired", "SQL"]
        self.assertEqual(parse_items(raw, ","), expected)
        
    def test_with_multiple_raw_inputs(self):
        raw = ["Python, Java", " Hello, there . ", "Help \n Me", ", I am ! tired , SQL"]
        expected = ["Python", "Java Hello", "there . Help \n Me", "I am ! tired", "SQL"]
        self.assertEqual(parse_items(raw, ","), expected)

    def test_with_pipe(self):
        raw = ["Docker | Kubernetes | Jenkins"]
        expected = ["Docker", "Kubernetes", "Jenkins"]
        self.assertEqual(parse_items(raw, "|"), expected)

    def test_with_none_separator(self):
        raw = ["Flutter Development"]
        expected = ["Flutter Development"]
        self.assertEqual(parse_items(raw, None), expected)

    def test_ignores_empty_items(self):
        raw = ["   ", "", "Python| , Java  "]
        expected = ["Python|", "Java  "]
        self.assertEqual(parse_items(raw, ","), expected)
        
    def test_irregular_spacing(self):
        raw = ["  Python&  ,  Java ,  SQL  "]
        expected = ["  Python&", "Java", "SQL  "]
        self.assertEqual(parse_items(raw, ","), expected)
        
    def test_trailing_separator(self):
        raw = ["Python, Java, "]
        expected = ["Python", "Java"]
        self.assertEqual(parse_items(raw, ","), expected)

    def test_multiple_commas(self):
        raw = ["Python,,Java"]
        expected = ["Python", "Java"]
        self.assertEqual(parse_items(raw, ","), expected)
        
    def test_mixed_case(self):
        raw = ["python, JAVA, Sql"]
        expected = ["python", "JAVA", "Sql"]
        self.assertEqual(parse_items(raw, ","), expected) 
        
    def test_pipe_separator(self):
        raw = ["Python | Java | SQL"]
        expected = ["Python", "Java", "SQL"]
        self.assertEqual(parse_items(raw, "|"), expected)

    def test_semicolon_separator(self):
        raw = ["Python;Java;SQL"]
        expected = ["Python", "Java", "SQL"]
        self.assertEqual(parse_items(raw, ";"), expected)

    def test_bullet_separator(self):
        raw = ["• Python • Java • SQL"]
        expected = ["Python", "Java", "SQL"]
        self.assertEqual(parse_items(raw, "•"), expected)

    def test_newline_separator(self):
        raw = ["Python\nJava\nSQL"]
        expected = ["Python", "Java", "SQL"]
        self.assertEqual(parse_items(raw, "\n"), expected)





if __name__ == '__main__':
    unittest.main()
