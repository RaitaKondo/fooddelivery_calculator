#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import os
import re
import matplotlib.pyplot as plt


# ## how to make a all_data.csv from bunch of csv files

# In[201]:



files = [file for file in os.listdir('./Documents/foodpanda')]

all_months_data = pd.DataFrame()

for file in files:
    df = pd.read_csv("./Documents/foodpanda/"+file)
    all_months_data = pd.concat([all_months_data, df])
    
all_months_data.to_csv("all_data.csv", index=False)


# In[3]:


all_data = pd.read_csv("all_data.csv")
all_data.head()


# ### clean up the data

# # extract data only which has certan column

# In[5]:


all_data = all_data[all_data['受け付け時刻：'].notna()]
all_data.head()


# Drop rows of NAN

# In[ ]:


# nan_df = all_data[all_data.isna().any(axis=1)]
# nan_df.head()

# all_data = all_data.dropna(how='all')
# all_data.head()


# # Add month column

# In[6]:


all_data['Month'] = all_data['受け付け時刻：'].str[5:7]
all_data['Month'] = all_data['Month'].astype('int32')
all_data.head()


# # Making a sales plot based on month column

# In[7]:


results = all_data.groupby('Month').sum()


# In[8]:


import matplotlib.pyplot as plt

months = range(4,10)

plt.bar(months, results['料理の価値'])
plt.xticks(months)
plt.ylabel('Foodpanda Sales in THB')
plt.xlabel('Month number')
plt.show()


# # change string date column into date type date column 

# In[9]:


all_data['受け付け時刻：'] = pd.to_datetime(all_data['受け付け時刻：'])


# In[10]:


all_data['Hour'] = all_data['受け付け時刻：'].dt.hour
all_data['Minute'] = all_data['受け付け時刻：'].dt.minute
all_data.head()


# # making sales number plot based on hours

# In[11]:


hours = [hour for hour, df in all_data.groupby('Hour')]

plt.plot(hours, all_data.groupby(['Hour']).count())
plt.xticks(hours)
plt.xlabel('Hour')
plt.ylabel('number of orders')
plt.grid()
plt.show()


# # unconvinient foodpanda form into usable parts

# In[45]:


import re

input_string = """1 Sausage, Cheese & Egg [1 Half, 1 Sliced english bread], 1 Home Roast Pork & Stuffing [1 Half, 1 Sliced english bread], 1 Bacon, Cheese & Egg [1 Half, 1 Sliced english bread]"""


### split by comma but avoiding certan menu name which includes comma in their name

def mysplit(s):
     parts = []
     bracket_level = 0
     irregular_parts = []
     current = []
     pattern = re.compile(r' ?(Sausage & Egg|Cheese & Egg|Bacon & Onions|from:|at:)')
     # trick to remove special-case of trailing chars
     for c in (s + ","):
         if c == "," and bracket_level == 0:
             validation = "".join(current)
             if re.match(pattern, validation):
                parts[-1] += validation
                current = []
             else:
                parts.append(validation)
                current = []
         else:
             if c == "[":
                 bracket_level += 1
             elif c == "]":
                 bracket_level -= 1
             current.append(c)

     return parts


### take return from mysplit function and make key value pair of order number and menu

def perfect_split(s):
    y = mysplit(s)
    pattern = re.compile(r'([0-9]+)([\D0-9]+)')
    x ={}
    for i in y:
        for (number, letter) in re.findall(pattern, i):
            letter = letter.strip().replace('"', '')
            number = number.strip()
            x[letter] = number
    return x



### makeing key into int from str and append into a list

all_data['yeah'] = all_data['商品'].apply(lambda x: perfect_split(x))
l2 =[]
for i in all_data['yeah']:
    l1 = list(i.items())
    for j in l1:
        jx = list(j)
        jx[1] = int(jx[1])
        l2.append(jx)


# In[15]:



import re


def l_cleaner(lis_x):
    pattern1 = re.compile(r"(.+?(?=\[))")  
    pattern2 = re.compile(r"\[(.*?)\]")
    l3 = []
    for i in lis_x:
        g = i[0]
        o = re.findall(pattern1, g)
        t = re.findall(pattern2, g)
        if t:
            for s in t:
                device = [item.strip() for item in s.split(",")]
                device.sort()
                device = ','.join(device)
                device= '[' + device + ']'
            o[-1] += device
            o.append(i[1])
            l3.append(o)
        else:
            l3.append(i)
    return l3
       
b = l_cleaner(l2)
totals = {}
for key, value in b:
    totals[key] = totals.get(key, 0) + value
    

    
## makeing order by number of orders

marklist = sorted(totals.items(), key=lambda x:x[1])
sortdict = marklist[::-1]
sortdict


# In[36]:


pattern = re.compile(r"(.+?(?=\[))") 

for k, v in sortdict:
    g = k.replace(' ', '_').replace(',', '_').replace('&', '_').replace('-', '_').replace('/', '_').replace("'", '_').replace('"', '_').replace('[', '_').replace(']', '_').replace(':', '_').replace('.', '_').replace('(', '_').replace(')', '_').replace('!', '_')
    g = g.lower()
    g = "_" + g
    print(g)


# In[44]:




for k, v in sortdict:
    ak = re.sub("[\W]", '_', k)
    ak = ak.lower()
    ak= "_" + ak
    print(ak)


# In[89]:


# import csv
# lf = [('The Full Monty Breakfast', 168),
#  ('Classic Bangers And Mash', 77),
#  ('Extra Gravy', 71),
#  ('Extra Yorkshire Puddinds', 70),
#  ('Classic English Style Fish and Chips', 63),
#  ('Extra Beans', 62)]
# with open('cleaned_list_demo.txt', 'w') as f:
#     f.write(str(lf))


# # making plot by the data previously made

# In[75]:


x, y = zip(*sortdict[0:100]) # unpack a list of pairs into two tuples

plt.bar(x, y)
plt.xticks(rotation=90)
plt.xlabel('menu')
plt.ylabel('number of menu')
plt.grid()
plt.show()


# In[76]:


k = 0
v = 20

for i in range(1, 8):
    x, y = zip(*sortdict[k:v]) # unpack a list of pairs into two tuples

    plt.bar(x, y)
    plt.xticks(rotation=90)
    plt.xlabel('menu')
    plt.ylabel('number of menu')
    plt.grid()
    plt.show()
    k = v
    v += 20


# In[ ]:




