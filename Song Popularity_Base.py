
# coding: utf-8

# In[13]:


import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import spotipy
# Input data files are available in the "../input/" directory.
# For example, running this (by clicking run or pressing Shift+Enter) will list the files in the input directory

import os
print(os.listdir('Desktop/SongsDataset'))


# In[7]:


import pandas as pd
fileName = 'Desktop/SongsDataset/Billboard_Spotify_Percentile.csv'
df = pd.read_csv(fileName, sep='\t')
df_mo = pd.read_csv('Desktop/SongsDataset/songDetail.csv')


# In[8]:


df_mo['date'], df_mo['month'],df_mo['year'] = df_mo['Entry_Date'].str.split('/').str
df_mo['year'] = df_mo['year'].apply(lambda x: ('19'+x) if int(x)>18 else ('20'+x))
df_mo["year"] = pd.to_numeric(df_mo["year"])
df_mo = df_mo.sort_values(by=['year'], ascending = True)


# In[9]:


df_mo.head()


# In[11]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(8,8))
dfx = df_mo.groupby('year', as_index=False)['Total_Weeks'].mean()
dfx['mov_avg']=dfx['Total_Weeks'].rolling(window=3,center=True,min_periods=1).mean()
dfx.head(40)
x  = dfx['year']
y  = dfx['mov_avg']
plt.plot(x,y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=5)
plt.ylabel('No of Weeks')
plt.xlabel('Year')
plt.title('No. Of Weeks vs Year')
plt.legend()
plt.show()


# In[12]:


df_mo = df_mo.sort_values(by=['year','Peak_Position'], ascending = [True,True])
df_mo.head(10)


# In[ ]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(8,8))
df_tt = df_mo.groupby('year', as_index=False).head(10)
dfx = df_tt.groupby('year', as_index=False)['Total_Weeks'].mean()
dfx['mov_avg']=dfx['Total_Weeks'].rolling(window=3,center=True,min_periods=1).mean()
x  = dfx['year']
y  = dfx['mov_avg']
plt.plot(x,y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=5)
plt.ylabel('No of Weeks')
plt.xlabel('Year')
plt.title('No. Of Weeks vs Year - Top 10')
plt.legend()


# In[ ]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(8,8))
df_tt = df_mo.groupby('year', as_index=False).head(20)
dfx = df_tt.groupby('year', as_index=False)['Total_Weeks'].mean()
dfx['mov_avg']=dfx['Total_Weeks'].rolling(window=3,center=True,min_periods=1).mean()
x  = dfx['year']
y  = dfx['mov_avg']
plt.plot(x,y, color='green', marker='o', linestyle='dashed', linewidth=2, markersize=5)
plt.ylabel('No of Weeks')
plt.xlabel('Year')
plt.title('No. Of Weeks vs Year - Top 20')
plt.legend()


# In[13]:


df.head(10)


# In[14]:


# 11th Feb

df = pd.read_csv('Desktop/SongsDataset/Billboard.csv')


# In[22]:


df_bill= df.copy()
df_bill.head()


# In[23]:


df_bill['month'], df_bill['date'],df_bill['year'] = df_bill['WeekID'].str.split('/').str
df_bill["year"] = pd.to_numeric(df_bill["year"])
df_bill["month"] = pd.to_numeric(df_bill["month"])
df_bill["date"] = pd.to_numeric(df_bill["date"])
df_bill = df_bill.drop(['url','WeekID'],axis=1)
df_bill['Initial Score Mass'] = 1/df_bill['Week Position']
df_bill = df_bill.sort_values(by=['year','month','date'])
df_bill=df_bill.groupby(['Song','Performer']).head(52).reset_index()
df_bill=df_bill.groupby(['Song','Performer'],as_index=False).agg({'Initial Score Mass': 'sum','Peak Position': 'min' , 'year':'first','Weeks on Chart':'max'})  
df_bill = df_bill.sort_values(by=['year','Initial Score Mass'],ascending=[True,False])
print(df_bill.shape)
df_bill.head()


# In[26]:


df_tt = df_bill.groupby('year', as_index=False).head(20)
dfx = df_tt.groupby('year', as_index=False)['Weeks on Chart'].mean()
dfx['mov_avg']=dfx['Weeks on Chart'].rolling(window=3,center=True,min_periods=1).mean()


# In[36]:


pd.options.mode.chained_assignment = None  # default='warn'
year = 1958
df_new = pd.DataFrame()
while year<2019:
    dftemp = df_bill.loc[df_bill['year'] == year]
    dftemp['Normalized Score']=0.0
    mov_avg = dfx[dfx['year']== year]['mov_avg']
    for i, row in dftemp.iterrows():
        dftemp.at[i,'Normalized Score'] = row['Initial Score Mass']/mov_avg
    df_new = df_new.append(dftemp, ignore_index=True)
    year+=1
df_new.head()


# In[38]:


df_bill = df_new.copy()


# In[39]:


df_bill['color'] = ''
df_bill.loc[df_bill.year>=2010,'color']='red'
df_bill.loc[ (df_bill.year>=2000) & (df_bill.year<2010) ,'color']= 'orange'
df_bill.loc[ (df_bill.year>=1990) & (df_bill.year<2000) ,'color'] = 'yellow'
df_bill.loc[ (df_bill.year>=1980) & (df_bill.year<1990) ,'color'] = 'green'
df_bill.loc[ (df_bill.year>=1970) & (df_bill.year<1980) ,'color'] = 'blue'
df_bill.loc[ (df_bill.year>=1960) & (df_bill.year<1970) ,'color'] = 'indigo'
df_bill.loc[ (df_bill.year<1960),'color'] = 'violet'


# In[41]:


dft = df_bill.copy()


# In[43]:


dft.head()


# In[44]:


dft['Spotify_Score'] = 0
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in dft.iterrows():
#     q = String.init(format:"artist:%@ track:%@",row['Performer'],row['Song'])
    q = 'track:%s artist:%s' % (row['Song'],row['Performer'])
    track_id1 = sp.search(q, type='track', limit=1)
    track_id2 = sp.search(q ='track:' + row['Song'] , type='track', limit=1)
    popularity=[]
#     print(fl)
    fl+=1
    x=0
    y=0
    for j, t in enumerate(track_id1['tracks']['items']):
        x= t['popularity']
    for j, t in enumerate(track_id2['tracks']['items']):
        y= t['popularity']    
    dft.at[i,'Spotify_Score']= max(x,y)   
print("done")   


# In[46]:


dft.head()


# In[47]:


dft[dft['Spotify_Score']==0].count()


# In[51]:


dfzero = dft[dft['Spotify_Score']==0]
dfnonzero = dft[dft['Spotify_Score']!=0]
print(len(dfzero.index))
print(len(dfnonzero.index))


# In[58]:


# Running for Zero's Again in a Smaller DataFrame
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in dfzero.iterrows():
#     q = String.init(format:"artist:%@ track:%@",row['Performer'],row['Song'])
    q = 'track:%s artist:%s' % (row['Song'],row['Performer'])
    track_id1 = sp.search(q, type='track', limit=1)
    track_id2 = sp.search(q ='track:' + row['Song'] , type='track', limit=1)
    popularity=[]
    if fl%1000==0:
        print(fl)
    fl+=1
    x=0
    y=0
    for j, t in enumerate(track_id1['tracks']['items']):
        x= t['popularity']
    for j, t in enumerate(track_id2['tracks']['items']):
        y= t['popularity']    
    dfzero.at[i,'Spotify_Score']= max(x,y)   
print("done") 


# In[60]:


df_norm = pd.concat([dfzero, dfnonzero], ignore_index=True)
len(df_norm.index)


# In[61]:


df_norm[df_norm['Spotify_Score']==0].count()


# In[68]:


df_norm = df_norm.sort_values(by=['year','Initial Score Mass'] , ascending = [True,False])
df_norm.head(20)


# In[77]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(20,20))
# plt.axis((x1,x2,15,100))
dftemp = df_norm[df_norm['color']=='violet']
x = dftemp['Spotify_Score']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '<1950')

dftemp = df_norm[df_norm['color']=='indigo']
x = dftemp['Spotify_Score']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1960-70')

dftemp = df_norm[df_norm['color']=='blue']
x = dftemp['Spotify_Score']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1970-80 ')

dftemp = df_norm[df_norm['color']=='green']
x = dftemp['Spotify_Score']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1980-90')

dftemp = df_norm[df_norm['color']=='yellow']
x = dftemp['Spotify_Score']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1990-00')

dftemp = df_norm[df_norm['color']=='orange']
x = dftemp['Spotify_Score']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2000-2010')

dftemp = df_norm[df_norm['color']=='red']
x = dftemp['Spotify_Score']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2010+')

plt.ylabel('Normalized Score')
plt.xlabel('Spotify Score')
plt.legend()
plt.grid()
# axes = plt.gca()
# axes.set_ylim([0,20])
# plt.yscale('linear')
plt.title('Spotify   vs  Normalized Score')
plt.show() 


# In[74]:


df_norm['Spotify_Score'].corr(df_norm['Normalized Score'])


# In[28]:


df_norm.to_csv('Desktop/SongsDataset/Normalised.csv')


# In[89]:


dfxx=df_norm.merge(df_mo, how='left')
dfxx.head()


# In[82]:


dfxx['Youtube viewcount'].head()


# In[83]:


dfxx.isna().sum()


# In[90]:


dfxx = dfxx.dropna()


# In[92]:


dfxx['log_youtube'] = np.log2(2+dfxx['Youtube viewcount'])


# In[ ]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(20,20))
# plt.axis((x1,x2,15,100))
dftemp = dfxx[dfxx['color']=='violet']
y = dftemp['log_youtube']
x = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '<1950')

dftemp = dfxx[dfxx['color']=='indigo']
y = dftemp['log_youtube']
x = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1960-70')

dftemp = dfxx[dfxx['color']=='blue']
y = dftemp['log_youtube']
x = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1970-80 ')

dftemp = dfxx[dfxx['color']=='green']
y = dftemp['log_youtube']
x = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1980-90')

dftemp = dfxx[dfxx['color']=='yellow']
y = dftemp['log_youtube']
x = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1990-00')

dftemp = dfxx[dfxx['color']=='orange']
y = dftemp['log_youtube']
x = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2000-2010')

dftemp = dfxx[dfxx['color']=='red']
y = dftemp['log_youtube']
x = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2010+')

plt.ylabel('Log Youtube Old')
plt.xlabel('Normalised Score')
plt.legend()
plt.grid()
# axes = plt.gca()
# axes.set_ylim([0,20])
# plt.yscale('linear')
plt.title('Youtube - Old   vs  Normalized Score')
plt.show() 


# In[85]:


import pandas as pd
import json
import requests

df = pd.read_csv('Desktop/SongsDataset/Normalised.csv')
# df = df.head(10)
df['Youtube_Score'] = 0
df['URL'] = ""
itr = 1;
for idx, row in df.iterrows():
    name = (row['Song'])
    name = name.replace(" ","%20")
    url = 'http://youtube-scrape.herokuapp.com/api/search?q={}&page=1'.format(name)
    response = requests.get(url)
    json_data = json.loads(response.text)
    i = 0
    view =[]
    url=[]
    view.append(0)
    url.append("")
    
    itr+=1
    ln = len(json_data['results'])
    while i< min(5,ln):
        temp = json_data['results'][i]['video']['views']
        temp = temp.replace(',','')
        if(temp.isdigit()):
            view.append(int(temp))
            url.append(json_data['results'][i]['video']['url'])
        i+=1
    mx = max(view)
    print(mx)
    index = view.index(mx)
    df.at[idx,'Youtube_Score'] = mx
    df.at[idx, 'URL'] = url[index]


# In[87]:


df[df['Youtube_Score']!=0].count()


# In[3]:


print(1)


# In[15]:


import pandas as pd
df = pd.read_csv('/Users/mohitchoudhary/PycharmProjects/tube/exec1.csv')


# In[16]:


df.shape


# In[17]:


dfy = df[df['Youtube_Score']!=0]


