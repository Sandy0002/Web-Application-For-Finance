import streamlit as st
import yfinance as y
import pandas as pd
import datetime
import wikipedia as wi
import requests as r
import plotly.graph_objs as go


st.set_page_config(page_title="Analysis with Investant",page_icon=":mag:",layout="wide")


def nif(company,tickrdf,low,high):
    st.header(company)
    st.write("##")
    try:
        st.info(wi.summary(company))
        st.write('##')
    except:
        pass

    st.header("**Stats**")
    if tickrdf['Close'][-1]:
        st.subheader("Previous Close Value")
        st.write(tickrdf['Close'][-1])
    st.write("##")
    if low:
        st.subheader("52 Week Low")
        st.write(low)
    st.write("##")
    if high:
        st.subheader("52 Week High")
        st.write(high)

    st.write("##")

    st.header("**Data**")
    st.write(tickrdf[['Open', 'Close']])
    st.header("Closing Values")
    st.write("Plots from ", stDate, "to ", end, "for ", company, "for closing values")
    st.line_chart(tickrdf['Close'])
    fig = go.Figure(data=[go.Candlestick(
        x=tickrdf.index,
        open=tickrdf['Open'],
        close=tickrdf['Close'],
        low=tickrdf['Low'],
        high=tickrdf['High']
    )])

    st.plotly_chart(fig)
    st.write("##")
    st.subheader("Volumes Exchanged")
    st.write(tickrdf['Volume'])
    st.line_chart(tickrdf['Volume'])
    st.bar_chart(tickrdf['Volume'])


hideStyle=""" <style>
    header {visibility:hidden}
    footer {visibility: hidden}
    #MainMenu {visibility:visible}"""

st.markdown(hideStyle,unsafe_allow_html=True)
st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-light" style="background-color:#D428C4">
  <a class="navbar-brand" href="https://sandy0002-final-year-project-homehome-fcjqd2.streamlitapp.com/" target="_self">Home  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item ">
        <a class="nav-link" href="https://sandy0002-final-year-project-news-o8u51n.streamlitapp.com/">News</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://sandy0002-final-year-project-forecast-favi2o.streamlitapp.com/">Forecast</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)

# defining functions for closing, Volume


