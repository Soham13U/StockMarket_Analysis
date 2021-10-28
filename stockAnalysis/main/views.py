from django.shortcuts import render
from django.http import HttpResponse
import numpy as np
from . import forms
import plotly.graph_objects as go
from plotly.offline import plot
import yfinance as yf
from plotly.subplots import make_subplots


def calculateMA(df, period, type, parameter):
    if type == 'SMA':
        df['MA'] = df[parameter].rolling(
            window=period, min_periods=period).mean()
    elif type == 'EMA':
        df['MA'] = df[parameter].ewm(span=period, adjust=False).mean()
    return df


def calculateRsi(df, period):
    delta = df['Close'].diff()
    up = delta.clip(lower=0)
    down = -1*delta.clip(upper=0)
    ema_up = up.ewm(com=period, adjust=False).mean()
    ema_down = down.ewm(com=period, adjust=False).mean()
    rs = ema_up/ema_down
    df['RSI'] = 100 - (100/(1 + rs))

    return df


def calculateMACD(df, paramters):
    df['k'] = df['Close'].ewm(
        span=paramters[0], adjust=False, min_periods=paramters[0]).mean()
    df['d'] = df['Close'].ewm(
        span=paramters[1], adjust=False,  min_periods=paramters[1]).mean()
    df['MACD'] = df['d'] - df['k']
    df['Signal'] = df['MACD'].ewm(
        span=paramters[2], adjust=False, min_periods=paramters[1]).mean()
    df['Hist'] = df['MACD'] - df['Signal']
    return df


def generateTable(df, period):
    df = calculateRsi(df, period)
    df['date'] = df.index.date.astype(str)
    dfGroup = df.groupby(['date']).agg({
        'Close': ['mean', 'std', lambda x: x.iloc[0], lambda x: x.iloc[-1]],
        'RSI': ['mean'],
    }).round(2)
    dfGroup.columns = [x[1] for x in dfGroup.columns]
    dfGroup = dfGroup.reset_index()
    dfGroup.columns = ['Date', 'Mean Price',
                       'STD Price', 'Start', 'End', 'RSI Mean']
    dfGroup['Net Change'] = (dfGroup['Start'] - dfGroup['End']).round(2)
    dfGroup = dfGroup[['Date', 'Mean Price', 'STD Price',
                       'RSI Mean', 'Start', 'End', 'Net Change']]
    return dfGroup


