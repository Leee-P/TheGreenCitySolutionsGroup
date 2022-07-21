import plotly.graph_objects as go
import seaborn as sns
import matplotlib.pyplot as plt

def plot_balance(timespan, adding, substracting, data):
    power_consumption = data.loc[timespan, adding].sum()
    power_generation = data.loc[timespan, substracting].sum()

    fig = go.Figure(go.Waterfall(
        name = "20", orientation = "v",
        measure = [*["relative"]*len(adding), "total", *["relative"]*len(substracting), "total"],
        x = [*adding, "Net consumption", *substracting, "grid power"],
        textposition = "outside",
        text = ["+", "+", "+", "=", "-", "="],
        y = [*power_consumption, 0, *[-i for i in power_generation], 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
    ))

    fig.update_layout(
            title = "Energy balance",
            showlegend = True
    )

    fig.show()

def plot_decomposition(seas_decomp_yearly):
    
    cmaps_hex = ['#193251','#FF5A36','#696969', '#7589A2','#FF5A36', '#DB6668']
    sns.set_palette(palette=cmaps_hex)
    sns_c = sns.color_palette(palette=cmaps_hex)

    # Plots:
    fig, ax = plt.subplots(4, 1, figsize=(12, 12), constrained_layout=True)

    #Plot Signal
    ax[0].set(title='Observed data (signal)', 
            ylabel='kWh')
    seas_decomp_yearly.observed.plot(color=sns_c[0], 
                                linewidth=1,
                                sharex=True,
                                ax=ax[0])
    #Plot Trend
    ax[1].set(title='Trend (364 days moving average)', 
            ylabel='kWh')
    seas_decomp_yearly.trend.plot(color=sns_c[1], 
                                linewidth=1,
                                sharex=True,
                                ax=ax[1])
    #Plot Seasonality
    ax[2].set(title='Seasonality', 
            ylabel='kWh')
    seas_decomp_yearly.seasonal.plot(
                                    color=sns_c[2], 
                                    linewidth=1,
                                    sharex=True,
                                    ax=ax[2])
    #Plot residual
    ax[3].set(title='Residual', 
            ylabel='kWh');
    ax[3].scatter(
        x=seas_decomp_yearly.resid.index,
        y=seas_decomp_yearly.resid,
        color=sns_c[3],
        s=4)