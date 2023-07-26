# Web Application For Finance

## Table Of Content

+ [Demo](#demo)
+ [Overview](#overview)
+ [Motivation](#motivation)
+ [Technical Aspects](#technincal)
+ [Installation](#installation)
+ [Execution](#running)
+ [Deployment on Streamlit Cloud](#deploy)
+ [Technologies Used](#tech)
+ [Team](#team)
+ [LICENSE](LICENSE)
+ [DISCLAIMER](#disclaimer)


<a id="demo"></a><h2>Demo</h2>

### Home Page
![Home page](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/99340e92-69bf-447c-9904-a4a0d043bcec)

**News Page**
![News page](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/799418ff-e93c-4de7-96f4-6d31da9ca0f4)


**News Feed Example**
![News Feed Example](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/5e197598-039b-434d-90f6-e9f985587940)

**Asset Analysis Page**
![Asset Analysis Page](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/d6c0e1ec-dd04-4ade-8182-3925e497451b)

**Sample Analaysis**
![Sample Analysis](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/74d1d1b5-c039-41ae-a221-525379509e77)

**Forecasting Page**
![forecasting page](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/cf31a57e-b4b0-4b0b-a1b9-5caae3f38259)

**Forecasts Generating**
![Forecast Generating](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/0b60890c-d26d-4a14-9136-dbf74ad05627)


**Forecasts**
![result1](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/63809156-a304-4c6f-96a5-0f838c9208c6)

![result2](https://github.com/Sandy0002/Web-Application-For-Finance/assets/110614803/f327defb-f4e7-45a5-8bce-214939eb53be)

App [link](https://sandy0002-web-application-for-finance-homehome-jz9ii7.streamlit.app/)
<a id="overview"></a><h2>Overview</h2>
This is a web application built extending my final year project. In that only stock price prediction across exchanges is being done. Here features extension have been done by adding functionalities such as desired news feed, stocks and crytpos analysis by providing visuals and data. For stocks data balance sheets,financial statements etc are also returned.

<a id="motivation"></a><h2>Motivation</h2>
An investor never simply invests anywhere they need to do some analysis, stay updated with the news such as what's going on out there and also need to have idea what might the future trend of the asset. With all that in mind this project have been made.

<a id="technincal"></a><h2>Technical Aspects</h2>

Whole project is written using only python programming language.

### Project Working
The working of the project have 4 pages which are explained one after other in sequence

+ **Home Page**
  + The home page works using 3 libraries. The streamlit library is for providing user interface of the page. The **streamlit_lotte** is for the GIF on the page. And requests have been used for the web requests purposes such as getting the yoututube video. Upon signing on user lands on the news feed page.

+ **News Page** \
  Here user can get various kinds of news based on the requirements. The news types are divided into 3 types which are explained below
  + **International News** : In this user gets international news based on the prefernce of the category selected.
  + **Local News** : In this users gets news related to India based on the selected category.
  + **Particular News** : This is if a user wants to read particular news then they can search for that using it.

+ **Analysis Page** 
  + Here users can get the information and insights about the stocks and crypto currencies.
  
+ **Forecasting Page**

  + **Fetching Data** : Program takes the user inputs such as the stock exchange, company name and forecast interval. **yFinance** library is used to fetch the data of the stock. By default we are taking only 5 years of data of  a stock for prediction
  
  + **Preprocessing Data** : Upon fetching data we need to preprocess it.We are using LSTM as they are suitable for time-series-analysis. So we need to convert the data into LSTM compatible format.

  + **Training Model** : After preprocessing the data is sent to the model for training it.

  + **Generating forecasts and displaying** :
  After training the past data is used to forecast the future values.
  

<a id="installation"></a><h2>Installation</h2>
The Code is written in Python 3.10. If you don't have Python installed you can find it [here](https://www.python.org/downloads/). If you are using a lower version of Python you can upgrade using the pip package, ensuring you have the latest version of pip. To install the required packages and libraries, run this command in the project directory after [cloning](https://www.howtogeek.com/451360/how-to-clone-a-github-repository/) the repository:

``` pip install -r requirements.txt```


<a id="running"></a><h2>Execution</h2>

```streamlit run appName.py```

<a id="deploy"></a><h2>Deployment on Streamlit Cloud</h2>

+ Create an account on streamlit
+ Connect your github account with the streamlit account.
+ Create an app by selecting the respective settings such as repository, path of the code etc.

**Note**: For guidance check [here](#https://www.youtube.com/watch?time_continue=1&v=kXvmqg8hc70&embeds_referring_euri=https%3A%2F%2Fwww.bing.com%2F&embeds_referring_origin=https%3A%2F%2Fwww.bing.com&source_ve_path=Mjg2NjY&feature=emb_logo)


<a id="tech"></a><h2>Technologies Used</h2>

| Libraries        | Usage       
| ------------- |:-------------:|
**Numpy**  | Used for numerical computations in python
 **Pandas** | Used for file reading and other operations when working with large data.
 **Sklearn** | This is a machine learning library for python.
 **Plotly** | Interactive data visualization library
 **TensorFlow** | Deep Learning library from which model has been built
 **Streamlit** | Framework for providing interface of the web app
 **Datetime** | For datetime operations
 **yFinance** | For fetching stock data
 **Streamlit Lottie** | Used for generating gifs on the web pages
 **Requests** | Used during for fetching the data from web
 **Wikipedia** | To get information about a topic from wikipedia
 **News Api** | This is an api used for getting the news feed from newsapi website.

<a id="team"></a><h2>Team</h2>
**P. Sandeep Murthy**


<a id="license"></a><h2>LICENSE</h2>
[MIT LICENSE](LICENSE)

<a id="disclaimer"></a><h2>Disclaimer</h2>
+ The video in the home page used for telling the importance of Investment is used just for educational purposes. This is not promotion of Edelweiss as it is taken for educational purposes only.
+  The predictions being done here are not for financial purposes rather they are just for demonstration purposes.