# In[22]:


dfy.head()


# In[21]:


import numpy as np
dfy['Log_Youtube'] =  np.log2(2+dfy['Youtube_Score'])


# In[27]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(20,20))
# plt.axis((x1,x2,15,100))
dftemp = dfy[dfy['color']=='violet']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '<1950')

dftemp = dfy[dfy['color']=='indigo']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1960-70')

dftemp = dfy[dfy['color']=='blue']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1970-80 ')

dftemp = dfy[dfy['color']=='green']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1980-90')

dftemp = dfy[dfy['color']=='yellow']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1990-00')

dftemp = dfy[dfy['color']=='orange']
y = dftemp['Log_Youtube']
x = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2000-2010')

dftemp = dfy[dfy['color']=='red']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2010+')

plt.ylabel('Normalized Score Mass ')
plt.xlabel('Log Youtube')
plt.legend()
plt.grid()
# axes = plt.gca()
# axes.set_ylim([0,20])
# plt.yscale('linear')
plt.title('Log Youtube vs  Normalized Score ( 8000 Data Points)')
plt.show() 


# In[43]:


dft = pd.read_csv('Desktop/SongsDataset/Normalised.csv')


# In[44]:


dft.head()


# In[45]:


dft = dft.sort_values(by= ['Spotify_Score'],ascending = [False])
dft = dft.head(300)


# In[46]:


dfp = dft.head(100)


# In[47]:


dfp.to_csv('Desktop/SongsDataset/Top100Spotify.csv')


# In[49]:


dft = pd.read_csv('Desktop/SongsDataset/Normalised.csv')
dft = dft.sort_values(by= ['Normalized Score'],ascending = [False])
dfp = dft.head(100)
dfp.head()


# In[50]:


dfp.to_csv('Desktop/SongsDataset/Top100NormalisedScore.csv')


# In[53]:


dfy = dfy.sort_values(by= ['Youtube_Score'],ascending = [False])
dfy = dfy.head(100)
dfy.head(50)


# In[54]:


dfy.to_csv('Desktop/SongsDataset/Top100Tube.csv')


# In[65]:


dft = pd.read_csv('Desktop/SongsDataset/Normalised.csv')
dft.head()


# In[66]:


dft['Spotify_Score2'] = 0
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in dft.iterrows():
#     q = String.init(format:"artist:%@ track:%@",row['Performer'],row['Song'])
    q = 'track:%s artist:%s' % (row['Song'],row['Performer'])
    track_id1 = sp.search(q, type='track', limit=1)
    track_id2 = sp.search(q ='track:' + row['Song'] , type='track', limit=1)
    popularity=[]
    if fl%1000==0:
        print(fl)
    fl+=1
    x=0
    y=0
    for j, t in enumerate(track_id1['tracks']['items']):
        x= t['popularity']
    for j, t in enumerate(track_id2['tracks']['items']):
        y= t['popularity']    
    if(x!=0):
        dft.at[i,'Spotify_Score2']= x
    else:
        dft.at[i,'Spotify_Score2']= -1*max(x,y)   
print("done") 


# In[73]:


dft[dft['Spotify_Score2']<0].count()


# In[69]:


dftemp = dft.sort_values(by= ['Spotify_Score2'],ascending = [False])
dftemp = dftemp.head(300)


# In[70]:


dftemp.head(50)


# In[147]:


df_pos = dft[dft['Spotify_Score2']>0]
df_neg = dft[dft['Spotify_Score2']<0]
df_zero = dft[dft['Spotify_Score2']==0]
df_zero.head()


# In[148]:


df_pos.to_csv('Desktop/TubeData/Spot_Pos.csv')
df_neg.to_csv('Desktop/TubeData/Spot_Neg.csv')
df_zero.to_csv('Desktop/TubeData/Spot_Zero.csv')


# In[75]:


df_pos['Normalized Score'].corr(df_pos['Spotify_Score2'])


# In[77]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(20,20))
# plt.axis((x1,x2,15,100))
dftemp = df_pos[df_pos['color']=='violet']
x = dftemp['Spotify_Score2']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '<1950')

dftemp = df_pos[df_pos['color']=='indigo']
x = dftemp['Spotify_Score2']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1960-70')

dftemp = df_pos[df_pos['color']=='blue']
x = dftemp['Spotify_Score2']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1970-80 ')

dftemp = df_pos[df_pos['color']=='green']
x = dftemp['Spotify_Score2']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1980-90')

dftemp = df_pos[df_pos['color']=='yellow']
x = dftemp['Spotify_Score2']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1990-00')

dftemp = df_pos[df_pos['color']=='orange']
x = dftemp['Spotify_Score2']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2000-2010')

dftemp = df_pos[df_pos['color']=='red']
x = dftemp['Spotify_Score2']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2010+')

plt.ylabel('Normalised Score')
plt.xlabel('Spotify')
plt.legend()
plt.grid()
# axes = plt.gca()
# axes.set_ylim([0,20])
# plt.yscale('linear')
plt.title('Spotify  vs  Normalized Score')
plt.show() 


# In[80]:


df_tmp = df_pos.sort_values(by= ['Spotify_Score2'],ascending = [False])
df_tmp = df_tmp.head(200)
df_tmp.to_csv('Desktop/TubeData/top100spotify.csv')


# In[ ]:


(/, ................................., START, HERE, .......................................................)


# In[82]:


df = pd.read_csv('Desktop/TubeData/tubedd/tubeOut.csv')
len(df.index)


# In[117]:


df.dtypes


# In[86]:


df.head()


# In[115]:


df["Youtube_Score"] = pd.to_numeric(df["Youtube_Score"])
df["Normalized Score"] = pd.to_numeric(df["Normalized Score"])
df["Normalized Score"] = pd.to_numeric(df["Spotify_Score"])


# In[104]:


df.head()


# In[102]:


df_nz.dtypes


# In[105]:


df_nz = df[df['Youtube_Score']>0]
len(df_nz.index)


# In[118]:





# In[116]:


df_nz['Log_Youtube'].corr(df_nz['Spotify_Score'])


# In[107]:


import numpy as np
df_nz['Log_Youtube'] =  np.log2(2+df_nz['Youtube_Score'])


# In[119]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(18,18))
# plt.axis((x1,x2,15,100))
dftemp = df_nz[df_nz['color']=='violet']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '<1950')

dftemp = df_nz[df_nz['color']=='indigo']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1960-70')

dftemp = df_nz[df_nz['color']=='blue']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1970-80 ')

dftemp = df_nz[df_nz['color']=='green']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1980-90')

dftemp = df_nz[df_nz['color']=='yellow']
x = dftemp['Log_Youtube']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1990-00')

# dftemp = df_nz[df_nz['color']=='orange']
# x = dftemp['Log_Youtube']
# y = dftemp['Normalized Score']
# plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2000-2010')

# dftemp = df_nz[df_nz['color']=='red']
# x = dftemp['Log_Youtube']
# y = dftemp['Normalized Score']
# plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2010+')

plt.xlabel('Log Youtube')
plt.ylabel('Normalized Score')
plt.legend()
plt.grid()
# axes = plt.gca()
# axes.set_ylim([0,20])
# plt.yscale('linear')
plt.title('Log Youtube  vs  Normalized Score')
plt.show() 


# In[123]:


df_toptube200 = df_nz.sort_values(by=['Youtube_Score'], ascending = [False])
df_toptube200 = df_toptube200.head(200)


# In[124]:


df_toptube200.to_csv('Desktop/TubeData/top100Tube.csv')


# In[128]:


df_mo = pd.read_csv('Desktop/songs_data_old.csv')


# In[137]:


df_mo.head()


# In[132]:


df_mo = df_mo.rename(columns={'Spotify Score': 'Spotify_Score'})


# In[134]:


df_mo['Log_Youtube'] = np.log2(2+df_mo['Youtube viewcount'])


# In[136]:


df_mo['date'], df_mo['month'],df_mo['year'] = df_mo['Entry_Date'].str.split('/').str
df_mo['year'] = df_mo['year'].apply(lambda x: ('19'+x) if int(x)>18 else ('20'+x))
df_mo["year"] = pd.to_numeric(df_mo["year"])
df_mo = df_mo.sort_values(by=['year'], ascending = True)


# In[144]:


df_mo = df_mo[(df_mo['year']>2000)]
df_mo.to_csv('Desktop/songs_visual_final.csv')


# In[ ]:


# Date : Feb 20


# In[50]:


import pandas as pd
# df = pd.read_csv('Desktop/TubeData/tubedd/tubeOut.csv')
df = pd.read_csv('Desktop/SongsDataset/Normalised.csv')
df.head()
dft = df.copy()


# In[51]:


dft['Spotify_Score2'] = 0
dft['Artist_Name_Found'] = ''
dft['Song_Name_Found'] = ''
dft['Song_Name_Edit_Distance'] = -1
dft['Artist_Name_Edit_Distance'] = -1

def editDistDP(str1, str2, m, n): 
   
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
    for i in range(m+1): 
        for j in range(n+1): 
  
            if i == 0: 
                dp[i][j] = j   
            elif j == 0: 
                dp[i][j] = i    
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])  
  
    return dp[m][n] 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in dft.iterrows():
    q = 'track:%s artist:%s' % (row['Song'],row['Performer'])
    track_id = sp.search(q, type='track', limit=10)
    popularity=[]
    
    if fl%500==0:
        print(fl)
    fl+=1
    score=[]
    ed_min= 10000000
    songNameDistance = -1
    artistNameDistance = -1
    songNameFound =''
    artistNameFound =''
    spot_score=0
#     print(enumerate(track_id['tracks']['items']))
#     for j, t in enumerate(track_id['tracks']['items']):
#         print(t['artists'][0])
#         print(t['popularity'])
#         print(t['name'])
    for j, t in enumerate(track_id['tracks']['items']):
       
        song_edit_dist = editDistDP(row['Song'].lower(),t['name'].lower(),len(row['Song']) , len(t['name']))
        artist_edit_dist = editDistDP(row['Performer'].lower(),t['artists'][0]['name'].lower(),len(row['Performer']) , len(t['artists'][0]['name']))
        
        if song_edit_dist+artist_edit_dist < ed_min :
            ed_min = song_edit_dist+artist_edit_dist
            spot_score = t['popularity']
            songNameDistance = song_edit_dist
            artistNameDistance = artist_edit_dist
            songNameFound = t['name']
            artistNameFound = t['artists'][0]['name']
            
            
    dft.at[i,'Spotify_Score2'] = spot_score
    dft.at[i,'Artist_Name_Found'] = artistNameFound
    dft.at[i,'Song_Name_Found'] = songNameFound
    dft.at[i,'Song_Name_Edit_Distance'] = songNameDistance
    dft.at[i,'Artist_Name_Edit_Distance'] = artistNameDistance
    
    
dft.to_csv('Desktop/newSpotify_21Feb.csv')    
print("done") 


# In[52]:


dft.head()


# In[56]:


df0=dft[dft['Spotify_Score2']==0]


# In[59]:


df0.tail(20)


# In[60]:


df_help = dft.copy()


# In[98]:


dft['LastFm_Listener_Count']=-1
dft['LastFm_Play_Count']=-1
dft['LastFm_Song_Found']=''
dft['LastFm_Artist_Found']=''
counter=0
import requests
import json
for i, row in dft.iterrows():

    url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=5b324bf69db842b9bea66421420f4b92&artist={}&track={}&format=json&autocorrect=1'.format(row['Performer'],row['Song'])
    response = requests.get(url)
    lis=-1
    play=-1
    song=''
    artist=''
    if(counter%500==0):
        print (counter)
    counter+=1
    if(response.status_code == 200):
        data = response.json()
        
        if 'track' in data:
            lis=data['track']['listeners']
            play= data['track']['playcount']
            song=data['track']['name']
            artist=data['track']['artist']['name']
    dft.at[i,'LastFm_Listener_Count'] = lis
    dft.at[i,'LastFm_Play_Count'] = play
    dft.at[i,'LastFm_Song_Found'] = song
    dft.at[i,'LastFm_Artist_Found'] = artist

