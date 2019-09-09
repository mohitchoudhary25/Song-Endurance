
# coding: utf-8

# In[137]:


import numpy as np
import pandas as pd 
import spotipy
import seaborn as sns
import os
import warnings
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt


# In[63]:


df = pd.read_csv('Desktop/524Project/NewSpotify.csv')
df = df.loc[:, ~dft.columns.str.match('Unnamed')]
df.head()


# In[64]:


df.head()


# In[100]:


# Function to Calculate Spotify Score 

# df['Spotify_Score4'] = 0
# df['Song_URI'] = ''
# calculate_spotify(dft)


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

def calculate_spotify(dft):
    SPOTIFY_CLIENT_ID = 'f7cdf4a9bdf34bca9dabb6c25047a1d9'
    SPOTIFY_CLIENT_SECRET = '2eb71b5485554e9b8f5376d880c09eb8'
    client_credentials_manager = SpotifyClientCredentials(SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    user = sp.user('plamere')

    counter = 0

    for i, row in dft.iterrows():
        q = row['Song']+' '+row['Performer']
        track_id = sp.search(q, type='track', limit=10)
        popularity=[]

        if counter%50==0:
            print(counter)
        counter+=1


        ed_min= 10000000
        songNameDistance = -1
        artistNameDistance = -1
        songNameFound =''
        artistNameFound =''
        spot_score=0

        for _, t in enumerate(track_id['tracks']['items']):

            song_edit_dist = editDistDP(row['Song'].lower(),t['name'].lower(),len(row['Song']) , len(t['name']))
            artist_edit_dist = editDistDP(row['Performer'].lower(),t['artists'][0]['name'].lower(),len(row['Performer']) , len(t['artists'][0]['name']))

            if song_edit_dist+artist_edit_dist < ed_min :
                ed_min = song_edit_dist+artist_edit_dist
                spot_score = t['popularity']
                songNameDistance = song_edit_dist
                artistNameDistance = artist_edit_dist
                songNameFound = t['name']
                artistNameFound = t['artists'][0]['name']
                a,b,c = t['uri'].split(':')
                songSpotifyURI = c

        dft.at[i,'Spotify_Score4'] = spot_score
        dft.at[i,'Song_URI'] = c
        
        
def calculate_song_params(vox):
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

    counter =0;
    for i,row in vox.iterrows():

        if counter%100 ==0:
            print (counter)
            
        x = sp.audio_features(row['Song_URI'])
        
        if len(x)!=0:
            if 'danceability' in x[0]:
                vox.at[i,'danceability'] = x[0]['danceability']
                
            if 'energy' in x[0]:
                vox.at[i,'energy'] = x[0]['energy']
            
            if 'key' in x[0]:
                vox.at[i,'key'] = x[0]['key']
            
            if 'loudness' in x[0]:
                vox.at[i,'loudness'] = x[0]['loudness']
            
            if 'mode' in x[0]:
                vox.at[i,'mode'] = x[0]['mode']
            
            if 'speechiness' in x[0]:
                vox.at[i,'speechiness'] = x[0]['speechiness']
            
            if 'acousticness' in x[0]:
                vox.at[i,'acousticness'] = x[0]['acousticness']
            
            if 'instrumentalness' in x[0]:
                vox.at[i,'instrumentalness'] = x[0]['instrumentalness']
            
            if 'liveness' in x[0]:
                vox.at[i,'liveness'] = x[0]['liveness']
            
            if 'valence' in x[0]:
                vox.at[i,'valence'] = x[0]['valence']
            
            if 'tempo' in x[0]:
                vox.at[i,'tempo'] = x[0]['tempo']
            
            if 'duration_ms' in x[0]:
                vox.at[i,'duration_ms'] = x[0]['duration_ms']
            
            counter+=1

    return vox


# In[70]:


dft.to_csv('Desktop/524Project/songURI.csv')


# In[ ]:


'''
    CHECKPOINT
'''


# In[98]:


df = pd.read_csv('Desktop/524Project/songURI.csv')
# df = df.loc[:, ~dft.columns.str.match('Unnamed')]
df = df.rename(columns={"Spotify_Score3": "Spotify_Score_April", "Spotify_Score4": "Spotify_Score_August"})
df = df.rename(columns={"Predicted_Score": "Predicted_Spotify_Score"})
df.head()


# In[87]:


plt.figure(figsize=(10,10))
plt.xlabel('Old Spotify')
plt.ylabel('New Spotify')
plt.title('Old Spotify vs New Spotify Scores')
plt.scatter(df['Spotify_Score_April'],df['Spotify_Score_August'],alpha = 0.4)


# In[88]:


df[abs(df['Spotify_Score_April'] - df['Spotify_Score_August']) > 10].count()

# 929 > 10
# 377 > 20
# 184 > 30
# 98 > 40
# 50 > 50


# In[ ]:


'''
    year wise analysis
    introduce Rank ID
    convert actual & predcited spotify score to Ranks
    Make a map of Spotify score to rank for each decade
    Calculate Relative Log Ratio
    
'''


# In[89]:


### 1960 ###

df_60 = df[(df['year']>=1960) & (df['year']<1970)]

df_60=df_60.sort_values(by=['Spotify_Score_August'],ascending=[False])
df_60.insert(0,'Rank_ID', range(1, 1 + len(df_60.index)))
spotify_rank_map_60_df= df_60.groupby('Spotify_Score_August',as_index=False)['Rank_ID'].mean()
spotify_rank_map_60_df.columns=['Spotify_Score','Mean_Rank']

df_60['Rank_Actual'] = 0
df_60['Rank_Predicted'] = 0
for i,row in df_60.iterrows():
    df_60.at[i,'Rank_Actual'] = spotify_rank_map_60_df[spotify_rank_map_60_df['Spotify_Score']==np.floor(row['Spotify_Score_August'])]['Mean_Rank']
    df_60.at[i,'Rank_Predicted'] = spotify_rank_map_60_df[spotify_rank_map_60_df['Spotify_Score']==np.floor(row['Predicted_Spotify_Score'])]['Mean_Rank']

df_60['Log_Rank_Ratio'] = np.log(df_60['Rank_Predicted']/df_60['Rank_Actual'])
df_60 = df_60.sort_values(by=['Log_Rank_Ratio'],ascending=False)
df_60.head()


# In[112]:


df_10.to_csv('Desktop/524Project/2010s.csv')


# In[90]:


# 1970s

df_70 = df[(df['year']>=1970) & (df['year']<1980)]
df_70=df_70.sort_values(by=['Spotify_Score_August'],ascending=[False])
df_70.insert(0,'Rank_ID', range(1, 1 + len(df_70.index)))

spotify_rank_map_70_df= df_70.groupby('Spotify_Score_August',as_index=False)['Rank_ID'].mean()
spotify_rank_map_70_df.columns=['Spotify_Score','Mean_Rank']

df_70['Rank_Actual'] = 0
df_70['Rank_Predicted'] = 0
for i,row in df_70.iterrows():
    
    df_70.at[i,'Rank_Actual'] = spotify_rank_map_70_df[spotify_rank_map_70_df['Spotify_Score']==np.floor(row['Spotify_Score_August'])]['Mean_Rank']
    df_70.at[i,'Rank_Predicted'] = spotify_rank_map_70_df[spotify_rank_map_70_df['Spotify_Score']==np.floor(row['Predicted_Spotify_Score'])]['Mean_Rank']

df_70['Log_Rank_Ratio'] = np.log(df_70['Rank_Predicted']/df_70['Rank_Actual'])
df_70 = df_70.sort_values(by=['Log_Rank_Ratio'],ascending=False)
df_70.head()


# In[54]:


# 1980s

df_80 = df[(df['year']>=1980) & (df['year']<1990)]
df_80=df_80.sort_values(by=['Spotify_Score_August'],ascending=[False])
df_80.insert(0,'Rank_ID', range(1, 1 + len(df_80.index)))

spotify_rank_map_80_df= df_80.groupby('Spotify_Score_August',as_index=False)['Rank_ID'].mean()
spotify_rank_map_80_df.columns=['Spotify_Score','Mean_Rank']

df_80['Rank_Actual'] = 0
df_80['Rank_Predicted'] = 0
for i,row in df_80.iterrows():
    
    df_80.at[i,'Rank_Actual'] = spotify_rank_map_80_df[spotify_rank_map_80_df['Spotify_Score']==np.floor(row['Spotify_Score_August'])]['Mean_Rank']
    df_80.at[i,'Rank_Predicted'] = spotify_rank_map_80_df[spotify_rank_map_80_df['Spotify_Score']==np.floor(row['Predicted_Spotify_Score'])]['Mean_Rank']

df_80['Log_Rank_Ratio'] = np.log(df_80['Rank_Predicted']/df_80['Rank_Actual'])
df_80 = df_80.sort_values(by=['Log_Rank_Ratio'],ascending=False)
df_80.head()


# In[58]:


# 1990s

df_90 = df[(df['year']>=1990) & (df['year']<2000)]
df_90=df_90.sort_values(by=['Spotify_Score_August'],ascending=[False])
df_90.insert(0,'Rank_ID', range(1, 1 + len(df_90.index)))

spotify_rank_map_90_df= df_90.groupby('Spotify_Score_August',as_index=False)['Rank_ID'].mean()
spotify_rank_map_90_df.columns=['Spotify_Score','Mean_Rank']

df_90['Rank_Actual'] = 0
df_90['Rank_Predicted'] = 0
for i,row in df_90.iterrows():
    
    df_90.at[i,'Rank_Actual'] = spotify_rank_map_90_df[spotify_rank_map_90_df['Spotify_Score']==np.floor(row['Spotify_Score_August'])]['Mean_Rank']
    df_90.at[i,'Rank_Predicted'] = spotify_rank_map_90_df[spotify_rank_map_90_df['Spotify_Score']==np.floor(row['Predicted_Spotify_Score'])]['Mean_Rank']

df_90['Log_Rank_Ratio'] = np.log(df_90['Rank_Predicted']/df_90['Rank_Actual'])
df_90 = df_90.sort_values(by=['Log_Rank_Ratio'],ascending=False)
df_90.head()


# In[59]:


# 2000s

df_00 = df[(df['year']>=2000) & (df['year']<2010)]
df_00=df_00.sort_values(by=['Spotify_Score_August'],ascending=[False])
df_00.insert(0,'Rank_ID', range(1, 1 + len(df_00.index)))

spotify_rank_map_00_df= df_00.groupby('Spotify_Score_August',as_index=False)['Rank_ID'].mean()
spotify_rank_map_00_df.columns=['Spotify_Score','Mean_Rank']

df_00['Rank_Actual'] = 0
df_00['Rank_Predicted'] = 0
for i,row in df_00.iterrows():
    
    df_00.at[i,'Rank_Actual'] = spotify_rank_map_00_df[spotify_rank_map_00_df['Spotify_Score']==np.floor(row['Spotify_Score_August'])]['Mean_Rank']
    df_00.at[i,'Rank_Predicted'] = spotify_rank_map_00_df[spotify_rank_map_00_df['Spotify_Score']==np.floor(row['Predicted_Spotify_Score'])]['Mean_Rank']

df_00['Log_Rank_Ratio'] = np.log(df_00['Rank_Predicted']/df_00['Rank_Actual'])
df_00 = df_00.sort_values(by=['Log_Rank_Ratio'],ascending=False)
df_00.head()


# In[60]:


#2010s

df_10 = df[(df['year']>=2010) & (df['year']<2020)]
df_10=df_10.sort_values(by=['Spotify_Score_August'],ascending=[False])
df_10.insert(0,'Rank_ID', range(1, 1 + len(df_10.index)))

spotify_rank_map_10_df= df_10.groupby('Spotify_Score_August',as_index=False)['Rank_ID'].mean()
spotify_rank_map_10_df.columns=['Spotify_Score','Mean_Rank']

df_10['Rank_Actual'] = 0
df_10['Rank_Predicted'] = 0
for i,row in df_10.iterrows():
    
    df_10.at[i,'Rank_Actual'] = spotify_rank_map_10_df[spotify_rank_map_10_df['Spotify_Score']==np.floor(row['Spotify_Score_August'])]['Mean_Rank']
    df_10.at[i,'Rank_Predicted'] = spotify_rank_map_10_df[spotify_rank_map_10_df['Spotify_Score']==np.floor(row['Predicted_Spotify_Score'])]['Mean_Rank']

df_10['Log_Rank_Ratio'] = np.log(df_10['Rank_Predicted']/df_10['Rank_Actual'])
df_10 = df_10.sort_values(by=['Log_Rank_Ratio'],ascending=False)
df_10.head()


# In[101]:


df_params = calculate_song_params(df)


# In[106]:


df_params.head()
df_params.to_csv('Desktop/524Project/songsParam.csv')


# In[ ]:


'''
consistency of over and under

Median of 3 spotify -- re calculation

Name matching 

Artist Search - SOng Name


Over & Under representedness 

'''


# In[ ]:



'''
    >>>> USING THE MEDIAN SPOTIFY OF THE TWO SCORES <<<<
    
    CALCULATING THE COLOR MAP OF MEDIAN SPOTIFY , YEAR and PERCENTILE BUCKET 

'''


# In[113]:


df_params = pd.read_csv('Desktop/524Project/songsParam.csv')
df_params['Median_Spotify'] = df_params[['Spotify_Score_April','Spotify_Score_August']].median(axis = 1, skipna = True) 


# In[121]:


df_params.columns


# In[126]:


# df_tt = df_params.groupby('year', as_index=False).head(20)
df_movAvg = df_params.groupby('year', as_index=False)['Weeks on Chart'].mean()
df_movAvg['mov_avg']=df_movAvg['Weeks on Chart'].rolling(window=3,center=True,min_periods=1).mean()
df_movAvg.head()


# In[128]:


year = 1958
df_new = pd.DataFrame()
while year<2019:
    dftemp = df_params.loc[df_params['year'] == year]
    dftemp['Normalized Score'] = 0.0
    mov_avg = df_movAvg[df_movAvg['year']== year]['mov_avg']
    for i, row in dftemp.iterrows():
        dftemp.at[i,'Normalized Score'] = row['Initial Score Mass']/mov_avg
    df_new = df_new.append(dftemp, ignore_index=True)
    year+=1
df_new.head()


# In[131]:


year_start = 1957
df_final = pd.DataFrame()
while year_start <= 2017:
    focus_year= year_start+1
    dftemp = df_new[(df_new['year']>=year_start)&(df_new['year']<year_start+3)]
    dftemp['Percentile_Normalised_Score_Window']= (dftemp['Normalized Score'].rank(pct=True))*100
#     dftemp['Percentile_Normalised_Score_Window'] = dftemp['Percentile_Normalised_Score_Window']*100
    dftemp['Percentile_Normalised_Score_Window']= dftemp['Percentile_Normalised_Score_Window'].apply(np.floor)
    dftemp['Percentile_Bucket'] = pd.cut(dftemp['Percentile_Normalised_Score_Window'], 50)
    x = dftemp.groupby('Percentile_Bucket',as_index=False)['Median_Spotify'].median()
    x.columns = ['Percentile_Bucket', 'Median_Spotify' ]
    x['Year'] = focus_year
    df_final=pd.concat([df_final,x])
    year_start+=1
    
df_final.head()


# In[132]:


df_final['Percentile_Bucket'] = df_final.Percentile_Bucket.astype(str)
df_final['Percentile'] =0.0
for i,row in df_final.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    df_final.at[i,'Percentile'] = b
df_final.head()


# In[135]:


plt.figure(figsize=(80,80))
sns.set(font_scale=2.2)
result = df_final.pivot(index='Percentile', columns='Year', values='Median_Spotify')

# sns.color_palette("rainbow", 5)
# sns.set_palette("rainbow", 10)
sns.heatmap(result, annot=True, fmt="g", cmap='rainbow',vmin =0 , vmax= 100,linewidths=.5)
plt.xticks(fontsize=20, rotation=90)
plt.yticks(fontsize=20, rotation=30)
plt.gca().invert_yaxis()
plt.savefig('Desktop/524Project/spotify_percentile_rainbow.png') 
plt.show()


# In[136]:


df_final.to_csv('Desktop/524Project/Percentile_Median_year_Sep8.csv')


# In[140]:


warnings.filterwarnings("ignore")
df_predictedVal=df_params.copy()
year = 1958
for i,row in df_predictedVal.iterrows():
    a,b = row['Percentile_Bucket'].split(',')
    b,c=b.split(']')
    b = b.strip()
    print(i)
    y = df_final[(df_final['Percentile'] == float(b) ) & (df_final['Year']== row['year'])]['Median_Spotify']
#                 print(len(y))
    if(len(y)>0):
        df_predictedVal.at[i,'Predicted_Spotify_Score'] = y
        df_predictedVal.at[i,'Score_Diff'] = y - row['Median_Spotify']
    else:
        df_predictedVal.at[i,'Predicted_Spotify_Score'] = 0
        df_predictedVal.at[i,'Score_Diff'] =  row['Median_Spotify']
df_predictedVal.to_csv('Desktop/524Project/songsData_medianSpotify_Sep.csv')        


# In[ ]:


'''
    Checkpoint -- Sep 9
'''

