import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from dm_function import sorted_profit 
from dm_function import predicted_sales
import pickle
inv_mon_name = pickle.load(open("inv_mon_name.p", "rb"))
inv_monsoldper_name = pickle.load(open("inv_monsoldper_name.p", "rb"))
l = pickle.load(open("l.p", "rb"))
lis_inv = pickle.load(open("lis_inv.p", "rb"))
lis_inv_sold_per = pickle.load(open("lis_inv_sold_per.p", "rb"))
data= pickle.load(open("4yrsBMW.p", "rb"))
firstyear= pickle.load(open("firstyear.p", "rb"))
secondyear= pickle.load(open("secondyear.p", "rb"))
thirdyear= pickle.load(open("thirdyear.p", "rb"))
fourthyear= pickle.load(open("fourthyear.p", "rb"))
thirdfourth= pickle.load(open("thirdfourth.p", "rb"))
twothree4= pickle.load(open("twothree4.p", "rb"))
twothree= pickle.load(open("twothree.p", "rb"))
onetwo= pickle.load(open("onetwo.p", "rb"))
onetwo3=pickle.load(open("onetwo3.p", "rb"))
lastdata1=pickle.load(open("last3mnthsBMW.p", "rb"))

# loading dataset
#dataset = pd.read_excel("store-dataset1.xlsx")

# sorting from lowest to highest date
#dataset1 = dataset.sort_values('Order Date')

# resetting index
#dataset1 = dataset1.reset_index(drop=True)


# selecting desired sales data for a given period of time
x=int(input("Enter year"))
y=int(input("Enter month "))
dataset1 = pd.DataFrame()
m=[1,2,3]
if(x==2017 and y in m):
    dataset1= thirdfourth
elif(x==2017 and y not in m):
    dataset1=fourthyear  
elif(x==2016 and y in m):
    dataset1=twothree    
elif(x==2016 and  y not in m):
    dataset1= thirdyear
elif(x==2015 and y in m):
    dataset1=onetwo
elif(x==2015 and  y not in m):
    dataset1=secondyear

else:
    dataset1=firstyear    
            
dataset1 = dataset1.reset_index(drop=True)
a = pd.DatetimeIndex(dataset1['Order Date']).year ==  x
b = pd.DatetimeIndex(dataset1['Order Date']).month ==  y

dataset2 = pd.DataFrame()
for i in range(len(dataset1)):
    if(a[i]== True and b[i]==True):
    
        dataset2 = dataset2.append(dataset1.iloc[i,:])    
        
dataset2 = dataset2.reset_index(drop=True)

# setting inventory size    
l = list(dataset2['Product Name'].unique())
inv_dict = {}
inv_dict = lis_inv[inv_mon_name[((x - 2014)*12 + y)-1]]

# =============================================================================
# for i in l:
#     inv_dict[i] = 500
# =============================================================================

# sold, remaining % sold, adding inventory
sold_percent = {} 
if(x==2017):
    if(y==12):
        data1=lastdata1
else:        
    data1= sorted_profit(x,y)
#full dat is dataset1
m = list(dataset1['Product Name'].unique())
#Pricing
import operator
new_l=[]
dic ={}
for i in range(len(m)):
    dic[m[i]]=0
    
for i in range(0,len(m)):
    new_l=[]
    new_l = predicted_sales(x, y, m[i] )
    #new_l= np.array(new_l).reshape(1, -1)
    h=np.array(range(0,len(new_l)))
    
    new_l= np.array(new_l).reshape(-1,1)
    h= np.array(h).reshape(-1,1)
    
    #X_train, x_test,Y_train, y_test = train_test_split(new_l, h, test_size= .3, random_state=3)
    reg =LinearRegression()
    reg.fit(h,new_l)
    y_predict= int(abs(reg.predict(len(h))))
    dic[m[i]]= y_predict
    dic1=sorted(dic.items(),key=lambda x:x[1])