dft.to_csv('Desktop/newLastFm_21Feb.csv')    
print("done") 


# In[100]:


dft1 = dft.iloc[0:19000]
dft2 = dft.iloc[19000:]


# In[95]:


x= dft.iloc[1311]
# x = 'There's A Star Spangled Banner Waving #2 (The Ballad Of Francis Powers)'
url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=5b324bf69db842b9bea66421420f4b92&artist={}&track={}&format=json&autocorrect=1'.format(x['Performer'],x['Song'])
response = requests.get(url)
# data = response.json()

print (response.status_code)


# In[102]:


dft2.head()


# In[103]:


dft2['LastFm_Listener_Count']=-1
dft2['LastFm_Play_Count']=-1
dft2['LastFm_Song_Found']=''
dft2['LastFm_Artist_Found']=''
counter=0
import requests
import json
for i, row in dft2.iterrows():

    url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=5b324bf69db842b9bea66421420f4b92&artist={}&track={}&format=json&autocorrect=1'.format(row['Performer'],row['Song'])
    response = requests.get(url)
    lis=-1
    play=-1
    song=''
    artist=''
    if(counter%500==0):
        print (counter)
    counter+=1
    if(response.status_code == 200):
        data = response.json()
        
        if 'track' in data:
            lis=data['track']['listeners']
            play= data['track']['playcount']
            song=data['track']['name']
            artist=data['track']['artist']['name']
    dft2.at[i,'LastFm_Listener_Count'] = lis
    dft2.at[i,'LastFm_Play_Count'] = play
    dft2.at[i,'LastFm_Song_Found'] = song
    dft2.at[i,'LastFm_Artist_Found'] = artist

# dft.to_csv('Desktop/newLastFm_21Feb.csv')    
print("done") 


# In[104]:


bigdata = pd.concat([dft1, dft2], ignore_index=True)
bigdata.head()


# In[114]:


bigdata[bigdata['LastFm_Play_Count']== -1].count()


# In[107]:


bigdata.tail()


# In[108]:


bigdata.to_csv('Desktop/newLastFm_21Feb.csv')    


# In[124]:


import numpy as np
bigdata['log_LastFm_Play_Count'] = np.log2(2+bigdata['LastFm_Play_Count'])
bigdata['log_LastFm_Listener_Count'] = np.log2(2+bigdata['LastFm_Listener_Count'])


# In[126]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(25,25))
# plt.axis((x1,x2,15,100))
dftemp = bigdata[bigdata['color']=='violet']
x = dftemp['log_LastFm_Play_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '<1950')

dftemp = bigdata[bigdata['color']=='indigo']
x = dftemp['log_LastFm_Play_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1960-70')

dftemp = bigdata[bigdata['color']=='blue']
x = dftemp['log_LastFm_Play_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1970-80 ')

dftemp = bigdata[bigdata['color']=='green']
x = dftemp['log_LastFm_Play_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1980-90')

dftemp = bigdata[bigdata['color']=='yellow']
x = dftemp['log_LastFm_Play_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1990-00')

dftemp = bigdata[bigdata['color']=='orange']
x = dftemp['log_LastFm_Play_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2000-2010')

dftemp = bigdata[bigdata['color']=='red']
x = dftemp['log_LastFm_Play_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2010+')

plt.xlabel('Log LastFm Play Count')
plt.ylabel('Normalized Score')
plt.legend()
plt.grid()
plt.title('Log LastFm Play Count  vs  Normalized Score')
plt.show() 


# In[123]:


lastfm_data = bigdata[bigdata['LastFm_Play_Count']>0]
lastfm_data = bigdata[bigdata['Spotify_Score2']>0]
print(lastfm_data['log_LastFm_Play_Count'].corr(lastfm_data['Spotify_Score2']))


# In[ ]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(25,25))
# plt.axis((x1,x2,15,100))
dftemp = bigdata[bigdata['color']=='violet']
x = dftemp['log_LastFm_Listener_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '<1950')

dftemp = bigdata[bigdata['color']=='indigo']
x = dftemp['log_LastFm_Listener_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1960-70')

dftemp = bigdata[bigdata['color']=='blue']
x = dftemp['log_LastFm_Listener_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1970-80 ')

dftemp = bigdata[bigdata['color']=='green']
x = dftemp['log_LastFm_Listener_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1980-90')

dftemp = bigdata[bigdata['color']=='yellow']
x = dftemp['log_LastFm_Listener_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1990-00')

dftemp = bigdata[bigdata['color']=='orange']
x = dftemp['log_LastFm_Listener_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2000-2010')

dftemp = bigdata[bigdata['color']=='red']
x = dftemp['log_LastFm_Listener_Count']
y = dftemp['Normalized Score']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2010+')

plt.xlabel('Log LastFm Listener Count')
plt.ylabel('Normalized Score')
plt.legend()
plt.grid()
plt.title('Log LastFm Listener Count  vs  Normalized Score')
plt.show() 


# In[129]:


import matplotlib.pyplot  as plt
plt.figure(figsize=(25,25))
# plt.axis((x1,x2,15,100))
dftemp = lastfm_data[lastfm_data['color']=='violet']
y = dftemp['log_LastFm_Play_Count']
x = dftemp['Spotify_Score2']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '<1950')

dftemp = lastfm_data[lastfm_data['color']=='indigo']
y = dftemp['log_LastFm_Play_Count']
x = dftemp['Spotify_Score2']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1960-70')

dftemp = lastfm_data[lastfm_data['color']=='blue']
y = dftemp['log_LastFm_Play_Count']
x = dftemp['Spotify_Score2']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1970-80 ')

dftemp = lastfm_data[lastfm_data['color']=='green']
y = dftemp['log_LastFm_Play_Count']
x = dftemp['Spotify_Score2']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1980-90')

dftemp = lastfm_data[lastfm_data['color']=='yellow']
y = dftemp['log_LastFm_Play_Count']
x = dftemp['Spotify_Score2']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '1990-00')

dftemp = lastfm_data[lastfm_data['color']=='orange']
y = dftemp['log_LastFm_Play_Count']
x = dftemp['Spotify_Score2']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2000-2010')

dftemp = lastfm_data[lastfm_data['color']=='red']
y = dftemp['log_LastFm_Play_Count']
x = dftemp['Spotify_Score2']
plt.scatter(x,y,c=dftemp['color'],alpha = 0.4,label = '2010+')

plt.xlabel('Spotify Score')
plt.ylabel('Log LastFm Play Count')
plt.legend()
plt.grid()
plt.title('Log LastFm Play Count  vs  Spotify Score')
plt.show() 


# In[135]:


top100LastFmPlay = bigdata.sort_values(by=['log_LastFm_Play_Count'], ascending = [False])
top100LastFmListener = bigdata.sort_values(by=['log_LastFm_Listener_Count'], ascending = [False])


# In[134]:


top100LastFm.head(40)


# In[139]:


top100LastFmListener=top100LastFmListener.head(200)


# In[140]:


top100LastFmListener.to_csv('Desktop/top100LastFm_ListenerCount.csv')


# In[ ]:


#################### Checkpoint 26th Feb ######################


# In[16]:


import pandas as pd
df = pd.read_csv('Desktop/newLastFm_21Feb.csv')
df.head()


# In[26]:


dft = df.copy()


# In[27]:


for i, row in dft.iterrows():
    per = row['Performer']
    son = row['Song']
    if(per.find('Featuring')!=-1):
        son = son 
        per = per[0:per.index('Featuring')]
    dft.at[i,'Song'] = son
    dft.at[i,'Performer'] = per

dft.tail()


# In[29]:


dft['Spotify_Score3'] = 0
dft['Artist_Name_Found'] = ''
dft['Song_Name_Found'] = ''
dft['Song_Name_Edit_Distance'] = -1
dft['Artist_Name_Edit_Distance'] = -1

def editDistDP(str1, str2, m, n): 
   
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
    for i in range(m+1): 
        for j in range(n+1): 
  
            if i == 0: 
                dp[i][j] = j   
            elif j == 0: 
                dp[i][j] = i    
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])  
  
    return dp[m][n] 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in dft.iterrows():
#     q = 'track:%s artist:%s' % (row['Song'],row['Performer'])
    
    q = row['Song'] + ' ' + row['Performer']
#     print(q)
    track_id = sp.search(q, type='track', limit=10)
    popularity=[]
    
    if fl%500==0:
        print(fl)
    fl+=1
    score=[]
    ed_min= 10000000
    songNameDistance = -1
    artistNameDistance = -1
    songNameFound =''
    artistNameFound =''
    spot_score=0
#     print(enumerate(track_id['tracks']['items']))
#     for j, t in enumerate(track_id['tracks']['items']):
#         print(t['artists'][0])
#         print(t['popularity'])
#         print(t['name'])
    for j, t in enumerate(track_id['tracks']['items']):
       
        song_edit_dist = editDistDP(row['Song'].lower(),t['name'].lower(),len(row['Song']) , len(t['name']))
        artist_edit_dist = editDistDP(row['Performer'].lower(),t['artists'][0]['name'].lower(),len(row['Performer']) , len(t['artists'][0]['name']))
        
        if song_edit_dist+artist_edit_dist < ed_min :
            ed_min = song_edit_dist+artist_edit_dist
            spot_score = t['popularity']
            songNameDistance = song_edit_dist
            artistNameDistance = artist_edit_dist
            songNameFound = t['name']
            artistNameFound = t['artists'][0]['name']
            
            
    dft.at[i,'Spotify_Score3'] = spot_score
    dft.at[i,'Artist_Name_Found'] = artistNameFound
    dft.at[i,'Song_Name_Found'] = songNameFound
    dft.at[i,'Song_Name_Edit_Distance'] = songNameDistance
    dft.at[i,'Artist_Name_Edit_Distance'] = artistNameDistance
    
    
dft.to_csv('Desktop/newData_26Feb.csv')    
print("done") 


# In[41]:


print(dft['Normalized Score'].corr(dft['Spotify_Score3'] , method = 'spearman'))


# In[31]:


dft[dft['Spotify_Score3']==0].count()


# In[32]:


dft.tail(20)


# In[35]:


dft2 = dft.copy()
dft2.head()


# In[37]:


dft2['LastFm_Listener_Count']=-1
dft2['LastFm_Play_Count']=-1
dft2['LastFm_Song_Found']=''
dft2['LastFm_Artist_Found']=''
counter=0
import requests
import json
for i, row in dft2.iterrows():

    url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=5b324bf69db842b9bea66421420f4b92&artist={}&track={}&format=json&autocorrect=1'.format(row['Performer'],row['Song'])
    response = requests.get(url)
    lis=-1
    play=-1
    song=''
    artist=''
#     if(counter%500==0):
    print (counter)
    print(response)
    counter+=1
    if(response.status_code == 200):
        data = response.json()
        
        if 'track' in data:
            lis=data['track']['listeners']
            play= data['track']['playcount']
            song=data['track']['name']
            artist=data['track']['artist']['name']
    dft2.at[i,'LastFm_Listener_Count'] = lis
    dft2.at[i,'LastFm_Play_Count'] = play
    dft2.at[i,'LastFm_Song_Found'] = song
    dft2.at[i,'LastFm_Artist_Found'] = artist

dft2.to_csv('Desktop/newData_27Feb.csv')    
print("done") 


# In[75]:


year = 1958
x=[]
spot_corr = []
lastfm_corr =[]
while year <=2018:
    x.append(year)
    dfx = dft[dft['year'] == year]
    spot_corr.append(dfx['Normalized Score'].corr(dfx['Spotify_Score3'] , method = 'spearman'))
    lastfm_corr.append(dfx['Normalized Score'].corr(dfx['LastFm_Play_Count'] , method = 'spearman'))
    year+=1

