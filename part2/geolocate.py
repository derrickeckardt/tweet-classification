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

training_file, testing_file, output_file = [sys.argv[1],sys.argv[2],sys.argv[3]]

# open import file
training_data, testing_data =[], []
with open(testing_file, 'r') as file:
    for line in file:
        testing_data.append([ str(i) for i in line.split() ])

with open(training_file, 'r') as file:
    for line in file:
        training_data.append([ str(i) for i in line.split() ])

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

# for i in range(5):
#     print len(training_data[i])," ",training_data[i]
# print len(training_data)
# print len(testing_data)

# Filter out stop words
# may be best to do it during file-read in

# Generate look-up tables:
