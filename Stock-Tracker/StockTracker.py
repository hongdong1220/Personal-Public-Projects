
# Latest Modified Day: 08/09/2020
# Created by Hong Dong
# This program uses the API provided from Alpha Vantage; Link: https://www.alphavantage.co/documentation/
# Their Official GitHub for
# This is intended for checking the average daily intraday move & the overnight move of a Stock
# You will enter input as instructed on the program in order for it to work

#JUST IN CASE THAT THE API FAILED HERE IS AN OTHER ONE: https://polygon.io/

from alpha_vantage.timeseries import TimeSeries
import os
import matplotlib.pyplot as plt
import pandas as pd
from APIKey import my_api_key 

running = True
symbol = "Unknown"
days = -1

ts = TimeSeries(key=my_api_key, output_format='pandas', indexing_type='date')


def main():
    global symbol
    global running
    global days
    while running:
        symbol = "Unknown"
        days = -1
        print("Enter \"Exit\" or \"q\" to exit")
        symbol = input("Enter the Stock Symbol: ")
        if symbol.lower() == "exit" or symbol.lower() == "q":
            running = False
            print("Program ended")
        elif get_day():
            print_avg()


def get_day():
    global days
    global running
    while days < 0:
        try:
            days = input("How many days from the most recent market day (MUST BE >= 0): ")
            if int(days) < 0:
                print("\nYo, I cant predict the future")
                print("Enter \"Exit\" or \"q\" to exit or ENTER A VALID DAY!!!!")
                days = int(-1)
            else:
                days = int(days)
        except ValueError as err:
            if days.lower() == "exit" or days.lower() == "q":
                running = False
                print("Program ended")
                return False
            else:
                print("\n****************ERROR********************")
                print("Please enter a number!!!")
                print("OR Enter \"Exit\" or \"q\" to exit")
                print("*****************************************\n")
                days = int(-1)
    return True


def print_avg():
    global days
    global symbol
    try:  # This will run if user entered a valid stock symbol
        data, meta_data = ts.get_daily(symbol=symbol, outputsize='full')
        data = data.sort_index(axis=0, ascending=False).head(days + 1)

        print(data)

        os.system('cls')
        print("\n----------------------------------------------------------------------")
        print("The info below shows you the average movement of " + symbol + " over " + str(days) + " days")
        print("----------------------------------------------------------------------")

        # This part gather info about the average/max/min daily move in percentage
        intraday_move = abs((((data["4. close"] - data["1. open"]) / data["1. open"]) * 100))
        print("\nIntraday------------------------------------------------------------")
        print("Common Move: " + str(round(intraday_move.mean(), 3)) + "%")
        print("Max Move: " + str(round(intraday_move.max(), 3)) + "%" + " @ " + str(intraday_move.idxmax()))
        print("Min Move: " + str(round(intraday_move.min(), 3)) + "%" + " @ " + str(intraday_move.idxmin()))

        # This part gather info about the average/max/min after hour move in percentage
        ah_move = abs(data["1. open"] - data["4. close"].shift(1))
        print("\nAfter hour Gap up or down-------------------------------------------")
        print("Common Move: " + str(round(ah_move.mean(), 3)) + "%")
        print("Max Move: " + str(round(ah_move.max(), 3)) + "%" + " @BM of " + str(ah_move.idxmax()))
        print("Min Move: " + str(round(ah_move.min(), 3)) + "%" + " @BM of " + str(ah_move.idxmin()) + "\n")


    except ValueError as msg:
        # This is where the user is a PEPEGA and enter the wrong Symbol
        os.system('cls')
        print("\n****************ERROR********************")
        print("Invalid stock symbol, Please double check")
        print("You Entered: " + symbol)
        print("*****************************************\n")


if __name__ == '__main__':
    main()
