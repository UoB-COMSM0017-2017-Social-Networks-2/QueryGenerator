from itertools import permutations
import nltk
import re
from nltk.corpus import stopwords

# remove the sensitive char in topic
def word_filter(topic):
    word = list()
    punctuation = ['+','-','.', ',', '"', "'", '?', '!', ':', ';', '(', ')', '[', ']', '{', '}','@','#']
    stop_words = set(stopwords.words('english'))
    stop_words.update(['AND','and','OR','or'])
    for el in punctuation:
        topic = topic.replace(el,"")
    for w in topic.split():
        if not w.lower() in stop_words:
            word.append(w)
    topic = ' '.join(word)
    return topic

# view tweets and add new topic
def retopic_tweets(topic,tweets): # tweets_queried
    tmp_query = dict()
    tmp_topic = []
    key =0
    for i in range(len(tweets)-1,-1,-1):
        # filter tweets if topic keywords in tweet
        for j in topic.split():
            if re.search(j, tweets[i]):
                key = 1 
        #print tweet.similar(query)
        # count keywords in tweets according to the queries
        if key ==1:
            key =0
            for word in tweets[i].split():
                word = word_filter(word)
                add_dict(word,tmp_query)
        else:
            del tweets[i]
    print 'Dictionary: '+str(tmp_query)+'\n'
    # add keywords counts as queries
    for k,v in tmp_query.items():
        if v >= len(tweets) * 0.8:
            tmp_topic.append(k)
    new_topic = ' '.join(tmp_topic)
    return new_topic

# generate queries based on the topic keywords
def keyword_query(topic):
    #if len(topic.split())==1:
    #query = query_request(topic)
    if len(topic.split())!=1:
        for i in permutations(topic.split(),len(topic.split())): # x is not actually looping
            topic = ' '.join(i)
            # define the format of queries, i.e., search for keyword, username, hashtag
            query.append(topic)
            query.append('@'+topic)
            query.append('#'+topic)
            ## search for common abbreviation  
    return query

def add_dict(word, dict):
    if (word in dict):
        num = dict[word]
        num = num + 1
        dict[word] = num
    else:
        dict[word] = 1

def query_tweets(query,tweets):
    tweets_queried =list()
    key = 0
    for i in range(0,len(tweets)):
        for j in range(0,len(query)):
            pattern = "("+ ')(.*?)('.join(query[j].split())+")"
            if re.search(pattern, tweets[i]):
                key = 1
        if key == 1:
            tweets_queried.append(tweets[i])
            key = 0
    return tweets_queried

# test
topic = "A Trump he is and and or 4+- cats."
tweets = ["Donald Trump catches 4 cats in the frontdoor of his house.","I am a dog lover","cute #cat and me","Donald #Trump his cat","@Donald Trump cat","Donald Trump has little cat inside his room http://","Donald Trump raises these small cat in White house."]
print 'original topic: '+topic+'\n'
modified_topic = word_filter(topic)
print 'modified topic: '+modified_topic+'\n'
new_topic = retopic_tweets(modified_topic, tweets)
print 'new topic: '+new_topic+'\n'
query = list()
#query = query_request_format(modified_topic)
query = keyword_query(modified_topic)
#query = keyword_query(new_topic)
print 'query: '+ str(query)+'\n'
tweets_queried = query_tweets(query,tweets)
print 'tweets: '+str(tweets_queried)+'\n'
