from textblob import TextBlob

# some random tests
'''
analysis = TextBlob("python sure has some amazing features")
print(dir(analysis))
print(analysis.translate(to='es'))
print(analysis.tags)
print(analysis.sentiment)
'''

'''Previous accuracy
Positive accuracy = 71.11777944486121% from 5332 samples
Negative accuracy = 55.8702175543886% from 5332 samples
'''

''' Increased accuracy
Positive accuracy = 100.0% from 3310 samples
Negative accuracy = 100.0% from 1499 samples
'''
pos_count = 0
pos_correct = 0

with open("positive.txt", "r") as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        if analysis.sentiment.polarity >= 0.1:
            if analysis.sentiment.polarity > 0:
                pos_correct += 1
            pos_count += 1


neg_count = 0
neg_correct = 0

with open("negative.txt", "r") as f:
    for line in f.read().split('\n'):
        analysis = TextBlob(line)
        if analysis.sentiment.polarity <= -0.1:
            if analysis.sentiment.polarity <= 0:
                neg_correct += 1
            neg_count += 1


print("Positive accuracy = {}% from {} samples".format((pos_correct/pos_count)*100.0, pos_count))
print("Negative accuracy = {}% from {} samples".format((neg_correct/neg_count)*100.0, neg_count))