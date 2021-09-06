import numpy as np
import pandas as pd
import re
import sys
from collections import Counter


class CasearCodeBreaker:
    """
    This class can decrypt text encrypted with Casear Cipher using letter frequencies.
    """
    _path_to_frequencies_csv = 'frequencies.csv'

    ALPHABET_EN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    ALPHABET_PL = 'AĄBCĆDEĘFGHIJKLŁMNŃOÓPRSŚTUWYZŹŻ'
    _selected_alphabet = ALPHABET_PL
    _selected_language = 'Polish'
    _input_string = None
    _clean_string = None

    def _read_txt(self, path, encoding='utf8'):
        self._input_string = open(path, "r", encoding=encoding).read().upper()
        self._clean_string = re.sub('[^' + self._selected_alphabet + ']+', '', self._input_string)

    def _count_letters_freq(self, ):
        counts = pd.DataFrame.from_dict(Counter(self._clean_string), orient='index').sort_index()
        return counts.rename(columns={0: 'counted'})

    def _merge_with_avg_freq(self, counted_df, ):
        df_avg = pd.read_csv(self._path_to_frequencies_csv, index_col='Letter')
        df_merged = counted_df.merge(df_avg, how='right', left_index=True, right_index=True).fillna(0).reindex(
            [char for char in self._selected_alphabet])

        df_merged = df_merged[['counted', self._selected_language]][
            (df_merged[[self._selected_language]] > 0).values]
        df_merged.rename(columns={'counted': 'counted', self._selected_language: 'averaged'}, inplace=True)
        return df_merged

    def _get_avg_occurences_counts(self, df):
        df.iloc[:, [1]] *= len(self._input_string)
        return df

    def _compute_square_dif_for_every_rotations(self, original, averaged):
        orig = original.values
        aver = averaged.values
        scores = {}
        for i in range(len(orig)):
            rotated = np.concatenate([orig[i:], orig[:i]])
            scores[i] = sum((aver - rotated) ** 2)
        return pd.DataFrame.from_dict(scores, orient='index').rename(columns={0: 'Square error'})

    def _compute_diffs(self, df_freqs):
        df_freqs = self._merge_with_avg_freq(df_freqs)
        df_freqs = self._get_avg_occurences_counts(df_freqs)
        df_diffs_plen = self._compute_square_dif_for_every_rotations(df_freqs.counted, df_freqs.averaged)
        return df_diffs_plen

    def _find_bottom_most_outliers_from_array(self, input_df):
        a = np.array([value for item in input_df.values for value in item.tolist()])
        upper_quartile = np.percentile(a, 75)
        lower_quartile = np.percentile(a, 25)
        results = [x for x in a.tolist() if
                   x < lower_quartile - (upper_quartile - lower_quartile) * 1.5]  # bottom outliers
        return results

    def _find_most_probable_rotations(self, freq_diff_dataframe):
        results = self._find_bottom_most_outliers_from_array(freq_diff_dataframe)
        if not results:
            return freq_diff_dataframe['Square error'].idxmin()
        else:
            results.sort()
            return freq_diff_dataframe[freq_diff_dataframe['Square error'] <= max(results[:3])].index

    def _rotate_text(self, text, rotation):
        alphabet_rotated = self._selected_alphabet[rotation:] + self._selected_alphabet[:rotation]
        rotation_dic = text.maketrans(alphabet_rotated, self._selected_alphabet)
        return text.translate(rotation_dic)

    def _udpate_alphabet(self):
        language = self._selected_language
        if language == 'Polish':
            new_alphabet = self.ALPHABET_PL
        elif language == 'English':
            new_alphabet = self.ALPHABET_EN
        else:
            new_alphabet = self._selected_alphabet
        self._selected_alphabet = new_alphabet

    def set_language(self, language='Polish'):
        self._selected_language = language
        self._udpate_alphabet()

    def decrypt(self, path_to_encrypted_text, language=None):
        if language: self.set_language(language=language)
        self._read_txt(path_to_encrypted_text)
        df_freqs = self._count_letters_freq()

        df_diffs = self._compute_diffs(df_freqs)
        guessed_rotations_pl = self._find_most_probable_rotations(df_diffs)
        for rotation in guessed_rotations_pl:
            print(f'\nRotation: {rotation}, alphabet: {self._selected_alphabet}\n')
            print(self._rotate_text(self._input_string, rotation))


"""
Run this file to automatically decrypt text encrypted with Casear cipher. 

Requirements: a file called `frequencies.csv` must be located in the same directory
as this Python file. 

Usage:
> python CasearCodeBreaker.py [path_to_encrypted_txt]

If no path is specified, the script will look for a file named 'message.txt' located
in the same directory as the script.
"""
if __name__ == '__main__':
    path_to_encrypted_message = sys.argv[1:] if len(sys.argv) > 1 else 'message.txt'

    decryptor = CasearCodeBreaker()
    decryptor.set_language('Polish')
    decryptor.decrypt(path_to_encrypted_message)
