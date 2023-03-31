# -*- coding: utf-8 -*-
"""HW02_1_591.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bBhAvnBxzWBKwY9rgyKtrSPWOeKFDfqj
"""

#สร้างชุดเลขrandom แบบวิธีตัดกลางกำลังสอง
#solution: 
#1.กำหนด x(0) เป็นเลข(จำนวนเต็ม)อะไรก็ได้ --->ก็คือการกำหนดseedนั่นแหละ
#2.เอามายกกำลังสอง
#3.ตัดฝั่งซ้าย2ตัว ฝั่งขวา 2 ตัว แล้วเอาresultที่ได้วนไปทำ2ใหม่
#ข้อเสียของวิธีนี้คือ ถ้ากำหนดseedไม่ได้ ก็จะเกิดcycle เร็ว

def is_four(addzero):
  while (len(addzero) < 4):
    addind = '0'+addzero
    return addzero

def mid_square(ans):
  ans = str(pow(ans,2))
  length = (len(ans)-4)//2
  ans = ans[length:len(ans)-length]
  print("return = ",ans)
  return (ans)

random_number = 3175
random_list = []

for i in range (10):
  k = int(mid_square(random_number))
  print('k: ',k)
  random_number = k
  random_list.append(k/1000)
  print('i: ',i)
  print("random number = ",random_number,"\nrandom set = ",random_list)

print(random_list)