import matplotlib.pyplot  as plt
plt.figure(figsize=(50,8))
plt.scatter(x,spot_corr,c='g',alpha = 0.9,label = 'Spotify')
plt.scatter(x,lastfm_corr,c='r',alpha = 0.9,label = 'Last Fm')
plt.ylabel('Spearman Corr')
plt.xlabel('Year')
plt.xticks(x)
plt.legend()
plt.show()
    
    


# In[57]:


df = pd.read_csv('Desktop/newData_26Feb.csv')
df['delta_year'] = 2018-df['year']
df.head()


# In[78]:


df = df[df['Spotify_Score3']>0]
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
lr = LinearRegression()

df_slice = df[[i for i in list(df.columns) if i == 'Normalized Score' or i == 'delta_year' or i == 'Spotify_Score3']]
x = df_slice.drop('Spotify_Score3',axis=1)
y = df_slice['Spotify_Score3']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 420)
lr.fit(x_train,y_train)
df_slice['Predicted Spotify'] = lr.predict(x)
# lrmse = np.sqrt(metrics.mean_squared_error(y_pred, df['Spotify_Score3']))
# print (lrmse)


# In[68]:


df_slice.head(10)


# In[79]:


print(np.sqrt(metrics.mean_squared_error(df_slice['Predicted Spotify'], df_slice['Spotify_Score3'])))


# In[84]:


x = df['LastFm_Play_Count'].max()
df[df['LastFm_Play_Count']== x]


# In[85]:


df


# In[ ]:


###### Regression Checkpoint 3rd March


# In[86]:


df = df[df['Spotify_Score3']>0]
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
import numpy as np
lr = LinearRegression()

decay_rate = 0.99
rmse=[]
while decay_rate > 0.5:
    df_slice = df[[i for i in list(df.columns) if i == 'Normalized Score' or i == 'delta_year' or i == 'Spotify_Score3']]
    df_slice['Decayed Normalized Score'] = df_slice['Normalized Score']*(decay_rate**df_slice['delta_year'])
    x = df_slice.drop('Spotify_Score3',axis=1)
    y = df_slice['Spotify_Score3']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 420)
    lr.fit(x_train,y_train)
    df_slice['Predicted Spotify'] = lr.predict(x)
    rmse.append(np.sqrt(metrics.mean_squared_error(df_slice['Predicted Spotify'], df_slice['Spotify_Score3'])))
    decay_rate -=0.03


# In[87]:


print(rmse)


# In[88]:


df_slice.head()


# In[176]:


dfx = df.copy()


# In[158]:


dfx['Year_Bucket']= pd.cut(dfx['year'] , 20 )
dfx['Normalised_Score_Bucket'] = pd.qcut(dfx['Normalized Score'], 50)
dfx['Predicted_Spotify'] = dfx.groupby(['Year_Bucket','Normalised_Score_Bucket'])['Spotify_Score3'].transform('median')
print(np.sqrt(metrics.mean_squared_error(dfx['Predicted_Spotify'], dfx['Spotify_Score3'])))


# In[160]:


dfx['Score_Diff'] = dfx['Predicted_Spotify'] - dfx['Spotify_Score3']
dfy = dfx.groupby('year').reset_index()
dfouthigh = dfy.sort_values(by=['Score_Diff'], ascending = [True])
dfouthigh = dfouthigh.head(10)
dfouthigh.to_csv('Desktop/Outliers_Top10.csv')


# In[309]:


import math
year_start = 1957
dfx = df.copy()
df_final = pd.DataFrame()
while year_start <= 2017:
    focus_year= year_start+1
    df_temp = dfx[(dfx['year']>=year_start)&(dfx['year']<year_start+3)]
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Normalized Score'].rank(pct=True)
    df_temp['Percentile_Normalised_Score_Window'] = df_temp['Percentile_Normalised_Score_Window']*100
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Percentile_Normalised_Score_Window'].apply(np.floor)
    df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score_Window'], 50)
    x = df_temp.groupby('Percentile_Bucket',as_index=False)['Spotify_Score3'].median()
    x.columns = ['Percentile_Bucket', 'Median_Spotify' ]
    x['Year'] = focus_year
    df_final=pd.concat([df_final,x])
    year_start+=1
    
df_final.head()


# In[344]:


df_mo[df_mo['year'] == 2015]


# In[321]:


x = '(7.0, 99.0]'
a,b = x.split(',')
b,c=b.split(']')
b = b.strip()
print(b)


# In[337]:


df_final['Percentile_Bucket'] = df_final.Percentile_Bucket.astype(str)
df_final['Percentile'] =0.0
for i,row in df_final.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    df_final.at[i,'Percentile'] = b
df_final.head()


# In[355]:


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.figure(figsize=(80,80))
sns.set(font_scale=2.2)
result = df_final.pivot(index='Percentile', columns='Year', values='Median_Spotify')

# sns.color_palette("rainbow", 5)
# sns.set_palette("rainbow", 10)
sns.heatmap(result, annot=True, fmt="g", cmap='rainbow',vmin =0 , vmax= 100,linewidths=.5)
plt.xticks(fontsize=20, rotation=90)
plt.yticks(fontsize=20, rotation=30)
plt.gca().invert_yaxis()
plt.savefig('Desktop/to_rainbow.png') 
plt.show()


# In[296]:


df_temp.head()


# In[262]:


df_final.Percentile_Bucket = df_final.Percentile_Bucket.astype(str)


# In[335]:


y=df_final[(df_final['Percentile'] == '100.0') & (df_final['Year']==1959)]['Median_Spotify']
print(y)


# In[346]:


df_under.head(100)


# In[340]:


import warnings
warnings.filterwarnings("ignore")

df_mo = df.copy()
year = 1958
df_over = pd.DataFrame()
df_under = pd.DataFrame()

while year <= 2018:
    
    df_temp = df_mo[df_mo['year'] == year]
    df_temp['Percentile_Normalised_Score']= df_temp['Normalized Score'].rank(pct=True)
    df_temp['Percentile_Normalised_Score'] = df_temp['Percentile_Normalised_Score']*100
    df_temp['Percentile_Normalised_Score']= df_temp['Percentile_Normalised_Score'].apply(np.floor)
    df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score'], 50)
    df_temp.Percentile_Bucket = df_temp.Percentile_Bucket.astype(str)
    df_temp['Predicted_Score'] = 0
    df_temp['Score_Diff'] = 0
    print(year)
    for i,row in df_temp.iterrows():
            
            x = row['Percentile_Normalised_Score']
#             a,b = x.split(',')
#             b,c=b.split(']')
#             b = b.strip()
            print(x)
            y = df_final[(df_final['Percentile'] == x) & (df_final['Year']== year)]['Median_Spotify']
            print(y)
            df_temp.at[i,'Predicted_Score'] = y
            df_temp.at[i,'Score_Diff'] = y - row['Spotify_Score3']
    df_temp = df_temp.sort_values(by=['Score_Diff'],ascending=[True])
    dfa = df_temp.head(10)
    dfb = df_temp.tail(10)
    df_over = pd.concat([df_over,dfa])
    df_under = pd.concat([df_under,dfb])
    year+=1 

print ("done")
                                                                 
                                                

    
    


# In[347]:


df_over.to_csv('Desktop/Overperforming.csv')
df_under.to_csv('Desktop/Underperforming.csv')


# ###### Checkpoint - 6th March #########

# In[357]:


dfp = df.copy()
dfp.head()


# In[380]:


ftrs = ['Song','Performer','Normalized Score','delta_year','Spotify_Score3']
dfp = dfp[ftrs]


# In[383]:


decay = 0.99 
cols_list = ['Decay 0.99', 'Decay 0.98','Decay 0.97','Decay 0.96','Decay 0.95','Decay 0.94','Decay 0.93','Decay 0.92','Decay 0.91','Decay 0.90']
for j in cols_list:
    dfp[j] = dfp['Normalized Score']*(decay**dfp['delta_year'])
    decay-=0.01
dfp.head()


# In[384]:


q = dfp.copy()
x = q.drop(['Spotify_Score3','Song','Performer'],axis=1)
y = q['Spotify_Score3']
rms=[]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 420)
lr.fit(x_train,y_train)
q['Predicted Spotify'] = lr.predict(x)
rms.append(np.sqrt(metrics.mean_squared_error(q['Predicted Spotify'], q['Spotify_Score3'])))
print(rms)


# In[385]:


from sklearn.isotonic import IsotonicRegression
dd = dfp.copy()
a = dd.drop(['Spotify_Score3','Song','Performer'],axis=1)
b = dd['Spotify_Score3']
a.head()
# rms=[]
# x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 420)
# #     lr.fit(x_train,y_train)
# ir = IsotonicRegression()
# y_ = ir.fit_transform(x_train, y_train)
# rms.append(np.sqrt(metrics.mean_squared_error(y_, dd['Spotify_Score3'])))
# print(rms)


# In[1]:


### Checkpoint --- 

import pandas as pd
df = pd.read_csv('Desktop/newData_26Feb.csv')
df.head()


# In[2]:


df.columns


# In[3]:


df = df.drop(df.columns[[0, 1, 2,11,12]], axis=1)
df.head()


# In[4]:


df = df.rename(columns={'Spotify_Score3': 'Spotify_Score'})


# In[5]:


df.to_csv('Desktop/Data_March22.csv')


# In[45]:


####################### Checkpoint ----> 22nd March

import pandas as pd
df = pd.read_csv('Desktop/Data_March22.csv')
df.head()


# In[46]:


import warnings
warnings.filterwarnings("ignore")

import math
import numpy as np
year_start = 1957
dfx = df.copy()
df_final = pd.DataFrame()
while year_start <= 2017:
    focus_year= year_start+1
    df_temp = dfx[(dfx['year']>=year_start)&(dfx['year']<year_start+3)]
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Normalized Score'].rank(pct=True)
    df_temp['Percentile_Normalised_Score_Window'] = df_temp['Percentile_Normalised_Score_Window']*100
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Percentile_Normalised_Score_Window'].apply(np.floor)
    df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score_Window'], 50)
    x = df_temp.groupby('Percentile_Bucket',as_index=False)['Spotify_Score'].median()
    x.columns = ['Percentile_Bucket', 'Median_Spotify' ]
    x['Year'] = focus_year
    df_final=pd.concat([df_final,x])
    year_start+=1
    

df_final['Percentile_Bucket'] = df_final.Percentile_Bucket.astype(str)
df_final['Percentile'] =0.0
for i,row in df_final.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    df_final.at[i,'Percentile'] = b
df_final.head()


# In[19]:


df_final.loc[(df_final['Percentile'] == 100.0) & (df_final['Year']== 1958)]['Median_Spotify']


# In[65]:


df_out = pd.DataFrame()


# In[71]:


import warnings
warnings.filterwarnings("ignore")
df_mo = df.copy()
year = 1958
df_over = pd.DataFrame()
df_under = pd.DataFrame()
while year <= 2018 :
    if year!=2015:
        df_temp = df_mo[df_mo['year'] == year]
        df_temp['Percentile_Normalised_Score']= df_temp['Normalized Score'].rank(pct=True)
        df_temp['Percentile_Normalised_Score'] = df_temp['Percentile_Normalised_Score']*100
        df_temp['Percentile_Normalised_Score']= df_temp['Percentile_Normalised_Score'].apply(np.floor)
        df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score'], 50)
        df_temp.Percentile_Bucket = df_temp.Percentile_Bucket.astype(str)
        df_temp['Predicted_Score'] = 0.0
        df_temp['Score_Diff'] = 0.0
    #     df_temp.head()
        print(year)
        for i,row in df_temp.iterrows():
                a,b = row['Percentile_Bucket'].split(',')
                b,c=b.split(']')
                b = b.strip()
    #             print(b)
                y = df_final[(df_final['Percentile'] == float(b) ) & (df_final['Year']== year)]['Median_Spotify']
    #             print(y)
                df_temp.at[i,'Predicted_Score'] = y
                df_temp.at[i,'Score_Diff'] = y - row['Spotify_Score']
        df_out = pd.concat([df_out,df_temp])
    year+=1 
    
    
