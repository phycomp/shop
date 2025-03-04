使用 Google Trends API 加強SEO 優化關鍵字

You can use the Google Trends API to enhance your SEO strategy by identifying trending keywords, analyzing search interest over time, and discovering regional keyword popularity. The pytrends library allows easy access to Google Trends data, which can help you optimize keywords effectively.

Steps for Using Google Trends to Optimize SEO Keywords:
Install the pytrends library.
Extract trending data for the keywords you're using or considering.
Analyze the popularity and performance of these keywords.
Optimize your SEO strategy by focusing on trending keywords and regions where they are popular.
Installation:
First, install the pytrends library:

pip install pytrends
Python Code for Using Google Trends API:
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Initialize the pytrends object
pytrends = TrendReq(hl='en-US', tz=360)

# Step 2: Define the list of keywords for SEO
keywords = ['SEO 顧問', '數位行銷', '網路行銷', '品牌行銷顧問', '關鍵字廣告']

# Step 3: Get Google Trends data for the keywords
pytrends.build_payload(keywords, cat=0, timeframe='today 12-m', geo='TW', gprop='')

# Step 4: Retrieve the interest over time data
interest_over_time_df = pytrends.interest_over_time()

# Step 5: Plot the interest over time
plt.figure(figsize=(10,6))
for keyword in keywords:
    plt.plot(interest_over_time_df.index, interest_over_time_df[keyword], label=keyword)
    
plt.title('Interest Over Time for SEO Keywords')
plt.xlabel('Date')
plt.ylabel('Interest')
plt.legend()
plt.show()

# Step 6: Retrieve related queries for each keyword
related_queries_dict = pytrends.related_queries()

# Step 7: Display related queries and their values
for keyword in keywords:
    print(f"Related queries for {keyword}:")
    print(related_queries_dict[keyword]['top'])
    print("\n")
Explanation of the Code:
TrendReq Initialization: pytrends connects to the Google Trends API. You can specify the language (hl='en-US') and timezone (tz=360).
Keyword Definition: You define a list of keywords (in this case, the ones relevant to 洸寅顧問公司).
Google Trends Payload: This collects data for the keywords, focusing on Taiwan (geo='TW') over the past 12 months (timeframe='today 12-m').
Interest Over Time: The script fetches search interest data over time and plots it using matplotlib to visualize keyword trends.
Related Queries: This section fetches related queries for each keyword, showing you other potential keywords you can target for SEO optimization.
Enhancing SEO with Google Trends Data:
Identify Seasonal Trends:

By looking at the interest over time, you can identify seasonal spikes in keyword searches. For example, some keywords might perform better during certain months or events.
Focus your SEO campaigns around these high-interest periods.
Discover Related Keywords:

The related queries data helps you discover new, high-performing keywords you might not have considered. These related terms often have lower competition but similar search intent, making them valuable for SEO.
You can use these related keywords to expand your content strategy and drive more organic traffic.
Optimize Regionally:

Google Trends provides regional data, showing which areas are most interested in specific keywords. You can tailor your SEO strategy to target regions where your services are in higher demand.
For example, if "SEO 顧問" is trending in certain cities or regions in Taiwan, you can create region-specific content or run localized ad campaigns.
Measure Keyword Performance:

By tracking keyword interest over time, you can measure the effectiveness of your SEO efforts. If certain keywords are declining in popularity, you may want to shift your focus to more trending topics.
Example Output:
Interest Over Time Plot: Shows the fluctuations in search interest for each keyword over the last 12 months.
Related Queries: Lists other popular keywords related to your primary keywords, which you can incorporate into your SEO strategy.
plaintext
複製程式碼
Related queries for SEO 顧問:
               query  value
0      SEO services     100
1         SEO公司         98
2   digital marketing    85
...

Related queries for 數位行銷:
               query  value
0       digital marketing    100
1        online marketing     95
...
Conclusion:
By leveraging Google Trends data, 洸寅顧問公司 can optimize its SEO strategy by:

