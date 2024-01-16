import unittest

from wordie.feedback import parse_pattern, score_guess


class ScoreGuessTests(unittest.TestCase):
    def test_right_answer_is_all_green(self):
        self.assertEqual(score_guess("abide", "abide"), "GGGGG")

    def test_no_shared_letters_is_all_black(self):
        self.assertEqual(score_guess("crane", "stomp"), "BBBBB")

    def test_letters_in_the_wrong_place_are_yellow(self):
        self.assertEqual(score_guess("stare", "rates"), "YYYYY")

    def test_mixed_pattern(self):
        self.assertEqual(score_guess("crane", "abide"), "BBYBG")

    def test_repeated_letter_in_guess(self):
        # Captured from the current output so a future change shows up here.
        self.assertEqual(score_guess("speed", "abide"), "BBYYY")

    def test_uppercase_input_is_accepted(self):
        self.assertEqual(score_guess("CRANE", "ABIDE"), "BBYBG")


class ParsePatternTests(unittest.TestCase):
    def test_lowercase_and_spaces_are_cleaned_up(self):
        self.assertEqual(parse_pattern(" bbybg "), "BBYBG")

    def test_bad_patterns_are_rejected(self):
        with self.assertRaises(ValueError):
            parse_pattern("BBYB")
        with self.assertRaises(ValueError):
            parse_pattern("BBXBG")


if __name__ == "__main__":
    unittest.main()
