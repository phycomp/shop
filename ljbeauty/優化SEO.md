使用python 優化SEO 關鍵字
Optimizing SEO keywords using Python can be accomplished by analyzing the content and suggesting relevant keyword improvements. You can use libraries like nltk, scikit-learn, or APIs like Google's Natural Language API to extract keywords and optimize them for SEO.
Steps for SEO Keyword Optimization:
    1. Extract Content: Get the text content from the webpage or article.
    2. Tokenize and Preprocess: Clean the text by removing stop words, punctuation, and non-essential elements.
    3. Keyword Frequency Analysis: Analyze the frequency of important words or phrases.
    4. Keyword Suggestions: Use external APIs to suggest related keywords based on trends or competitors.
    5. Output Optimized Keywords: Present a list of optimized and potential keywords for SEO purposes.
Python Code for SEO Keyword Optimization:
Install Required Libraries:
pip install nltk sklearn rake-nltk requests beautifulsoup4
Example Code:
import re
import requests
from bs4 import BeautifulSoup
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from rake_nltk import Rake

# Download stopwords if not already present
nltk.download('stopwords')

# Step 1: Scrape the webpage or get the text content
def get_webpage_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    # Extract the main content text from the webpage
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    return text

# Step 2: Clean and preprocess the text content
def preprocess_text(text):
    # Remove punctuation, numbers, and special characters
    text = re.sub(r'\d+', '', text)
    text = re.sub(r'\W+', ' ', text.lower())
    
    # Tokenize and remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = nltk.word_tokenize(text)
    filtered_words = [word for word in tokens if word not in stop_words]
    return ' '.join(filtered_words)

# Step 3: Extract keywords using TF-IDF (Term Frequency-Inverse Document Frequency)
def extract_keywords_tfidf(text):
    vectorizer = TfidfVectorizer(max_df=0.85, stop_words=stopwords.words('english'))
    X = vectorizer.fit_transform([text])
    tfidf_scores = dict(zip(vectorizer.get_feature_names_out(), X.toarray()[0]))
    
    # Sort by highest scores
    sorted_keywords = sorted(tfidf_scores.items(), key=lambda item: item[1], reverse=True)
    return [keyword for keyword, score in sorted_keywords[:10]]  # Top 10 keywords

# Step 4: Extract keywords using RAKE (Rapid Automatic Keyword Extraction)
def extract_keywords_rake(text):
    rake = Rake(stopwords.words('english'))
    rake.extract_keywords_from_text(text)
    return rake.get_ranked_phrases()[:10]  # Top 10 keywords

# Step 5: Suggest related keywords (basic implementation)
def suggest_related_keywords(seed_keywords):
    related_keywords = []
    for keyword in seed_keywords:
        response = requests.get(f"https://api.datamuse.com/words?ml={keyword}")
        words = response.json()
        related_keywords.extend([word['word'] for word in words[:3]])  # Get top 3 related words
    return related_keywords

# Step 6: Run the SEO keyword optimization
def seo_keyword_optimization(url):
    print(f"Optimizing keywords for: {url}\n")
    
    # Get webpage content
    text = get_webpage_content(url)
    cleaned_text = preprocess_text(text)
    
    # Extract and print keywords
    print("Top keywords using TF-IDF:")
    tfidf_keywords = extract_keywords_tfidf(cleaned_text)
    print(tfidf_keywords)
    
    print("\nTop keywords using RAKE:")
    rake_keywords = extract_keywords_rake(cleaned_text)
    print(rake_keywords)
    
    # Suggest related keywords
    related_keywords = suggest_related_keywords(tfidf_keywords)
    print("\nSuggested related keywords:")
    print(related_keywords)

# Example usage
url = "https://example.com/article"  # Replace with actual article URL
seo_keyword_optimization(url)
Explanation of the Code:
    1. Webpage Scraping:
        ◦ The get_webpage_content function scrapes a webpage and extracts the main text content (e.g., from <p> tags).
    2. Preprocessing:
        ◦ The preprocess_text function cleans the text by removing numbers, special characters, and stop words.
    3. Keyword Extraction:
        ◦ The extract_keywords_tfidf function uses the TF-IDF (Term Frequency-Inverse Document Frequency) technique to rank important keywords.
        ◦ The extract_keywords_rake function uses the RAKE (Rapid Automatic Keyword Extraction) method to identify key phrases from the text.
    4. Related Keyword Suggestions:
        ◦ The suggest_related_keywords function fetches related keywords from the Datamuse API, a service for finding words related to a specific term.
    5. Output:
        ◦ The code prints the top keywords extracted by both TF-IDF and RAKE methods, along with suggestions for related keywords.
Example Output:
Optimizing keywords for: https://example.com/article

Top keywords using TF-IDF:
['keyword1', 'keyword2', 'keyword3', ...]

Top keywords using RAKE:
['phrase one', 'phrase two', 'phrase three', ...]

Suggested related keywords:
['related1', 'related2', 'related3', ...]
Use Cases:
    • SEO Strategy: Use this script to analyze content from your website and competitors to identify the best keywords.
    • Keyword Suggestions: Expand your SEO reach by getting related keyword suggestions from external APIs.
    • Content Improvement: Optimize existing content by adjusting the density and usage of high-value keywords.
You can further enhance this script by adding tools like Google Trends API or a more sophisticated NLP library for deeper keyword insights
