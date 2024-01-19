import unittest

from wordie.ranking import letter_frequencies, rank, suggest


class RankingTests(unittest.TestCase):
    WORDS = ["vwxyz", "abcdf", "abcde"]

    def test_letter_frequencies_counts_letters_across_words(self):
        counts = letter_frequencies(["abcde", "abcdf"])
        self.assertEqual(counts["a"], 2)
        self.assertEqual(counts["e"], 1)
        self.assertEqual(counts["z"], 0)

    def test_rank_orders_by_letter_score_then_alphabetically(self):
        self.assertEqual(rank(self.WORDS), ["abcde", "abcdf", "vwxyz"])

    def test_suggest_returns_the_requested_number_of_words(self):
        self.assertEqual(suggest(self.WORDS, n=1), ["abcde"])
        self.assertEqual(suggest(self.WORDS, n=2), ["abcde", "abcdf"])

    def test_suggest_on_no_words_is_empty(self):
        self.assertEqual(suggest([]), [])


if __name__ == "__main__":
    unittest.main()
