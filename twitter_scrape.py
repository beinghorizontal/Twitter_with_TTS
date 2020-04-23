from twython import Twython
import pandas as pd
import re
"go to https://developer.twitter.com/ and make a new app, then add these details below 
app_key = ""
app_secret=""
oauth_token=""
oauth_token_secret=""

twitter = Twython(app_key, app_secret, oauth_token, oauth_token_secret,0,5)

"Search keyword. Since the script is mainly intended for TTS I filtered media and to avoid spam filtered replies"

keyword = 'list:BeingHorizontal/Markets -filter:media -filter:replies lang:en'

"count = 50 i.e. 50 tweets will be fetched."
results = twitter.search(q=keyword,count=50,result_type='recent',tweet_mode='extended')
statdf = pd.DataFrame(results.get('statuses'))
"statdf contains all the search data"
print(statdf)

"Now let's purify the text so it will be easy to understand when we listen to them"
textl = []
rows = int(len(statdf.index))
for i in range(0, rows):
    "Get user name"    
    name = statdf.iloc[i]['user'].get('name')
    "Twitter stores retweeted text seperately. Here True means RT text is absent"
    if pd.isnull(statdf['retweeted_status'].iloc[i])==True:
        text = statdf.iloc[i]['full_text']
        rtname = '--'
    else:
        var= statdf.iloc[i]['retweeted_status']
        "Name of the RT handle"
        rtname = var['user'].get('name')
        text = var['full_text']
    "Make text TTS friendly further by removing links, new lines etc"        
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r'\n','. ',text)
    text = re.sub(r'&amp','and',text)

    "This will pull quote tweet"
    if statdf.iloc[i]['is_quote_status']==True:
        try:
            qtext =' .'+ 'Quote Tweet: '+statdf.iloc[i]['quoted_status'].get('full_text')
            qtext = re.sub(r"http\S+", "", qtext)
            qtext = re.sub(r'\n','. ',qtext)
            qtext = re.sub(r'&amp','and',qtext)
            
        except:
            qtext=' . '
            pass
            
        try:
            qname = statdf.iloc[i]['quoted_status'].get('user').get('name')
        except:
            qname=' '
            pass
        text_sum =qname+qtext+'.comment on quote tweet by '+name+'. Tweet. '+text

        "append quote tweet in our list"
        textl.append(text_sum)
    else:
        if len(rtname)>3: #If tweet was RT then we will add RT user name
            text_sum ='RT by '+name+'. '+' RT source '+rtname+'. '+text
        else:
            text_sum ='From '+name+'. Tweet. '+text

        textl.append(text_sum)


df = pd.DataFrame({'text':textl})
"export tweets to local folder. I used html file format because I intend to listen to it on Microsoft Edge on desktop/laptop"

df.to_html('tweets.html')
