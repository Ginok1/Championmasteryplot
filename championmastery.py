import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def scrape_data(summoner_name, region="EUW"):
    """ Scrapes data from championmastery.gg

    Parameters
    ----------
    summoner_name : str
                    Summoner name of the person you want the data from
    
    Returns
    -------
    pandas.DataFrame
    """
    adjusted_name = summoner_name.replace(" ", "+")
    result = requests.get(r"https://championmastery.gg/summoner?summoner={}&region={}".format(adjusted_name, region))
    df = pd.read_html(result.text)[0]
    return df[:-1]


def plot_mastery_distribution(summoners):
    """ Plots the Mastery rank distribution of given summoners in comparison

    Parameters
    ----------
    summoners : list of strings
                contains the Summoner names of the people you want to compare
    """
    for summoner_name in summoners:
        df = scrape_data(summoner_name)
        x, y = np.unique(df['Level'], return_counts=True)
        plt.plot(x, y, label=summoner_name)
    plt.legend()
    plt.grid()
    plt.xlabel("Mastery Rank")
    plt.ylabel("# of Champions")
    plt.show()


if __name__ == "__main__":
    summoners = ["Rivers Pride", "Psiteryder", "TeilschenFürUmme", "dieser Helge", "KIT MiLe", "Verynxia", "Chef Ainsley"]
    plot_mastery_distribution(summoners)
