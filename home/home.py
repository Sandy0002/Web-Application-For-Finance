# always install scikit-learn with sklearn
import streamlit as st
from streamlit_lottie import st_lottie
import requests as re


hideStyle="""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility:hidden;}
    footer {visibility:hidden;}
    </style>"""

st.set_page_config(page_title="Investant",page_icon=":moneybag:",layout="wide")
st.markdown(hideStyle,unsafe_allow_html=True)

st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)


# ef5b10
# add margin-left=800px for the li having Login
st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-light" style="background-color:#7E0994">
  <a class="navbar-brand" href="#" target="_self"><b><h4>Investant</h4><b></a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item ">
        <a class="nav-link" href="https://sandy0002-final-year-project-news-o8u51n.streamlitapp.com/">SignOn <span class="sr-only">(current)</span></a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)


def lott(url):
    r = re.get(url)
    if r.status_code!=200:
        return None
    return r.json()
lottieCode = lott("https://assets9.lottiefiles.com/packages/lf20_ewpkvfw4.json")
st.markdown("""
    <h1><i><b>Investments are accessible than ever.</b></i></h1>""",unsafe_allow_html=True)

with st.container():
    leftCol,rightCol =st.columns(2)
    with leftCol:
        st.header("What to do with this?")
        st.markdown("""
        As we have seen in the past few years. Life is uncertain.
        Anything can happen at anytime.We must be prepared. So when nobody comes to help it is
        our investments that aid us in hard times. We look forward to help you in  that with our tool
         which provides basic functionalities that is needed to get started investing.""",unsafe_allow_html=True)
        
        st.write("##")

        
        st.write("Watch the Importance Of Investment below  ")
        video="""
        <style>
        .iframe-container{
        position: relative;
        width: 100%;
        padding-bottom: 56.25%;
        height: 0;
        }
        .iframe-container iframe{
        position:absolute;
        top:0;
        left:0;
        width: 100%;
        height: 100%;
        }
        </style>
        <div class="iframe-container">
        <iframe width="560" height="315" src="https://www.youtube.com/embed/udfEG48f8UE" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
        </div>
        """

        st.markdown(video,unsafe_allow_html=True)
        st.write("##")
        st.header('With our web application:')
        st.write('User can get the prefrred news feed.')
        st.write('User can analyze various stocks of various exchanges and cryptos as well.')
        st.write('User can get the future predictions as well.')
        
        st.write('##')
        st.write('** Hurry up and get started today by signing on **')
   
        # now we are going to add animation using lottie
    with rightCol:
        st_lottie(lottieCode,height=350,key="Investing")
        
      