#     df_temp = df_temp.sort_values(by=['Score_Diff'],ascending=[True])
#     dfa = df_temp.head(10)
#     dfb = df_temp.tail(10)
#     df_over = pd.concat([df_over,dfa])
#     df_under = pd.concat([df_under,dfb])
    
# df_out.head()
# print ("done")


# In[72]:


df_out.head()


# In[73]:


df_out = df_out.drop(df_out.columns[[0]], axis=1)
df_out.to_csv('Desktop/Data_22March.csv')


# In[ ]:


##### Checkpoint . ------> 23 March 


# In[74]:


df = pd.read_csv('Desktop/Data_22March.csv')
df.head()


# In[108]:


# Retrying Spotify 
di = pd.read_csv('Desktop/Data_March23.csv')
di = di.iloc[27528:]
print(len(di.index))
df2 = di.copy()
df2['Spotify_Score2'] = 0
df2['Artist_Name_Found'] = ''
df2['Song_Name_Found'] = ''
df2['Song_Name_Edit_Distance'] = -1
df2['Artist_Name_Edit_Distance'] = -1

def editDistDP(str1, str2, m, n): 
   
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
    for i in range(m+1): 
        for j in range(n+1): 
  
            if i == 0: 
                dp[i][j] = j   
            elif j == 0: 
                dp[i][j] = i    
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])  
  
    return dp[m][n] 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in df2.iterrows():
    x = row['Song']
    y = row['Performer']
#     q = 'artist:%s track:%s' % (y,x)
#     print(q)
    q = row['Performer'] + ' ' + row['Song']
    track_id = sp.search(q, type='track', limit=10)
    popularity=[]   
    print(fl)
    fl+=1
    score=[]
    ed_min= 10000000
    songNameDistance = -1
    artistNameDistance = -1
    songNameFound =''
    artistNameFound =''
    spot_score=0
#     print(enumerate(track_id['tracks']['items']))
#     for j, t in enumerate(track_id['tracks']['items']):
#         print(t['artists'][0])
#         print(t['popularity'])
#         print(t['name'])
    for j, t in enumerate(track_id['tracks']['items']):
       
        song_edit_dist = editDistDP(row['Song'].lower(),t['name'].lower(),len(row['Song']) , len(t['name']))
        artist_edit_dist = editDistDP(row['Performer'].lower(),t['artists'][0]['name'].lower(),len(row['Performer']) , len(t['artists'][0]['name']))
        if artist_edit_dist < ed_min :
            ed_min = artist_edit_dist
            spot_score = t['popularity']
            songNameDistance = song_edit_dist
            artistNameDistance = artist_edit_dist
            songNameFound = t['name']
            artistNameFound = t['artists'][0]['name']
            
    
    df2.at[i,'Spotify_Score2'] = spot_score
    df2.at[i,'Artist_Name_Found'] = artistNameFound
    df2.at[i,'Song_Name_Found'] = songNameFound
    df2.at[i,'Song_Name_Edit_Distance'] = songNameDistance
    df2.at[i,'Artist_Name_Edit_Distance'] = artistNameDistance
    
    
# dft.to_csv('Desktop/newData_26Feb.csv')    
print("done") 


# In[107]:


dfp.tail(20)


# In[105]:


len(dfp.index)


# In[96]:


dfp=df_done


# In[ ]:


#### Checkpint --  April 1


# In[45]:





# In[103]:


import pandas as pd
df = pd.read_csv('Desktop/Data_22March.csv')
df.head()


# In[105]:


len(df.index)


# In[26]:


x = dfp.groupby(['Performer']).size()
dfx=x.to_frame(name = 'size').reset_index()
dfx.head()


# In[35]:


dfx = dfx.sort_values(by=['size'], ascending = False)
dfx.to_csv('Desktop/Artist_Frequency_Count.csv')


# In[101]:


df_temp.head()


# In[100]:


# dfx -- artist count
import matplotlib.pyplot as plt
dq = dfx.iloc[1:20]
for idx,row in dq.iterrows():
    df_temp = df[df['Performer'] == row['Performer']]
    df_temp = df_temp.sort_values(by=['year'],ascending=True)
    max_value = df_temp['year'].max()
    min_value = df_temp['year'].min()
    df_temp['normalised_year'] = (df_temp['year'] - min_value) / (max_value - min_value)
    plt.scatter(df_temp['normalised_year'],df_temp['Score_Diff'])
    plt.title(row['Performer'])
    plt.ylabel('Popularity Difference')
    plt.xlabel('Relative Time')
    plt.axhline(0, color='red')
#     plt.axvline(0, color='white')
    
    plt.show() 
plt.savefig('Desktop/foo.png')


# In[37]:


dx1 = dfp.iloc[0:1300]
dx1.head()


# In[39]:


dfp['LastFm_Listener_Count']=-1
dfp['LastFm_Play_Count']=-1
dfp['LastFm_Song_Found']=''
dfp['LastFm_Artist_Found']=''
counter=0
import requests
import json
for i, row in dfp.iterrows():

    url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=5b324bf69db842b9bea66421420f4b92&artist={}&track={}&format=json&autocorrect=1'.format(row['Performer'],row['Song'])
    response = requests.get(url)
    listener=-1
    play=-1
    song=''
    artist=''
#     if(counter%500==0):
    print (counter)
#     print(response)
    counter+=1
    if(response.status_code == 200):
        try:
            data = response.json()
        except:
            print("exception")
        
        if 'track' in data:
            listener=data['track']['listeners']
            play= data['track']['playcount']
            song=data['track']['name']
            artist=data['track']['artist']['name']
    dfp.at[i,'LastFm_Listener_Count'] = listener
    dfp.at[i,'LastFm_Play_Count'] = play
    dfp.at[i,'LastFm_Song_Found'] = song
    dfp.at[i,'LastFm_Artist_Found'] = artist

# dft2.to_csv('Desktop/newData_27Feb.csv')    
print("done") 


# In[44]:


len(dfp.index)


# In[46]:


df = pd.read_csv('Desktop/march22.csv')
df.head()
print(len(df.index))


# In[47]:


df.head()


# In[48]:


df = df.drop(df.columns[[0, 1, 2,11,12]], axis=1)
df.head()


# In[49]:


dfp=df.copy()
dfp['LastFm_Listener_Count']=-1
dfp['LastFm_Play_Count']=-1
dfp['LastFm_Song_Found']=''
dfp['LastFm_Artist_Found']=''
counter=0
import requests
import json
for i, row in dfp.iterrows():

    url = 'http://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key=5b324bf69db842b9bea66421420f4b92&artist={}&track={}&format=json&autocorrect=1'.format(row['Performer'],row['Song'])
    response = requests.get(url)
    listener=-1
    play=-1
    song=''
    artist=''
#     if(counter%500==0):
    print (counter)
#     print(response)
    counter+=1
    if(response.status_code == 200):
        try:
            data = response.json()
        except:
            print("exception")
        
        if 'track' in data:
            listener=data['track']['listeners']
            play= data['track']['playcount']
            song=data['track']['name']
            artist=data['track']['artist']['name']
    dfp.at[i,'LastFm_Listener_Count'] = listener
    dfp.at[i,'LastFm_Play_Count'] = play
    dfp.at[i,'LastFm_Song_Found'] = song
    dfp.at[i,'LastFm_Artist_Found'] = artist

#dft2.to_csv('Desktop/newData_27Feb.csv')    
print("done") 


# In[50]:


dfp.head()


# In[ ]:


dfp[dfp['LastFm_Listener_Count']==-1]


# In[51]:


# Retrying Spotify 
dt = dfp.copy()
dt['Spotify_Score4'] = 0
dt['Artist_Name_Found'] = ''
dt['Song_Name_Found'] = ''
dt['Song_Name_Edit_Distance'] = -1
dt['Artist_Name_Edit_Distance'] = -1

def editDistDP(str1, str2, m, n): 
   
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
    for i in range(m+1): 
        for j in range(n+1): 
  
            if i == 0: 
                dp[i][j] = j   
            elif j == 0: 
                dp[i][j] = i    
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])  
  
    return dp[m][n] 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in dt.iterrows():
    x = row['Song']
    y = row['Performer']
    q = 'artist:%s track:%s' % (y,x)
#     print(q)
#     q = row['Performer'] + ' ' + row['Song']
    track_id = sp.search(q, type='track', limit=10)
    popularity=[]   
    print(fl)
    fl+=1
    score=[]
    ed_min= 10000000
    songNameDistance = -1
    artistNameDistance = -1
    songNameFound =''
    artistNameFound =''
    spot_score=0
#     print(enumerate(track_id['tracks']['items']))
#     for j, t in enumerate(track_id['tracks']['items']):
#         print(t['artists'][0])
#         print(t['popularity'])
#         print(t['name'])
    for j, t in enumerate(track_id['tracks']['items']):
       
        song_edit_dist = editDistDP(row['Song'].lower(),t['name'].lower(),len(row['Song']) , len(t['name']))
        artist_edit_dist = editDistDP(row['Performer'].lower(),t['artists'][0]['name'].lower(),len(row['Performer']) , len(t['artists'][0]['name']))
        if artist_edit_dist < ed_min :
            ed_min = artist_edit_dist
            spot_score = t['popularity']
            songNameDistance = song_edit_dist
            artistNameDistance = artist_edit_dist
            songNameFound = t['name']
            artistNameFound = t['artists'][0]['name']
            
    
    dt.at[i,'Spotify_Score4'] = spot_score
    dt.at[i,'Artist_Name_Found'] = artistNameFound
    dt.at[i,'Song_Name_Found'] = songNameFound
    dt.at[i,'Song_Name_Edit_Distance'] = songNameDistance
    dt.at[i,'Artist_Name_Edit_Distance'] = artistNameDistance
    
    
# dft.to_csv('Desktop/newData_26Feb.csv')    
print("done") 


# In[52]:


dt[dt['Spotify_Score4']==0].count()


# In[53]:


dt.head()


# In[56]:


dt[dt['Performer'] == 'Aretha Franklin'].count()


# In[55]:


len(dt.index)


# In[57]:


x = dt.groupby(['Performer']).size()
pp=x.to_frame(name = 'size').reset_index()
pp.head()


# In[61]:


pp.head()


# In[59]:


pp = pp.sort_values(by=['size'], ascending = False)


# In[62]:


pp.to_csv('Desktop/TopArtistFrequency.csv')


# In[66]:


dt[(dt['Spotify_Score3']==0) & (dt['Spotify_Score4']==0) ].count()


# In[67]:


dt['Spotify_Score4'] = max(dt['Spotify_Score4'],dt['Spotify_Score3'])


# In[68]:


for idx,row in dt.iterrows():
    dt.at[idx,'Spotify_Score4'] = max(row['Spotify_Score4'],row['Spotify_Score3'])
dt.head()


# In[77]:


dt[dt['Spotify_Score3']==0].count()


# In[70]:


dt.to_csv('Desktop/April9.csv')


# In[75]:


dpos = dt[dt['Spotify_Score4']!=0]


# In[71]:


dneg = dt[dt['Spotify_Score4']==0]


# In[76]:


dpos.head()


# In[74]:


dneg.to_csv('Desktop/notFound.csv')


# In[95]:


vox = dpos.copy()
vox=vox.iloc[0:10]
vox['Spotify_Score5'] = 0
vox['Artist_Name_Found'] = ''
vox['Song_Name_Found'] = ''
vox['Song_Name_Edit_Distance'] = -1
vox['Artist_Name_Edit_Distance'] = -1
vox['Spotify_Uri'] =''
def editDistDP(str1, str2, m, n): 
   
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
    for i in range(m+1): 
        for j in range(n+1): 
  
            if i == 0: 
                dp[i][j] = j   
            elif j == 0: 
                dp[i][j] = i    
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])  
  
    return dp[m][n] 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in vox.iterrows():
    x = row['Song']
    y = row['Performer']
    q1 = 'track:%s artist:%s' % (x,y)
