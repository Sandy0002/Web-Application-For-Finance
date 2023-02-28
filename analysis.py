import streamlit as st
import yfinance as y
import pandas as pd
import datetime
import wikipedia as wi
import requests as re
import plotly.graph_objs as go

# Page setting
st.set_page_config(page_title="Analysis with InvestEd", page_icon=":mag:", layout="wide")

y.pdr_override()

hideStyle = """ <style>
    header {visibility:hidden}
    footer {visibility: hidden}
    #MainMenu {visibility:visible}"""

key = "C3F2S4QE73ESDY9G"

st.markdown(hideStyle, unsafe_allow_html=True)
st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True)

st.markdown(hideStyle, unsafe_allow_html=True)
st.markdown(
    '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
    unsafe_allow_html=True)

st.markdown("""
<nav class="navbar fixed-top navbar-expand-lg navbar-light" style="background-color:#D428C4">
  <a class="navbar-brand" href="https://sandy0002-web-application-for-finance-homehome-jz9ii7.streamlit.app/" target="_self">Home  </a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>
  <div class="collapse navbar-collapse" id="navbarNav">
    <ul class="navbar-nav">
      <li class="nav-item ">
        <a class="nav-link" href="https://sandy0002-web-application-for-finance-news-ealg1b.streamlit.app/" target="_self" >News</a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="https://sandy0002-web-application-for-finance-forecast-ooclvh.streamlit.app/" target="_self">Forecast</a>
      </li>
    </ul>
  </div>
</nav>
""", unsafe_allow_html=True)


