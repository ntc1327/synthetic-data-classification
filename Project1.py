# Author - Noah Cribelar
# Class: CS 460

from __future__ import division
from math import log2
import matplotlib.pyplot as plt
import pandas as pd

# May have to change the "data/synthetic-*.csv" format depending on how the program is ran
# To replicate this format make sure the Project file is in the same folder the datasets are in
print("Which dataset would you like to use? Use format data/synthetic-*.csv, replace * with number 1-4")
givenDataset = input("Enter your desired dataset: ")

data = pd.read_csv(givenDataset)
leftBin1 = rightBin1 = pd.DataFrame()
leftBin2 = leftBin3 = rightBin2 = rightBin3 = pd.DataFrame()
leftBin21 = leftBin22 = leftBin31 = leftBin32 = rightBin21 = rightBin22 = rightBin31 = rightBin32 = pd.DataFrame()
groupedBins = {}
binCount = count = 0


# calculates entropy given two integer values
def entropy(x, y):
    if x == 0 or y == 0:
        return 0.0
    total = x + y
    return -(x/total) * log2(x/total) - (y/total) * log2(y/total)


# simple subtraction for information gain, assume entropy is value passed in for both parameters
def infogain(e1, e2):
    return e1 - e2


# function that helped calculate the accuracy by giving the needed values for calculation, can play with this to see how
def accuracy(bin):
    oneCount = zeroCount = 0
    for i in range(len(bin)):
        if bin.loc[bin.index[i], '3'] == 1:
            oneCount += 1
        else:
            zeroCount += 1

    total = oneCount + zeroCount
    if zeroCount > oneCount:
        print(zeroCount/total)
    else:
        print(oneCount/total)

    print(total)
    return


# given a bin, does both possible splits, calculates the information gain for each one, then passes the optimal split
# to the tree
def bin_decision(bin):
    tempBin1 = tempBin2 = tempBin3 = tempBin4 = pd.DataFrame()
    mainBinOneCount = mainBinZeroCount = 0
    tb1OneCount = tb1ZeroCount = tb2OneCount = tb2ZeroCount = tb3OneCount = tb3ZeroCount = tb4OneCount = tb4ZeroCount = 0

    # runs through bin, sorts by Column 1 values compared to mean
    for i in range(len(bin)):
        if bin.loc[bin.index[i], '1'] < bin['1'].mean():
            tempBin1 = tempBin1.append(bin.iloc[i, :])
        else:
            tempBin2 = tempBin2.append(bin.iloc[i, :])

    # runs through bin, sorts by Column 2 values comapared to mean
    for i in range(len(bin)):
        if bin.loc[bin.index[i], '2'] < bin['2'].mean():
            tempBin3 = tempBin3.append(bin.iloc[i, :])
        else:
            tempBin4 = tempBin4.append(bin.iloc[i, :])

    # tallies up class label counts for all bins
    for i in range(len(bin)):
        if bin.loc[bin.index[i], '3'] == 1:
            mainBinOneCount += 1
        else:
            mainBinZeroCount += 1

    for i in range(len(tempBin1)):
        if tempBin1.loc[tempBin1.index[i], '3'] == 1:
            tb1OneCount += 1
        else:
            tb1ZeroCount += 1

    for i in range(len(tempBin2)):
        if tempBin2.loc[tempBin2.index[i], '3'] == 1:
            tb2OneCount += 1
        else:
            tb2ZeroCount += 1

    for i in range(len(tempBin3)):
        if tempBin3.loc[tempBin3.index[i], '3'] == 1:
            tb3OneCount += 1
        else:
            tb3ZeroCount += 1

    for i in range(len(tempBin4)):
        if tempBin4.loc[tempBin4.index[i], '3'] == 1:
            tb4OneCount += 1
        else:
            tb4ZeroCount += 1

    # calculates information gain using entropy
    # formula is the average information gained over both bins depending on the column chosen
    gainedInfo1 = (infogain(entropy(mainBinZeroCount, mainBinOneCount), entropy(tb1ZeroCount, tb1OneCount)) + infogain(entropy(mainBinZeroCount, mainBinOneCount), entropy(tb2ZeroCount, tb2OneCount))) / 2
    gainedInfo2 = (infogain(entropy(mainBinZeroCount, mainBinOneCount), entropy(tb3ZeroCount, tb3OneCount)) + infogain(entropy(mainBinZeroCount, mainBinOneCount), entropy(tb4ZeroCount, tb4OneCount))) / 2

    if gainedInfo1 > gainedInfo2:
        return '1'
    elif gainedInfo1 < gainedInfo2:
        return '2'


# for all possible bins, calculates the decision to use column 1 or column 2 to split
if bin_decision(data) == '1':
    for i in range(len(data)):
        if data.loc[i, '1'] < data['1'].mean():
            leftBin1 = leftBin1.append(data.iloc[i, :])
        else:
            rightBin1 = rightBin1.append(data.iloc[i, :])
