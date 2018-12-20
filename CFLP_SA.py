# coding:utf-8

import numpy as np
import time as ti
import pandas as pd

Capacity =[]
Open = []
OpenCost = []
Demand = []
AssignCost = [[]]
Assign = [[]]

def readFile(file_name):
  global Capacity, Assign, Demand, OpenCost, AssignCost, Open
  fr = open('Instances/' + file_name)
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

def initData():
    cusNum = 0
    #i = len(Assign) - 1
    #while i >= 0:
    for i in range(len(Assign)):
        for j in range(cusNum, len(Assign[0])):
            Assign[i][j] = 1
            if capcaityLimit(i) == 1:
                Assign[i][j] = 0
                break
            cusNum += 1
     #   i -= 1
    #print Assign
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

def exchange():
    while True:  
        while True:
            fac1 = np.int(np.ceil(np.random.rand()*(len(Open)-1)))
            cus = np.int(np.ceil(np.random.rand()*(len(Assign[0])-1)))
            if Assign[fac1][cus] == 1:
                break
        fac2 = np.int(np.ceil(np.random.rand()*(len(Open)-1)))
        Assign[fac1][cus], Assign[fac2][cus] = Assign[fac2][cus], Assign[fac1][cus]
        if capcaityLimit(fac1) == 0 and capcaityLimit(fac2) == 0:
            break
        else:
            Assign[fac1][cus], Assign[fac2][cus] = Assign[fac2][cus], Assign[fac1][cus]
    return fac1, fac2, cus


def initpara():
    alpha = 0.9
    t = (1,100)
    markovlen = 200
 
    return alpha,t,markovlen

def main(file_name):
    readFile(file_name)

    start = ti.time()
    greedy()
    
    costcurrent = getcost() 
    #print costcurrent
    alpha,t2,markovlen = initpara()
    t = t2[1]

    costbest = costcurrent
    while t > t2[0]:
        for i in np.arange(markovlen):
            fac1, fac2, cus = exchange()
            costnew = getcost()
            #print costnew
            '''print Assign[0]
            print Assign[1]
            print Assign[2]
            print Assign[3]
            print Assign[4]
            print Assign[5]
            print Assign[6]
            print Assign[7]
            print Assign[8]
            print Assign[9]'''
            if costnew < costcurrent: 
                costcurrent = costnew
            else:#按一定的概率接受该解
                if np.random.rand() < np.exp(-(costnew-costcurrent)/t):
                    costcurrent = costnew
                    if costcurrent < costbest:
                        costbest = costcurrent
                else:
                    Assign[fac1][cus], Assign[fac2][cus] = Assign[fac2][cus], Assign[fac1][cus]

        t = alpha*t
    end = ti.time()
    time = end-start
    print costbest

    cus_fac = [0] * len(Demand)
    for i in range(len(Demand)):
        for j in range(len(Open)):
            if Assign[j][i] == 1:
                cus_fac[i] = j + 1
                Open[j] = 1
    print Open
    print cus_fac
    f = open('result.txt', 'a')
    f.write(file_name + '\n')
    f.write(str(costbest) + '\n')
    for i in range(len(Open)):
        f.write(str(Open[i]) + ' ')
    f.write('\n')
    for i in range(len(cus_fac)):
        f.write(str(cus_fac[i]) + ' ')
    f.write('\n\n')
    f.close()
    return costbest, time

if __name__ == "__main__":
    file_name = []
    for i in range(71):
        file_name.append("p" + str(i + 1))
    result = []
    times = []
    for i in range(71):
        r, t = main(file_name[i])
        result.append(r)
        times.append(t)
    #print result ,times
    #字典中的key值即为csv中列名
    dataframe = pd.DataFrame({' ': file_name, 'result': result,'time':times})

    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("result.csv",index=False,sep=',')