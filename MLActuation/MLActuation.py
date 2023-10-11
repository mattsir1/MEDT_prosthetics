# -*- coding: utf-8 -*-
# imports
import numpy as np

# important files: clapping, handshaking, waving

# Figure out how many data points are actually needed to get the required accuracy (98%)
# 10,000 points for training and 10,000 points for testing is a good start (this is not actually implemented, but is rather a suggestion.)

features = ['RBic', 'RTri', 'LBic', 'LTri', 'RThi', 'RHam', 'LThi', 'LHam']


# Algorithm 1
def classifyk(newItem, data, labels, k):
    """using the new item, step through each row of data,
    sort the labels by closest data, return k nearest neighbour"""
    #get how many times it is near k

    distances = ((data-newItem)**2).sum(axis = 1)**0.5 
    d_sort = distances.argsort() # sorts with closest distance first

    #the sorted arrays
    #distances  = distances[d_sort]
    labels = labels[d_sort] # sorts the labels according to which one has closest distance
    return np.unique(labels[:k], return_counts=True) 


# Load in data
def loadData(path):
    files = ['Clapping', 'Handshaking', 'Waving']
    
    data = [] # 2D list, [row][column], rows correspond to labels, columns correspond to features
    labels = []
    
    for i in range (0,3):
        for fileName in files:
            with open(path%(i+1) + fileName + ".txt") as f:
                text = f.readlines()
                
            for line in text[::10]:
                values = line.replace("\n", "").split("\t")
                data.append(values)
                labels.append(fileName)
        
    data = np.array(data, dtype = np.intc) # convert data to integers
    labels = np.array(labels)
    
    # debugging
    print(labels[0])
    print(features[1])
    print(data[0][1])
    
    return data, labels
    
    
def main():
    path = r"EMGPhysicalActionDataSet\\sub%s\\Normal\\txt\\"
    data, labels = loadData(path)
    
    #create a random sort order to be applied to all data
    sort = labels.argsort(axis = 0) # creates list of indices that, if applied, would sort data rows
    
    for j in range(1):
        np.random.shuffle(sort) # creates a random order

        # sorts the data into that random order
        data = data[sort]
        labels = labels[sort]

        #get the size of testing/training data
        full_size = data.shape[0] # num rows
        top = int(full_size * 0.75) # 3/4 of the data, for training
        bot = int(full_size - top) # 1/4 of the data, for testing

        print()
        print("Training Set")
        print("Features, Min, Max, Mean, Median") 
        # first 3/4 of data
        # features, of top 75% find the min value, of top 75% find max value, etc
        print(np.array([features, data[:top].min(axis=0), data[:top].max(axis=0), data[:top].mean(axis=0),np.median(data[:top], axis = 0)]))
        print()
        print("Testing Set")
        print("Features, Min, Max, Mean, Median") 
        # last 1/4 of data
        print(np.array([features, data[top:].min(axis=0), data[top:].max(axis=0), data[top:].mean(axis=0),np.median(data[top:], axis = 0)]))
        print()

        ##kNN classification
        correct_k_count = [0,0,0,0]

        top_data = data[:top] # first 75% of data
        top_labels = labels[:top]

        data_len = len(data[top:]) # length of last 25% of data

        from datetime import datetime

        print("\n")
        print("Iteration ", j)
        startTime = datetime.now()
        for i in range(len(data[top:])): # for every point in last 25%:
            row = data[top:][i] # slice the list to the bottom part and then take the ith element
            label = labels[top:][i] # corresponding label

            if sum(classifyk(row, top_data, top_labels, 1)[0] == label) > 0:
                correct_k_count [0] += 1
            if sum(classifyk(row, top_data, top_labels, 5)[0] == label) > 0:
                correct_k_count [1] += 1
            if sum(classifyk(row, top_data, top_labels, 15)[0] == label) > 0:
                correct_k_count [2] += 1
        
        endTime = datetime.now()
        print("Time elapsed", endTime-startTime) # how long it takes the algorithm to run

        print(data_len, " values in testing data")

        print("kNN Euclidian")
        print(correct_k_count [0], " correct ", " with an accuracy of ", correct_k_count[0]/data_len)
        print(correct_k_count [1], " correct ", " with an accuracy of ", correct_k_count[1]/data_len)
        print(correct_k_count [2], " correct ", " with an accuracy of ", correct_k_count[2]/data_len)
    
    
main()