elif bin_decision(data) == '2':
    for i in range(len(data)):
        if data.loc[i, '2'] < data['2'].mean():
            leftBin1 = leftBin1.append(data.iloc[i, :])
        else:
            rightBin1 = rightBin1.append(data.iloc[i, :])

if bin_decision(leftBin1) == '1':
    for ind in range(len(leftBin1)):
        if leftBin1.loc[leftBin1.index[ind], '1'] < leftBin1['1'].mean():
            leftBin2 = leftBin2.append(leftBin1.iloc[ind, :])
        else:
            leftBin3 = leftBin3.append(leftBin1.iloc[ind, :])
elif bin_decision(leftBin1) == '2':
    for ind in range(len(leftBin1)):
        if leftBin1.loc[leftBin1.index[ind], '2'] < leftBin1['2'].mean():
            leftBin2 = leftBin2.append(leftBin1.iloc[ind, :])
        else:
            leftBin3 = leftBin3.append(leftBin1.iloc[ind, :])

if bin_decision(rightBin1) == '1':
    for ind in range(len(rightBin1)):
        if rightBin1.loc[rightBin1.index[ind], '1'] < rightBin1['1'].mean():
            rightBin2 = rightBin2.append(rightBin1.iloc[ind, :])
        else:
            rightBin3 = rightBin3.append(rightBin1.iloc[ind, :])
elif bin_decision(rightBin1) == '2':
    for ind in range(len(rightBin1)):
        if rightBin1.loc[rightBin1.index[ind], '2'] < rightBin1['2'].mean():
            rightBin2 = rightBin2.append(rightBin1.iloc[ind, :])
        else:
            rightBin3 = rightBin3.append(rightBin1.iloc[ind, :])

if bin_decision(leftBin2) == '1':
    for ind in range(len(leftBin2)):
        if leftBin2.loc[leftBin2.index[ind], '1'] < leftBin2['1'].mean():
            leftBin21 = leftBin21.append(leftBin2.iloc[ind, :])
        else:
            leftBin22 = leftBin22.append(leftBin2.iloc[ind, :])
elif bin_decision(leftBin2) == '2':
    for ind in range(len(leftBin2)):
        if leftBin2.loc[leftBin2.index[ind], '2'] < leftBin2['2'].mean():
            leftBin21 = leftBin21.append(leftBin2.iloc[ind, :])
        else:
            leftBin22 = leftBin22.append(leftBin2.iloc[ind, :])

if bin_decision(leftBin3) == '1':
    for ind in range(len(leftBin3)):
        if leftBin3.loc[leftBin3.index[ind], '1'] < leftBin3['1'].mean():
            leftBin31 = leftBin31.append(leftBin3.iloc[ind, :])
        else:
            leftBin32 = leftBin32.append(leftBin3.iloc[ind, :])
elif bin_decision(leftBin3) == '2':
    for ind in range(len(leftBin3)):
        if leftBin3.loc[leftBin3.index[ind], '2'] < leftBin3['2'].mean():
            leftBin31 = leftBin31.append(leftBin3.iloc[ind, :])
        else:
            leftBin32 = leftBin32.append(leftBin3.iloc[ind, :])

if bin_decision(rightBin2) == '1':
    for ind in range(len(rightBin2)):
        if rightBin2.loc[rightBin2.index[ind], '1'] < rightBin2['1'].mean():
            rightBin21 = rightBin21.append(rightBin2.iloc[ind, :])
        else:
            rightBin22 = rightBin22.append(rightBin2.iloc[ind, :])
elif bin_decision(rightBin2) == '2':
    for ind in range(len(rightBin2)):
        if rightBin2.loc[rightBin2.index[ind], '2'] < rightBin2['2'].mean():
            rightBin21 = rightBin21.append(rightBin2.iloc[ind, :])
        else:
            rightBin22 = rightBin22.append(rightBin2.iloc[ind, :])

if bin_decision(rightBin3) == '1':
    for ind in range(len(rightBin3)):
        if rightBin3.loc[rightBin3.index[ind], '1'] < rightBin3['1'].mean():
            rightBin31 = rightBin31.append(rightBin3.iloc[ind, :])
        else:
            rightBin32 = rightBin32.append(rightBin3.iloc[ind, :])
elif bin_decision(rightBin3) == '2':
    for ind in range(len(rightBin3)):
        if rightBin3.loc[rightBin3.index[ind], '2'] < rightBin3['2'].mean():
            rightBin31 = rightBin31.append(rightBin3.iloc[ind, :])
        else:
            rightBin32 = rightBin32.append(rightBin3.iloc[ind, :])

