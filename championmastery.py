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


def plot_mastery_rank_distribution(summoners):
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


def plot_mastery_points_distribution(summoners, numberofchampions):
    """Makes some subplots to show interesting statistics

    Parameters
    ----------
    summoners : list of strings
                contains the Summoner names of the people you want to compare
    numberofchampions : int
                        number of champions currently in the game. Will be requested
                        from the Riot API in future updates 
    """
    fig, ax = plt.subplots(2,2)
    for summoner_name in summoners:
        df = scrape_data(summoner_name)
        # Mastery Points
        y = list(df['Points'])[::-1]
        y = [0] * (numberofchampions - len(y)) + y
        x = np.linspace(0, 1, len(y))
        ax[0][0].plot(x, y, "o-", ms=3, label=summoner_name)
        ax[0][0].set_yscale('log')
        ax[0][0].set_title("Mastery Points Distribution")
        # Mastery Rank
        xmr, ymr = np.unique(df['Level'], return_counts=True)
        xmr = [0] + list(xmr)
        ymr = [numberofchampions - sum(ymr)] + list(ymr)
        ax[0][1].plot(xmr, ymr, "o-", label=summoner_name)
        ax[0][1].set_xlabel("Mastery Rank")
        ax[0][1].set_ylabel("Number of Champions")
        ax[0][1].set_title("Mastery Rank Distribution")
        # Top 10 most played champions
        y10 = y[-10:]
        x10 = np.linspace(0, 1, len(y10))
        ax[1][0].plot(x10, y10, "o-", label=summoner_name)
        ax[1][0].set_title("Top 10 Mastery Points Distribution")
        ax[1][1].plot(x10, y10, "o-", label=summoner_name)
        ax[1][1].set_yscale('log')
        ax[1][1].set_title("Top 10 Mastery Points Distribution")
    for i in [0,1]:
        for j in [0,1]:
            if i == 0 and j == 1:
                pass
            else:
                ax[i][j].set_ylabel("Mastery Points")
                ax[i][j].set_xlabel("Champions ordered by Mastery Points")
                ax[i][j].set_xticks([])
                ax[i][j].legend()
            ax[i][j].grid(which="both")
    plt.show()


if __name__ == "__main__":
    summoners = ["Rivers Pride", "Psiteryder", "TeilschenFürUmme", "dieser Helge",
                 "KIT MiLe", "J0RMUNG4NDR", "D4ND3L10N", "nemzizXD",
                 "Snensenman", "w4rmduscher"]
    #plot_mastery_rank_distribution(summoners)
    plot_mastery_points_distribution(summoners, 160)