# Fetching the asset to be analyzed
asset = st.sidebar.radio("Select Asset", ["Stocks", "Cryptos"])
if asset == "Stocks":
    indexes = ["SENSEX", "S&P 500", "NASDAQ-100", ""]
    index = st.sidebar.selectbox("Select Index", options=indexes, index=len(indexes) - 1)
    company=None
    
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

    if index == "SENSEX":
        opt = [i for i in sensex.keys()]

    elif index == "S&P 500":
        comp = ''
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
                st.write("# Unavailable")
        company = comp

    elif index == "NASDAQ-100":
        opt = [i for i in nasd.keys()]

    if index != "S&P 500" and index:
        company = st.sidebar.selectbox("Select Company", options=opt)

    # using yfinance for analysis from here
    stDate = st.sidebar.date_input("Start date", datetime.date(2022, 1, 1))
    endDate = st.sidebar.date_input("End date", datetime.date.today())

    # So in order to generate data of the ticker we need to pass the ticker
    companyTicker = ''
    if index == "SENSEX":
        companyTicker = sensex[company]
        t = sensex[company]
    elif index == "S&P 500" and company in sp:
        companyTicker = sp[company]
    elif index == "NASDAQ-100":
        companyTicker = nasd[company]
    else:
        companyTicker = None
    
    tickr=None
    # Generating ticker object
    if companyTicker != None:
        tickr = y.Ticker(companyTicker)

    tickrdf =None
  
    # This statment works as a button and activates when "Enter" is pressed
    if st.sidebar.button("Enter") and companyTicker!=None:
        tickrData = tickr.fast_info
        if stDate < endDate:
            st.header(f"**{company}**")

            # fetching stock history data
            tickrdf = tickr.history(start=stDate, end=endDate)
            try:
                try:
                    st.info(wi.summary(company))
                except: pass

                st.write("##")
                st.header("**Stats**")
                if tickrData['previousClose']:
                    st.subheader("Previous Close Price")
                    st.write(tickrData['previousClose'])
                st.write("##")

                if tickrData['dayLow']:
                    st.subheader("Today's low value:")
                    st.write(tickrData['dayLow'])
                st.write("##")

                if tickrData['dayHigh']:
                    st.subheader("Today's high value:")
                    st.write(tickrData['dayHigh'])
                st.write("##")

                if tickrData['yearLow']:
                    st.subheader("52 Week Low")
                    st.write(round(tickrData['yearLow'], 2))
                st.write("##")
                if tickrData['yearHigh']:
                    st.subheader("52 Week High")
                    st.write(round(tickrData['yearHigh'], 2))

                st.write("##")
                st.header("**Data**")
                st.write(tickrdf)
                st.header("**Closing Values**")
                st.write("Plots from ", stDate, "to ", endDate, "for ", company, "for closing values")
                st.line_chart(tickrdf['Close'])
                fig = go.Figure(data=[go.Candlestick(
                    x=tickrdf.index,
                    open=tickrdf['Open'],
                    close=tickrdf['Close'],
                    low=tickrdf['Low'],
                    high=tickrdf['High']
                )])

                st.plotly_chart(fig)
                st.subheader("**Volumes Exchanged**")
                st.write(tickrdf['Volume'])
                st.write("##")
                st.line_chart(tickrdf['Volume'])
                st.write("##")
                st.bar_chart(tickrdf['Volume'])

                sheetUrl = 'https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={0}&apikey={1}'.format(companyTicker, key)
                req1 = re.get(sheetUrl)
                sheetData = req1.json()
                try:
                    st.write("##")
                    st.header("**Annual Balence Sheets**")
                    annualDf = pd.DataFrame(sheetData['annualReports'])
                    balanceSheetColumns = {'fiscalDateEnding': 'Fiscal Year', 'reportedCurrency': 'Reported Currency',
                                            'totalAssets': 'Assets', 'totalCurrentAssets': 'Current Assets',
                                           'cashAndCashEquivalentsAtCarryingValue': 'Cash and Equivalent Value',
                                           'cashAndShortTermInvestments': 'Cash & Short Term Investments',
                                           'inventory': 'Inventory', 'currentNetReceivables': 'Net Recievables',
                                           'totalNonCurrentAssets': 'Non-Current Assets',
                                           'propertyPlantEquipment': 'Property Plant Equipment',
                                           'accumulatedDepreciationAmortizationPPE': 'Depreciation Amortization PPE',
                                           'intangibleAssets': 'Intangible Assets',
                                           'intangibleAssetsExcludingGoodwill': 'Asset Excluding GoodWill',
                                           'goodwill': 'Good Will', 'investments': 'Investments',
                                           'longTermInvestments': 'Long Term Investments',
                                           'shortTermInvestments': 'Short Term Investments',
                                           'otherCurrentAssets': 'Other Current Assets',
                                           'otherNonCurrentAssets': 'Other Non-Current Assets',
                                           'totalLiabilities': 'Liabilities',
                                           'totalCurrentLiabilities': 'Current Liabilities',
                                           'currentAccountsPayable': 'Current Accounts Payable',
                                           'deferredRevenue': 'Deferred Revenue', 'currentDebt': 'Current Debt',
                                           'shortTermDebt': 'Short-Term Debt',
                                           'totalNonCurrentLiabilities': 'Non-Current Liabilities',
                                           'capitalLeaseObligations': 'Capital Lease Obligations',
                                           'longTermDebt': 'Long-Term Debt',
                                           'currentLongTermDebt': 'Current Long-Term Debt',
                                           'longTermDebtNoncurrent': 'Long-Term Debt Noncurrent',
                                           'shortLongTermDebtTotal': 'Short Long-Term Debt Total',
                                           'otherCurrentLiabilities': 'Other Current Liabilities',
                                           'otherNonCurrentLiabilities': 'Other Non-Current Liabilities',
                                           'totalShareholderEquity': 'Share Holder Equity',
                                           'treasuryStock': 'Treasury Stock', 'retainedEarnings': 'Retained Earnings',
                                           'commonStock': 'Common Stock',
                                           'commonStockSharesOutstanding': 'Outstanding Stocks'}


                    annualDf.rename(columns=balanceSheetColumns, inplace=True)
                    st.dataframe(annualDf)

                    st.write("##")
                    st.header("**Quarterly Balence Sheet**")
                    quarterDf = pd.DataFrame(sheetData['quarterlyReports'])
                    quarterDf.rename(columns=balanceSheetColumns, inplace=True)
                    st.dataframe(quarterDf)
                except: pass

                incomeUrl = "https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={0}&apikey={1}".format(companyTicker, key)
                req2 = re.get(incomeUrl)
                incomeData = req2.json()
                try:
                    st.write("##")
                    st.header("**Annual Income Statements**")

                    annualdf = pd.DataFrame(incomeData['annualReports'])

                    incomeStmtColumns = {'fiscalDateEnding': 'Fiscal Date', 'reportedCurrency': 'Reported Currency',
                                         'grossProfit': 'Gross Profit',
                                         'totalRevenue': 'Total Revenue', 'costOfRevenue': 'Cost Of Revenue',
                                         'costofGoodsAndServicesSold': 'Goods And Services Sold',
                                         'operatingIncome': 'Operating Income',
                                         'sellingGeneralAndAdministrative': 'General And Administrative Sold',
                                         'researchAndDevelopment': 'R & D',
                                         'operatingExpenses': 'Operating Expenses',
                                         'investmentIncomeNet': 'Net Investment Income',
                                         'netInterestIncome': 'Net Interest Income', 'interestIncome': 'Interest Income',
                                         'interestExpense': 'Interest Expense', 'nonInterestIncome': 'Non-Interest Income',
                                         'otherNonOperatingIncome': 'Other Non0OperatingIncome',
                                         'depreciation': 'Depreciation',
                                         'depreciationAndAmortization': 'Depreciation And Amortization',
                                         'incomeBeforeTax': 'Income Before Tax',
                                         'incomeTaxExpense': 'Income Tax Expense',
                                         'interestAndDebtExpense': 'Interest & Debt Expense',
                                         'netIncomeFromContinuingOperations': 'Income From ContinuingOperations',
                                         'comprehensiveIncomeNetOfTax': 'Net Income Of Tax',
                                         'ebit': 'EBIT', 'ebitda': 'EBITDA', 'netIncome': 'Net Income'}

                    annualDf.rename(columns=incomeStmtColumns, inplace=True)
                    st.dataframe(annualDf)

                    st.write("##")
                    st.header("**Quarterly Income Statement**")
                    quarterDf = pd.DataFrame(incomeData['quarterlyReports'])
                    quarterDf.rename(columns=incomeStmtColumns, inplace=True)
                    st.dataframe(quarterDf)

                except: pass
                cashFlowUrl='https://www.alphavantage.co/query?function=CASH_FLOW&symbol={0}&apikey={1}'.format(companyTicker,key)
                req3 = re.get(cashFlowUrl)
                cashFlowData = req3.json()
                try:
                    st.write("##")
                    st.header("**Annual CashFlow**")
                    annualdf = pd.DataFrame(cashFlowData['annualReports'])
                    cashflowColumns = {'fiscalDateEnding': 'Fiscal Date Ending', 'reportedCurrency': 'Reported Currency',
                                       'operatingCashflow': 'Operating CashFlow',
                                       'paymentsForOperatingActivities': 'Operating Activities Payments',
                                       'proceedsFromOperatingActivities': 'Operating Activities Proceeds',
                                       'changeInOperatingLiabilities': 'Operating Liabilities Changes',
                                       'changeInOperatingAssets': 'Operating Assets Changes',
                                       'depreciationDepletionAndAmortization': 'Depreciation Depletion & Amortization',
                                       'capitalExpenditures': 'Capital Expenditures',
                                       'changeInReceivables': 'Receivables Changes',
                                       'changeInInventory': 'Inventory Changes',
                                       'profitLoss': 'Profit-Loss', 'cashflowFromInvestment': 'Cashflow From Investment',
                                       'cashflowFromFinancing': 'Cashflow From Financing',
                                       'proceedsFromRepaymentsOfShortTermDebt': 'Short Term Debt Repayments Proceeds',
                                       'paymentsForRepurchaseOfCommonStock': 'Repurchase Of CommonStock Payments',
                                       'paymentsForRepurchaseOfEquity': 'Equity Repurchase Payments',
                                       'paymentsForRepurchaseOfPreferredStock': 'Preferred Stock Repurchase Payments',
                                       'dividendPayout': 'Dividend Payout',
                                       'dividendPayoutPreferredStock': 'Preferred Stocks Payout',
                                       'proceedsFromIssuanceOfCommonStock': 'Issuance Of Common Stocks Proceeds',
                                       'proceedsFromIssuanceOfLongTermDebtAndCapitalSecuritiesNet': 'Net Issuance Of Long-Term Debt And Capital Securities',
                                       'proceedsFromIssuanceOfPreferredStock': 'Issuance Of Preferred Stocks Proceeds',
                                       'proceedsFromRepurchaseOfEquity': 'Equity Repurchase Proceeds',
                                       'proceedsFromSaleOfTreasuryStock': 'Treasuary Stock Sale Proceeds',
                                       'changeInCashAndCashEquivalents': 'Cash And Cash Equivalents Changes',
                                       'changeInExchangeRate': 'Change In ExchangeRate', 'netIncome': 'Net Income'}

                    annualDf.rename(columns=cashflowColumns, inplace=True)
                    st.dataframe(annualDf)

                    st.write("##")
                    st.header("**Quarterly CashFlow**")
                    quarterDf = pd.DataFrame(cashFlowData['quarterlyReports'])
                    quarterDf.rename(columns=cashflowColumns, inplace=True)
                    st.dataframe(quarterDf)
                except: pass

                earningsUrl ='https://www.alphavantage.co/query?function=EARNINGS&symbol={0}&apikey={1}'.format(companyTicker,key)
                req = re.get(earningsUrl)
                earningsData = req.json()
                try:
                    st.write("##")
                    st.header("**Annual Earnings**")
                    annualDf = pd.DataFrame(earningsData['annualEarnings'])
                    earningsColumns = {'fiscalDateEnding': 'Fiscal Date Ending', 'reportedEPS': 'EPS'}
                    annualDf.rename(columns=earningsColumns, inplace=True)
                    st.dataframe(annualDf)

                    st.write("##")
                    st.header("**Quarterly Earnings**")
                    quarterDf = pd.DataFrame(earningsData['quarterlyEarnings'])
                    col ={'fiscalDateEnding':'Fiscal Date Ending','reportedEPS':'EPS','reportedDate':'Reported Date',
                      'estimatedEPS':'Estimated EPS','surprise':'Surprise','surprisePercentage':'Surprise Percentage'}
                    quarterDf.rename(columns=col, inplace=True)
                    st.dataframe(quarterDf)
                except:pass
            except: pass
        else:
            st.header("Unavailable")