asset = st.sidebar.radio("Select Asset",["Stocks","Cryptos"])
if asset=="Stocks":
    indexes = ["SENSEX","S&P 500","NASDAQ-100",""]
    index =st.sidebar.selectbox("Select Index",options=indexes,index=len(indexes)-1)

    sensexUrl = pd.read_html('https://en.wikipedia.org/wiki/List_of_BSE_SENSEX_companies')
    sencomp = list(sensexUrl[0]['Companies'])
    sensym = list(sensexUrl[0]['Symbol'])
    sensex ={}
    for i,j in zip(sencomp,sensym):
        sensex[i]=j


    spUrl=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks')
    spcomp = spUrl[0]['Security']
    spsym = spUrl[0]['Symbol']
    sp={}
    for i,j in zip(spcomp,spsym):
        sp[i]=j

    nasUrl = pd.read_html('https://en.wikipedia.org/wiki/Nasdaq-100#Components')
    nasCom = nasUrl[4]['Company']
    nasSym= nasUrl[4]['Ticker']
    nasd ={}
    for i,j in zip(nasCom,nasSym):
        nasd[i]=j

    if index=="SENSEX":
        opt = [i for i in sensex.keys()]


    elif index=="S&P 500":
        comp = st.sidebar.text_input("Enter Company Name")
        if comp not in spcomp:
                comp=None
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
        company = comp

    elif index=="NASDAQ-100":
        opt = [i for i in nasd.keys()]


    if index !="S&P 500" and index:
        company = st.sidebar.selectbox("Select Company",options=opt)


    # using yfinance for analysis from here

    stDate=st.sidebar.date_input("Start date",datetime.date(2022,1,1))
    endDate=st.sidebar.date_input("End date",datetime.date.today())

    # So in order to generate data of the ticker we need to pass the ticker
    tickr=''
    if index == "SENSEX":
        tickr = sensex[company]
        t = sensex[company]
    elif index == "S&P 500" and company :
        tickr = sp[company]
    elif index == "NASDAQ-100":
        tickr = nasd[company]
    else:
        tickr=None

    if tickr!=None:
        tickrData=y.Ticker(tickr)

    inter = {"1 Minute":'1m',"2 Minutes":'2m',"5 Minutes":'5m',"15 Minutes":'15m', "30 Minutes":'30m',
             "1 Hour":'1h',"1 Day":'1d',"5 Days": '5d',"1 Month":'1mo', "3 Months":'3mo'}
    intList = [i for i in inter.keys()]


    interval = st.sidebar.selectbox("Select interval of data",options=intList,index=8)
    st.write("##")
    if st.sidebar.button("Enter"):
        if stDate<endDate and ticker!=None:
            tickrdf = tickrData.history(period=interval,start=stDate,end=endDate)

            try:
                # Display of data
                if tickrData.info['logo_url']:
                    logo = '<img src=%s>' % tickrData.info['logo_url']
                    st.markdown(logo,unsafe_allow_html=True)

                name = tickrData.info['longName']
                st.header('**%s**' % name)

                if 'longBusinessSummary' in tickrData.info:
                    st.info(tickrData.info['longBusinessSummary'])
                else:
                    st.info(wi.summary(name))

                st.header("**Stats**")
                if tickrData.info['previousClose']:
                    st.subheader("Previous Close Value")
                    st.write(tickrData.info['previousClose'])
                st.write("##")
                if tickrData.info['fiftyTwoWeekLow']:
                    st.subheader("52 Week Low")
                    st.write(tickrData.info['fiftyTwoWeekLow'])
                st.write("##")
                if tickrData.info['fiftyTwoWeekHigh']:
                    st.subheader("52 Week High")
                    st.write(tickrData.info['fiftyTwoWeekHigh'])

                st.write("##")

                st.header("**Data**")
                st.write(tickrdf[['Open','Close']])
                st.header("Closing Values")
                st.write("Plots from ",stDate,"to ",endDate, "for ",company,"for closing values" )
                st.line_chart(tickrdf['Close'])
                fig = go.Figure(data=[go.Candlestick(
                    x=tickrdf.index,
                    open=tickrdf['Open'],
                    close=tickrdf['Close'],
                    low=tickrdf['Low'],
                    high=tickrdf['High']
                )])

                st.plotly_chart(fig)
                st.write("##")
                st.subheader("Volumes Exchanged")
                st.write(tickrdf['Volume'])
                st.line_chart(tickrdf['Volume'])
                st.bar_chart(tickrdf['Volume'])


                st.write("##")
                st.header("**Balence Sheet**")
                st.write(tickrData.balancesheet)

                st.write("##")
                st.header("**Quarterly Balence Sheet**")
                st.write(tickrData.quarterly_balancesheet)

                st.write("##")
                st.header("**Earnings**")
                st.write(tickrData.earnings)

                st.write("##")
                st.header("**Quarterly Earnings**")
                st.write(tickrData.quarterly_earnings)

                st.write("##")
                st.write(tickrData.shares)
                st.write(tickrData.institutional_holders)

                st.write(tickrData.get_major_holders())


                st.write("##")
                st.header("**Financial Statements**")
                st.write(tickrData.financials)

                st.write("##")
                st.header("**Quarterly Financial Statements**")
                st.write(tickrData.quarterly_financials)

                st.write("##")
                st.header("**Cash Flows**")
                st.write(tickrData.cashflow)

                st.write("##")
                st.header("**Quarterly Cash Flows**")
                st.write(tickrData.quarterly_cashflow)

                st.write("##")
                st.header("**Actions**")
                act = tickrData.actions
                st.write(tickrData.actions)
                if len(act)>1:
                    st.bar_chart(act['Dividends'])

                st.write('##')
                st.header("**Activities**")
                st.write(tickrData.recommendations)
            except:
                pass

        else:
            st.header('Not available')


