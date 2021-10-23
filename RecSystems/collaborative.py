from numpy import *
import math
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel


def rec_clcalculator(arr, users, foods, user_data):
    def getUser():
        count = 0
        for x in users:
            if(x == user_data):
                return count
            count = count + 1

    def noneatenFood():
        noFood = []
        count = 0
        for food in arr[getUser()]:
            if(food == 0):
                noFood.append(count)
            count = count + 1
        return noFood

    def average(a, user):

        sum = 0
        count = 0
        for i in range(0, len(user)):
            if(user[i] != 0 and a[i] != 0):
                sum = sum + user[i]
                count = count + 1
        
        return sum / count

    def sim(a, b):
        pay = 0
        for i in range(0, len(arr[0])):
            if(a[i] != 0 and b[i] != 0):
                pay = pay + (a[i] - average(a, a))*(b[i] - average(a, b))

        payda_a = 0
        for i in range(0, len(arr[0])):
            if(a[i] != 0 and b[i] != 0):
                payda_a = payda_a + (a[i] - average(a, a))**2

        payda_a = sqrt(payda_a)

        payda_b = 0
        for i in range(0, len(arr[0])):
            if(a[i] != 0 and b[i] != 0):
                payda_b = payda_b + (b[i] - average(a, b))**2

        payda_b = sqrt(payda_b)
        if((payda_a * payda_b) == 0):
            return -1

        similarity = pay / (payda_a * payda_b)

        return similarity

    sim_array = []
    for user in range(1, len(arr)):
        sim_array.append(sim(arr[0], arr[user]))

    list = []
    maxPred = 0
    foodnameid = 2

    for user in range(0, len(sim_array)):
        list.append(arr[user+1])

    def Averages(lst):
        return sum(lst) / len(lst)

    def pred(a, p):

        prediction = 0
        prediction = prediction + average(a, a)

        pay = 0
        for i in range(0, len(list)):

            pay = pay + sim(a, list[i])*(list[i][p] - Averages(list[i]))

        payda = 0
        for i in range(0, len(list)):
            payda = payda + sim(a, list[i])

        prediction = prediction + (pay / payda)

        return prediction

    
    for i in noneatenFood():
        if(pred(arr[getUser()], i) > maxPred):
            foodnameid = i
            maxPred = pred(arr[getUser()], i)
    return (foodnameid)