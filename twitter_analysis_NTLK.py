import string
from collections import Counter
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
import GetOldTweets3 as got

#Getting Tweets
def get_tweets():

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('CoronaOutbreak') \
        .setSince("2020-01-01") \
        .setUntil("2020-04-01") \
        .setMaxTweets(10000)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    text_tweets = [[tweet.text] for tweet in tweets]
    return text_tweets

#Reading Tweets
text = ""
text_tweets = get_tweets()
length = len(text_tweets)

#List to string
for i in range(0, length):
    text = text_tweets[i][0] + " " + text

#cleaning text
lower_case = text.lower()
cleaned_text = lower_case.translate(str.maketrans('', '', string.punctuation))

#Tokennization
tokenized_words = word_tokenize(cleaned_text, "english")

#Remove stop words
final_words = []
for word in tokenized_words:
    if word not in stopwords.words('english'):
        final_words.append(word)
print(final_words)

emotion_list = []
with open('emotions.txt', 'r') as file:
    for line in file:
        clear_line = line.replace("\n", '').replace(",", '').replace("'", '').strip()
        word, emotion = clear_line.split(':')

        if word in final_words:
            emotion_list.append(emotion)

print(emotion_list)
w = Counter(emotion_list)
print(w)

#Using NLTK
def sentiment_analyse(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    if score['neg'] > score['pos']:
        print("Negative Sentiment")
    elif score['neg'] < score['pos']:
        print("Positive Sentiment")
    else:
        print("Neutral Sentiment")


sentiment_analyse(cleaned_text)

#Plotting Graph
fig, ax1 = plt.subplots()
ax1.bar(w.keys(), w.values())
fig.autofmt_xdate()
plt.savefig('graph.png')
plt.show()