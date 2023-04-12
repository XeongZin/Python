# -*- coding: utf-8 -*-
"""DCC_ALOHA_Family_Assign_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iT4Y3dugQKETYeBkX0gC9SyzdxF2d5Go
"""

from numpy import random as rand
import numpy as np #숫차 연산을 도와주는 패키지
import matplotlib.pyplot as plt #내용물 시각화
from copy import copy, deepcopy
from matplotlib.pyplot import figure

reps = 100; #reps : repetitions
max_gen_rate = 4 #lambda의 최댓값
intv_gen_rate = 0.05 #자르는 단위
nintv = int(max_gen_rate/intv_gen_rate) +1 #max 값을 0.5로 나누었을때 나오는 구간의 수
gen_rate = np.linspace(0, max_gen_rate, nintv) #lambda
T_max = 3600; #Simulation TIme

S_ideal = deepcopy(gen_rate); #Throughput of ideal MAC
S_ideal[S_ideal > 1] = 1; #Access Elements with Logical Index
print([min(gen_rate), max(gen_rate)])
print([min(S_ideal), max(S_ideal)])

figure(figsize=(24,6), dpi = 80) #그래프의 크기 지정(개인 취향)

plt.plot(gen_rate, S_ideal, ':k', linewidth = 3) #x좌표와 y좌표에 배열의 크기가 같아야 출력 가능
plt.xlabel(r'Normalized Generation Rate $\lambda$'); #x축
plt.ylabel("Normalized Throughput"); #y축
plt.title("Throughput of Ideal Medium Access Control Protocol"); #제목
plt.legend(['ideal Medium Access Control']) #범례
plt.grid('on');
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.minorticks_on()
plt.axis([0, 4, 0, 1.003]) #표현하고 싶은 그래프의 범위

'''Pure ALOHA 시뮬레이션'''
reps = 2
S_pure = np.zeros((nintv, reps)); #행렬(이차원 배열), 행 : lambda, 열 : 시행의 차수
len_pkt = 1
i = 0
for gr in gen_rate:
  print(gr)
  j=0
  for  r in range(reps):
    npkt = int(T_max *gr);                      #Pure ALOHA
    tpkt_s = np.sort(rand.random(npkt) * T_max) #다른 프로토콜 구현 시
    tpkt_e = tpkt_s+len_pkt                     #패킷 전송의 시작 시간이 변경 되어야함
    
    p_collided = np.zeros(npkt);
    for k in range(npkt - 1):
      if(tpkt_s[k+1] > T_max) : break
      if tpkt_e[k] > tpkt_s[k+1]: #Overlapped
        p_collided[k] = 1;
        p_collided[k+1] = 1;

    per = 0 if npkt == 0 else sum(p_collided) / npkt;
    pdr = 1 - per

    S_pure[i][j] = gr * pdr;
    j = j + 1;
  i = i + 1;

#print(S_pure)

