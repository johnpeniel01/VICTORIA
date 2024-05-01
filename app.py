from flask import Flask, request, jsonify, render_template
import pickle
import re
import numpy as np
from urllib.parse import urlparse
from flask_cors import CORS
import time
import webbrowser


#app = Flask(__name__)
app = Flask(__name__, static_url_path='/static') 
CORS(app)



# Open the browser and display index.html
webbrowser.open('http://127.0.0.1:5000/')
browser_open = True


with open('model.pkl', 'rb') as f:
    model = pickle.load(f)



# Function to perform feature extraction
def extract_url_features(url):
    
    #Extract url_length

    def urllength(url):
        
        prefixes = ['http://', 'https://']
        for prefix in prefixes:
            if url.startswith(prefix):
                url = url[len(prefix):]
        
        url = url.replace('www.', '')
        
        return len(url)
    url_length = urllength(url)


    #Extract presence of HTTPS
    def httpS(url):
        htps = urlparse(url).scheme
        match = str(htps)
        if match== 'https':
            return 1
        else:
            return 0
    n_https = httpS(url)


    #Extract presence of HTTP

    def http(url):
        htp = urlparse(url).scheme
        match = str(htp)
        if match== 'http':
            return 1
        else:
            return 0
        
    n_http= http(url)

    
    #Count number of digits in URL

    def num_count(url):
        num = 0
        for i in url:
            if i.isnumeric():
                num = num + 1
        return num

    n_num = num_count(url)


    #Count Alphabets in URL

    def count_alpha(url):
        alphas = 0
        for i in url:
            if i.isalpha():
                alphas = alphas + 1
        return alphas

    n_alpha = count_alpha(url)


    #Check if URL has IP address

    def have_ip(url):
        match = re.search(
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4
            '(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.'
            '([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\/)|'  # IPv4 with port
            '((0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\.(0x[0-9a-fA-F]{1,2})\\/)' # IPv4 in hexadecimal
            '(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
            '([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
            '((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)', url)  # Ipv6
        if match:
            return 1
        else:
            return 0
        
    has_ip = have_ip(url)
    

    #Count Special characters in URL

    def count_special_characters(url):
        special_char_pattern = re.compile(r'[^a-zA-Z0-9]')

        special_characters = re.findall(special_char_pattern, url)
        
        return len(special_characters)

    n_xtr = count_special_characters(url)


    #Count number of lowercase characters

    def count_lowercase(url):
    
        lowercase_count = sum(1 for char in url if char.islower())
        
        return lowercase_count

    n_lowcase = count_lowercase(url)


    #Count number of Uppercase characters

    def count_uppercase(url):
    
        uppercase_count = sum(1 for char in url if char.isupper())
        
        return uppercase_count

    n_upcase = count_uppercase(url)


    #Count the number of @ in url

    def count_at_symbols(url):
        
        at_count = url.count('@')
        
        return at_count

    num_at = count_at_symbols(url)


    #Count the number of & in url

    def count_and_symbols(url):
    
        and_count = url.count('&')
        
        return and_count

    n_and = count_and_symbols(url)


    #Count the number of semi-colon in url

    def count_semi(url):
    
        semi_count = url.count(';')
        
        return semi_count

    n_semi = count_semi(url)


    #Count the number of // in url

    def count_double_slashes(url):
        
        double_slash_count = url.count('//')
        
        return double_slash_count

    n_dbslash =count_double_slashes(url)



    #Count number of "." in URL


    def count_dots(url):
        
        dot_count = url.count('.')
        
        return dot_count

    n_dot_domain =count_dots(url)
    


    #Count number of '-' in domain

    def count_hyphen_in_domain(url):
    
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        hyphen_count = domain.count('-')
        
        return hyphen_count

    n_hyphen_domain = count_hyphen_in_domain(url)



    #Count number of "-" in URL


    def count_hyphen(url):
        
        hyphen_count = url.count('-')
        
        return hyphen_count

    n_hyphen = count_hyphen(url)

   
   #Count length of domain in url

    def domain_len(url):
    
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        
        # Calculate the length of the domain
        domain_length = len(domain)
        
        return domain_length

    domain_length = domain_len(url)


    #Calulate ratio of numbers in url

    def calculate_numbers_ratio(url):
        
        num_count = sum(1 for char in url if char.isdigit())
        
        total_chars = len(url)
            
        numbers_ratio = num_count / total_chars if total_chars > 0 else 0
        
        return numbers_ratio

    num_ratio = calculate_numbers_ratio(url)


    #Calculate ratio of alphabets in url

    def calculate_alphabets_ratio(url):
        alphabet_count = sum(1 for char in url if char.isalpha())
        
        total_chars = len(url)
        
        alphabets_ratio = alphabet_count / total_chars if total_chars > 0 else 0
        
        return alphabets_ratio

    alpha_ratio = calculate_alphabets_ratio(url)


    # Calculate ratio of lowercase letters in url

    def calculate_lowercase_ratio(url):
    
        lowercase_count = sum(1 for char in url if char.islower())
        
        total_chars = len(url)
        
        lowercase_ratio = lowercase_count / total_chars if total_chars > 0 else 0
        
        return lowercase_ratio

    lwcase_ratio =calculate_lowercase_ratio(url)


    # Calculate ratio of upperercase letters in url

    def calculate_uppercase_ratio(url):
    
        uppercase_count = sum(1 for char in url if char.isupper())
        
        total_chars = len(url)
        
        uppercase_ratio = uppercase_count / total_chars if total_chars > 0 else 0
        
        return uppercase_ratio

    upcase_ratio = calculate_uppercase_ratio(url)


    #Calculte special character ratio in url

    def calculate_special_characters_ratio(url):
        special_count = sum(1 for char in url if not char.isalnum())
        
        total_chars = len(url)
        
        special_ratio = special_count / total_chars if total_chars > 0 else 0
        
        return special_ratio

    sp_char_ratio = calculate_special_characters_ratio(url)


    #Count the number of English words in url

    def count_english_words(url):
        words = re.findall(r'\b[a-zA-Z]+\b', url)
        
        num_words = len(words)
        
        return num_words

    n_eng_words = count_english_words(url)


    #Count number of random words in url

    def count_random_words(url):
        random_word_pattern = re.compile(r'\b[^a-zA-Z0-9]+\b')
        
        random_words = re.findall(random_word_pattern, url)
        
        return len(random_words)

    n_rd_words = count_random_words(url)



    #Calculate average legth of English word in url

    def average_word_length(url):
        # Extract consecutive sequences of alphabetic characters as words
        words = re.findall(r'\b[a-zA-Z]+\b', url)
        
        # Calculate the average word length
        avg_word_length = sum(len(word) for word in words) / len(words) if len(words) > 0 else 0
        
        return avg_word_length

    avg_wd_len = average_word_length(url)


    #Calculate average length of random words in url

    def average_random_word_length(url):
        random_word_pattern = re.compile(r'\b[^a-zA-Z0-9]+\b')
        
        random_words = re.findall(random_word_pattern, url)
        
        avg_random_word_length = sum(len(word) for word in random_words) / len(random_words) if len(random_words) > 0 else 0
        
        return avg_random_word_length

    avg_rd_wd_len = average_random_word_length(url)


    #Shortening services 

    def has_shortening_service(url):
        pattern = re.compile(r'https?://(?:www\.)?(?:\w+\.)*(\w+)\.\w+')
        match = pattern.search(url)
        
        if match:
            domain = match.group(1)
            common_shortening_services = ['bit', 'goo', 'tinyurl', 'ow', 't', 'is',
                                        'cli', 'yfrog', 'migre', 'ff', 'url4', 'twit',
                                        'su', 'snipurl', 'short', 'BudURL', 'ping', 
                                        'post', 'Just', 'bkite', 'snipr', 'fic', 
                                        'loopt', 'doiop', 'short', 'kl', 'wp', 
                                        'rubyurl', 'om', 'to', 'bit', 't', 'lnkd', 
                                        'db', 'qr', 'adf', 'goo', 'bitly', 'cur', 
                                        'tinyurl', 'ow', 'bit', 'ity', 'q', 'is', 
                                        'po', 'bc', 'twitthis', 'u', 'j', 'buzurl', 
                                        'cutt', 'u', 'yourls', 'x', 'prettylinkpro', 
                                        'scrnch', 'filoops', 'vzturl', 'qr', '1url', 
                                        'tweez', 'v', 'tr', 'link', 'zip']
            
            if domain.lower() in common_shortening_services:
                return 1
        return 0

    shortened = has_shortening_service(url)


    #Count number of . in url

    def count_dot(url):
        count_dot = url.count('.')
        return count_dot
    n_dot = count_dot(url)


    #Count www in url

    def count_www(url):
        url.count('www')
        return url.count('www')
    n_www = count_www(url)


    #Count number of DIR in URL. the '/' comes before each directory

    def no_of_dir(url):
        urldir = urlparse(url).path
        return urldir.count('/')
    n_slash = no_of_dir(url)


    #Count the number of % in URL

    def count_per(url):
        return url.count('%')
    n_per = count_per(url)


    #Count ? marks in URL
    def count_ques(url):
        return url.count('?')
    n_quest = count_ques(url)


    #Count = signs in URL

    def count_equal(url):
        return url.count('=')
    n_equal = count_equal(url)


    #Count consonants in URL
    def count_consonants(url):
        # Convert the URL to lowercase for case-insensitive counting
        url_lower = url.lower()
        
        # Define a set of vowels
        vowels = set("aeiou")
        
        # Count the number of consonants
        num_consonants = sum(1 for char in url_lower if char.isalpha() and char not in vowels)
        
        return num_consonants

    n_consonant = count_consonants(url)


    #Count Vowels in URL
    def count_vowels(url):
        # Convert the URL to lowercase for case-insensitive counting
        url_lower = url.lower()
        
        # Define a set of vowels
        vowels = set("aeiou")
        
        # Count the number of vowels
        num_vowels = sum(1 for char in url_lower if char.isalpha() and char in vowels)
        
        return num_vowels

    n_vowel = count_vowels(url)


    # Return the extracted features as a list
    features =[url_length, n_https, n_http, n_num, n_alpha, has_ip, n_xtr, n_lowcase, n_upcase, num_at, n_and, n_semi,n_dbslash, n_dot_domain,n_hyphen_domain, n_hyphen,domain_length, num_ratio, alpha_ratio, lwcase_ratio, upcase_ratio,sp_char_ratio, n_eng_words, n_rd_words, avg_wd_len, avg_rd_wd_len, shortened, n_dot , n_www, n_slash, n_per, n_quest, n_equal, n_consonant, n_vowel]


    
    return features

    


@app.route('/predict', methods=['POST'])
def predict():
    text = request.form.get('text')
    if text == (""):
        return jsonify({'error': 'Input text not provided.'})
    
    else:
        url_features = extract_url_features(text)

    # Predict the URL
        prediction = model.predict([url_features])[0]
        return jsonify({'prediction': int(prediction)})
        

@app.route('/')
def home():
    return render_template('index.html')

  

if __name__ == '__main__':
    app.run(debug=True)