# finds all filled bins and gets a count of all bins
if not rightBin32.empty:
    groupedBins[count] = rightBin32
    count += 1
    groupedBins[count] = rightBin31
    count += 1
elif not rightBin3.empty:
    groupedBins[count] = rightBin3
    count += 1
elif not rightBin1.empty:
    groupedBins[count] = rightBin1
    count += 1

if not rightBin22.empty:
    groupedBins[count] = rightBin22
    count += 1
    groupedBins[count] = rightBin21
    count += 1
elif not rightBin2.empty:
    groupedBins[count] = rightBin2
    count += 1

if not leftBin32.empty:
    groupedBins[count] = leftBin32
    count += 1
    groupedBins[count] = leftBin31
    count += 1
elif not leftBin3.empty:
    groupedBins[count] = leftBin3
    count += 1
elif not leftBin1.empty:
    groupedBins[count] = leftBin1
    count += 1

if not leftBin22.empty:
    groupedBins[count] = leftBin22
    count += 1
    groupedBins[count] = leftBin21
    count += 1
elif not leftBin2.empty:
    groupedBins[count] = leftBin2
    count += 1

# re-assigns all bins to be able to work with them easier
if count >= 1:
    bin1 = groupedBins[0]
if count >= 2:
    bin2 = groupedBins[1]
if count >= 3:
    bin3 = groupedBins[2]
if count >= 4:
    bin4 = groupedBins[3]
if count >= 5:
    bin5 = groupedBins[4]
if count >= 6:
    bin6 = groupedBins[5]
if count >= 7:
    bin7 = groupedBins[6]
if count == 8:
    bin8 = groupedBins[7]

# starts plotting
fig = plt.figure()
ax = groupedBins[0].plot(kind='scatter', x='1', y='2')

# depending on the number of bins, figures out all class label colors and plots them
# also realized after the fact I could have done this all from the initial read in of the dataset
if count >= 1:
    for i in range(len(bin1)):
        if bin1.loc[bin1.index[i], '3'] == 1:
            bin1.plot(kind='scatter', x='1', y='2', color='red', ax=ax)
        elif bin1.loc[bin1.index[i], '3'] == 0:
            bin1.plot(kind='scatter', x='1', y='2', color='blue', ax=ax)
if count >= 2:
    for i in range(len(bin2)):
        if bin2.loc[bin2.index[i], '3'] == 1:
            bin2.plot(kind='scatter', x='1', y='2', color='red', ax=ax)
        elif bin2.loc[bin2.index[i], '3'] == 0:
            bin2.plot(kind='scatter', x='1', y='2', color='blue', ax=ax)
if count >= 3:
    for i in range(len(bin3)):
        if bin3.loc[bin3.index[i], '3'] == 1:
            bin3.plot(kind='scatter', x='1', y='2', color='red', ax=ax)
        elif bin3.loc[bin3.index[i], '3'] == 0:
            bin3.plot(kind='scatter', x='1', y='2', color='blue', ax=ax)
if count >= 4:
    for i in range(len(bin4)):
        if bin4.loc[bin4.index[i], '3'] == 1:
            bin4.plot(kind='scatter', x='1', y='2', color='red', ax=ax)
        elif bin4.loc[bin4.index[i], '3'] == 0:
            bin4.plot(kind='scatter', x='1', y='2', color='blue', ax=ax)
if count >= 5:
    for i in range(len(bin5)):
        if bin5.loc[bin5.index[i], '3'] == 1:
            bin5.plot(kind='scatter', x='1', y='2', color='red', ax=ax)
        elif bin5.loc[bin5.index[i], '3'] == 0:
            bin5.plot(kind='scatter', x='1', y='2', color='blue', ax=ax)
if count >= 6:
    for i in range(len(bin6)):
        if bin6.loc[bin6.index[i], '3'] == 1:
            bin6.plot(kind='scatter', x='1', y='2', color='red', ax=ax)
        elif bin6.loc[bin6.index[i], '3'] == 0:
            bin6.plot(kind='scatter', x='1', y='2', color='blue', ax=ax)
if count >= 7:
    for i in range(len(bin7)):
        if bin7.loc[bin7.index[i], '3'] == 1:
            bin7.plot(kind='scatter', x='1', y='2', color='red', ax=ax)
        elif bin7.loc[bin7.index[i], '3'] == 0:
            bin7.plot(kind='scatter', x='1', y='2', color='blue', ax=ax)
if count >= 8:
    for i in range(len(bin8)):
        if bin8.loc[bin8.index[i], '3'] == 1:
            bin8.plot(kind='scatter', x='1', y='2', color='red', ax=ax)
        elif bin8.loc[bin8.index[i], '3'] == 0:
            bin8.plot(kind='scatter', x='1', y='2', color='blue', ax=ax)

plt.show()