elif asset=="Cryptos":
    countries = {'Australia': 'AUD', 'Canada': 'CAD',
                 'China': 'CNY', 'Germany': 'EUR', 'France': 'EUR',
                 'Indonesia': 'IDR', 'Israel': 'ILS', 'India': 'INR', 'Japan': 'JPY',
                 'New Zealand': 'NZD', 'Philippines': 'PHP',
                 'Russia': 'RUB', 'Saudi Arabia': 'SAR', 'Singapore': 'SGD', 'South Korea': 'KRW', 'Switzerland': 'CHF',
                 'Turkey': 'TRY', 'Taiwan': 'TWD', 'Ukraine': 'UAH', 'United Arab Emirates': 'AED',
                 'United Kingdom': 'GBP', 'United States': 'USD', 'South Africa': 'ZAR', '': ''}
    # currency Api key
    curKey = 'bd167aef0623e4cc6a2140e4b30055ba'
    # keys = [i for i in contryCodes.keys()]

    # getting the cryptos symbol
    crypSym = st.sidebar.text_input("Enter the crypto  symbol")

    # getting the name of the country for currrency
    curr = st.sidebar.selectbox("Select the Country for currency exchange", countries.keys(), index=len(countries) - 1)


    # we will use this url to get the results
    url = 'https://v6.exchangerate-api.com/v6/f3bb0e3c82bee3decd651e90/latest/USD'

    st.sidebar.write("##")

    strt = st.sidebar.date_input("Start Date of Data", datetime.date(2022, 1, 1))
    end = st.sidebar.date_input("End Date of Data", datetime.date.today())
    inter = {"1 Minute": '1m', "2 Minutes": '2m', "5 Minutes": '5m', "15 Minutes": '15m', "30 Minutes": '30m',
             "1 Hour": '1h', "1 Day": '1d', "5 Days": '5d', "1 Month": '1mo', "3 Months": '3mo'}
    intList = [i for i in inter.keys()]
    interval = st.sidebar.selectbox("Select interval of data", options=intList, index=8)

    class converter:
        def __init__(self, url):
            data = r.get(url).json()
            self.rates = data['conversion_rates']

        def convert(self, frm, to, amount):
            if frm != 'EUR':
                amount /= self.rates[frm]

            amount *= self.rates[to]
            return amount


    tickr = None
    def verifier(sym):
        # to verify if the data exists  we will find if the coin existed yesterday by finding if  closing value was
        # there
        tickr = y.Ticker(f'{sym.upper()}-USD')
        today = datetime.date.today()
        oneDay = datetime.timedelta(days=1)
        yesterday = today - oneDay

        data = tickr.history(period='1h', start=yesterday - oneDay, end=yesterday)
        if len(data):
            return True

        return

    flag = 0
    if crypSym and curr:
        tickr = y.Ticker(f'{crypSym.upper()}-USD')
        flag = verifier(crypSym)


    if st.sidebar.button("Enter") :
        if flag and strt<end:
            if countries[curr] != 'USD' and tickr:
                c = converter(url)
                frm = 'USD'
                to = countries[curr]
                amount = 1
                mf = c.convert(frm, to, amount)


            else:
                mf=1
            tickrData = tickr.history(period='1d', start=strt, end=end)
            dta =tickrData

            try:
                st.header(tickr.info['name'])
                st.subheader("Symbol")
                st.info(f'{crypSym.upper()}-{countries[curr]}')
            except:
                pass

            st.write("##")

            st.header("Last Closing Value")
            st.write(tickrData['Close'][-1]*mf)

            st.write('##')

            st.header("Description")
            if tickr.info['description']:
                st.info(tickr.info['description'])
            else:
                st.info(wi.summary(tickr['name']))
            st.write("##")

            st.header("Data")
            tickrData = tickr.history(period=interval, start=strt, end=end)
            # calculating multiplication factor for adding those to the data values in the df
            tickrData['High'] = tickrData['High'].apply(lambda x: x * mf)
            tickrData['Close'] = tickrData['Close'].apply(lambda x: x * mf)
            tickrData['Low'] = tickrData['Low'].apply(lambda x: x * mf)
            tickrData['Open'] = tickrData['Open'].apply(lambda x: x * mf)
            del tickrData['Dividends'], tickrData['Stock Splits']
            st.write(tickrData)

            st.header("Closings")
            st.write(tickrData[['Open', 'Close']])
            st.header("Closing Values")
            st.write("Plots from ", strt, "to ", end, "for ", tickr.info['name'], "for closing values")
            st.line_chart(tickrData['Close'])
            fig = go.Figure(data=[go.Candlestick(
                x=dta.index,
                open=dta['Open'],
                close=dta['Close'],
                low=dta['Low'],
                high=dta['High']
            )])
            st.plotly_chart(fig)
            st.write("##")
            st.header("Volumes Exchanged")
            st.line_chart(tickrData['Volume'])
            st.bar_chart(tickrData['Volume'])
            st.write("##")

            st.write("##")

            st.header("52 Weeks High")
            try:
                st.write(tickr.info['fiftyTwoWeekHigh']*mf)
            except:
                st.write('NA')

            st.write("##")
            st.header(" 52 Weeks Low")
            try:
                st.write(tickr.info['fiftyTwoWeekLow']*mf)
            except:
                st.write('NA')
        else:
            st.header('Not available')
