# coding:utf-8

import numpy as np
import time
Capacity =[]
Open = []
OpenCost = []
Demand = []
AssignCost = [[]]
Assign = [[]]

def readFile():
  global Capacity, Assign, Demand, OpenCost, AssignCost, Open
  fr = open('../Instances/p63')
  firstArr = fr.readline().strip().split()
  fac_num = int(firstArr[0])
  cus_num = int(firstArr[1])
  Capacity = [0] * fac_num
  OpenCost = [0] * fac_num
  Demand = [0] * cus_num
  Open = [0] * fac_num
  AssignCost = [[0 for _ in range(cus_num)] for _ in range(fac_num)]
  Assign = [[0 for _ in range(cus_num)] for _ in range(fac_num)]
  for i in range(fac_num):
    lineArr = fr.readline().strip().split()
    Capacity[i] = float(lineArr[0])
    OpenCost[i] = float(lineArr[1])
  for i in range(cus_num / 10):
    lineArr = fr.readline().strip().split()
    for j in range(10):
        Demand[i * 10 + j] = float(lineArr[j])
  for i in range(fac_num):
    for j in range(cus_num / 10):
        lineArr = fr.readline().strip().split()
        for k in range(10):
            AssignCost[i][j * 10 + k] = float(lineArr[k])
  fr.close()


def greedy():
    #print len(Assign[0])
    i = len(Assign[0]) - 1
    while i >= 0:
    #for i in range(len(Assign[0])):
      min = 99999
      fac = 0
      cus = 0
      for j in range(len(Assign)):
          Assign[j][i] = 1
          if capcaityLimit(j) == 1:   
              Assign[j][i] = 0 
              continue
          Assign[j][i] = 0
          cost = getOneCost(j, i)
          if cost < min:
            min = cost
            fac = j
            cus = i
      Assign[fac][cus] = 1
      i -= 1
    #print Assign

def getOneCost(fac, cus):
  cost = OpenCost[fac] + AssignCost[fac][cus]
  return cost

def getcost():
    global Open
    cost = 0
    Open = [0] * len(Capacity)
    for i in range(len(Demand)):
        for j in range(len(Open)):
            if Assign[j][i] == 1:
                Open[j] = 1
    for i in range(len(OpenCost)):
        cost += OpenCost[i] * Open[i]
    for i in range(len(AssignCost)):
        for j in range(len(AssignCost[0])):
            cost += AssignCost[i][j] * Assign[i][j]
    return cost

def capcaityLimit(fac):
    cap = 0
    flag = 0
    for i in range(len(Assign[fac])):
        cap += Assign[fac][i] * Demand[i]
        if cap > Capacity[fac]:
            flag = 1
            break
    return flag

def capcaityNow(fac):
    cap = 0
    for i in range(len(Assign[fac])):
        cap += Assign[fac][i] * Demand[i]
    return cap

readFile()

start = time.time()
greedy()
  
cost = getcost() 

end = time.time()
print end - start
print cost

cus_fac = [0] * len(Demand)
for i in range(len(Demand)):
    for j in range(len(Open)):
        if Assign[j][i] == 1:
            cus_fac[i] = j + 1
            Open[j] = 1
print Open
print cus_fac
#print [num for num in range(50)]
#for i in range(10):
    #print capcaityNow(i)