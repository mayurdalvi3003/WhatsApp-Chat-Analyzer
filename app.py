import streamlit as st
import preprocessor , helper
import matplotlib.pyplot as plt
import seaborn as sns 

st.sidebar.title("WhatsApp Chat Analyzer")
st.sidebar.header("      Made By Mayur Dalvi")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique users
    user_list = df["User"].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis wrt", user_list)

    if st.sidebar.button("Show  Analysis"):
        # stats area
        num_messages , words , num_media_shared , num_links  = helper.fetch_stats(selected_user ,df)
        st.title("Top-Statistics")
        col1 , col2 , col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header('Media Shared')
            st.title(num_media_shared)
        with col4:
            st.header('Links Shared')
            st.title(num_links)

        # MOnthly Timeline 
        st.title("Monthly-Timeline Series")
        timeline = helper.monthly_timeline(selected_user , df)
        fig, ax  = plt.subplots()

        ax.plot(timeline["time"] , timeline["Message"] , color = "red")
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)

        # daily Timeline 

        st.title("Daily-Timeline Series")
        daily_timeline = helper.daily_timeline(selected_user , df)
        fig, ax  = plt.subplots()
        ax.plot(daily_timeline["Date"] , daily_timeline["Message"])
        plt.xticks(rotation = "vertical")
        st.pyplot(fig)


        # Activity map 
        
        st.title("Activity-Map")
        
        col1 , col2 = st.columns(2)
        # Daily activity map 
        with col1 :
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)

            fig ,ax = plt.subplots()
            plt.xticks(rotation = "vertical")
            ax.bar(busy_day.index , busy_day.values)
            st.pyplot(fig)

        # Monthly activity map 

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)

            fig ,ax = plt.subplots()
            plt.xticks(rotation = "vertical")
            ax.bar(busy_month.index , busy_month.values)
            st.pyplot(fig)

        st.title("Activity-Heatmap")
        user_heatmap = helper.activity_heatmap(selected_user , df)
        fig , ax = plt.subplots()

        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # Finding the busy user inside the Group 

        if selected_user == "Overall":
            st.title("Most Busy User's")
            x , new_df = helper.most_busy_user(df)
            fig , ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation = "vertical")
                st.pyplot(fig)

            with col2:
                
                st.dataframe(new_df)

        # WordCloud 
        st.title("WordCloud")
        df_wc = helper.create_word_cloud(selected_user , df)
        fig , ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # MOst common words
        most_common_df = helper.most_common_words(selected_user , df)

        fig , ax = plt.subplots()
        ax.bar(most_common_df[0] , most_common_df[1])
        plt.xticks(rotation = "vertical")
        st.title("Most Common Words")
        st.pyplot(fig)




