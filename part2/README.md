## Part 2: Tweet Classification 

Completed by Derrick Eckardt on October 26, 2018.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 2 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a2/blob/master/a2.pdf).  This readme file provides the required elements and my discussion of the process and the findings.

## Getting Started

As directed in the assignment, to run this program type the following at the command line:

    ./geolocate.py [training_tweets_file] [test_tweets_file] [output_file]
    
To run the data in the folder, you would specifically run:

    ./gelocate.py tweets.train.clean.txt tweets.test1.clean.txt output.txt                    
It takes approximately four seconds to run on the Silo server.

For a more details on the required set-up, please see the [Assignment 2 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a2/blob/master/a2.pdf)

## Summary of Problem

In general, think of this as a search problem.

**Initial State:** TBD

**Goal State:** TBD

**State Space:** TBD

**Successor Function:** TBD

**Heurestic Function:** TBD

**Cost Function:** TBD

## Discussion of Approach

TBD

## Reading in the data

It quickly became evident that how the data was read into the program significantly impacted the run time on the program.  I considered two main ways to read the information in: Lists and Dictionaries.

    '''python
    with open(training_file, 'r') as file:
        for line in file:
            Loads as dictiorary - presorted, takes a lot of time to do so.  it takes
            almost two minutes to do so.  not terribly efficient
            if line.split()[0] in training_dict.keys():
                training_dict[line.split()[0]]['tweet_count'] += 1
            else:
                training_dict[line.split()[0]] = {}
                training_dict[line.split()[0]]['tweet_count'] = 1
            for token in line.split()[1:]:
                # print token
                if token in training_dict[line.split()[0]].keys():
                    training_dict[line.split()[0]][token] += 1
                else:
                    training_dict[line.split()[0]][token] = 1
    '''

Dictionaries offered the benefit that as information was being added, it could also be used to calculate the absolute counts, which would be used to calculate the probabilities.

I also briefly looked at a pandas dataframe, and it seemed to be additional work for no additional performance payoff.

## Filtering the Input - To (over)Fit or Not to (over)Fit

Probably the most important thing in this data set is to make sure to make sure the data that is the most useful.  I set-up a function in my code called filter_token() which performs several different types of filter.  I did it this way so it would clean to filter terms, and that I could easily add/test a new filter.

First, I made everything lowercase.  This allows 'Chicago' to be the same as 'chicago'.  This was achieved simply with:

    token = token.lower()

Next, my I really struggled with finding a happy step, because the next issue is a common problem.  Data scientists can get themselves into trouble by creating a model that works particularly well for a given dataset, and does not necessarily work well for other similar datasets.  This is called overfitting.  This became an issue for me in determining what noise to filter out, and what noise to leave in.  Ultimately, I went with the major ones that I could see in the common terms, which were:

    _!.-()@#'

Something I should note here, is that within Twitter, # and @ are important symbols with meaning. They are not stray punctiation. Contrary to what I expected, when I included them in the punctiation to filter out, my prediction accuracy actually improved from 65.6% to 66.2%  When I removed the words "jobs" and "hiring" since they appeared in almost every dataset, my accuracy then went to 66.8%.  Are these two 0.6% improvements true for other datasets?  I do not know.  Or, does that just happen to work for my dataset.   Those are small margins. Ultimately, more experimentation could solve that.  See my discussion under "Opportunities for Improvement" below on how this might be solved.

Lastly, once my code was filtered to the tokens I wanted, I got rid of all of the "stop words."  These are high frequency words in the English language that mean almost nothing in terms of substantive meaning (the, he, she, etc).  It is common to filter these out with natural language processing.  I got my 128 stop words from the Natural Language Toolkit (NLTK), which is a popular library for natural language processing.  You can find by clicking [NLTK stop words](ttps://pythonprogramming.net/stop-words-nltk-tutorial/).  When I removed the stop words capability, my accuracy dropped to 62.6% from the 66.8%.  While before I was concerned about overfitting, I'm fairly certain filtering stop words almost always makes sense. 

A general comment to make here is also that there were many different ways to perform the filtering.  Some are more "pythonic" than ours.  With tens of thousands of tokens, I went for the ones that seemed the fast.  I currently use join() to perform.  I also looked into [using the string library to filter punctuation](https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python).  I also looked at daisychaining .replace() functions, but that took too long.

## Opportunities for Improvement

** Run Experiments to Determine Overfitting** - To settle some of the questions I had about overfitting, it would be helpful in the future to actually have additional datasets.  Another way that is often achieved in Machine Learning is to do multiple "folds" of the training data.  For example, I could do ten folds, each has 10% (3200 datapoints) from the training datasats, where 3200 datapoints are made the testing dataset, and the rest remains in the training set.  I would do this with one model that filters out the # and @ and one that does not.  I would then average the results of each set of those ten runs, and compare the results.  This would give me a much better feel for what punctuation actually mattered.