def updateChart(form):
    plotCount = 2

    if form is None:
        form = forms.MainForm()
        print('Form is none')
        ticker = form.fields['equityName'].initial
        interval = form.fields['interval'].initial
        period = form.fields['period'].initial
        chartType = form.fields['chartType'].initial
        rsiStatus = form.fields['rsiStatus'].initial
        macdStatus = form.fields['macdStatus'].initial
        ma1Status = form.fields['ma1Status'].initial
        ma2Status = form.fields['ma2Status'].initial

    else:
        print('Form is not none')
        ticker = form.cleaned_data['equityName']
        interval = form.cleaned_data['interval']
        period = form.cleaned_data['period']
        chartType = form.cleaned_data['chartType']
        rsiStatus = form.cleaned_data['rsiStatus']
        macdStatus = form.cleaned_data['macdStatus']
        ma1Status = form.cleaned_data['ma1Status']
        ma2Status = form.cleaned_data['ma2Status']
        rsiParameter = form.cleaned_data['rsiParameter']
        macdParameters = form.cleaned_data['macdParameters']
        ma1Parameter = form.cleaned_data['ma1Parameter']
        ma1Type = form.cleaned_data['ma1Type']
        ma1Period = form.cleaned_data['ma1Period']
        ma2Parameter = form.cleaned_data['ma2Parameter']
        ma2Type = form.cleaned_data['ma2Type']
        ma2Period = form.cleaned_data['ma2Period']

    # Get the data from yfinance
    df = yf.download(ticker, interval=interval, period=period)

    # Define default parameters for chart
    specs = [[{}], [{}]]
    rowHeights = [2.0, 0.3]
    subplotTitles = [chartType, 'Volume']

    # Check if the user wants to see the RSI
    if(rsiStatus):
        # Increase plot count by 2
        plotCount += 2

        # Calculate the RSI
        df = calculateRsi(df, period=int(rsiParameter))
        # Calculate the table
        df_group = generateTable(df, period=int(rsiParameter))

        # Add the values for the RSI to the parameters
        specs.extend([[{}], [{"type": "table"}]])
        rowHeights.extend([0.3, 0.3])
        subplotTitles.extend(['RSI', ''])

    # Check if the user wants to see the MACD
    if(macdStatus):
        # Increase plot count by 1
        plotCount += 1

        # Calculate the MACD
        df = calculateMACD(df, [int(x) for x in macdParameters.split(',')])

        # Add the values for the MACD to the parameters
        rowHeights.append(0.3)
        if not rsiStatus:
            specs.append([{}])
            subplotTitles.append('MACD')
        else:
            specs.insert(-1, [{}])
            subplotTitles.insert(-1, 'MACD')

    # Create subplots for the chart
    fig = go.Figure(make_subplots(
        rows=plotCount, cols=1, shared_xaxes=True,
        vertical_spacing=0.06,
        specs=specs,
        row_heights=rowHeights,
        subplot_titles=subplotTitles
    ))

    chartName = dict(form.fields['equityName'].choices)[
        ticker] + ' ' + chartType
    # Add the Candlestick or OHLC chart to the figure
    if chartType == 'Candlestick':
        fig.add_trace(
            go.Candlestick(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'], name=chartName,
                increasing_line_color='rgb(27,158,119)', decreasing_line_color='rgb(204,80,62)'
            ), row=1, col=1,

        )
    elif chartType == 'OHLC':
        fig.add_trace(
            go.Ohlc(
                x=df.index, open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Close'], name=chartName,
                increasing_line_color='rgb(27,158,119)', decreasing_line_color='rgb(204,80,62)'
            ), row=1, col=1,
        )

    # Add the Volume chart to the figure
    fig.add_trace(
        go.Bar(
            x=df.index, y=df['Volume'],
            marker_color='orange', showlegend=False),
        row=2, col=1
    )

    # Check if user wants to see Moving Average 1
    if(ma1Status):
        # Calculate the Moving Average 1
        df = calculateMA(df, period=int(ma1Period),
                         parameter=ma1Parameter, type=ma1Type)

        # Add the Moving Average 1 chart to the figure
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['MA'], name='Moving Avg(1)'),
            row=1, col=1
        )

    # Check if user wants to see Moving Average 2
    if(ma2Status):
        # Calculate the Moving Average 2
        df = calculateMA(df, period=int(ma2Period),
                         parameter=ma2Parameter, type=ma2Type)
        # Add the Moving Average 2 chart to the figure
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['MA'], name='Moving Avg(2)'),
            row=1, col=1
        )

    # Check if user wants to see RSI
    if rsiStatus:
        # Find the row index for the RSI plot
        rowIndex = plotCount - 2 if macdStatus else plotCount - 1

        # Add the RSI plot to the figure
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['RSI'],
                name='RSI', marker_color='#109618'
            ), row=rowIndex, col=1,
        )

        # Add the plot for the overbought and oversold lines
        fig.add_trace(
            go.Scatter(
                x=df.index, y=[70] * len(df.index),
                name='Overbought', marker_color='#109618',
                line=dict(dash='dot'),
            ), row=rowIndex, col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=df.index, y=[30] * len(df.index),
                name='Oversold', marker_color='#109610',
                line=dict(dash='dot'),
            ), row=rowIndex, col=1,
        )

        # Add the Table to the figure
        fig.add_trace(
            go.Table(
                header=dict(
                    values=list(df_group.columns),
                    fill_color='#C2D4FF',
                    font=dict(size=10), align="left"),
                cells=dict(
                    fill_color='#F5F8FF',
                    values=[df_group[k].tolist() for k in df_group.columns[0:]], align="left")
            ), row=plotCount, col=1
        )

    # Check if user wants to see MACD
    if macdStatus:
        # Find the row index for the MACD plot
        rowIndex = plotCount - 1 if rsiStatus else plotCount

        # Add the MACD plot to the figure
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['MACD'],
                name='MACD', marker_color='#ff9900'
            ), row=rowIndex, col=1,
        )

        # Add the MACD Signal plot to the figure
        fig.add_trace(
            go.Scatter(
                x=df.index, y=df['Signal'],
                name='Signal', marker_color='#000000',
                line=dict(dash='dot'),
            ), row=rowIndex, col=1,
        )

        # Calculate colors based on the MACD histogram values
        colors = np.where(df['Hist'] < 0, '#000', '#ff9900')

        # Add the MACD Histogram plot to the figure
        fig.append_trace(
            go.Bar(
                x=df.index,
                y=df['Hist'],
                name='Histogram',
                marker_color=colors,
            ), row=rowIndex, col=1
        )

    # Update the X-axis values based on values of interval
    # fig.update_xaxes(
    #     rangebreaks=[
    #         dict(bounds=[16, 9], pattern="hour"),
    #         dict(bounds=["sat", "mon"]),
    #     ]
    # )

    # Update the layout
    fig.update_layout(
        title=dict(form.fields['equityName'].choices)[ticker] + ' Report',
        xaxis={
            'rangeslider': {'visible': False},
            'type': 'date'
        },
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=1300,
        width=1500,
    )

    # Return the figure
    return plot(fig, output_type='div')


def main(request):
    if request.method == 'POST':
        print('POST')
        form = forms.MainForm(request.POST)
        if form.is_valid():
            print('valid')
            context = {'form': form, 'chart': updateChart(
                form), 'title': dict(form.fields['equityName'].choices)[form.cleaned_data['equityName']]}
            return render(request, 'main/index.html', context)

    print('GET')
    form = forms.MainForm()
    context = {'form': form, 'chart': updateChart(
        None), 'title': form.fields['equityName'].choices[0][1]}
    return render(request, 'main/index.html', context)
