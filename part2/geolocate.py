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

training_file, testing_file, output_file = [sys.argv[1],sys.argv[2],sys.argv[3]]

# open import file
training_data, testing_data =[], []
training_locations, items = [],[]
training_dict = {}
with open(testing_file, 'r') as file:
    for line in file:
        testing_data.append([ str(i) for i in line.split() ])


with open(training_file, 'r') as file:
    for line in file:
        # Loads as list of lists of lists
        if any(line.split()[0] == city[0] for city in training_data):
            print training_data[training_data.index(line.split()[0])]
            test = [line.split()[0], training_data[training_data.index(line.split()[0])][1]+[ str(i) for i in line.split()[1:] ]]
        else:
            training_data.append([line.split()[0], [str(i) for i in line.split()[1:]]])

        print len(training_data)
        print training_data
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

for i in range(5):
    print len(training_data[i])," ",training_data[i]

# print training_dict['Boston,_MA']['tweet_count']
# print training_dict['Boston,_MA']['Boston']
# print len(training_data)
# print len(testing_data)


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


# Filter out stop words
# may be best to do it during file-read in

# Generate look-up tables:
