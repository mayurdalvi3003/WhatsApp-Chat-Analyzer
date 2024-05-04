import pandas as pd 
import re 

def preprocess(data):

    # Read the text data
    lines = data.split('\n')  # Assuming each line is separated by '\n'

    timestamps = []
    messages = []

    # Define regular expressions to extract timestamp and message
    timestamp_pattern = r'\d{1,2}/\d{1,2}/\d{2}, \d{1,2}:\d{2}\s[ap]m\s-\s'

    # Extract timestamps and messages
    for line in lines:
        timestamp_match = re.match(timestamp_pattern, line, re.IGNORECASE)
        if timestamp_match:
            timestamps.append(timestamp_match.group())
            # Extract message by removing the timestamp part from the line
            message = line[len(timestamp_match.group()):].strip()
            messages.append(message)

    # Create a DataFrame
    df = pd.DataFrame({'Time': timestamps, 'Message': messages})

    df.to_csv("Updated_file.csv", index = False)

    df = pd.read_csv('Updated_file.csv', encoding='utf-8')

    # Removing the trailing dash and extra spaces
    # Also replacing the narrow no-break space with a regular space
    #df['Time'] = df['Time'].str.replace('\u202f', ' ').str.replace('-', '').str.strip()

    df['Time'] = df['Time'].str.replace('\u202f', ' ').str.replace(' -', '').str.strip()

    # Converting to datetime with the specified format
    format_str = '%m/%d/%y, %I:%M %p'
    df['Time'] = pd.to_datetime(df['Time'], format=format_str, errors='coerce')


    # Seperating user name and message of that particular user
    users = []
    messages = []

    for message in df["Message"]:
        entry = re.split("([\w\W]+?):\s" , message)
        if entry[1:]: # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append("group_notification")
            messages.append(entry[0])

    df["User"] = users
    df["Message"] = messages

    year = df["Time"].dt.year
    month = df['Time'].dt.month_name()
    month_num = df["Time"].dt.month
    day = df["Time"].dt.day
    day_name = df["Time"].dt.day_name()
    date = df["Time"].dt.date
    hour = df["Time"].dt.hour
    minute = df["Time"].dt.minute

    df.insert(1,"Date" ,date)
    df.insert(2,"Day" ,day)
    df.insert(3,"Day_name" ,day_name)
    df.insert(4,"Month" , month)
    df.insert(5, "Month_num" , month_num)
    df.insert(6, "Year" ,year)
    df.insert(7 , "Hour" ,hour)
    df.insert(8 , "Minute" ,minute)
    


    period = []
    for hour in df[['Day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    period_time = period
    df.insert(9 ,"Period" , period_time)


    return df
