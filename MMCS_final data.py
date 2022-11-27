#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 14 10:31:24 2022

@author: air
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel('old_data/Demand_Data.xlsx')

data1 = pd.DataFrame()

demand = data[['Demand_0','Demand_1','Demand_2','Demand_3']]

demand['sum'] = demand.sum(axis='columns')

new_data=data[demand['sum']!=0]


'''
nei = np.array(new_data['NEIGHBORS'])
nei=list(nei)

list1=[] 
for i in nei:
    list1.append(i.split(','))
    

list2=[]
for i in range(len(list1)):
    for j in range(len(list1[i])):
        list2.append(list1[i][j].replace("[","").replace("]","").replace(" ",""))



for i in range(len(list2)):
    list2[i] = int(list2[i])

index_nei=list(np.unique(list2))
old_index = list(new_data["Ref"])

for i in index_nei:
    old_index.append(i)

final_index = np.unique(old_index)

final_data=data.loc[final_index-1]

'''


geometry=list(new_data['geometry'])


geometry1=[]
for i in range(len(geometry)):
    geometry1.append(geometry[i].split(', '))
    

geometry2=[]
for i in range(len(geometry1)):
    for j in range(len(geometry1[i])):
        geometry2.append(geometry1[i][j].replace("POLYGON ","").replace("(","").replace(")",""))


geometry3=[]
for k in range(len(geometry2)):
        geometry3.append(geometry2[k].split(' '))
        
x=[]   
for i in range(len(geometry3)):
    x.append(float(geometry3[i][0]))

y=[]
for i in range(len(geometry3)):
    y.append(float(geometry3[i][1]))  
    
center_x=[]
for i in range(len(geometry3)//5):
       center_x.append(np.mean(x[i*5:i*5+5]))

center_y=[]
for i in range(len(geometry3)//5):
       center_y.append(np.mean(y[i*5:i*5+5]))


# central area
new_data["x_centre"] = center_x
new_data["y_centre"] = center_y


limit = np.percentile(new_data['Distance from Centre'],30)#2743.2006677604836

central_area=new_data[new_data['Distance from Centre']<= limit]
sub_area=new_data[new_data['Distance from Centre']>limit]


plt.scatter(central_area['x_centre'],central_area['y_centre'])

'''
max(final_data['Distance from Centre'])
min(final_data['Distance from Centre'])
'''

'''
# save final data and central, sub data
new_data.to_csv('MMCS_final/MMCS_DATA/new_data.csv')
central_area.to_csv('MMCS_final/MMCS_DATA/central_demand.csv')           !!!
sub_area.to_csv('MMCS_final/MMCS_DATA/sub_demand.csv')                    !!!!
'''


new_data.shape[0]-central_area.shape[0]#72
central_area.shape#(31, 16)
sub_area.shape#(72, 16)


#conbined potential and current points
points_data = pd.read_csv('MMCS_final/Total_point_final.csv')
points_data.columns

central_points=points_data[points_data['Distance']<= limit]
sub_points=points_data[points_data['Distance']>limit]
central_points.shape[0]#185
sub_points.shape[0]#162

'''
#save central and sub points data
central_points.to_csv('potential_data/central_potential.csv')
sub_points.to_csv('potential_data/sub_potential.csv')

current_data = pd.read_excel('old_data/Charging_points.xlsx')
central_current=current_data[current_data['Ditance']<= limit]
sub_current=current_data[current_data['Ditance']>limit]
central_current.shape[0]#52
sub_current.shape#273

'''
'''
#save central and sub points data
central_points.to_csv('/Users/air/Desktop/MMCS_final/central_points.csv')    
sub_points.to_csv('/Users/air/Desktop/MMCS_final/sub_points.csv')           
'''


#Calculate distance between points and demand points

#for central area
points_coordinates1=central_points[['Longitude','Latitude']]
center_demand =central_area[['x_centre', 'y_centre']]

#for suburb area
points_coordinates2=sub_points[['Longitude','Latitude']]
sub_demand = sub_area[['x_centre', 'y_centre']]


point_coordinates = points_data[['Longitude','Latitude']]
point_coordinates.shape#(325, 2)
demand_coordinates = new_data[['x_centre','y_centre']]
#one potential point to all demand points (169,103)

import math
def Distance(potential,demand):
    Distance = []
    for i in range(np.array(potential).shape[0]):
        for j in range(np.array(demand).shape[0]):
            d = np.array(potential)[i]-np.array(demand)[j]
            Distance.append(math.hypot(d[0],d[1]))
      
    Distance = np.array(Distance).reshape(potential.shape[0],demand.shape[0])*60592.95595
    return Distance

#the distance from one pont to every demand points
Distance_D_and_P=Distance(point_coordinates,demand_coordinates) 

CC_Distance_D_and_P = Distance(points_coordinates1,center_demand) 
pd.DataFrame(CC_Distance_D_and_P).to_csv('/Users/air/Desktop/MMCS_final/CC_Distance_D_and_P.csv')   


SS_Distance_D_and_P = Distance(points_coordinates2,sub_demand) 
pd.DataFrame(SS_Distance_D_and_P).to_csv('/Users/air/Desktop/MMCS_final/SS_Distance_D_and_P.csv')  

#save to csv
pd.DataFrame(Distance_D_and_P).to_csv('/Users/air/Desktop/MMCS_final/Distance_D_and_P.csv')         

#calculate the distance between each potential point
points_coordinates11 = points_data[['Longitude','Latitude']]
Distance_between_points = Distance(point_coordinates,points_coordinates11) 


#save distance between each potential point to csv
pd.DataFrame(Distance_between_points).to_csv('MMCS_final/MMCS_DATA/Distance_between_points.csv')


def demand_index_near_point(Distance,propotion):
    d1 = limit * propotion
    index1 = pd.DataFrame(Distance)<=d1
    index_demand = []
    for i in range(index1.shape[0]):
        index2 = []
        for j in range(index1.shape[1]):
            if index1.iloc[i,j] == True:
                index2.append(j)
        index_demand.append(index2)
    return index_demand

# the index of demand point within central area: index_demand_c
Dc = Distance(points_coordinates1,center_demand) 


index_demand_c = demand_index_near_point(Dc,0.25)
len(index_demand_c)#185

# the index of demand point within central area: index_demand_s
Ds = Distance(points_coordinates2,sub_demand) 
index_demand_s = demand_index_near_point(Ds,0.5)
len(index_demand_s) #162

x = [i for i in range(103)]
demand_coordinates.index = x


def demand_coordinates_near_point(index):
    demandc=[]
    for i in range(len(index)):
        xx = []
        for j in range(len(index[i])):
            index1 = index[i][j]
            xx.append(list(demand_coordinates.iloc[index1,:]))
        demandc.append(xx)
    return demandc

# the coordinates of demand point near the central and suburb potential points 
demandc = demand_coordinates_near_point(index_demand_c)
demands = demand_coordinates_near_point(index_demand_s)

pd.DataFrame(demandc).to_csv('MMCS_final/MMCS_DATA/demandc.csv')
pd.DataFrame(demands).to_csv('MMCS_final/MMCS_DATA/demands.csv')