#     print(q)
    q2 = row['Song'] + ' ' + row['Performer']
    track_id1 = sp.search(q1, type='track', limit=10)
    track_id2 = sp.search(q2, type='track', limit=10)  
    print(fl)
    fl+=1
    score=[]
    ed_min1= 10000000
    ed_min2= 10000000

    songNameDistance1 = -1
    artistNameDistance1 = -1
    songNameFound1 =''
    artistNameFound1 =''
    spot_score1=0
    
    songNameDistance2 = -1
    artistNameDistance2 = -1
    songNameFound2 =''
    artistNameFound2 =''
    spot_score2=0
#     print(enumerate(track_id['tracks']['items']))
#     for j, t in enumerate(track_id['tracks']['items']):
#         print(t['artists'][0])
#         print(t['popularity'])
#         print(t['name'])
    for j, t in enumerate(track_id1['tracks']['items']):
        print(t)
        
        song_edit_dist1 = editDistDP(row['Song'].lower(),t['name'].lower(),len(row['Song']) , len(t['name']))
        artist_edit_dist1 = editDistDP(row['Performer'].lower(),t['artists'][0]['name'].lower(),len(row['Performer']) , len(t['artists'][0]['name']))
        if artist_edit_dist1 < ed_min1 :
            ed_min1 = artist_edit_dist1
            spot_score1 = t['popularity']
            songNameDistance1 = song_edit_dist1
            artistNameDistance1 = artist_edit_dist1
            songNameFound1 = t['name']
            artistNameFound1 = t['artists'][0]['name']
            a,b,c = (t['uri']).split(':')
            uri1 = c
            
            
    for j, t in enumerate(track_id2['tracks']['items']):
       
        song_edit_dist2 = editDistDP(row['Song'].lower(),t['name'].lower(),len(row['Song']) , len(t['name']))
        artist_edit_dist2 = editDistDP(row['Performer'].lower(),t['artists'][0]['name'].lower(),len(row['Performer']) , len(t['artists'][0]['name']))
        if artist_edit_dist2 < ed_min2 :
            ed_min2 = artist_edit_dist2
            spot_score2 = t['popularity']
            songNameDistance2 = song_edit_dist2
            artistNameDistance2 = artist_edit_dist2
            songNameFound2 = t['name']
#             print(t['name'])
            artistNameFound2 = t['artists'][0]['name']
            a,b,c = (t['uri']).split(':')
            uri2 = c
            
    if(spot_score1 > spot_score2):
        vox.at[i,'Spotify_Score5'] = spot_score1
        vox.at[i,'Artist_Name_Found'] = artistNameFound1
        vox.at[i,'Song_Name_Found'] = songNameFound1
        vox.at[i,'Song_Name_Edit_Distance'] = songNameDistance1
        vox.at[i,'Artist_Name_Edit_Distance'] = artistNameDistance1
        vox.at[i,'Spotify_Uri'] = uri1
    else:
        vox.at[i,'Spotify_Score5'] = spot_score2
        vox.at[i,'Artist_Name_Found'] = artistNameFound2
        vox.at[i,'Song_Name_Found'] = songNameFound2
        vox.at[i,'Song_Name_Edit_Distance'] = songNameDistance2
        vox.at[i,'Artist_Name_Edit_Distance'] = artistNameDistance2
        vox.at[i,'Spotify_Uri'] = uri2

print("Done")


# In[89]:


vox.iloc[6267]


# In[96]:


vox.head()


# In[97]:


import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials

SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
vox['danceability']=0.0
vox['energy']=0.0
vox['key']=0.0
vox['loudness']=0.0
vox['mode']=0.0
vox['speechiness']=0.0
vox['acousticness']=0.0
vox['instrumentalness']=0.0
vox['liveness']=0.0
vox['valence']=0.0
vox['tempo']=0.0
vox['duration_ms']=0.0


for i,row in vox.iterrows():
    x = sp.audio_features(row['Spotify_Uri'])
    if len(x)!=0:
        if 'danceability' in x[0]:
            vox.at[i,'danceability'] = x[0]['danceability']
        
        vox.at[i,'energy'] = x[0]['energy']
        vox.at[i,'key'] = x[0]['key']
        vox.at[i,'loudness'] = x[0]['loudness']
        vox.at[i,'mode'] = x[0]['mode']
        vox.at[i,'speechiness'] = x[0]['speechiness']
        vox.at[i,'acousticness'] = x[0]['acousticness']
        vox.at[i,'instrumentalness'] = x[0]['instrumentalness']
        vox.at[i,'liveness'] = x[0]['liveness']
        vox.at[i,'valence'] = x[0]['valence']
        vox.at[i,'tempo'] = x[0]['tempo']
        vox.at[i,'duration_ms'] = x[0]['duration_ms']

    


# In[102]:


df.head()


# In[99]:


vox.to_csv('Desktop/Detailed_Sheet.csv')


# In[ ]:


# dfx -- artist count
import matplotlib.pyplot as plt
dq = pp.iloc[1:20]
for idx,row in dq.iterrows():
    df_temp = df[df['Performer'] == row['Performer']]
    df_temp = df_temp.sort_values(by=['year'],ascending=True)
    max_value = df_temp['year'].max()
    min_value = df_temp['year'].min()
    df_temp['normalised_year'] = (df_temp['year'] - min_value) / (max_value - min_value)
    plt.scatter(df_temp['normalised_year'],df_temp['Score_Diff'])
    plt.title(row['Performer'])
    plt.ylabel('Popularity Difference')
    plt.xlabel('Relative Time')
    plt.axhline(0, color='red')
#     plt.axvline(0, color='white')
    
    plt.show() 
plt.savefig('Desktop/foo.png')


# In[107]:


import warnings
warnings.filterwarnings("ignore")

import math
import numpy as np
year_start = 1957
dfx = dpos.copy()
df_final = pd.DataFrame()
while year_start <= 2017:
    focus_year= year_start+1
    df_temp = dpos[(dfx['year']>=year_start)&(dfx['year']<year_start+3)]
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Normalized Score'].rank(pct=True)
    df_temp['Percentile_Normalised_Score_Window'] = df_temp['Percentile_Normalised_Score_Window']*100
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Percentile_Normalised_Score_Window'].apply(np.floor)
    df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score_Window'], 50)
    x = df_temp.groupby('Percentile_Bucket',as_index=False)['Spotify_Score4'].median()
    x.columns = ['Percentile_Bucket', 'Median_Spotify' ]
    x['Year'] = focus_year
    df_final=pd.concat([df_final,x])
    year_start+=1
    

df_final['Percentile_Bucket'] = df_final.Percentile_Bucket.astype(str)
df_final['Percentile'] =0.0
for i,row in df_final.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    df_final.at[i,'Percentile'] = b
df_final.head()


# In[111]:


import warnings
warnings.filterwarnings("ignore")
df_mo = dpos.copy()
year = 1958
df_over = pd.DataFrame()
df_under = pd.DataFrame()
df_out = pd.DataFrame()

while year <= 2018 :
    if (year!=2015) & (year!=2006):
        df_temp = df_mo[df_mo['year'] == year]
        df_temp['Percentile_Normalised_Score']= df_temp['Normalized Score'].rank(pct=True)
        df_temp['Percentile_Normalised_Score'] = df_temp['Percentile_Normalised_Score']*100
        df_temp['Percentile_Normalised_Score']= df_temp['Percentile_Normalised_Score'].apply(np.floor)
        df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score'], 50)
        df_temp.Percentile_Bucket = df_temp.Percentile_Bucket.astype(str)
        df_temp['Predicted_Score'] = 0.0
        df_temp['Score_Diff'] = 0.0
    #     df_temp.head()
        print(year)
        for i,row in df_temp.iterrows():
                a,b = row['Percentile_Bucket'].split(',')
                b,c=b.split(']')
                b = b.strip()
    #             print(b)
                y = df_final[(df_final['Percentile'] == float(b) ) & (df_final['Year']== year)]['Median_Spotify']
    #             print(y)
                df_temp.at[i,'Predicted_Score'] = y
                df_temp.at[i,'Score_Diff'] = y - row['Spotify_Score4']
        df_out = pd.concat([df_out,df_temp])
        df_temp = df_temp.sort_values(by=['Score_Diff'],ascending=[True])
        dfa = df_temp.head(10)
        dfb = df_temp.tail(10)
        df_over = pd.concat([df_over,dfa])
        df_under = pd.concat([df_under,dfb])
    year+=1 
    


# In[118]:


len(df_out.index)


# In[115]:


df_over.to_csv('Desktop/overPerf.csv')
df_under.to_csv('Desktop/underPerf.csv')


# In[182]:


# dfx -- artist count
import matplotlib.pyplot as plt
dq = pp.iloc[1:20]
df = df_out
# fig, ax = plt.subplots(nrows=20,ncols=1)
j=0
for idx,row in dq.iterrows():
    df_temp = df[df['Performer'] == row['Performer']]
    df_temp = df_temp.sort_values(by=['year'],ascending=True)
    max_value = df_temp['year'].max()
    min_value = df_temp['year'].min()
    df_temp['normalised_year'] = (df_temp['year'] - min_value) / (max_value - min_value)
    
    plt.scatter(df_temp['normalised_year'],-1*df_temp['Score_Diff'],c='b')
    axes = plt.gca()
    axes.set_xlim([-0.1,1.1])
    axes.set_ylim([-60,+60])
    plt.title(row['Performer'])
    plt.ylabel('Popularity Difference')
    plt.xlabel('Relative Time')
    plt.axhline(0, color='red')
    plt.axvline(0, color='white')
    
    plt.show() 
# plt.savefig('Desktop/foo.png')


# In[3]:


import pandas as pd
df = pd.read_csv('Desktop/April9.csv')


# In[4]:


dp = df[df['year']==2018]


# In[5]:


dp = dp.sort_values(by=['Spotify_Score4'],ascending=[False])


# In[6]:


dp.head()


# In[7]:


print(len(dp.index))


# In[8]:


dp = dp.reset_index()
# dp.columns[0] = 'New_ID'
dp['New_ID'] = dp.index
dp.head()


# In[136]:


dp['level_0']


# In[14]:


import matplotlib.pyplot as plt

plt.figure(figsize=(20,20))
dx = dp.iloc[0:500]
plt.scatter(dx['New_ID'],(dx['Spotify_Score4']),c='red')

y=[]
x = np.arange(500)
print(len(x))
i=0
while i<500:
#     y.append(100*(1 - 1/(1 + 2*(0.995**i))))
#     y.append(100*(1 - 1/(1+ 2*(0.9917**i))) )
    y.append(100-i**0.575)
    i+=1;
plt.scatter(x,y)
# dx.head()


# In[18]:


len(df)


# In[17]:


df = df[df['Spotify_Score4']>0]


# In[19]:


df_mo = df.copy()


# In[48]:


year = 1958
df_yy=pd.DataFrame()
while year <=2018:
    df_temp = df_mo[df_mo['year']==year]
    df_temp = df_temp.sort_values(by=['Spotify_Score4'],ascending=[False])
    df_temp = df_temp.head(500)
    df_temp.insert(0,'Rank', range(1, 1 + len(df_temp.index)))
    df_temp['Predicted_Score_Formulae'] = 100-df_temp['Rank']**0.5777
    df_yy=pd.concat([df_yy,df_temp])
    year+=1
    


# In[41]:


df_yy.tail()


# In[42]:


df_yy.head()


# In[36]:


df_yy.to_csv('Desktop/Dataframe_Apr24.csv')


# In[49]:


df_yy['Log_Ratio'] =np.log( df_yy['Predicted_Score_Formulae']/df_yy['Spotify_Score4'])


# In[44]:


df_yy.tail()


# In[46]:


df_yy=df_yy.sort_values(by=['Log_Ratio','year'], ascending=[False,True])


# In[50]:


df_yy.head(300)


# In[51]:


qx = pd.DataFrame()
qx['Rank'] = df_yy['Rank']
qx['Year'] = df_yy['year']
qx['Song'] = df_yy['Song']
qx['Performer'] = df_yy['Performer']
qx['Spotify_Actual'] = df_yy['Spotify_Score4']
qx['Spotify_Predicted'] = df_yy['Predicted_Score_Formulae']
qx['Log_Ratio'] = df_yy['Log_Ratio']
qx.head()


