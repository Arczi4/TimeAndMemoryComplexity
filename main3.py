import random
from numpy.lib.shape_base import expand_dims
import pandas as pd
import timeit
import matplotlib.pyplot as plt
import psutil
import os
import numpy as np
import csv

Data = None

def init():
    with open('init.txt') as f:
        plik = f.readlines()
    we = plik[0].rstrip()
    wy = plik[1].rstrip()
    przedzialy = plik[2].rstrip().split(',')
    przedzialy = [int(x) for x in przedzialy[1:]]
    return we, wy, przedzialy

def readData(csvFile):
    '''
    Wyczytanie danych z pliku csv. Funkcja wczytuje kolumne `Dane`, przypisuje to do zmiennej globalnej Data
    '''
    global Data
    try:
        df = pd.read_csv(csvFile)
        Data = df['Dane'].to_list()
    except:
        print("Błąd wczytania danych")

def createData(N, fileDest):
    '''
    Zapis listy zlozonej z N randomowych elementow, do pliku CSV
    '''
    df = pd.DataFrame({'Dane': [random.randint(-100000, 100000) for x in range(N)]})
    df.to_csv(fileDest, index=None)

def writeData(data, fileDest, mode='w'):
    with open(fileDest, mode, encoding='utf-8') as csvfile: # w-zapis
        writer = csv.writer(csvfile)
        for key in data.keys():
            writer.writerow([key])
            for x in data[key].keys():
                writer.writerow([x, data[key][x]])

def chart(x, y, pltTitle, pltYLabel, deg, YLim=False):
    try:
        plt.plot(x, y, 'bo')
        plt.title(pltTitle)
        plt.xlabel('Wielkość instancji')
        plt.ylabel(pltYLabel)
        z = np.polyfit(x, y, deg)
        p = np.poly1d(z)
        plt.plot(x, p(x),"r--")
        plt.grid()
        if YLim:
            plt.ylim([0, 90])
        plt.show()
    except:
        print("Blad wyswietlania wykresu!")

#########################################################
# Algorytmy do zadania
def partition(arr, low, high):
    '''
    Oś ustawiona na ostatnim elemencie w liscie, liczby mniejsze od osi na lewo
    liczby większe od osi na prawo
    '''
    i = (low-1)
    pivot = arr[high] 
  
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
    
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)

def quickSort(arr, first, last):
    if len(arr) == 1:
        return arr

    if first < last:
        pi = partition(arr, first, last)
        quickSort(arr, first, pi-1)
        quickSort(arr, pi+1, last)

def bubbleSort(data):
    dataCpy = data[::]
    n = len(dataCpy)
    for i in range(n):
        for j in range(0, n-i-1):
            if dataCpy[j] > dataCpy[j+1] :
                dataCpy[j], dataCpy[j+1] = dataCpy[j+1], dataCpy[j]
    return dataCpy
    
###############################################################3

we, wy, przedzial = init()
# createData(1000000, we)
readData(we)

BubbleSortInfo = {'time': {}, 'memoryUsed': {}}
QuickSortInfo = {'time': {}, 'memoryUsed': {}}

while True:
    print("\tMENU:")
    print("1. Sortowanie babelkowe")
    print("2. Quicksort")
    print("3. Wyswietl dane")
    print("4. Wykres sortowania babelkowego")
    print("5. Wykres quicksorta")
    print("6. Wykres zuzycia pamieci (sortowanie babelkowe)")
    print("7. Wykres zuzycia pamieci (quicksort)")
    print('8. Zapisz wyniki')
    print("9. Pesymistyczna wersja")
    print("10. Wyjscie")

    x = int(input("Co chcesz zrobić? "))

    if x==1: # Bubble sort
        for inst in przedzial:
            dataCpy = Data[:inst]
            start = timeit.default_timer()
            dataSort = bubbleSort(dataCpy[0:inst])

            stop = timeit.default_timer()
            memory = psutil.Process(os.getpid()).memory_info().rss / 1024**2

            timeFormat = float("{:.3f}".format(stop-start))
            memoryFormat = float("{:.3f}".format(memory))

            BubbleSortInfo['memoryUsed'].update({inst: memoryFormat})  
            BubbleSortInfo['time'].update({inst: timeFormat})

    if x==2: # Quicksort
        for inst in przedzial:
            dataCpy = Data[0:inst]
            start = timeit.default_timer()
            quickSort(dataCpy[0: inst], 0, len(dataCpy[0:inst])-1)
            memory = (psutil.Process(os.getpid()).memory_info().rss) / (1024**2)
            stop = timeit.default_timer()

            timeFormat = float("{:.3f}".format(stop-start))
            memoryFormat = float("{:.3f}".format(memory))

            QuickSortInfo['time'].update({inst: timeFormat})
            QuickSortInfo['memoryUsed'].update({inst: memoryFormat})

    if x==3:
        print("\nDANE WEJSCIOWE: \n",Data, end='\n\n')

    if x==4:
        chart(list(BubbleSortInfo['time'].keys()), list(BubbleSortInfo['time'].values()), 'Bubble sort', 'Czas [s]', 2)
    
    if x==5:
        chart(list(QuickSortInfo['time'].keys()), list(QuickSortInfo['time'].values()), 'Quicksort', 'Czas [s]', 1)
    
    if x==6:
        chart(list(BubbleSortInfo['memoryUsed'].keys()), list(BubbleSortInfo['memoryUsed'].values()), 'Bubble sort', 'Pamiec [MB]', 1, True)
    
    if x==7:
        chart(list(QuickSortInfo['memoryUsed'].keys()), list(QuickSortInfo['memoryUsed'].values()), 'Quicksort', 'Pamiec [MB]', 1, True)
    
    if x==8:
        with open(wy, 'w', encoding='utf-8') as csvfile: # w-zapis
            writer = csv.writer(csvfile)
            writer.writerow(['Bubblesort'])
        writeData(BubbleSortInfo, wy)

        with open(wy, 'a', encoding='utf-8') as csvfile: # w-zapis
            writer = csv.writer(csvfile)
            writer.writerow(['Quicksort'])
        writeData(QuickSortInfo, wy, mode='a')
    
    if x==9:
        Data = sorted(Data)
        Data = list(reversed(Data))
        print(Data)
    if x==10:
        break
