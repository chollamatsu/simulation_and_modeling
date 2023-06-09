# -*- coding: utf-8 -*-
"""HW04_591.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Ah8HYVDh1wOIwA8O88p42YciNYDsHf6V
"""

จาก Activity Flow ที่กำหนดให้  เขียนโปรแกรมจำลองระบบการทำงานในช่วงเวลา 8 ชั่วโมง (480 time units)

จากนั้นทำการคำนวณค่าเฉลี่ยของการรอคิวเพื่อเข้าแต่ละ Activity (3 Activities:- Registration, GP Consultation, and Book Test)

การตั้งชื่อไฟล์เป็นดังนี้ HW04_6XXXXXXXX.ipynb  ซึ่ง 6XXXXXXXX คือรหัสนักศึกษา

#people arriving at GP surgrey(generator mean: every 3 miniutes) -queue-> Registration(receptioninst mean: 2 mins) -queue-> 
#GP Consultation(GP mean: 8 mins) -(1)-> 75% sink, -(2)Queue-> 25% Book Test (receptionist mean: 4 mins)
#there is 1 receptionist and 2 GPs.

!pip install simpy

import simpy
import random
from statistics import mean 
#this allows us to take a mean of a list easily

"""SimPy in Queuing simulation and store results in list"""

#arrivals generator function
def customer_generator(env, wl_inter, mean_consult, receptionist):
  while True:
    #create instance of activity generator
    wp = activity_generator(env, mean_consult, receptionist)
    
    #run the activity generator for customer p_id
    env.process(wp)

    #sample time until next customer == เวลาออก?
    t = random.expovariate(1.0 / wl_inter)

    #Freeze until that time has passed
    yield env.timeout(t)

#arrivals generator function
def customer_booking_generator(env, wl_inter, mean_consult, receptionist):
  while True:
    #create instance of activity generator
    wp = booking_generator(env, mean_consult, receptionist)

    #run the activity generator for customer p_id
    env.process(wp)

    #sample time until next customer == เวลาออก
    t = random.expovariate(1.0 / wl_inter)

    #Freeze until that time has passed
    yield env.timeout(t)

def activity_generator(env, mean_consult, receptionist):
  global list_of_queue_times_receptionist
  #list for storing results, declare to be global

  time_enqueue_of_receptionist = env.now
  
  #request a receptionist
  with receptionist.request() as req:
    #Freeze until the request can be met
    yield req

    time_dequeue_of_receptionist = env.now
    #time ออก - time เข้า = เวลาที่ใช้ตอนเข้าปรึกษา
    time_in_queue_for_receptionist = (time_dequeue_of_receptionist -
                               time_enqueue_of_receptionist)
    
    list_of_queue_times_receptionist.append(time_in_queue_for_receptionist)
    #กลุ่ม ตย. เข้ามาแบบexpo ==เวลาเข้า
    sampled_consult_time = random.expovariate(1.0/mean_consult)
    print("sample consult time=",sampled_consult_time)

    #Freeze until that time has passed
    yield env.timeout(sampled_consult_time)

def booking_generator(env, mean_consult, receptionist):
  global list_of_queue_times_booking
  global list_of_queue_times_receptionist
  #list for storing results, declare to be global
  booking = random.uniform(0,1)
  if booking < 0.25:
    time_enqueue_of_booking = env.now
  
  #request a booking
    with receptionist.request() as req:
    #Freeze until the request can be met
      yield req

      time_dequeue_of_booking = env.now
    #time ออก - time เข้า = เวลาที่ใช้ตอนเข้าปรึกษา
      time_in_queue_for_booking = (time_dequeue_of_booking -
                               time_enqueue_of_booking)
    
      list_of_queue_times_booking.append(time_in_queue_for_booking)
    #กลุ่ม ตย. เข้ามาแบบexpo ==เวลาเข้า??
      sampled_consult_time = random.expovariate(1.0/mean_consult)
      print("booking time=",sampled_consult_time)

    #Freeze until that time has passed
      yield env.timeout(sampled_consult_time)

#Set up simulation environment
env = simpy.Environment()
#Set up resources
receptionist = simpy.Resource(env, capacity=1)
#Set up parameter values
wl_inter = 3 #arrival time
#wl_inter = 5
mean_consult = 8
#mean_consult = 6

#Set up a list to store queuing time 
list_of_queue_times_receptionist = []
list_of_queue_times_booking = []
#Start the arrivals generator
env.process(customer_generator(env, wl_inter, mean_consult, receptionist))
mean_consult = 4
env.process(customer_booking_generator(env, wl_inter, mean_consult, receptionist))
#Run the simulation
env.run(until=480)
#env.run(until=120)

#Calculate and print mean_queuing time for the receptionist
mean_queue_time_receptionist = mean(list_of_queue_times_booking)
print("Mean queuing time of receptionist (mins) : ", mean_queue_time_receptionist," length=",len(list_of_queue_times_booking))
