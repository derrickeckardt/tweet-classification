#!/usr/bin/env python
#
# CS B551 - Elements of AI
# Indiana University, Fall 2018
# Assignment 2, Part 2 - Tweet classification
#
# Completed by Derrick Eckardt
# derrick@iu.edu

# import libraries
import sys
import pandas as pd
from collections import Counter
from operator import itemgetter
import string
from copy import deepcopy

training_file, testing_file, output_file = [sys.argv[1],sys.argv[2],sys.argv[3]]
# open import file
training_data, testing_data =[], []
training_locations = []
training_dict = {}

# function to clean up tokens as they go through
def filter_token(token):
    # changing everything to lower case as it comes in.
    # improved performance from 57.4% to 58.8%
    # as it likely allows Chicago to equal chicago and increase quantities there
    token = token.lower()

    # From looking at data, punctiation is adding meaning, which will ignore for now, as it changes some words.  'chicago' is different than 'chicago!'
    # learned how to do that from:
    # https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python
    # token = token.translate(None, string.punctuation)
    # doing it with that method got rid of hashtags and @ symbols, which are actually very
    # useful.  Performance dropped from 58.0 to 43.0 by filtering all punctuation
    token = token.replace("!","").replace("_","") #.replace("@","").replace("-","").replace("_","").replace("#hiring","") #.replace("(","").replace(")","")
    # Got up to 59.4 percent getting rid of exclamations points only    
    
    # filter out stopwords
    # stopwords taken from NLTK list of 128 stop words
    # https://pythonprogramming.net/stop-words-nltk-tutorial/
    stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']
    if token in set(stop_words):
        return None

    return token


with open(testing_file, 'r') as file:
    for line in file:
        testing_data.extend([[line.split()[0], filter(None,[filter_token(str(i)) for i in line.split()[1:]])]])
    # print testing_data[0:20]


with open(training_file, 'r') as file:
    for line in file:
        # Loads as list of lists of lists
        training_data.extend([[line.split()[0], filter(None,[filter_token(str(i)) for i in line.split()[1:]])]])
        training_locations.extend([line.split()[0]]) if line.split()[0] not in set(training_locations) else None

# Sort it so that it sorts them in alphabetical order by the city.
training_data= sorted(training_data, key=itemgetter(0))

# Add like cities until there is only one list for each list.  The zero element
# is the city name and the second element is all the tokens.
i=0
while len(training_data) > len(training_locations):
    if training_data[i][0] == training_data[i+1][0]:
        training_data[i][1].extend(training_data[i+1][1])
        training_data.remove(training_data[i+1])
    else:
        i += 1

# Now time to analysis, create easy lookup of each term, by creating summary
# lookup in dictionary.
for city, terms in training_data:
    training_dict[city] = Counter(terms)
    print city, " ",Counter(terms).most_common(5)
    training_dict[city]["total_token_count"] = float(len(terms))

def predict_tweet(training_dict, training_locations, testing_data):
    correct = 0
    for tweet_city, tweet_tokens in testing_data:
        # score each token
        city_score_results = [[city,0] for city in training_locations]
        for token in tweet_tokens:
            # Get the number of times that word appears in total.
            token_occurances = sum([training_dict[city][token] if training_dict[city][token] else 0 for city in training_locations])
            # score each city
            for i, city in enumerate(training_locations):
                # Tried it where it just kept the highest value only, but that only get me 28% accuracy
                # also tried filtering by low frequency words, and any number above 0 resulted in a decrease in performance
                # low frequency words appear to be strong indicators of a tweet's location
                city_score_results[i][1] += training_dict[city][token] / token_occurances if training_dict[city][token] and token_occurances > 10 else 0
        city_score_results = sorted(city_score_results,key=itemgetter(1),reverse=True)
        # print 
        # print tweet_city
        # check if predicted properly
        # print tweet_city," ", city_score_results[0][0]
        if tweet_city == city_score_results[0][0]:
            correct += 1
    print "You successfully classified ",correct," of ",len(testing_data)," tweets."
    print "That's equal to ",round(correct/float(len(testing_data))*100,2),"%"
        
predict_tweet(training_dict, training_locations, testing_data)

training_counts = deepcopy(training_data)

while len(training_counts) > 1:
    training_counts[0][1].extend(training_counts[1][1])
    training_counts.remove(training_counts[1])

training_counts_dict = Counter(training_counts[0][1])
#print training_counts_dict


# Find
        
# for i in range(5):
#     print len(training_data[i])," ",training_data[i]

# print training_dict['Boston,_MA']['tweet_count']
# print training_dict['Boston,_MA']['Boston']
# print len(training_data)
# print len(testing_data)




# Filter out stop words
# may be best to do it during file-read in

# Generate look-up tables:




#########################
# Unused or old code
# For use when loading code in 

        # Loads as dictiorary - presorted, takes a lot of time to do so.  it takes
        # almost two minutes to do so.  not erribly efficient
        # if line.split()[0] in training_dict.keys():
        #     training_dict[line.split()[0]]['tweet_count'] += 1
        # else:
        #     training_dict[line.split()[0]] = {}
        #     training_dict[line.split()[0]]['tweet_count'] = 1
        # for token in line.split()[1:]:
        #     # print token
        #     if token in training_dict[line.split()[0]].keys():
        #         training_dict[line.split()[0]][token] += 1
        #     else:
        #         training_dict[line.split()[0]][token] = 1

# print training_dict['Boston,_MA']['tweet_count']
# print training_dict['Boston,_MA']['Boston']


#Below not needed - just calculate it on the fly for each new tweet, instead of doing a lot of calculations that aren't needed.

# Get unique locations and unique words
# Generate look-up tables for each word.
# frequency_table = pd.DataFrame({'token':[]})
# print frequency_table
# Originally I was planning to build a frequency table by counting all the cities
# and all of the words
# now, i think I rather just generate those on the fly, perhaps
# locations = []
# tokens = []
# for tweet in training_data[0:10000]:
#     locations = list(set(locations) | set([tweet[0]]))
#     tokens = list(set(tokens) | set(tweet[1:]))
#     # if tweet[0] not in locations
#     #     locations.append(tweet[0])
#     # for token in tweet[1:]:
#     #     if token not in tokens:
#     #         tokens.append(token)
# print locations
# print len(locations)
# print len(tokens)
