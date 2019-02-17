# -*- coding: utf-8 -*-
"""
Created on Sat Feb 16 12:52:11 2019

@author: Sarith Fernando
"""

import pandas as pd

# Preprocessing for Existing services: Data 1
dat1 = pd.read_excel('Australia_Service_List_2017.xlsx', sheet_name='Australia', header=None)

# Getting the coloums of subub, postal_code and number of age care centers
# Then group by state and suburb
df1=dat1.iloc[2:, [4,5,8]]
df1=df1.fillna(0)
df1=df1.groupby([df1[4],df1[5]]).sum()

# Reset index and renaming
df1.reset_index(inplace=True)
df1.rename(columns={4: 'State', 5: 'Suburb', 8:'No_of_AGEC'}, inplace=True)

# Preprocessing for piopulation: Data 2
dat2 = pd.read_excel('age_postalcode.xlsx', sheet_name='Data Sheet 0', header=None)
df2=dat2.iloc[10:2660, 1:23]

# Split State and Suburb into two coloums
new = df2[1].str.split(", ", n = 1, expand = True) 
df2[24]=new[0]
df2[25]=new[1]
df2.drop(columns =[1], inplace = True) 

# Reset index and renaming
df2.reset_index(inplace=True)
df2.drop(columns =['index'], inplace = True)
df2.rename(columns={2: '0-4y', 3: '5-9y', 4: '10-14y',5: '15-19y',6: '20-44y',
                    7: '25-29y',8: '30-34y',9: '35-39y',10: '40-44y',11: '45-49y',
                    12: '50-54y',13: '55-59y',14: '60-64y',15: '65-69y',16: '70-74y',
                    17: '75-79y',18: '80-84y',19: '85-89y',20: '90-94y',21: '95-99y',
                    22:'100y over',24:'Suburb',25:'State'}, inplace=True)


# Join two tables together base on common key State and Suburb
result = pd.merge(df1, df2, how='right', on=['State','Suburb'])
result=result.fillna(0)

# Culculate Age Care Centre requirement in 2017 for each suburb in each state
# Requirement = Total population obove 85 - Available Age care centre
req_2017 = result['85-89y']+result['90-94y']+result['95-99y']+result['100y over']-result['No_of_AGEC']
req_2017 = pd.concat([req_2017, result['State'],result['Suburb']], axis=1)
req_2017.rename(columns={0: 'Req'}, inplace=True)

# Finding top 200 suburs which requre age care centres including maximum requirement
top_200=req_2017.nlargest(200,'Req')
# Save findings as a csv
top_200.to_excel('output.xlsx',index=False)