for i in range(len(dataset2)):
    # percentage of sales for each product
    sold_percent[dataset2['Product Name'][i]] = (((((inv_dict[dataset2['Product Name'][i]])-(inv_dict[dataset2['Product Name'][i]]-int(dataset2['Quantity'][i])))/inv_dict[dataset2['Product Name'][i]])*100),dataset2['Quantity'][i])
    # updating inventory
    #temp = inv_dict[dataset2['Product Name'][i]]
    temp= int(dataset2['Quantity'][i])
    inv_dict[dataset2['Product Name'][i]] -= int(dataset2['Quantity'][i])
    # updating inventory for next month/quarter/year
    if(sold_percent[dataset2['Product Name'][i]][1] >= 5.0):
        
        
        
            
        #dfb = data[data['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]  
                
        
        #for j in dataset2['Product Name']:

        try:
            
            count=0     
            dfb = data[data1['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]   
        except:
            
            count =1
            pass 

        if(count==1):
            dfb = data[data['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]
            
           
                
                
            if(dfb < 0.2*(len(data))):
                
                
                print('HB')
                inv_dict[dataset2['Product Name'][i]] += (80*temp)//100
            
            if(dfb >= 0.2*(len(data))):
                
                print('HMW')
                inv_dict[dataset2['Product Name'][i]] += (50*temp)//100
        else:
            if(dfb < 0.2*(len(data1))):
                
                
                print('HB1')
                inv_dict[dataset2['Product Name'][i]] += (80*temp)//100
            
            if(dfb >= 0.2*(len(data1))):
                
                print('HMW1')
                inv_dict[dataset2['Product Name'][i]] += (50*temp)//100
        
        
    if(sold_percent[dataset2['Product Name'][i]][1] <= 5.0 and sold_percent[dataset2['Product Name'][i]][1] >= 3.0  ):
        
         
        #for j in dataset2['Product Name']:
        #dfb = data[data['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]   
        
        try:
            
            count=0     
            dfb = data[data1['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]   
        except:
            
            count =1
            pass 
        if(count==1):
            dfb = data[data['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]

        
            if(dfb < 0.2*(len(data))):
                
                
                   
                
                print('MB')
                inv_dict[dataset2['Product Name'][i]] += (80*temp)//100
            
            if(dfb > 0.2*(len(data)and dfb < 0.8*(len(data)))):
                
                print('MM')
                inv_dict[dataset2['Product Name'][i]] += (50*temp)//100   
            
            if(dfb >= 0.8*(len(data))):
                
                print('MW')
                inv_dict[dataset2['Product Name'][i]] += (20*temp)//100

        else:
            if(dfb < 0.2*(len(data1))):
                
                
                   
                
                print('MB1')
                inv_dict[dataset2['Product Name'][i]] += (80*temp)//100
            
            if(dfb > 0.2*(len(data1)and dfb < 0.8*(len(data1)))):
                
                print('MM1')
                inv_dict[dataset2['Product Name'][i]] += (50*temp)//100   
            
            if(dfb >= 0.8*(len(data1))):
                
                print('MW1')
                inv_dict[dataset2['Product Name'][i]] += (20*temp)//100
            
            
    if(sold_percent[dataset2['Product Name'][i]][1] <= 3.0  ):
        
        #for j in dataset2['Product Name']:
        #dfb = data[data['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]   
        try:
            count=0     
            dfb = data[data1['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]   
        except:
            count =1
            pass 
        
        if(count==1):
            dfb = data[data['d_product']==dataset2['Product Name'][i]].index.values.astype(int)[0]


        
            if(dfb < 0.2*(len(data))):
                   
                
                print('WB')
                inv_dict[dataset2['Product Name'][i]] += (50*temp)//100
            
            if(dfb > 0.2*(len(data)and dfb < 0.8*(len(data)))):
                   
                   
                
                print('WM')
                inv_dict[dataset2['Product Name'][i]] += (50*temp)//100   
            
            if(dfb >= 0.8*(len(data))):
                   
                
                print('WW')
                inv_dict[dataset2['Product Name'][i]] += (0*temp)//100

        else:
              if(dfb < 0.2*(len(data1))):
                   
                
                print('WB1')
                inv_dict[dataset2['Product Name'][i]] += (50*temp)//100
            
              if(dfb > 0.2*(len(data1)and dfb < 0.8*(len(data1)))):
                   
                   
                
                print('WM1')
                inv_dict[dataset2['Product Name'][i]] += (50*temp)//100    
            
              if(dfb >= 0.8*(len(data1))):
                   
                
                print('WW1')
                inv_dict[dataset2['Product Name'][i]] += (0*temp)//100
                

data2=data1[1523:]
tot1=data2['d_profit'].sum()
data2 = data2.reset_index(drop=True)
for i in range(len(data2)):
    if(data2['d_quantity'][i] >= 30):
        #data2['d_MRP'][i]= data2['d_MRP'][i]+data2['d_MRP'][i]*0.2
        data2['d_MRP'][i]=data2['d_inventory'][i]+data2['d_inventory'][i]*0.1
        data2['d_profit'][i]=(data2['d_MRP'][i]-data2['d_inventory'][i])*data2['d_quantity'][i]
    else:
        data2['d_MRP'][i]=data2['d_inventory'][i]-data2['d_inventory'][i]*0.2
        data2['d_profit'][i]=(data2['d_MRP'][i]-data2['d_inventory'][i])*data2['d_quantity'][i]
        
tot=data2['d_profit'].sum()  
