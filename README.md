
>项目地址：https://github.com/GostBop/CFLP

@[toc]
# Capacitated Facility Location Problem
## 问题描述

Suppose there are n facilities and m customers. We wish to choose:
1. which of the n facilities to open 
2.  the assignment of customers to facilities

Note：
1. The objective is to minimize the sum of the opening cost and the assignment cost. 
2. The total demand assigned to a facility must not exceed its capacity.

## 问题建模：
 Let
 $I$={1,..., $I$}：the set of $facilities$
 $J$={1,..., $J$}：the set of $customers$
 $d_j$：$customer$ $j$ 's $Demand$，$j∈J$
 $V_i$：$facility$ $i$ 's $Capacity$，$i∈I$
 $C_i$：$facility$ $i$ 's $OpeningCost$，$i∈I$
 $A_{ij}$:  $facility$ $i$ 's $AssignmentCost$ for $customer$ $j$，$i∈I$，$j∈J$

For every $facility$ $i$，$i∈I$， define the following notations：
$$y_i = \begin{cases}  
1 & if.facility.i.is.opened \\
0 & otherwise
\end{cases}$$

For every $facility$ $i$，$i∈I$；$customer$ $j$，$j∈J$；
$$x_{ij} = \begin{cases}  
1 & if.facility.i.is.assigned.for.customer.j\\
0 & otherwise
\end{cases}$$

Then the Capacitated Facility Location Problem may be written：
$$\sum_{j∈J}d_jx_{ij} \leq V_iy_i，i∈I$$
$$min\lbrace \sum_{i∈I}c_iy_i+\sum_{i∈I}\sum_{j∈J}A_{ij}x_{ij}\rbrace$$
$$\sum_{i∈I}x_{ij}=1，j∈J $$
$$x_{ij}，y_i∈\lbrace0, 1\rbrace，i∈I，j∈J$$

## 贪心算法
CFLP问题是NP问题，很难设计一种直接求出最优解的算法，但是我们可以用贪心算法来接近最优解。

贪心算法的策略是：
1. 遍历每一个$customer$ $j$，$j∈J$
2. 让$customer$ $j$逐个选择cost最小的$facility$ $i$，即：
$$min\lbrace \sum_{i∈I}c_iy_i+\sum_{i∈I}A_{ij}x_{ij}\rbrace$$

### 代码实现
```python
# coding:utf-8

import numpy as np
import time
import pandas as pd

Capacity =[]
Open = []
OpenCost = []
Demand = []
AssignCost = [[]]
Assign = [[]]

def readFile(file_name):
  global Capacity, Assign, Demand, OpenCost, AssignCost, Open
  fr = open('../Instances/' + file_name)
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

def main(file_name):
    readFile(file_name)

    start = time.time()
    greedy()
    
    cost = getcost() 

    end = time.time()
    t = end - start
    print cost

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
    f.write(str(cost) + '\n')
    for i in range(len(Open)):
        f.write(str(Open[i]) + ' ')
    f.write('\n')
    for i in range(len(cus_fac)):
        f.write(str(cus_fac[i]) + ' ')
    f.write('\n\n')
    f.close()
    return cost, t

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
    dataframe = pd.DataFrame({'file': file_name, 'result': result,'time':times})

    #将DataFrame存储为csv,index表示是否显示行名，default=True
    dataframe.to_csv("Greedy.csv",index=False,sep=',')
```
### 运算结果
file|result|time
:--|:--|:--
p1|12581.0|0.016000032424926758
p2|8010.0|0.016000032424926758
p3|10010.0|0.014999866485595703
p4|12010.0|0.016000032424926758
p5|12128.0|0.0
p6|8329.0|0.0
p7|10329.0|0.0
p8|12329.0|0.016000032424926758
p9|10776.0|0.0
p10|7726.0|0.0
p11|9726.0|0.016000032424926758
p12|11726.0|0.0
p13|10913.0|0.015000104904174805
p14|9180.0|0.016000032424926758
p15|13180.0|0.014999866485595703
p16|17180.0|0.016000032424926758
p17|10104.0|0.014999866485595703
p18|9180.0|0.015000104904174805
p19|13180.0|0.032000064849853516
p20|17180.0|0.014999866485595703
p21|9845.0|0.016000032424926758
p22|9180.0|0.0
p23|13180.0|0.015000104904174805
p24|17180.0|0.0
p25|18186.0|0.14499998092651367
p26|16095.0|0.1419999599456787
p27|21495.0|0.127000093460083
p28|26895.0|0.127000093460083
p29|18225.0|0.18000006675720215
p30|16173.0|0.14300012588500977
p31|21573.0|0.12800002098083496
p32|26973.0|0.1530001163482666
p33|17364.0|0.1550002098083496
p34|15989.0|0.14599990844726562
p35|21389.0|0.14400005340576172
p36|26789.0|0.15900015830993652
p37|16825.0|0.20200014114379883
p38|15989.0|0.15900015830993652
p39|21389.0|0.127000093460083
p40|26789.0|0.14300012588500977
p41|9276.0|0.016000032424926758
p42|9267.0|0.03099989891052246
p43|7629.0|0.031000137329101562
p44|8833.0|0.02499985694885254
p45|8331.0|0.03299999237060547
p46|8581.0|0.1099998950958252
p47|9203.0|0.046000003814697266
p48|9262.0|0.04699993133544922
p49|7766.0|0.03099989891052246
p50|11502.0|0.015000104904174805
p51|10099.0|0.06299996376037598
p52|13352.0|0.031000137329101562
p53|13680.0|0.04699993133544922
p54|13598.0|0.016000032424926758
p55|11411.0|0.04699993133544922
p56|23882.0|0.2760000228881836
p57|32882.0|0.33500003814697266
p58|53882.0|0.3280000686645508
p59|43697.0|0.24000000953674316
p60|23882.0|0.2519998550415039
p61|32882.0|0.2369999885559082
p62|53882.0|0.2519998550415039
p63|39308.0|0.23600006103515625
p64|23882.0|0.252000093460083
p65|32882.0|0.2519998550415039
p66|53882.0|0.34800004959106445
p67|42079.0|0.252000093460083
p68|23882.0|0.23799991607666016
p69|32882.0|0.26799988746643066
p70|53882.0|0.25299978256225586
p71|42449.0|0.2519998550415039


