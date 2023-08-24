import requests
from bs4 import BeautifulSoup
from nltk.stem import WordNetLemmatizer
import csv  
import time

def convert_to_past_tense(verb):
    lemmatizer = WordNetLemmatizer()
    past_tense_verb = lemmatizer.lemmatize(verb, 'v')
    return past_tense_verb

def get_word_meaning_from_longman(word):
    try:
        # Define the URL for the Longman page
        url = f'https://www.ldoceonline.com/dictionary/english/{word}'
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers)

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the element that contains the meaning
        meaning_element = soup.find('span', {'class': 'Sense'})
        time.sleep(1)
        if meaning_element:
            # Get the text content of the meaning element
            meaning = meaning_element.get_text()
            return meaning.strip()
        else:
            return None
        
    except requests.exceptions.RequestException as e:
        print("Error fetching data from Longman website:", str(e))
        return None

def fetch_longman_words(lc_words):
    try:
        # Use the URL link to Longman Communication 3000
        url = 'https://www.ldoceonline.com/dictionary/english'

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception if the response is not successful

        soup = BeautifulSoup(response.text, 'html.parser')

        for entry in soup.select('.Entry'):
            word = entry.select_one('.Head .HYPHENATION')
            if word:
                lc_words.add(word.get_text().strip().lower())

        return lc_words

    except requests.exceptions.RequestException as e:
        print("Error fetching data from Longman website:", str(e))
        return set()

def find_unsimilar_words(srt_file_l, lc_words):
    with open(srt_file_l, 'r') as srt_file:
            srt_content = srt_file.read()

        # Split the content into words
    words = srt_content.split()

        # Create a list to store words without special characters
    clean_words = [word for word in words if word.isalpha()]

    unsimilar_with_meaning = {}
    for word in clean_words:
        if word.lower() in lc_words:
            pass
        elif len(word) == 1:
            pass  
        else:
                # Check if the verb is in base form (convert it to base form)
            base_word = convert_to_past_tense(word.lower())
            if base_word not in lc_words:
                meaning = get_word_meaning_from_longman(base_word)
                if meaning:
                    unsimilar_with_meaning[word.lower()] = meaning

    return unsimilar_with_meaning
# Create an empty set to store Longman Communication 3000 words
lc_words = set()

# Fetch Longman Communication 3000 words
lc_words = fetch_longman_words(lc_words)

# Get the file paths from user input
srt_file_l = "FILE.srt"

# Call the function and retrieve the results
unsimilar_words_with_meaning = find_unsimilar_words(srt_file_l, lc_words)

# Create a dictionary to store word meanings
unsimilar_words_with_meaning_dict = {}

# Fetch meanings for unsimilar words and store in the dictionary
for word in unsimilar_words_with_meaning:
    meaning = get_word_meaning_from_longman(word)
    if meaning:
        unsimilar_words_with_meaning_dict[word] = meaning

# Print the unsimilar words with their meanings
for word, meaning in unsimilar_words_with_meaning_dict.items():
    print(f"{word}\n {meaning}\n")

# Write the unsimilar words and their meanings to a CSV file
csv_file_path = 'unsimilar_words_with_meaning.csv'
with open(csv_file_path, 'w') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Word', 'Meaning'])  # Write header row
    for word, meaning in unsimilar_words_with_meaning_dict.items():
        csv_writer.writerow([word, meaning])