import streamlit as st
import yfinance as y
from keras.layers import Dense,LSTM
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import datetime

# Configuring
class config:
    def __init__(self):
        self.configuration = """ <style>
            header {visibility:hidden}
            footer {visibility: hidden}
            MainMenu {visibility:visible}</style>"""
        self.navBar="""
    <nav class="navbar fixed-top navbar-expand-lg navbar-light" style="background-color:#67EADA">
      <a class="navbar-brand" href="https://sandy0002-web-application-for-finance-homehome-jz9ii7.streamlit.app/" target="_self">Home  </a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
          <li class="nav-item ">
            <a class="nav-link" href="https://sandy0002-web-application-for-finance-news-ealg1b.streamlit.app/" target="_self">News</a>
          </li>
          <li class="nav-item ">
            <a class="nav-link" href="https://sandy0002-web-application-for-finance-analysis-nj6vsm.streamlit.app/" target="_self">Analysis</a>
          </li>
        </ul>
      </div>
    </nav>
    """

    def conf(self):
        st.set_page_config(page_title="  Forecast By InvestEd", page_icon=":mag_right:", layout="wide")
        st.markdown(self.configuration, unsafe_allow_html=True)
        st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
            unsafe_allow_html=True)
        st.markdown(self.navBar, unsafe_allow_html=True)

# Getting Ticker Data
class Asset:
    dic = {'1 Day': 1, '1 Week': 7, '15 Days': 15, '1 Month': 30, '2 Months': 60, '3 Months': 90}
    futInterval = None
    c=None
    def __init__(self):
        indexes = ["SENSEX","S&P 500", "NASDAQ-100", " "]
        index = st.sidebar.selectbox("Select Index", options=indexes, index=3)
        company=None
   
        st.sidebar.write("##")

        sensexUrl = pd.read_html('https://en.wikipedia.org/wiki/List_of_BSE_SENSEX_companies')
        sencomp = list(sensexUrl[0]['Companies'])
        sensym = list(sensexUrl[0]['Symbol'])
        sensex = {}
        for i, j in zip(sencomp, sensym):
            sensex[i] = j

        spUrl = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks')
        spcomp = spUrl[0]['Security']
        spsym = spUrl[0]['Symbol']
        sp = {}
        for i, j in zip(spcomp, spsym):
            sp[i] = j

        nasUrl = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100#Components')
        nasCom = nasUrl[4]['Company']
        nasSym = nasUrl[4]['Ticker']
        nasd = {}
        for i, j in zip(nasCom, nasSym):
            nasd[i] = j

        opt = []
        if index == "SENSEX":
            opt = [i for i in sensex.keys()]
            company = st.sidebar.selectbox("Select Company", options=opt)

        elif index == "S&P 500":
            # variable for ptr
            comp = st.sidebar.text_input("Enter Company Name")
            if comp:
                temp = ''
                t = comp[0].upper()
                t1 = comp[1:].lower()
                comp = t + t1
                if comp == "Google" or comp == "Alphabet":
                    if comp == 'Google':
                        comp = 'Alphabet Inc. (Class A)'
                    elif comp == 'Alphabet':
                        comp = 'Alphabet Inc. (Class C)'
                    temp = comp

                else:
                    i = 0
                    while i < len(sp):
                        if comp in spcomp[i]:
                            comp = spcomp[i]
                            temp = spcomp[i]
                        i += 1
                if temp == '':
                    st.write("# Currently unavailable")
            company=comp


        elif index == "NASDAQ-100":
            opt = [i for i in nasd.keys()]
            company = st.sidebar.selectbox("Select Company", options=opt)

        self.tickr=None
        if index=='SENSEX':
            self.tickr=sensex[company]
        elif index == "S&P 500":
            if comp:
                try:
                    self.tickr = sp[company]
                except Exception as e:
                    pass
        elif index == "NASDAQ-100":
            self.tickr = nasd[company]
        else:
            self.tickr = None

        st.sidebar.write("##")

        Asset.futInterval = st.sidebar.selectbox("Select The Period For Future Predictions", options=Asset.dic.keys())
        Asset.c=company
    def tick(self):
        if self.tickr != None :
            self.t = y.Ticker(self.tickr)
            return (self.t,Asset.c)

# Generating Data from ticker data
class Data:
    def __init__(self,tickr):
        self.data = tickr.history(period='5y', interval='1d')

    def getData(self):
        return self.data