每一个测例的具体结果
https://gostbop.github.io/CFLP/

## 模拟退火
模拟退火是一种启发式搜索，该算法每次从当前解的临近解空间中选择一个最优解作为当前解，直到达到一个局部最优解。

模拟退火其实也是一种贪心算法，但是它的搜索过程引入了随机因素。模拟退火算法以一定的概率来接受一个比当前解要差的解，因此有可能会跳出这个局部的最优解，达到全局的最优解。

### 初始解
可以使用贪心算法的解作为初始解

### 邻域搜索
这里使用一种简单的邻域搜索。

1. 随机选择一个$facility$和一个$customer$：$a$，$b$
2. 如果该$facility$ $a$已经$Open$并且$Assign$ $for$ $customer$ $b$
3. 那么随机选择另一个 $facility$ $c$
4. 否则重复选择$a$和$b$
5. 将$customer$ $b$从$facility$ $a$中撤出给$facility$ $c$
6. 如果没有超出$facility$ $c$的$Capacity$限制，则操作成功
7. 否则从1开始重复该操作

### 初始参数设置
初温：100℃
内循环迭代次数：200
退火速率：$t = t *0.9$
退火停止点：$t < 1$

### 代码实现
```python
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

def greedy():
    i = len(Assign[0]) - 1
    while i >= 0:
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
    alpha,t2,markovlen = initpara()
    t = t2[1]

    costbest = costcurrent
    while t > t2[0]:
        for i in np.arange(markovlen):
            fac1, fac2, cus = exchange()
            costnew = getcost()
            if costnew < costcurrent: 
                costcurrent = costnew
            else:
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
    dataframe = pd.DataFrame({' ': file_name, 'result': result,'time':times})
    dataframe.to_csv("result.csv",index=False,sep=',')
```

### 运算结果
file|result|time
:--|:--|:--
p1|9678.0|2.75600004196167
p2|7990.0|2.744999885559082
p3|9603.0|2.640000104904175
p4|11591.0|2.743000030517578
p5|9605.0|3.25600004196167
p6|8138.0|2.810999870300293
p7|10329.0|2.6430001258850098
p8|12329.0|2.49399995803833
p9|9148.0|2.372000217437744
p10|7704.0|2.4840002059936523
p11|9504.0|2.305000066757202
p12|11455.0|2.312000036239624
p13|8452.0|4.171000003814697
p14|7560.0|4.086000204086304
p15|10662.0|4.01200008392334
p16|11602.0|4.312000036239624
p17|9014.0|4.2099997997283936
p18|8003.0|5.271000146865845
p19|9775.0|5.880000114440918
p20|11640.0|5.6559998989105225
p21|8349.0|7.17300009727478
p22|7831.0|6.1540000438690186
p23|9877.0|7.026000022888184
p24|12410.0|6.108999967575073
p25|14339.0|20.210000038146973
p26|13302.0|19.980000019073486
p27|15251.0|18.19099998474121
p28|19461.0|23.40000009536743
p29|15079.0|19.846999883651733
p30|13307.0|20.64199995994568
p31|16281.0|20.246000051498413
p32|17362.0|19.317000150680542
p33|13992.0|20.42799997329712
p34|13222.0|19.358999967575073
p35|15299.0|21.421000003814697
p36|17986.0|18.194000005722046
p37|13301.0|18.980000019073486
p38|12688.0|20.819000005722046
p39|15036.0|21.80900001525879
p40|18436.0|20.05400013923645
p41|7366.0|6.083000183105469
p42|7391.0|8.682999849319458
p43|6614.0|11.13700008392334
p44|7577.0|6.707000017166138
p45|7425.0|10.75600004196167
p46|6829.0|13.08899998664856
p47|7678.0|6.708999872207642
p48|6772.0|9.803999900817871
p49|6676.0|13.911999940872192
p50|9516.0|7.547000169754028
p51|8883.0|11.312000036239624
p52|9972.0|6.828999996185303
p53|10456.0|11.537000179290771
p54|11990.0|5.876000165939331
p55|9105.0|11.332000017166138
p56|23882.0|29.610000133514404
p57|32882.0|27.73200011253357
p58|53882.0|26.651000022888184
p59|32983.0|30.92199993133545
p60|23882.0|29.806999921798706
p61|32882.0|27.8989999294281
p62|53736.0|28.141000032424927
p63|29141.0|32.33500003814697
p64|23882.0|29.52300000190735
p65|32882.0|30.270999908447266
p66|53882.0|28.205999851226807
p67|29236.0|29.211999893188477
p68|23882.0|30.06599998474121
p69|32882.0|26.61400008201599
p70|53882.0|29.68400001525879
p71|31321.0|29.894999980926514

每一个测例的具体结果
https://gostbop.github.io/CFLP/
