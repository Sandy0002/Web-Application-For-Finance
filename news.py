from newsapi import NewsApiClient
import pycountry as pc
import streamlit as st
import datetime
import requests as re
# Page layout setting
st.set_page_config(page_title="News By InvestEd",page_icon=":newspaper:",layout="wide")
hideStyle=""" <style>
    header {visibility:hidden}
    footer {visibility: hidden}
    #MainMenu {visibility:visible}"""

st.markdown(hideStyle,unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown(f"""
<nav class="navbar fixed-top navbar-expand-lg navbar-light" style="background-color: #B2EA14;">
  <a class="navbar-brand" href="https://sandy0002-web-application-for-finance-homehome-jz9ii7.streamlit.app/" target="_self">Home</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item ">
        <a class="nav-link" href="https://sandy0002-web-application-for-finance-analysis-nj6vsm.streamlit.app/" target="_self">Analysis</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://sandy0002-web-application-for-finance-forecast-ooclvh.streamlit.app/" target="_self">Forecast</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

key ="92ad4e5911bf487b9a93395d56692ec6"
newsapi = NewsApiClient(api_key=key)

# category for the news
feedType =["International", "Local", "Particulars"]
kind = st.sidebar.selectbox("Select news type",options=feedType)
st.sidebar.write("##")
categoryList = ['General', 'Business', 'Health', 'Technology', 'Science', 'Entertainment', 'Sports']

oneDay = datetime.timedelta(days=1)
frm = datetime.date.today() - oneDay
to = datetime.date.today()

headlines=None
everything=None
if kind!="Particulars":
    cat = st.sidebar.selectbox("Select News Category",categoryList)
    st.sidebar.write("##")
    newsCount = st.sidebar.selectbox("Select the number of news headlines", [5, 10, 15, 20, 25, 30], index=3)
    st.sidebar.write("##")

    if kind=="International":
        headlines = newsapi.get_top_headlines(language="en", category=cat.lower(), page_size=newsCount)
        # otherNews = newsapi.get_everything(language="en",page_size=newsCount,from_param=frm,to=to)
    else:

        link = re.get('https://newsapi.org/v2/top-headlines?country=in&category={0}&apiKey={1}'.format(cat, key))
        headlines = link.json()
        # headlines = newsapi.get_top_headlines(category=cat.lower(), country='in', language='en', page_size=newsCount)
        everything = newsapi.get_everything(q="India",language="en", page_size=newsCount, from_param=frm,to=to)
else:
    particularNews= st.sidebar.text_input("Enter the topic:")
    newsCount=st.sidebar.selectbox("Select the number of articles",[5,10,15,20,25,30],index=3)
    if particularNews:
        headlines = newsapi.get_top_headlines(q=particularNews,qintitle=particularNews,language="en",page_size=newsCount)
        everything = newsapi.get_everything(q=particularNews, language='en',page_size=newsCount)

articles=None
articles=headlines['articles']

# here we are needed to give try because when no topic is given in particular news then its showing error
if not articles:
    try:
        # if no headlines are there then we are giving the all the articles regarding that country
        articles=everything['articles']
    except: pass
    
button  = st.sidebar.button("Enter")
# Generating Articles
if button:
    for article in articles:
        st.header(article['title'])
        if article['author']:
            st.write('Author:', article['author'])
        st.write('Source:', article['source']['name'])
        try:
            st.image(article['urlToImage'])
        except Exception:
            pass
        loc = article['url']
        content= ('Read more clicking [here]({loc})'.format(loc=loc))
        st.markdown(content,unsafe_allow_html=True)
