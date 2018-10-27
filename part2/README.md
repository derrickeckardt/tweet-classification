## Part 2: Tweet Classification 

Completed by Derrick Eckardt on October 26, 2018.  Please direct any questions to [derrick@iu.edu](mailto:derrick@iu.edu)

The assignment prompt can be found at [Assignment 2 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a2/blob/master/a2.pdf).  This readme file provides the required elements and my discussion of the process and the findings.

## Getting Started

As directed in the assignment, to run this program type the following at the command line:

    ./geolocate.py [training_tweets_file] [test_tweets_file] [output_file]
    
To run the data in the folder, you would specifically run:

    ./geolocate.py tweets.train.clean.txt tweets.test1.clean.txt output.txt                    
It takes approximately four seconds to run on the Silo server.

For a more details on the required set-up, please see the [Assignment 2 Prompt](https://github.iu.edu/cs-b551-fa2018/derrick-a2/blob/master/a2.pdf)

## Summary of Problem

This is different than previous problems where we move from one state to another.  We are implement a naive Bayes model of identifying tweets by geolocation.  What is nice about this is with the training data, we are able to create lookup values for how often a particular word (or token) appears for a given location.  We call that P (L =l | w).  Once we read our data in, we know it for all the data.  Then, with test data, we can then see how well our model holds up.

## Discussion of Approach

There were many factors that went into the making of this predictor.  While I ended up with a predicted accuracy of 67.6% for the test data and 91.95% for the training data, there were many decisions that could change those numbers a little or a lot for different, similar datasets.

## Reading in the data

It quickly became evident that how the data was read into the program significantly impacted the run time on the program.  I considered two main ways to read the information in: Lists and Dictionaries.  (I also briefly looked at a pandas dataframe, and it quickly showed to not provide any additional benefit for this data handling.)

Dictionaries offered the benefit that as information was being added, it could also be used to calculate the absolute counts, which would be used to calculate the probabilities.  Below is the code that reads the information right into a dictionary, and then I would then easily be able to get word counts for each token.

```python
with open(training_file, 'r') as file:
    for line in file:
        # Loads as dictiorary - presorted, takes a lot of time to do so.  it takes
        # almost two minutes to do so.  not terribly efficient
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
```

So, had this worked quickly, it would have been nice since it basically gives me all of my counts right away. As noted in the comments within the above code lock, it took two minutes to just perform that part.  On the class discussion, we focused on lists.  It was pointed out by Prof. Crandall that using .extend() is significantly more efficent than .append() for lists.  In doing this, this part of the program took about two seconds to run. 

I end up with a list that has all of the tweets as their own item (training\_data).  I also get a list of every city in the dataset (training\_locations).  While I could have hardcoded manually since I knew the twelve cities, I thought it best to work with any similar dataset that could have more or fewer cities.  Then, I sorted the training\_data by tweet city, found the most popular tweet city, and then combined like cities into just 12 lists, one for each city.

Once I had all of my tweets into those twelve lists within training\_data, I used Counter from collections to create a dictionary that did the counts.  Basically, I got the benefit of the dictionary, while compiling the information through lists.  The other nice thing about Counter i discovered in the [Counter documentation](https://docs.python.org/2/library/collections.html) is that if you ask for a term in the Counter dictionary that is not there, it returns 0 instead of a KeyError.  This is tremendously helpful in the event that test data has a token that is not found in the training data, which often happens.

By the way, I found the most popular city so that it would be set as the default city in the event that a tweet has a score of 0 (meaning, it has words never seen in the training\_data.)  Later on in my code, you will see that I have actually commented that functionality out.  The reason?  It actually slightly decreased performance.  Since, the tweets are fairly well distributed, it didn't quite matter what the default was.  For different datasets, it might matter, so that is why I left it in so it could be easily turned on.  This does lead nicely into my next point--overfitting.

## Filtering the Input - To (over)Fit or Not to (over)Fit

Probably the most important thing in this data set is to make sure to make sure the data that is the most useful.  I set-up a function in my code called filter_token() which performs several different types of filter.  I did it this way so it would clean to filter terms, and that I could easily add/test a new filter.

First, I made everything lowercase.  This allows 'Chicago' to be the same as 'chicago'.  This was achieved simply with:

    token = token.lower()

Next, my I really struggled with finding a happy step, because the next issue is a common problem.  Data scientists can get themselves into trouble by creating a model that works particularly well for a given dataset, and does not necessarily work well for other similar datasets.  This is called overfitting.  This became an issue for me in determining what noise to filter out, and what noise to leave in.  Ultimately, I went with the major ones that I could see in the common terms, which were:

    _!.,"*:?-()&#'

Something I should note here, is that within Twitter, # and @ are important symbols with meaning. They are not stray punctiation. Contrary to what I expected, when I included them in the punctiation to filter out, my prediction accuracy actually improved from 65.8% to 66.6% when i removed the #.  When I removed @ it fell 0.2%  So, I kept that in for now. When I removed the words "jobs" and "hiring" since they appeared in almost every dataset, my accuracy then went to 67.6%.  Are these less than 1% improvements true for other datasets?  I do not know.  Or, does that just happen to work for my dataset?   Those are small margins.  Should I have left in the behavior to default to the most popular city since that might be a better design decision, but not good in practice? Ultimately, more experimentation could solve that.  See my discussion under "Opportunities for Improvement" below on how this might be solved.

Lastly, once my code was filtered to the tokens I wanted, I got rid of all of the "stop words."  These are high frequency words in the English language that mean almost nothing in terms of substantive meaning (the, he, she, etc).  It is common to filter these out with natural language processing.  I got my 128 stop words from the Natural Language Toolkit (NLTK), which is a popular library for natural language processing.  You can find by clicking [NLTK stop words](ttps://pythonprogramming.net/stop-words-nltk-tutorial/).  When I removed the stop words capability, my accuracy dropped to 62.6% from the 67.6%.  While before I was concerned about overfitting, I'm fairly certain filtering stop words almost always makes sense. 

A general comment to make here is also that there were many different ways to perform the filtering.  Some are more "pythonic" than ours.  With tens of thousands of tokens, I went for the ones that seemed the fast.  I currently use join() to perform.  I also looked into [using the string library to filter punctuation](https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string-in-python).  I also looked at daisychaining .replace() functions, but that took too long.

## How Important are the Words?

One of the things that was most interesting for me, was to see how much individual words mattered.  As it turns out, the rarer words were, the more important they were.  I tested this out by requiring that a word appear at least two times in order for it to contribute to the scoring of a tweet.  The result was my accuracy went down to 64.8%.  When I required three occurances, it dropped further to 63.4%.  When I required ten occurances, it dropped to 61.6%.  At twenty occurances, accuracy fell to 60.8%.  That is strong evidence that the rarely used words are actually good predictors.

I also experimented briefly instead of scoring each individual word and then summing them together, I would only use the score for the most important token in the tweet.  The accuracy for that was around 28%, and did not merit further exploration at that time.

## Most Important Words

The assignment also says that we should rank the top 5 words for each city.  Since I just saw that low frequency words are relevant, we can't simply use their P(L|W) values, since many of those would be 1.

The way I decided to define 'top' words is by only including words that appear at least 20 times, and had to appear on one city's list for at least 80% of those times.  This resulted in the following amount of 'top' words for each city:

    Atlanta,_GA   11
    Boston,_MA   12
    Chicago,_IL   9
    Houston,_TX   17
    Los_Angeles,_CA   38
    Manhattan,_NY   33
    Orlando,_FL   24
    Philadelphia,_PA   6
    San_Francisco,_CA   6
    San_Diego,_CA   7
    Toronto,_Ontario   18
    Washington,_DC   6

This resulted in a total of 187 'top' words.  While the 10 was somewhat arbitrarily selected, the 80% is just to got the dataset down.  Since we are interested in the top 5, we have enough to get a feel for the top words for this dataset.

The results are as follows (which also print to screen):

    The top 5 words and their frequency in that city compared to the overall usage are as follows:
    Atlanta,_GA:  [['georgia', 1.0], ['duranduran', 1.0], ['scaa2016', 1.0], ['buckhead', 1.0], ['duran', 1.0]]
    Boston,_MA:  [['fenway', 1.0], ['dorchester', 1.0], ['massachusetts', 0.9885057471264368], ['onebostonday', 0.9795918367346939], ['boston', 0.9732824427480916]]
    Chicago,_IL:  [['wrigley', 1.0], ['ohare', 1.0], ['jarvis', 1.0], ['chitown', 1.0], ['chicago', 0.9939320388349514]]
    Houston,_TX:  [['baths', 1.0], ['astros', 1.0], ['bbva', 1.0], ['i45', 1.0], ['tx', 0.9989669421487604]]
    Los_Angeles,_CA:  [['dodger', 1.0], ['dtla', 1.0], ['granada', 1.0], ['ucla', 1.0], ['woodlandhills', 1.0]]
    Manhattan,_NY:  [['nycmissed', 1.0], ['tribeca2016', 1.0], ['tribecafilmfestival', 1.0], ['centralpark', 1.0], ['rockefeller', 1.0]]
    Orlando,_FL:  [['orlpol', 1.0], ['ocso', 1.0], ['suspiciousperson', 1.0], ['32801', 1.0], ['housebusinesscheck', 1.0]]
    Philadelphia,_PA:  [['phillies', 1.0], ['philadelphia', 0.9965457685664939], ['pa', 0.979002624671916], ['pennsylvania', 0.9397590361445783], ['philly', 0.9252336448598131]]
    San_Francisco,_CA:  [['fran', 1.0], ['sanfrancisco', 0.9978540772532188], ['francisco', 0.9890350877192983], ['request', 0.9846153846153847], ['sf', 0.9473684210526315]]
    San_Diego,_CA:  [['petco', 1.0], ['lajolla', 1.0], ['jolla', 1.0], ['seaworld', 1.0], ['sandiego', 0.991869918699187]]
    Toronto,_Ontario:  [['b/w', 1.0], ['scarborough', 1.0], ['ud', 1.0], ['highrise', 1.0], ['the6ix', 1.0]]
    Washington,_DC:  [['washingtondc', 1.0], ['dc', 0.9856230031948882], ['nationals', 0.9523809523809523], ['capitol', 0.9512195121951219], ['washington', 0.9090909090909091]]

Manual inspection of these words seem to make the most sense.  They describe city-specific baseball items (astros, nationals, fenway) or local neighborhoods like La Jolla for San Diego or WoodlandHills for Los Angeles.  Some of the top tags have the city's name.  A value of 1.0 here indicates that word appeared only in that city's tweets, which makes it a very strong indicator for that city.

## Opportunities for Improvement

** Run Experiments to Determine Overfitting** - To settle some of the questions I had about overfitting, it would be helpful in the future to actually have additional datasets.  Another way that is often achieved in Machine Learning is to do multiple "folds" of the training data.  For example, I could do ten folds, each has 10% (3200 datapoints) from the training datasats, where 3200 datapoints are made the testing dataset, and the rest remains in the training set.  I would do this with one model that filters out the # and @ and one that does not.  I would then average the results of each set of those ten runs, and compare the results.  This would give me a much better feel for what punctuation actually mattered.

** Refactor My Code ** - This code is relatively lean, and it benefited from me trying several different ways to do the most important functions.  This allowed me to drive my initial runtime of over two minutes down to four seconds overall.  With that said, there is probably an opportunity to refactor the code even more.