#!/usr/bin/env python
#
# CS B551 - Elements of AI
# Indiana University, Fall 2018
# Assignment 2, Part 2 - Tweet classification
#
# Completed by Derrick Eckardt
# derrick@iu.edu
#
###############################################################################
###############################################################################
#
# A full discussion and details can be found in the Readme file for Part 2, 
# which is located at:
# https://github.iu.edu/cs-b551-fa2018/derrick-a2/tree/master/part2
#
###############################################################################
###############################################################################

# import libraries
import sys
from collections import Counter
from operator import itemgetter
from copy import deepcopy

# function to clean up tokens as they go through
def filter_token(token):
    # changing everything to lower case as it comes in.
    token = token.lower()

    # filter out punctuation.
    token = "".join([char for char in token if char not in "_!.,?\"*:-()&#'" ]).replace("hiring","").replace("job","")

    # filter out stopwords, stopwords taken from NLTK list of 128 stop words
    # https://pythonprogramming.net/stop-words-nltk-tutorial/
    stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
    if token in set(stop_words):
        return None

    return token

# import command line inputs
training_file, testing_file, output_file = [sys.argv[1],sys.argv[2],sys.argv[3]]

# open imported file
training_data, testing_data =[], []
training_locations, training_dict = [], {}

with open(testing_file, 'r') as file:
    for line in file:
        testing_data.extend([[line.split()[0], filter(None,[filter_token(str(i)) for i in line.split()[1:]]), line]])


with open(training_file, 'r') as file:
    for line in file:
        # Loads as list of lists of lists
        training_data.extend([[line.split()[0], filter(None,[filter_token(str(i)) for i in line.split()[1:]])]])
        training_locations.extend([line.split()[0]]) if line.split()[0] not in set(training_locations) else None

# Sort it so that it sorts them in alphabetical order by the city.
training_data= sorted(training_data, key=itemgetter(0))

# Add like cities until there is only one list for each list.  The zero element
# is the city name and the 'first' element is all the tokens.
# Also using this loop to find city with most tweets, and that will be used as the default if the score is
# 0 (ie, the test tweet uses words not in the training data).  otherwise, it would use
# either the first city in training locatons or the alphabetical list.
most_tweets = ["",0] # city, total
city_tweets_counter = 0
i=0
while len(training_data) > len(training_locations):
    if training_data[i][0] == training_data[i+1][0]:
        training_data[i][1].extend(training_data[i+1][1])
        training_data.remove(training_data[i+1])
        city_tweets_counter += 1
    else:
        i += 1
        if city_tweets_counter > most_tweets[1]:
            most_tweets = [training_data[i][0], city_tweets_counter+1]
        city_tweets_counter = 0

# Now time to analysis, create easy lookup of each term, by creating summary
# lookup in dictionary.
for city, terms in training_data:
    training_dict[city] = Counter(terms)
    # print city, " ",Counter(terms).most_common(5)
    training_dict[city]["total_token_count"] = float(len(terms))

# Deepcopying training data so I can use it for total counts easily.
training_counts = deepcopy(training_data)

while len(training_counts) > 1:
    training_counts[0][1].extend(training_counts[1][1])
    training_counts.remove(training_counts[1])

training_counts_dict = Counter(training_counts[0][1])

# Let's predict some tweets and output to file
def predict_tweet(training_dict, training_locations, testing_data, output_file):
    correct = 0
    results_file = open(output_file,"w+")
    for tweet_city, tweet_tokens, original_line in testing_data:
        # score each token
        city_score_results = [[city,0] for city in training_locations]
        # predicted_city = most_tweets[0]
        for token in tweet_tokens:
            # Get the number of times that word appears in total.
            # originally i had a check for if training_dict[city][token] else 0 
            # in reading the python documentation, discovered that Counter 
            # dictionaries return 0 and not errors when something isn't there
            # which is a nice little feature of the program.  since those were
            # extra operations, I removed them.  this speed up the program negliably though
            # if training_dict[city][token] else 0 removed from below
            # score each city
            for i, city in enumerate(training_locations):
                city_score_results[i][1] += training_dict[city][token] / float(training_counts_dict[token]) if training_counts_dict[token] > 0 else 0
        city_score_results = sorted(city_score_results,key=itemgetter(1),reverse=True)
        predicted_city =  city_score_results[0][0]  #if city_score_results[0][1] > float(0) else predicted_city
        if tweet_city == predicted_city:
            correct += 1
        results_file.write(predicted_city+" "+original_line)
    results_file.close
    print "You successfully classified ",correct," of ",len(testing_data)," tweets."
    print "That's equal to ",round(correct/float(len(testing_data))*100,2),"%"
    print "Predicted results and original tweets outputted to file: "+output_file+"\n"
    
    
predict_tweet(training_dict, training_locations, testing_data, output_file)

# manually found that the first 4000 terms have a low value of 7 and 3000 terms
# have a low value of 10.  To be sure, I pulled 4000 terms and can filter
# out those with fewer than 10.
topwords = []
threshold = 0.80
print "The top 5 words and their frequency in that city compared to the overall usage are as follows:"
for city in sorted(training_locations,key=itemgetter(0)):
    for token, count in training_counts_dict.most_common(4000):
        if count >= 20:
                if training_dict[city][token] / float(count) > threshold:
                    topwords.extend([[token,training_dict[city][token]/float(count)]])
    print city +":  "+"".join([word +" "+ str(round(score, 2)) + "   " for word, score in sorted(topwords,key=itemgetter(1), reverse=True)[0:5]])
    topwords =[]