# In[52]:


qx.to_csv('Desktop/Ratio_Sheet.csv')


# In[54]:


np.min(qx['Log_Ratio'])


# In[ ]:


####### April 24


# In[6]:


import pandas as pd
df = pd.read_csv('Desktop/Dataframe_Apr24.csv')
df.head()
df = df.drop(df.columns[[0, 1, 2,11,12]], axis=1)
df.head()


# In[56]:


import warnings
warnings.filterwarnings("ignore")

import math
import numpy as np
year_start = 1957
dfx = df.copy()
df_final = pd.DataFrame()
while year_start <= 2017:
    focus_year= year_start+1
    df_temp = dfx[(dfx['year']>=year_start)&(dfx['year']<year_start+3)]
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Normalized Score'].rank(pct=True)
    df_temp['Percentile_Normalised_Score_Window'] = df_temp['Percentile_Normalised_Score_Window']*100
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Percentile_Normalised_Score_Window'].apply(np.floor)
    df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score_Window'], 50)
    x = df_temp.groupby('Percentile_Bucket',as_index=False)['Spotify_Score'].median()
    x.columns = ['Percentile_Bucket', 'Median_Spotify' ]
    x['Year'] = focus_year
    df_final=pd.concat([df_final,x])
    year_start+=1
    

df_final['Percentile_Bucket'] = df_final.Percentile_Bucket.astype(str)
df_final['Percentile'] =0.0
for i,row in df_final.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    df_final.at[i,'Percentile'] = b
df_final.head()


# In[61]:


df.head()


# In[62]:


df = df.sort_values(by=['Spotify_Score'],ascending=[False])
df.head()


# In[63]:


df = df[df['Spotify_Score']>0]


# In[64]:


df.head(10)


# In[78]:


oq = df.copy()
oq.head()
oq['Rank'] = 0.0


# In[86]:


# oq.insert(0, 'New_ID', range(1, 1 + len(oq)))
t =  oq['Spotify_Score'].rank(ascending=False , method ='average')
oq.head()


# In[87]:


t.head(20)


# In[71]:


xer = df.groupby('Spotify_Score')


# In[74]:


len(xer)


# In[88]:


oq.groupby('Spotify_Score')['New_ID'].mean()


# In[90]:


oq['New_ID'].max()


# In[91]:


import pandas as pd
df = pd.read_csv('Desktop/Data_22March.csv')
df.head()
df = df.drop(df.columns[[0, 1, 2,11,12]], axis=1)
df.head()


# In[93]:


len(df_yy.index)


# In[94]:


df_yy.head()


# In[97]:


df_yy['Rank'] = 0.0
df_yy['Log_Ratio'] = 0.0
df_yy=df_yy.sort_values(by=['Spotify_Score4'],ascending=[False])
df_yy.insert(0, 'Rank_ID', range(1, 1 + len(df_yy.index)))
df_yy.head()


# In[98]:


df_yy['Rank_ID'].max()


# In[101]:


df_yy.groupby('Spotify_Score4')['Rank_ID'].mean()


# In[102]:


df_yy.head()


# In[104]:


df_yy[df_yy['Rank_ID']==3200]


# In[105]:


df_yy.head()


# In[124]:


v=pd.DataFrame(columns=['X', 'Y'])


# In[127]:


v['X','Y'] = df_yy.groupby('Spotify_Score4')['Rank_ID'].mean()


# In[126]:


v.head()


# In[130]:


dx.head()


# In[129]:


dx = df_yy.groupby('Spotify_Score4',as_index=False)['Rank_ID'].mean()
dx.columns=['Spotify','Mean_Rank']


# In[134]:


for i,row in df_yy.iterrows():
    df_yy.at[i,'Rank'] = dx[dx['Spotify']==row['Spotify_Score4']]['Mean_Rank']


# In[135]:


df_yy.head()


# In[136]:


df_yy['Predicted_Score_Formulae'] = 100-df_yy['Rank']**0.458


# In[138]:


df_yy['Log_Ratio'] = np.log(df_yy['Predicted_Score_Formulae']/df_yy['Spotify_Score4'])


# In[139]:


df_yy.head()


# In[140]:


df_yy=df_yy.sort_values(by=['Log_Ratio'], ascending=[False])
df_yy.head()


# In[141]:


df_yy.head(20)


# In[143]:


df_yy[df_yy['Song']=='Johnny B. Goode']


# In[144]:


dx.head()


# In[145]:


dx[dx['Spotify']==9]


# In[160]:


import warnings
warnings.filterwarnings("ignore")

import math
import numpy as np
year_start = 1957
dfx = df_yy.copy()
df_final = pd.DataFrame()
while year_start <= 2017:
    focus_year= year_start+1
    df_temp = dfx[(dfx['year']>=year_start)&(dfx['year']<year_start+3)]
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Normalized Score'].rank(pct=True)
    df_temp['Percentile_Normalised_Score_Window'] = df_temp['Percentile_Normalised_Score_Window']*100
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Percentile_Normalised_Score_Window'].apply(np.floor)
    df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score_Window'], 50)
    x = df_temp.groupby('Percentile_Bucket',as_index=False)['Spotify_Score3'].median()
    x.columns = ['Percentile_Bucket', 'Median_Spotify' ]
    x['Year'] = focus_year
    df_final=pd.concat([df_final,x])
    year_start+=1
    

df_final['Percentile_Bucket'] = df_final.Percentile_Bucket.astype(str)
df_final['Percentile'] =0.0
for i,row in df_final.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    df_final.at[i,'Percentile'] = b
df_final.head()


# In[161]:


import warnings
warnings.filterwarnings("ignore")
df_mo = df.copy()
df_per=pd.DataFrame()
year = 1958
while year <= 2018 :
    
        df_temp = df_yy[df_yy['year'] == year]
        df_temp['Percentile_Normalised_Score']= df_temp['Normalized Score'].rank(pct=True)
        df_temp['Percentile_Normalised_Score'] = df_temp['Percentile_Normalised_Score']*100
        df_temp['Percentile_Normalised_Score']= df_temp['Percentile_Normalised_Score'].apply(np.floor)
        df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score'], 50)
        df_temp.Percentile_Bucket = df_temp.Percentile_Bucket.astype(str)
        df_temp['Predicted_Score'] = 0.0
        df_temp['Score_Diff'] = 0.0
    #     df_temp.head()
        print(year)
        df_per=pd.concat([df_per,df_temp])
        year+=1 


# In[162]:


len(df_per.index)


# In[171]:



for i,row in df_per.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    print(i)
    y = df_final[(df_final['Percentile'] == float(b) ) & (df_final['Year']== row['year'])]['Median_Spotify']
#                 print(len(y))
    if(len(y)>0):
        df_per.at[i,'Predicted_Score'] = y
        df_per.at[i,'Score_Diff'] = y - row['Spotify_Score3']
    else:
        df_per.at[i,'Predicted_Score'] = 0
        df_per.at[i,'Score_Diff'] =  row['Spotify_Score3']


# In[172]:


df_per = df_per[df_per['Predicted_Score']>0]
print(len(df_per.index))


# In[175]:


df_per = df_per.rename(columns={'Rank': 'Rank_Actual'})


# In[ ]:


for idx,row in df_per.iterrows():
    df_per['Spotify_Ratio'] = 
    df_per['Rank']


# In[179]:


df_per.head()


# In[178]:


for i,row in df_per.iterrows():
    df_per.at[i,'Rank_Predicted'] = dx[dx['Spotify']==np.floor(row['Predicted_Score'])]['Mean_Rank']


# In[183]:


df_per['Rank_Ratio_'] = np.log(df_per['Rank_Predicted']/df_per['Rank_Actual'])
df_per['Spotify_Ratio'] = df_per['Spotify_Score3']/df_per['Predicted_Score']


# In[184]:


df_per.head()


# In[186]:


df_per=df_per.sort_values(by='Rank_Ratio_',ascending=[False])
df_per.head(20)


# In[187]:


df_per.to_csv('Desktop/vvx.csv')


# In[1]:


len(df_per.index)


# In[ ]:


###### 6th May ######


# In[2]:


import pandas as pd
oof = pd.read_csv('Desktop/vvx.csv')
# df = df.drop(df.columns[[0, 1, 2,11,12]], axis=1)
oof.head()


# In[ ]:


df_yy['Rank'] = 0.0
df_yy['Log_Ratio'] = 0.0
df_yy=df_yy.sort_values(by=['Spotify_Score4'],ascending=[False])
df_yy.insert(0, 'Rank_ID', range(1, 1 + len(df_yy.index)))


# In[9]:


import pandas as pd
df = pd.read_csv('Desktop/Dataframe_Apr24.csv')
df = df.drop(df.columns[[0, 1, 2,11,12]], axis=1)
df.head()


# In[10]:


print(len(df.index))


# In[11]:


df_yy=df.copy()
df_yy['Log_Ratio'] = 0.0
df_yy=df_yy.sort_values(by=['Spotify_Score4'],ascending=[False])
df_yy.insert(0, 'Rank_ID', range(1, 1 + len(df_yy.index)))
df_yy.head()


# In[13]:


dx = df_yy.groupby('Spotify_Score4',as_index=False)['Rank_ID'].mean()
dx.columns=['Spotify','Mean_Rank']


# In[15]:


dx.head(100)


# In[16]:


import pandas as pd
oof = pd.read_csv('Desktop/vvx.csv')
# df = df.drop(df.columns[[0, 1, 2,11,12]], axis=1)
oof.head()


# In[18]:


oof = oof[oof['year']!=2018]
oof = oof[oof['year']!=2017]

oof.to_csv('Desktop/kk.csv')


# In[19]:


c = oof[(oof['year']>=1960) & (oof['year']<1970)]
c.to_csv('Desktop/pp.csv')


# In[ ]:


################## 15th May


# In[23]:


df = pd.read_csv('Desktop/newData_26Feb.csv')
df = df.drop(df.columns[[0, 1, 2]], axis=1)
df.head()


# In[24]:


df.columns


# In[26]:


df = df.drop(df.columns[[7,8,9]], axis=1)
df.head()


# In[27]:


df.to_csv('Desktop/Raw_Data_May14.csv')


# In[30]:


import warnings
warnings.filterwarnings("ignore")
df = df[df['Spotify_Score3']>0]
import math
import numpy as np
year_start = 1957
dfx = df.copy()
df_final = pd.DataFrame()
while year_start <= 2017:
    focus_year= year_start+1
    df_temp = dfx[(dfx['year']>=year_start)&(dfx['year']<year_start+3)]
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Normalized Score'].rank(pct=True)
    df_temp['Percentile_Normalised_Score_Window'] = df_temp['Percentile_Normalised_Score_Window']*100
    df_temp['Percentile_Normalised_Score_Window']= df_temp['Percentile_Normalised_Score_Window'].apply(np.floor)
    df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score_Window'], 50)
    x = df_temp.groupby('Percentile_Bucket',as_index=False)['Spotify_Score3'].median()
    x.columns = ['Percentile_Bucket', 'Median_Spotify' ]
    x['Year'] = focus_year
    df_final=pd.concat([df_final,x])
    year_start+=1
    

df_final['Percentile_Bucket'] = df_final.Percentile_Bucket.astype(str)
df_final['Percentile'] =0.0
for i,row in df_final.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    df_final.at[i,'Percentile'] = b
df_final.head()


# In[32]:


df_final.to_csv('Desktop/Percentile_Median_Year.csv')


# In[34]:


