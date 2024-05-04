import pandas as pd 
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
extract = URLExtract()

def fetch_stats(selected_user , df):
    if selected_user !="Overall":
        df = df[df["User"] == selected_user]
    num_messages = df.shape[0]
    words = []
    for message in df["Message"]:
        words.extend(message.split())

    # fetch number of media 
    num_media_shared = len(df[df["Message"] == "<Media omitted>"])

    # Fetch number of links 

    links = []

    for message in df["Message"]:
        links.extend(extract.find_urls(message))




    return num_messages, len(words) , num_media_shared ,len(links)

# Fetch most busy users
def most_busy_user(df):
    x = df["User"].value_counts().head()
    df = round((df["User"].value_counts()/df.shape[0])*100 , 2).reset_index().rename(columns ={"index":"name" ,"user":"percent"})
    return x ,df 


def create_word_cloud(selected_user , df):


    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc = WordCloud(width=500 , height=500, min_font_size=10,background_color="white")
    temp["Message"] = temp["Message"].apply(remove_stop_words)
    df_wc = wc.generate(df["Message"].str.cat(sep=" "))
    return df_wc



def most_common_words(selected_user,df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    temp = df[df['User'] != 'group_notification']
    temp = temp[temp['Message'] != '<Media omitted>']

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df



def monthly_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]
    timeline = df.groupby(["Year" , "Month_num" ,"Month"])["Message"].count().reset_index()
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline["Month"][i] + "-" +str(timeline["Year"][i]))

    timeline["time"] = time

    return timeline

def daily_timeline(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    df["Date"]  = pd.to_datetime(df["Date"])
    daily_timeline = df.groupby("Date")["Message"].count().reset_index()
    
    return daily_timeline


def week_activity_map(selected_user , df ):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df["Day_name"].value_counts()

def month_activity_map(selected_user , df ):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    return df["Month"].value_counts()

def activity_heatmap(selected_user , df):
    if selected_user != 'Overall':
        df = df[df['User'] == selected_user]

    user_heatmap = df.pivot_table(index='Day_name', columns='Period', values='Message', aggfunc='count').fillna(0)

    return user_heatmap