'''Slotted ALOHA 시뮬레이션'''
reps = 2
S_slotted = np.zeros((nintv, reps)); #행렬(이차원 배열), 행 : lambda, 열 : 시행의 차수
len_pkt = 1
i = 0
for gr in gen_rate:
  print(gr)
  j=0
  for  r in range(reps):
    npkt = int(T_max *gr);
    tpkt_s = (((np.sort(rand.random(npkt) * T_max))//len_pkt)+1)*len_pkt #패킷의 길이만큼 나눈 후 몫에 1을 더한 후 패킷의 길이만큼 곱한다
    tpkt_e = tpkt_s+len_pkt                     
    
    p_collided = np.zeros(npkt);
    for k in range(npkt - 1):
      if(tpkt_s[k+1] > T_max) : break
      if tpkt_e[k] > tpkt_s[k+1]: #Overlapped
        p_collided[k] = 1;
        p_collided[k+1] = 1;

    per = 0 if npkt == 0 else sum(p_collided) / npkt;
    pdr = 1 - per

    S_slotted[i][j] = gr * pdr;
    j = j + 1;
  i = i + 1;
  
#print(S_slotted)

'''CSMA 1-persistent 시뮬레이션'''
reps = 2
S_1_persistent = np.zeros((nintv, reps)); #행렬(이차원 배열), 행 : lambda, 열: 시행의 차수
len_pkt = 1
i = 0
max_per_y = 0
for gr in gen_rate:
  print(gr)
  j=0
  idx = []
  for  r in range(reps):
    npkt = int(T_max *gr);
    tpkt_s = np.sort(rand.random(npkt) * T_max) #다른 프로토콜 구현 시
    tpkt_e = tpkt_s+len_pkt                     #패킷 전송의 시작 시간이 변경 되어야함
    k=0
    e_count=0
    if npkt > 0:
      while True :
        if(k>=npkt-1) :
          break
        idx = np.logical_and(tpkt_s > tpkt_s[k], tpkt_s < tpkt_e[k])

        tpkt_s[idx] = tpkt_e[k]
        tpkt_e[idx] = tpkt_e[k] + len_pkt
        
        idx1 = tpkt_s == tpkt_e[k]

        over = sum(idx1)

        if over > 1 :
          k=k+over
          e_count=e_count+over
        else :
          k=k+1

        if tpkt_s[k] > T_max :
            break
    per = 0 if npkt == 0 else e_count / npkt; #패킷 오류율
    pdr = 1 - per
    S_1_persistent[i][j] = gr * pdr;
    j = j + 1;
  print("평균 처리율 : ",np.mean(S_1_persistent[i]))
  if max_per_y < np.mean(S_1_persistent[i]) :
    max_per_y = np.mean(S_1_persistent[i])
    max_per_x = gr
  print("--------------------------------------------------------------------")
  i = i + 1;

print(S_1_persistent)

'''CSMA Non-persistent 시뮬레이션'''
reps = 1
S_n_persistent = np.zeros((nintv, reps)); #행렬(이차원 배열), 행 : lambda, 열: 시행의 차수
len_pkt = 1
i = 0
tpkt_n_s = 0
for gr in gen_rate:
  print(gr)
  j=0
  idx = []
  for  r in range(reps):
    npkt = int(T_max *gr);
    tpkt_s = np.sort(rand.random(npkt) * T_max) #다른 프로토콜 구현 시
    tpkt_e = tpkt_s+len_pkt                     #패킷 전송의 시작 시간이 변경 되어야함
    e_count=0
    k=0
    sp=0
    if npkt > 0 :
      while True :
        if(tpkt_e[0] >= T_max or tpkt_s[0] >= T_max) :
          break;

        idx = np.logical_and(tpkt_s > tpkt_s[0], tpkt_s < tpkt_e[0]) #busy 상태일때 전송을 시도한 패킷의 갯수

        for s in range(1, len(idx)) :
          if(idx[s] == True) :
            sp = tpkt_s[s]
            tpkt_s[s] = sp + (1.5 * rand.randint(1, 2000))
            tpkt_e[s] = tpkt_s[s] + len_pkt

        tpkt_s = np.sort(tpkt_s) #랜덤 값이 다를것이므로 
        tpkt_e = np.sort(tpkt_e) #배열 재정렬

        tpkt_s = np.delete(tpkt_s, 0) #패킷의 시작점과 끝점의 첫번째 값 제거
        tpkt_e = np.delete(tpkt_e, 0)
        
        if(len(tpkt_s) <= 0) : 
          break;

        idx = tpkt_s[0] == tpkt_s #정렬된 배열에 있는 값중 첫번째 값과 동일한 값 idx에 저장

        over = sum(idx)

        if over > 1 : #idx의 합이 1초과라면 시작 지점이 같은 충돌이 있으므로 제거 및 충돌이라 가정
          e_count=e_count+over #충돌 갯수 저장
          k=k+over #총실행된 패킷의 갯수 확인을 위해 저장
          for z in range(0, over-1) :
            tpkt_s = np.delete(tpkt_s, 0) #겹치는 갯수만큼 제거
            tpkt_e = np.delete(tpkt_e, 0)
        else :
          k=k+1

        if(len(tpkt_s) <= 0) : 
          break;
        
    e_count = e_count + (npkt-k)
    per = 0 if npkt == 0 else e_count / npkt; #패킷 오류율
    pdr = 1 - per
    S_n_persistent[i][j] = gr * pdr;
    j = j + 1;
    print("평균 처리율 : ",np.mean(S_n_persistent[i]))
  print("--------------------------------------------------------------------")
  i = i + 1;
print(S_n_persistent)

'''CSMA 0.5-persistent 시뮬레이션'''
reps = 1
S_half_persistent = np.zeros((nintv, reps)); #행렬(이차원 배열), 행 : lambda, 열: 시행의 차수
len_pkt = 1
i = 0
tpkt_n_s = 0
timeslot = 0.25
for gr in gen_rate:
  print(gr)
  j=0
  idx = []
  for  r in range(reps):
    npkt = int(T_max *gr);
    tpkt_s = np.sort(rand.random(npkt) * T_max) #다른 프로토콜 구현 시
    tpkt_e = tpkt_s+len_pkt                     #패킷 전송의 시작 시간이 변경 되어야함
    e_count=0
    k=0
    a = 0
    if npkt > 0 :
      while True :
        if(tpkt_e[0] >= T_max or tpkt_s[0] >= T_max) :
          break;

        idx = np.logical_and(tpkt_s > tpkt_s[0], tpkt_s < tpkt_e[0]) #busy 상태일때 전송을 시도한 패킷의 갯수
        
        tpkt_s[idx] = tpkt_e[0]
        tpkt_e[idx] = tpkt_e[0] + len_pkt

        idx = tpkt_s == tpkt_e[0]

        for s in range(1, len(idx)) :
          if(idx[s] == True) :
            while True :
              a = rand.randint(1, 11)
              if(a < 6) :
                break
              else :
                tpkt_s[s] = tpkt_s[s] + timeslot
                tpkt_e[s] = tpkt_s[s] + len_pkt

        tpkt_s = np.sort(tpkt_s) #랜덤 값이 다를것이므로 
        tpkt_e = np.sort(tpkt_e) #배열 재정렬

        tpkt_s = np.delete(tpkt_s, 0) #패킷의 시작점과 끝점의 첫번째 값 제거
        tpkt_e = np.delete(tpkt_e, 0)
        
        if(len(tpkt_s) <= 0) : 
          break;

        idx = tpkt_s[0] == tpkt_s #정렬된 배열에 있는 값중 첫번째 값과 동일한 값 idx에 저장

        over = sum(idx)

        if over > 1 : #idx의 합이 1초과라면 시작 지점이 같은 충돌이 있으므로 제거 및 충돌이라 가정
          e_count=e_count+over #충돌 갯수 저장
          k=k+over #총실행된 패킷의 갯수 확인을 위해 저장
          for z in range(0, over-1) :
            tpkt_s = np.delete(tpkt_s, 0) #겹치는 갯수만큼 제거
            tpkt_e = np.delete(tpkt_e, 0)
        else :
          k=k+1

        if(len(tpkt_s) <= 0) : 
          break;
        
    e_count = e_count + (npkt-k)
    per = 0 if npkt == 0 else e_count / npkt; #패킷 오류율
    pdr = 1 - per
    S_half_persistent[i][j] = gr * pdr;
    j = j + 1;
    print("평균 처리율 : ",np.mean(S_half_persistent[i]))
  print("--------------------------------------------------------------------")
  i = i + 1;
print(S_half_persistent)

'''CSMA 0.1-persistent 시뮬레이션'''
reps = 1
S_tenp_persistent = np.zeros((nintv, reps)); #행렬(이차원 배열), 행 : lambda, 열: 시행의 차수
len_pkt = 1
i = 0
tpkt_n_s = 0
timeslot = 0.25
for gr in gen_rate:
  print(gr)
  j=0
  idx = []
  for  r in range(reps):
    npkt = int(T_max *gr);
    tpkt_s = np.sort(rand.random(npkt) * T_max) #다른 프로토콜 구현 시
    tpkt_e = tpkt_s+len_pkt                     #패킷 전송의 시작 시간이 변경 되어야함
    e_count=0
    k=0
    a = 0
    if npkt > 0 :
      while True :
        if(tpkt_e[0] >= T_max or tpkt_s[0] >= T_max) :
          break;

        idx = np.logical_and(tpkt_s > tpkt_s[0], tpkt_s < tpkt_e[0]) #busy 상태일때 전송을 시도한 패킷의 갯수
        
        tpkt_s[idx] = tpkt_e[0]
        tpkt_e[idx] = tpkt_e[0] + len_pkt

        idx = tpkt_s == tpkt_e[0]

        for s in range(1, len(idx)) :
          if(idx[s] == True) :
            while True :
              a = rand.randint(1, 11)
              if(a < 2) :
                break
              else :
                tpkt_s[s] = tpkt_s[s] + timeslot
                tpkt_e[s] = tpkt_s[s] + len_pkt

        tpkt_s = np.sort(tpkt_s) #랜덤 값이 다를것이므로 
        tpkt_e = np.sort(tpkt_e) #배열 재정렬

        tpkt_s = np.delete(tpkt_s, 0) #패킷의 시작점과 끝점의 첫번째 값 제거
        tpkt_e = np.delete(tpkt_e, 0)
        
        if(len(tpkt_s) <= 0) : 
          break;

        idx = tpkt_s[0] == tpkt_s #정렬된 배열에 있는 값중 첫번째 값과 동일한 값 idx에 저장

        over = sum(idx)

        if over > 1 : #idx의 합이 1초과라면 시작 지점이 같은 충돌이 있으므로 제거 및 충돌이라 가정
          e_count=e_count+over #충돌 갯수 저장
          k=k+over #총실행된 패킷의 갯수 확인을 위해 저장
          for z in range(0, over-1) :
            tpkt_s = np.delete(tpkt_s, 0) #겹치는 갯수만큼 제거
            tpkt_e = np.delete(tpkt_e, 0)
        else :
          k=k+1

        if(len(tpkt_s) <= 0) : 
          break;
        
    e_count = e_count + (npkt-k)
    per = 0 if npkt == 0 else e_count / npkt; #패킷 오류율
    pdr = 1 - per
    S_tenp_persistent[i][j] = gr * pdr;
    j = j + 1;
    print("평균 처리율 : ",np.mean(S_tenp_persistent[i]))
  print("--------------------------------------------------------------------")
  i = i + 1;
print(S_tenp_persistent)

'''그래프 출력'''
import math

print(nintv)
print(reps)
#print(np.mean(S_pure, axis =1))

figure(figsize = (24,6), dpi = 80)

plt.plot(gen_rate, S_ideal, ':k', linewidth=3)
#Pure ALOHA 표시
plt.plot(gen_rate, np.mean(S_pure, axis=1), 'b', linewidth=1.5)
markerlines, _, _ = plt.stem([1/2], [1/2/math.e], markerfmt='*r', linefmt = '--k', use_line_collection=True)
#markerlines.set_markersize(15)

#slotted ALOHA 표시
plt.plot(gen_rate, np.mean(S_slotted, axis=1), 'r', linewidth=1.5)
markerlines, _, _ = plt.stem([1], [1/math.e], markerfmt='*r', linefmt='--k', use_line_collection=True)
#markerlines.set_markersize(15)

#CSMA 1-persistant 표시
plt.plot(gen_rate, np.mean(S_1_persistent, axis=1), 'm', linewidth=1.5)
#markerlines, _, _ = plt.stem([max_per_x], [max_per_y], markerfmt='*r', linefmt='--k', use_line_collection=True)
#markerlines.set_markersize(15)

#CSMA non-persistant 표시
plt.plot(gen_rate, np.mean(S_n_persistent, axis=1), 'y', linewidth=1.5)

#CSMA 0.5-persistant 표시
plt.plot(gen_rate, np.mean(S_half_persistent, axis=1), 'k', linewidth=1.5)

#CSMA 0.1-persistant 표시
plt.plot(gen_rate, np.mean(S_tenp_persistent, axis=1), 'g', linewidth=1.5)



plt.xlabel(r'Normalized Generation Rate $\lambda$');
plt.ylabel("Normalized Throughput");
plt.title("Throughput of Medium Access Protocols");
plt.legend(['Ideal Medium Access Control', 'Pure ALOHA', 'Slotted ALOHA', 'CSMA 1-persistant', 'CSMA non-persistant', 'CSMA 0.5-persistent', 'CSMA 0.1-persistent'])
plt.grid('on');
plt.grid(b=True, which='minor', color='#999999', linestyle='-', alpha=0.2)
plt.minorticks_on()

plt.axis([0, 4, 0, 1.003])

