# CasearCodeBreaker
### Give me your text and I will decrypt it - probably ;)
CasearCodeBreaker is a Python class that automatically decrypts given text based on relative frequencies of letters in given language.

The decryption process consists of these steps:
- count occurences of each letter in given text,
- compare these counted frequencies with those found in [Wikipedia](https://en.wikipedia.org/wiki/Letter_frequency#Relative_frequencies_of_letters_in_other_languages),
- find the alphabet shift in Casear cipher that minimizes the difference
- shift all letters in the given text back to decrypt it.

### The longer the text, the better are your chances of succeeding!

Source of letter frequencies specified in `frequencies.csv` file: [Wikipedia](https://en.wikipedia.org/wiki/Letter_frequency#Relative_frequencies_of_letters_in_other_languages).
