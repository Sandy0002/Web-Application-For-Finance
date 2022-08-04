from newsapi import NewsApiClient
import pycountry as pc
import streamlit as st

st.set_page_config(page_title="News By Investant",page_icon=":newspaper:",layout="wide")
hideStyle=""" <style>
    header {visibility:hidden}
    footer {visibility: hidden}
    #MainMenu {visibility:visible}"""

st.markdown(hideStyle,unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)


# 3498DB
st.markdown(f"""
<nav class="navbar fixed-top navbar-expand-lg navbar-light" style="background-color: #B2EA14;">
  <a class="navbar-brand" href="https://share.streamlit.io/sandeep12-2021/stream-prac/main/app.py" target="_self">Home</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item">
        <a class="nav-link" href="https://share.streamlit.io/sandeep12-2021/stream-prac/main/newApp.py" target="_self">News</a>
      </li>
      <li class="nav-item ">
        <a class="nav-link" href="#">Analysis <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="http://localhost:8501" target="_self">Forecast</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://www.youtube.com" target="_self" >Logout</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

# pass =#@Project123
key ="ef8a6ffb16594c56820310414dc5922d"

newsapi = NewsApiClient(api_key=key)

# category for the news
feedType =["International", "Local", "Particulars"]
kind = st.sidebar.selectbox("Select news type",options=feedType)
st.sidebar.write("##")

categoryList = ['General', 'Business', 'Health', 'Technology', 'Science', 'Entertainment', 'Sports']
if kind=="International":

    cat = st.sidebar.selectbox("Select News Category",categoryList)
    st.sidebar.write("##")
    newsCount = st.sidebar.selectbox("Select the number of news headlines", [5, 10, 15, 20, 25, 30], index=3)
    st.sidebar.write("##")
    headlines = newsapi.get_top_headlines(language="en", category=cat.lower(), page_size=newsCount)

if kind=="Local":
    cat = st.sidebar.selectbox("Select the news category",options=categoryList)
    st.sidebar.write("##")

    newsCount=st.sidebar.selectbox("Select the number of news headlines",[5,10,15,20,25,30],index=3)

    # name of the country in 2 digits
    # contryList= ['Australia', 'Canada',
    #               'China',   'Germany',  'France',
    #               'Britain', 'Indonesia','Israel', 'India','Japan',
    #               'New Zealand','Philippines',
    #                'Russia', 'Saudi Arabia', 'Singapore','South Korea', 'Switzerland',
    #               'Turkey', 'Taiwan', 'Ukraine','United Arab Emirates',   'United States', 'South Africa']

    # codes ={"South Korea":"KR",  "Russia":"RU","Taiwan":"TW","Britain":"GB"}
    st.sidebar.write("##")
    # contry = st.sidebar.selectbox("Select the country for headlines",options=contryList,index=8)
    # if contry in codes:
    #     contName=codes[contry]
    # else:
    #     contName=pc.countries.get(name=contry).alpha_2
    contName = pc.countries.get(name="India").alpha_2
    headlines = newsapi.get_top_headlines(category=cat.lower(), country=contName.lower(), language='en', page_size=newsCount)
    # everything= newsapi.get_everything(q=contName, language='en',page_size=newsCount)


elif kind=="Particulars":
    particularNews= st.sidebar.text_input("If any particular news type here")
    newsCount=st.sidebar.selectbox("Select the number of articles",[5,10,15,20,25,30],index=3)
    if particularNews:
        everything = newsapi.get_everything(q=particularNews, language='en',page_size=newsCount)
articles=""
if kind!="Particular Topic":
    articles= headlines['articles']

# if no headlines are there then we are giving the all the articles regarding that country

if not articles:
    # here we are needed to give try because when no topic is given in particular news then its showing error
    try:
        articles = everything['articles']
    except:
        pass

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