# if we choose cryto-currencies to look for
else:
    countries = {'Australia': 'AUD', 'Canada': 'CAD',
                 'China': 'CNY', 'Germany': 'EUR', 'France': 'EUR',
                 'Indonesia': 'IDR', 'Israel': 'ILS', 'India': 'INR', 'Japan': 'JPY',
                 'New Zealand': 'NZD', 'Philippines': 'PHP',
                 'Russia': 'RUB', 'Saudi Arabia': 'SAR', 'Singapore': 'SGD', 'South Korea': 'KRW', 'Switzerland': 'CHF',
                 'Turkey': 'TRY', 'Taiwan': 'TWD', 'Ukraine': 'UAH', 'United Arab Emirates': 'AED',
                 'United Kingdom': 'GBP', 'United States': 'USD', 'South Africa': 'ZAR', '': ''}

    curKey = 'bd167aef0623e4cc6a2140e4b30055ba'

    # getting the cryptos symbol
    crypSym = st.sidebar.text_input("Enter the crypto  symbol")
    crypSym = crypSym.upper()

    # getting the name of the country for currrency
    curr = st.sidebar.selectbox("Select the Country for currency exchange", countries.keys(), index=len(countries) - 1)

    # taking the start and end dates for data
    startDate = st.sidebar.date_input("Start date", datetime.datetime(2022, 1, 1))
    endDate = st.sidebar.date_input("End date", datetime.datetime.today())

    # Creating crypto string with currency to be used
    crypto = "{0}-{1}".format(crypSym, countries[curr])

    if st.sidebar.button("Enter"):
        try:
            tickrData = y.download(crypto,start=startDate,end=endDate)
        except:
            st.header("Unvailable")
       
        if tickrData:
            st.header("**Data**")
            st.write(tickrData)

            st.write("##")

            st.header("**Previous Closing Price**")
            st.write(tickrData['Close'][-1])

            st.write('##')
            st.header("Closings")
            st.write(tickrData[['Open', 'Close']])

            st.header("Closing Values")
            st.write("Plots from ", startDate, "to ", endDate, "for closing values")
            st.line_chart(tickrData['Close'])

            dta = tickrData
            fig = go.Figure(data=[go.Candlestick(
                x=dta.index,
                open=dta['Open'],
                close=dta['Close'],
                low=dta['Low'],
                high=dta['High']
            )])
            st.plotly_chart(fig)
            st.write("##")
            st.header("**Volumes Exchanged**")
            st.line_chart(tickrData['Volume'])
            st.write("##")
            st.bar_chart(tickrData['Volume'])

        