import warnings
warnings.filterwarnings("ignore")
df_per=pd.DataFrame()
year = 1958
while year <= 2018 :
    
        df_temp = df[df['year'] == year]
        df_temp['Percentile_Normalised_Score']= df_temp['Normalized Score'].rank(pct=True)
        df_temp['Percentile_Normalised_Score'] = df_temp['Percentile_Normalised_Score']*100
        df_temp['Percentile_Normalised_Score']= df_temp['Percentile_Normalised_Score'].apply(np.floor)
        df_temp['Percentile_Bucket'] = pd.cut(df_temp['Percentile_Normalised_Score'], 50)
        df_temp.Percentile_Bucket = df_temp.Percentile_Bucket.astype(str)
        df_temp['Predicted_Score'] = 0.0
        df_temp['Score_Diff'] = 0.0
    #     df_temp.head()
        print(year)
        df_per=pd.concat([df_per,df_temp])
        year+=1 
        
for i,row in df_per.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    print(i)
    y = df_final[(df_final['Percentile'] == float(b) ) & (df_final['Year']== row['year'])]['Median_Spotify']
#                 print(len(y))
    if(len(y)>0):
        df_per.at[i,'Predicted_Score'] = y
        df_per.at[i,'Score_Diff'] = y - row['Spotify_Score3']
    else:
        df_per.at[i,'Predicted_Score'] = 0
        df_per.at[i,'Score_Diff'] =  row['Spotify_Score3']


# In[36]:


df_per.head()


# In[38]:


df_per.to_csv('Desktop/Data_May14.csv')


# In[53]:


### 1960
df_60 = df_per[(df_per['year']>=1960) & (df_per['year']<1970)]


# In[55]:


df_60=df_60.sort_values(by=['Spotify_Score3'],ascending=[False])
df_60.head()


# In[56]:


df_60.insert(0,'Rank_ID', range(1, 1 + len(df_60.index)))
df_60.head()


# In[57]:


dx_60= df_60.groupby('Spotify_Score3',as_index=False)['Rank_ID'].mean()
dx_60.columns=['Spotify','Mean_Rank']


# In[58]:


dx_60.head()


# In[59]:


df_60['Rank_Actual'] = 0
df_60['Rank_Predicted'] = 0
for i,row in df_60.iterrows():
    df_60.at[i,'Rank_Actual'] = dx[dx['Spotify']==np.floor(row['Spotify_Score3'])]['Mean_Rank']
    df_60.at[i,'Rank_Predicted'] = dx[dx['Spotify']==np.floor(row['Predicted_Score'])]['Mean_Rank']
df_60.head()


# In[61]:


df_60['Log_Rank_Ratio'] = np.log(df_60['Rank_Predicted']/df_60['Rank_Actual'])


# In[67]:


df_60.head()


# In[76]:


df_60.to_csv('Desktop/1960_sample.csv')


# In[79]:


art_60 = df_60.groupby(['Performer']).size().reset_index(name='counts')
# qq.columns=['Performer','Count']


# In[78]:


qq.to_csv('Desktop/Aritst_1960_sample.csv')


# In[73]:


qq.head()


# In[81]:


art_60=art_60.sort_values(by=['counts'],ascending=[False])


# In[130]:


art_60[art_60['counts']==10]


# In[90]:


count = 1
ratioList60=[]
while count<=40:
    temp = art_60[art_60['counts'] == count]
    su=0.0
    ct=0.0
    for i,row in temp.iterrows():
        perf = row['Performer']
        su+=df_60[df_60['Performer']==perf]['Log_Rank_Ratio'].sum()
        ct+=df_60[df_60['Performer']==perf]['Log_Rank_Ratio'].count()
#     print(ct)
    if ct!=0.0:
        ratioList60.append(su/ct)
    else:
        ratioList60.append(0)
    count+=1
print(ratioList60)


# In[101]:


x = np.arange(1,41,1)
import matplotlib.pyplot as plt

plt.figure(figsize=(6,6))
plt.xlabel('Number of Hits')
plt.ylabel('Average Log Ratio')
plt.title('Number of Hits vs Avg. Log Ratio 1960-1970')
plt.plot(x,ratioList60,marker='o')
plt.axhline(0, color='red')
plt.savefig('Desktop/1960s_AvgLogRatio.png')
# plt.show()


# In[104]:


## Hunting For Dave Clark Five 
df_60[df_60['Performer']=='The Dave Clark Five']


# In[105]:


df_per[df_per['Performer']=='The Dave Clark Five']


# In[133]:


# Connie Francis -->

import matplotlib.pyplot as plt
performer = 'Simon & Garfunkel'

j=0
# for idx,row in dq.iterrows():
df_temp = df_60[df_60['Performer'] == performer]
df_temp = df_temp.sort_values(by=['year'],ascending=True)
max_value = df_temp['year'].max()
min_value = df_temp['year'].min()
df_temp['normalised_year'] = (df_temp['year'] - min_value) / (max_value - min_value)

x = df_temp['normalised_year']
y = df_temp['Log_Rank_Ratio']

plt.scatter(x,y,c='b')
plt.plot(x, np.poly1d(np.polyfit(x, y, 1))(x))
slope, intercept = np.polyfit(x, y, 1)
print(slope,intercept)
axes = plt.gca()
axes.set_xlim([-0.1,1.1])
axes.set_ylim([-3,+3])
plt.title(performer + " 60's Songs")
plt.ylabel('Log Ratio')
plt.xlabel('Relative Time')
plt.axhline(0, color='red')
# plt.axvline(0, color='white')
plt.savefig('Desktop/Simon&Garfunkel60s.png')
plt.show() 


# In[134]:


test = pd.read_csv('Desktop/newData_26Feb.csv')


# In[136]:


test[test['Performer']=='The Dave Clark Five']


# In[139]:


art = art_60[(art_60['counts']>=10) & (art_60['counts']<=30)]
art=art.sort_values(by=['counts'],ascending=[True])


# In[147]:


count = 0
art['Score']=0.0
plt.figure(figsize=(9,9))
axes.set_xlim([9,41])
axes.set_ylim([-1,+1])
plt.xlabel('Number of Hits')
plt.ylabel('Log Ratio')
for i,row in art.iterrows():
#     temp = art_60[art_60['counts'] == count]
    su=0.0
    ct=0.0
    perf = row['Performer']
    count = row['counts']
    su+=df_60[df_60['Performer']==perf]['Log_Rank_Ratio'].sum()
    ct+=df_60[df_60['Performer']==perf]['Log_Rank_Ratio'].count()
    
#     print(ct)
    if ct!=0.0:
       
        plt.scatter(count,(su/ct),c='b')
        art.at[i,'Score']=su/ct
    else:
        plt.scatter(count,0,c='b')
        art.at[i,'Score']=0
    count+=1

# plt.plot(x, np.poly1d(np.polyfit(x, y, 1))(x))
# print(ratioList60)


# In[177]:



hit=pd.DataFrame()
flop=pd.DataFrame()


# In[163]:


a = oob[oob['Artist']=='GREEN DAY']
a=a.sort_values(['Popularity'],ascending=[False])
t1 = a.head(1)
t2 = a.tail(1)
xx = pd.concat([xx, t1], ignore_index=True)
xx = pd.concat([xx, t2], ignore_index=True)
xx.head(15)


# In[229]:


art[art['Score']>0.5]


# In[164]:


hit.to_csv('Desktop/Artist_Compare.csv')


# In[173]:


df = pd.read_csv('Desktop/ProjectData_564.csv')


# In[174]:


df["valence"] = (df["valence"]-df["valence"].min()) / (df["valence"].max()-df["valence"].min())
df["loudness"] = (df["loudness"]-df["loudness"].min()) / (df["loudness"].max()-df["loudness"].min())
df["danceability"] = (df["danceability"]-df["danceability"].min()) / (df["danceability"].max()-df["danceability"].min())
df["speechiness"] = (df["speechiness"]-df["speechiness"].min()) / (df["speechiness"].max()-df["speechiness"].min())
df["acousticness"] = (df["acousticness"]-df["acousticness"].min()) / (df["acousticness"].max()-df["acousticness"].min())
df["instrumentalness"] = (df["instrumentalness"]-df["instrumentalness"].min()) / (df["instrumentalness"].max()-df["instrumentalness"].min())
df["liveness"] = (df["liveness"]-df["liveness"].min()) / (df["liveness"].max()-df["liveness"].min())
df["energy"] = (df["energy"]-df["energy"].min()) / (df["energy"].max()-df["energy"].min())


# In[175]:


df.head()


# In[205]:


a = df[df['Artist']=='JONAS BROTHERS']
a=a.sort_values(['Popularity'],ascending=[False])
t1 = a.head(1)
t2 = a.tail(1)
hit = pd.concat([hit, t1], ignore_index=True)
flop = pd.concat([flop, t2], ignore_index=True)


# In[206]:


hit.to_csv('Desktop/Artist_Hit.csv')
flop.to_csv('DEsktop/Artist_Flop.csv')


# In[204]:


a = df[df['Artist']=='JONAS BROTHERS']
a.head(20)


# In[208]:


dft = pd.read_csv('Desktop/Data_May14.csv')


# In[209]:


dft.head()


# In[215]:


dft['Spotify_Score4'] = 0
# dft['Artist_Name_Found'] = ''
# dft['Song_Name_Found'] = ''
# dft['Song_Name_Edit_Distance'] = -1
# dft['Artist_Name_Edit_Distance'] = -1

def editDistDP(str1, str2, m, n): 
   
    dp = [[0 for x in range(n+1)] for x in range(m+1)] 
    for i in range(m+1): 
        for j in range(n+1): 
  
            if i == 0: 
                dp[i][j] = j   
            elif j == 0: 
                dp[i][j] = i    
            elif str1[i-1] == str2[j-1]: 
                dp[i][j] = dp[i-1][j-1] 
            else: 
                dp[i][j] = 1 + min(dp[i][j-1],dp[i-1][j],dp[i-1][j-1])  
  
    return dp[m][n] 

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
user = sp.user('plamere')
fl = 0
for i, row in dft.iterrows():
    q = row['Song']+' '+row['Performer']
    track_id = sp.search(q, type='track', limit=10)
    popularity=[]
    
    if fl%500==0:
        print(fl)
    fl+=1
    score=[]
    ed_min= 10000000
    songNameDistance = -1
    artistNameDistance = -1
    songNameFound =''
    artistNameFound =''
    spot_score=0
#     print(enumerate(track_id['tracks']['items']))
#     for j, t in enumerate(track_id['tracks']['items']):
#         print(t['artists'][0])
#         print(t['popularity'])
#         print(t['name'])
    for j, t in enumerate(track_id['tracks']['items']):
       
        song_edit_dist = editDistDP(row['Song'].lower(),t['name'].lower(),len(row['Song']) , len(t['name']))
        artist_edit_dist = editDistDP(row['Performer'].lower(),t['artists'][0]['name'].lower(),len(row['Performer']) , len(t['artists'][0]['name']))
        
        if song_edit_dist+artist_edit_dist < ed_min :
            ed_min = song_edit_dist+artist_edit_dist
            spot_score = t['popularity']
            songNameDistance = song_edit_dist
            artistNameDistance = artist_edit_dist
            songNameFound = t['name']
            artistNameFound = t['artists'][0]['name']
            
            
    dft.at[i,'Spotify_Score4'] = spot_score
#     dft.at[i,'Artist_Name_Found'] = artistNameFound
#     dft.at[i,'Song_Name_Found'] = songNameFound
#     dft.at[i,'Song_Name_Edit_Distance'] = songNameDistance
#     dft.at[i,'Artist_Name_Edit_Distance'] = artistNameDistance
    
    
dft.to_csv('Desktop/newSpotify_21Feb.csv')    
print("done") 


# In[211]:


dft.head()


# In[226]:


pq = dft[(dft['Spotify_Score3']>0) & (dft['Spotify_Score4']>0)]
oe = dft[abs(dft['Spotify_Score3']-dft['Spotify_Score4'])<50]
len(oe.index)


# In[224]:


plt.figure(figsize=(12,12))
plt.xlabel('Old Spotify')
plt.ylabel('New Spotify')
plt.title('Stability of Spotify Scores')
plt.scatter(oe['Spotify_Score3'],oe['Spotify_Score4'])


# In[227]:


np.corrcoef(oe['Spotify_Score3'],oe['Spotify_Score4'])