Focusing on trending keywords that are gaining interest.
Discovering related queries to target for additional traffic.
Tailoring content to specific regions where the interest is highest.
Adjusting SEO efforts based on seasonal trends to capture maximum traffic when interest is at its peak.
This data-driven approach ensures you're focusing on high-impact keywords, improving both traffic and conversions.
******************************************************************
打破SEO的8個迷思 掌握搜尋引擎上篇 作者 陳辛妤
為什麼搜尋引擎優化很重要？
◎ SEO迷思1 盡可能廣泛的關鍵字
◎ SEO迷思2 內容精簡
◎ SEO迷思3 試圖一次優化每個頁面
◎ SEO迷思4 在內容中填充關鍵字
優化最佳實踐技巧 Google每天處理超過85 億次搜尋 等同於每秒將近 100 萬次搜尋 它擁有全球搜尋市場90%以上的份額 也就是說 要在這海量的資訊中 想讓人們看到你的網站 你需要進行搜尋引擎優化 SEO 以便為合適的讀者展示你的內容 然而 搜尋引擎優化的工作 可以說既是一門科學也是一門藝術 許多 SEO 專家擁有分析 技術和內容策略等技能的獨特組合 由於搜尋引擎規則經常會改變 即使是技術嫻熟的專業人士 有時也不自知地犯了 SEO 迷思 導致影響你的網站內容排名
SEO 迷思 1 盡可能廣泛的關鍵字 總想著大小通吃 一網打盡 試圖抓住高流量只會讓你感到沮喪 你的關鍵字越廣泛 競爭越激烈 你的網頁就越難獲得良好的排名 例如 當有人搜尋美食時 你可能不會出現在搜尋結果的第一頁上 但是縮小你的關注點並變得具體 比如汐止的辛辣韓國料理外賣 可能會提高你的排名
SEO 最佳實踐 具體說明你的產品或服務 不要害怕僅專注於搜尋量較低的搜尋詞 如果你在汐止遠東科技園區附近 設立了優質的復健診所 請不要以復健診所為目標進行排名 讓你頁面上的內容聚焦汐止遠東科技園區附近優質的復健診所而製作 你將獲得該搜尋結果的寶座
SEO 迷思 2 內容精簡 內容製作通常需要投入大量時間來長期經營 許多品牌在資源有限的情況下 通常選擇為廣告活動製作精簡的一頁式網站或一頁式銷售頁又稱登陸頁 並同時應用在自然搜尋上 這是非常愚蠢的原因在於 適用於付費廣告的登陸頁主要由購買按鈕和少量內容所組合而成 對於自然搜尋訪問者來說資訊明顯不足夠 搜尋訪問者通常會期望能先研究你的品牌或產品 他們不一定準備要購買 如果訪問者發現缺乏有用和優質的內容 或者內容被一系列點擊和表單所限制 他們就會離開 SEO 最佳實踐 製作專為你的自然搜尋訪問者構建內容豐富的網站 因為 你更清楚的了解 通過自然搜尋點擊你的網站的訪問者 與點擊搜尋廣告的人相比 他們通常處於客戶旅程銷售漏斗中的不同階段
SEO 迷思 3 試圖一次優化每個頁面
Google 不會將你網站上的每個頁面都編入索引 在搜尋結果的第一頁上獲得多個頁面的可能性很低 因此 你必須確定你網站上的哪個頁面是最重要的頁面 來設定重要關鍵字 例如 如果你想推廣筋膜按摩 你可能希望你的首頁在筋膜按摩方面排名第一 因為人們最有可能在進入首頁後進而瀏覽網站的其他頁面 或者 你可能希望你的商城頁面獲得排名 以便來自四面八方的顧客可以向你訂購復健輔具
SEO 最佳實踐 在最重要頁面上 例如主頁或商城 持續提供優質的內容 雖然像復健食譜這樣的文章不會經常更新 但它們應該被鏈接到首頁或商城上 讓網站的訪問者能隨時獲得有用的優質內容
SEO 迷思 4 在內容中填充關鍵字 關鍵字堆積keyword stuffing 是指內容創建者試圖在網頁中非常密集地放置關鍵字 這樣做是期望能操縱網站在 Google 搜尋結果中的排名 這種技術反而會導致糟糕的網站使用者體驗
下面是一個密集放置關鍵字的例子 我們有專業的筋膜按摩服務 我們的筋膜按摩專家有全方位的認證及多年的經驗 如果你正在找尋優質的筋膜按摩服務 請通過填寫表單聯繫我們的筋膜按摩專家
SEO 最佳實踐 建立內容時不僅僅是為了給搜尋引擎的 更要考慮實際讀者的感受 在你的內容中包含與關鍵字語義相關的同義詞 使用自然語言來描述產品或服務 避免過度重複 這樣關鍵字同樣會被搜尋引擎給拾取的
******************************************************
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
