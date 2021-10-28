from django import forms

INTERVALS = (
    ('1m', '1 minute'),
    ('2m', '2 minute'),
    ('5m', '5 minute'),
    ('15m', '15 minute'),
    ('30m', '30 minute'),
    ('1h', '1 hour'),
    ('1d', '1 day'),
    ('5d', '5 day'),
    ('1wk', '1 week'),
    ('1mo', '1 month'),
    ('3mo', '3 month'),
)

PERIODS = (
    ('1d', '1 day'),
    ('5d', '5 day'),
    ('1mo', '1 month'),
    ('3mo', '3 month'),
    ('6mo', '6 month'),
    ('1y', '1 year'),
    ('2y', '2 year'),
    ('5y', '5 year'),
    ('10y', '10 year'),
    ('ytd', 'year-to-date'),
    ('max', 'Max'),
)
CHARTS = (
    ('Candlestick', 'Candlestick'),
    ('OHLC', 'OHLC'),
)

EQUITY_NAMES = (('ADANIPORTS.NS', 'Adani Ports and Special Economic Zone Ltd.'), ('ASIANPAINT.NS', 'Asian Paints Ltd.'), ('AXISBANK.NS', 'Axis Bank Ltd.'), ('BAJAJ-AUTO.NS', 'Bajaj Auto Ltd.'), ('BAJFINANCE.NS', 'Bajaj Finance Ltd.'), ('BAJAJFINSV.NS', 'Bajaj Finserv Ltd.'), ('BPCL.NS', 'Bharat Petroleum Corporation Ltd.'), ('BHARTIARTL.NS', 'Bharti Airtel Ltd.'), ('BRITANNIA.NS', 'Britannia Industries Ltd.'), ('CIPLA.NS', 'Cipla Ltd.'), ('COALINDIA.NS', 'Coal India Ltd.'), ('DIVISLAB.NS', "Divi's Laboratories Ltd."), ('DRREDDY.NS', "Dr. Reddy's Laboratories Ltd."), ('EICHERMOT.NS', 'Eicher Motors Ltd.'), ('GRASIM.NS', 'Grasim Industries Ltd.'), ('HCLTECH.NS', 'HCL Technologies Ltd.'), ('HDFCBANK.NS', 'HDFC Bank Ltd.'), ('HDFCLIFE.NS', 'HDFC Life Insurance Company Ltd.'), ('HEROMOTOCO.NS', 'Hero MotoCorp Ltd.'), ('HINDALCO.NS', 'Hindalco Industries Ltd.'), ('HINDUNILVR.NS', 'Hindustan Unilever Ltd.'), ('HDFC.NS', 'Housing Development Finance Corporation Ltd.'), ('ICICIBANK.NS', 'ICICI Bank Ltd.'), ('ITC.NS', 'ITC Ltd.'), ('IOC.NS',
                'Indian Oil Corporation Ltd.'), ('INDUSINDBK.NS', 'IndusInd Bank Ltd.'), ('INFY.NS', 'Infosys Ltd.'), ('JSWSTEEL.NS', 'JSW Steel Ltd.'), ('KOTAKBANK.NS', 'Kotak Mahindra Bank Ltd.'), ('LT.NS', 'Larsen & Toubro Ltd.'), ('M&M.NS', 'Mahindra & Mahindra Ltd.'), ('MARUTI.NS', 'Maruti Suzuki India Ltd.'), ('NTPC.NS', 'NTPC Ltd.'), ('NESTLEIND.NS', 'Nestle India Ltd.'), ('ONGC.NS', 'Oil & Natural Gas Corporation Ltd.'), ('POWERGRID.NS', 'Power Grid Corporation of India Ltd.'), ('RELIANCE.NS', 'Reliance Industries Ltd.'), ('SBILIFE.NS', 'SBI Life Insurance Company Ltd.'), ('SHREECEM.NS', 'Shree Cement Ltd.'), ('SBIN.NS', 'State Bank of India'), ('SUNPHARMA.NS', 'Sun Pharmaceutical Industries Ltd.'), ('TCS.NS', 'Tata Consultancy Services Ltd.'), ('TATACONSUM.NS', 'Tata Consumer Products Ltd.'), ('TATAMOTORS.NS', 'Tata Motors Ltd.'), ('TATASTEEL.NS', 'Tata Steel Ltd.'), ('TECHM.NS', 'Tech Mahindra Ltd.'), ('TITAN.NS', 'Titan Company Ltd.'), ('UPL.NS', 'UPL Ltd.'), ('ULTRACEMCO.NS', 'UltraTech Cement Ltd.'), ('WIPRO.NS', 'Wipro Ltd.'))

MA_TYPES = (
    ('SMA', 'Simple'),
    ('EMA', 'Exponential'),
)

MA_VALUES = (
    ('Open', 'Open'),
    ('High', 'High'),
    ('Low', 'Low'),
    ('Close', 'Close'),
)


class MainForm(forms.Form):

    equityName = forms.ChoiceField(
        choices=EQUITY_NAMES, widget=forms.Select(attrs={'class': 'custom-select'}), label='Equity Name', required=True, initial=EQUITY_NAMES[0][0]
    )

    interval = forms.ChoiceField(
        choices=INTERVALS, widget=forms.Select(attrs={'class': 'custom-select'}), label='Interval', required=True, initial=INTERVALS[0][0]
    )

    period = forms.ChoiceField(
        choices=PERIODS, widget=forms.Select(attrs={'class': 'custom-select'}), label='Period', required=True, initial=PERIODS[0][0])

    chartType = forms.ChoiceField(
        choices=CHARTS, widget=forms.Select(attrs={'class': 'custom-select'}), label='Chart', required=True, initial=CHARTS[0][0])

    rsiStatus = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input'}),
        required=False, label='RSI: Relative Strength Index', initial=False)
    macdStatus = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input'}),
        required=False, label='MACD: Moving Average Convergence Divergence', initial=False)

    ma1Status = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input'}), required=False, label='MA1: Moving Average', initial=False)
    ma2Status = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'class': 'custom-control-input'}),
        required=False, label='MA2: Moving Average', initial=False)

    rsiParameter = forms.IntegerField(
        required=False, min_value=1, max_value=100, label='RSI Parameter',
        initial='14', widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    macdParameters = forms.CharField(
        required=False, label='MACD Parameter',
        initial='12, 26, 9', widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    ma1Period = forms.IntegerField(
        required=False, min_value=1, max_value=100,
        initial='20', widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    ma1Type = forms.ChoiceField(
        choices=MA_TYPES, widget=forms.Select(attrs={'class': 'custom-select'}), required=False, initial=MA_TYPES[0][0]
    )

    ma1Parameter = forms.ChoiceField(
        choices=MA_VALUES, widget=forms.Select(attrs={'class': 'custom-select'}), required=False, initial=MA_VALUES[0][0]
    )

    ma2Period = forms.IntegerField(
        required=False, min_value=1, max_value=100,
        initial='50', widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    ma2Type = forms.ChoiceField(
        choices=MA_TYPES, widget=forms.Select(attrs={'class': 'custom-select'}), required=False, initial=MA_TYPES[0][0]
    )

    ma2Parameter = forms.ChoiceField(
        choices=MA_VALUES, widget=forms.Select(attrs={'class': 'custom-select'}), required=False, initial=MA_VALUES[0][0]
    )
