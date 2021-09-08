# CasearCodeBreaker
### Give me your text, and I will decrypt it - probably ;)
CasearCodeBreaker is a Python class that automatically decrypts given text based on relative frequencies of letters. Work for Polish and English.

The decryption process consists of these steps:
- count occurrences of each letter in given text,
- compare these counted frequencies with those specified in `frequencies.csv`,
- find the alphabet shift in Casear cipher that minimizes the difference
- shift all letters in the given text back to decrypt it.

### Usage  
Argument 'path_to_file' is optional. Default path is 'message.txt' (meaning a file located in your current directory).
>\> python CasearCodeBreaker.py [path_to_file]

### The longer the text, the better.

Letter frequencies specified in `frequencies.csv` are from [Wikipedia](https://en.wikipedia.org/wiki/Letter_frequency#Relative_frequencies_of_letters_in_other_languages).