# Model building
class Model:
    def __init__(self,data):
        self.data = data

    def create_dataset(dataset, time_step=1):
        dataX, dataY = [], []
        for i in range(len(dataset) - time_step - 1):
            a = dataset[i:(i + time_step), 0]  # i=0, 0,1,2,3-----99   100
            # appending i to i+100 value here
            dataX.append(a)
            # appending the i+100 value
            dataY.append(dataset[i + time_step, 0])
        return np.array(dataX), np.array(dataY)

    def makeModel (self):
        try:
            data = self.data
            d1 = data.reset_index()['Close']

            # our data is somewhat having a linear trend
            scaler = MinMaxScaler(feature_range=(0, 1))
            arrayD1 = np.array(d1)

            # this generates a 2d array where each element is a 1d array due to reshape
            sd1 = scaler.fit_transform(arrayD1.reshape(-1, 1))

            training_size = int(len(sd1) * 0.65)
            test_size = len(sd1) - training_size
            train_data, test_data = sd1[0:training_size, :], sd1[training_size:len(sd1), :1]

            # giving class name in which the method is to avoid errors we ues Model.create_dataset()
            X_train, y_train = Model.create_dataset(train_data, 100)
            X_test, ytest = Model.create_dataset(test_data, 100)

            X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
            X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

            model = Sequential()
            model.add(LSTM(50, return_sequences=True, input_shape=(100, 1), activation='sigmoid'))
            model.add(LSTM(50))
            model.add(Dense(1))
            model.compile(loss='mean_squared_error', optimizer='adam',metrics=['mape'])

            model.fit(X_train, y_train, validation_data=(X_test, ytest), epochs=30, batch_size=24, verbose=1,workers=4,
                      use_multiprocessing=True)

            return model
        except Exception as e:
            pass

# Generating future predicitions
class Forecast:
    def __init__(self, tickr, data,model):
        self.model = model
        st.sidebar.write("##")
        self.dic = Asset.dic
        # dic = {'1 Day': 1, '1 Week': 7, '15 Days': 15, '1 Month': 30, '2 Months': 60, '3 Months': 90}
        self.futInterval = Asset.futInterval
        # futInterval = st.sidebar.selectbox("Select the period for future predictions", options=dic.keys())
        # st.sidebar.write("##")
        # butt = st.sidebar.button("Enter")

        try:
            d1 = data.reset_index()['Close']
            scaler = MinMaxScaler(feature_range=(0, 1))
            arrayD1 = np.array(d1)
            sd1 = scaler.fit_transform(arrayD1.reshape(-1, 1))

            training_size = int(len(sd1) * 0.65)
            test_size = len(sd1) - training_size
            train_data, test_data = sd1[0:training_size, :], sd1[training_size:len(sd1), :1]

            # 819-101 =718
            # m= Model(data)
            X_train, y_train = Model.create_dataset(train_data, 100)
            X_test, ytest = Model.create_dataset(test_data, 100)

            X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
            X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

            x_input = test_data[len(test_data) - 100:].reshape(1, -1)
            temp_input = list(x_input)
            temp_input = temp_input[0].tolist()

            lst_output = []
            n_steps = 100
            i = 0
            while (i < self.dic[self.futInterval]):

                if (len(temp_input) > 100):
                    x_input = np.array(temp_input[1:])
                    x_input = x_input.reshape(1, -1)
                    x_input = x_input.reshape((1, n_steps, 1))
                    # print(x_input)
                    yhat = model.predict(x_input, verbose=0)
                    temp_input.extend(yhat[0].tolist())
                    temp_input = temp_input[1:]
                    lst_output.extend(yhat.tolist())
                    i = i + 1
                else:
                    x_input = x_input.reshape((1, n_steps, 1))
                    yhat = self.model.predict(x_input, verbose=0)
                    temp_input.extend(yhat[0].tolist())
                    lst_output.extend(yhat.tolist())
                    i = i + 1

            # we are having data till yesterday
            self.ls = []
            for i in range(self.dic[self.futInterval]):
                self.ls.append(pd.to_datetime(datetime.date.today()+datetime.timedelta(days=1)) + datetime.timedelta(days=i))
            ls1 = scaler.inverse_transform(lst_output)
            self.close = []
            for i in ls1:
                for j in i:
                    self.close.append(j)
            dates = {'Date': self.ls, 'Predictions': self.close}
            df = pd.DataFrame(dates)
            self.df = df.set_index('Date')
        except :
            pass

        # Display of results
    def forecast(self,company):
        try:

                st.header(f"**{company}**")
                st.write("##")

                st.write("##")
                st.header(f"Forecast for the next {self.futInterval}")
                st.header("Predictions Data")
                st.write(self.df)
                st.header("Plots of forecast")
                if self.dic[self.futInterval]>1:
                    st.line_chart(self.df['Predictions'])
                open = self.close[:len(self.close) - 1]
                open.insert(0, data['Close'][-1])
                low = [min(i, j) for i, j in zip(open, self.close)]
                high = [max(i, j) for i, j in zip(open, self.close)]
                fig = go.Figure(data=[go.Candlestick(
                    x=self.ls,
                    open=open,
                    close=self.close,
                    low=low,
                    high=high
                )])
                st.plotly_chart(fig)
        except:
            pass

# configuration object
con = config()
con.conf()
a = Asset()
st.sidebar.write("##")
butt = st.sidebar.button("Enter")
if butt:
    with st.empty():
        st.header('Please wait results are being prepared')
        tickr,company = a.tick()
        data = None
        if tickr:
            data = Data(tickr)
            data = data.getData()

        m = Model(data)
        model = m.makeModel()
        st.write('')
    f = Forecast(tickr, data, model)
    if company:
        f.forecast(company)
    st.write("# Unavailbable")
    
    
