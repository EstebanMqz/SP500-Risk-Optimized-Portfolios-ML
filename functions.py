"""
# -- -------------------------------------------------------------------------------------------------------------- -- #   
# -- project: S&P500-Risk-Optimized-Portfolios-PostCovid-ML.                                                        -- #           
# -- script: data.py : Python script with general functions for the proj.                                           -- #                 
# -- author: EstebanMqz                                                                                             -- #  
# -- license: CC BY 3.0                                                                                             -- #
# -- repository: https://github.com/EstebanMqz/SP500-Risk-Optimized-Portfolios-PostCovid-ML/blob/main/functions.py  -- #           
# -- ----------------------------------------------------------------------------------------------------------------- #  
"""

import glob, os, sys, warnings
import pipreqs
pipreqs.__path__ = ['/path/to/pipreqs']

#Dependencies
import visualizations as vs
import data as dt


# Libraries in functions.py
import numpy as np
import pandas as pd


import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use("dark_background")

import plotly.graph_objects as go 
import plotly.express as px

import scipy
import scipy.stats as st
from scipy import optimize
from scipy.optimize import minimize

import sklearn
from sklearn.neighbors import KernelDensity
from sklearn.model_selection import GridSearchCV
from sklearn import metrics

from yahoofinancials import YahooFinancials 
from tabulate import tabulate
import IPython.display as d
import IPython.core.display

import ast
from io import StringIO
from fitter import Fitter, get_common_distributions, get_distributions 
import logging

import datetime 
import time
import warnings

logging.getLogger().setLevel(logging.ERROR)
warnings.filterwarnings("ignore")
warnings.filterwarnings("ignore", category=UserWarning)

# -- ------------------------------------------------------------------------------------------------------------------------------ Functions ----------------------------------------------------------------------------------------------------------------------------- -- #

##############################################################################################################################################################################################################################################################################
def get_requirements(docstring):
    """
    Function to create requirements.txt file for a repository.
    Parameters
    ----------
    docstring: str
        Docstring of requirements.txt script in a project: project, script, author, license and remote.
    Returns
    -------
    requirements.txt
        requirements.txt with modules and versions used in project.
    """
    
    with open("requirements.txt", "r+") as f:
        old = f.read() 
        f.seek(0) 
        f.write((docstring + old).replace("==", " >="))
        f.write("jupyter >= 1.0.0 \n")

########################################################################################################################################################################################################################################
def library_install(requirements_txt):
    """Install requirements.txt file in project created with fn.get_requirements.
    Parameters
        requirements_txt : str
        requirements.txt file name.
    """
    import os
    import warnings
    warnings.filterwarnings("ignore")
    os.system(f"pip install -r {requirements_txt}")
    print("Requirements installed.")
    with open("requirements.txt", "r") as f:
        print(f.read())

#########################################################################################################################################################################################################################################
def SP500_tickers(batches):
    """
    Function to fetch tickers from S&P500 .html by batches or (N) lists of lists. Undivisible n batches sizes slice list[-1] 
    Parameters:
    ----------
    batches : int
             N tickers in lists of lists in function S&P 500 tickers.
    index: str
             Index to fetch tickers from S&P 500.    
    Returns:
    -------
    'list 1': List of S&P 500 companies for all quotes listed in the S&P 500 acc0rding to refs.
    """
    list = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]["Symbol"].values.tolist()
    data = [[x.replace(".", "-") for x in list[x:x+batches]] for x in range(0, len(list), batches)]
    
    return data

##########################################################################################################################################################################################################################################
def VaR(df, alpha):
    """
    Function to calculate the Value at Risk (VaR) percentile to the upside/downside of a time series.
    Parameters:
    ----------
    prices : pd.DataFrame
        df from which to obtain VaRs with the percentile method (np.quantile).
    alpha : float
        Confidence level for historical VaR considering f(x) = z (.5 is the median).
        + e.g alpha = 0.975 : 2.5% of the values are below VaR.
        + e.g alpha =.025 : 97.5% of the values are above VaR.
        Because percentages have a normal distribution.0

    Returns:
    -------
    VaR : float
        Value at Risk (VaR) of a prices series.
    """
    VaR = df.quantile(1-alpha)

    return VaR

###########################################################################################################################################################################################################################################
def retSLog_Selection(data, rf, best, start, end):

    Simple = vs.selection_data(data, "Simple", rf, best, start, end)[1]
    Log = vs.selection_data(data, "Log", rf, best, start, end)[1]

    summary = pd.concat([Simple, Log], axis=1, join="outer")
    markdown = d.Markdown(tabulate(summary, headers = "keys", tablefmt = "pipe")) 

    return markdown

############################################################################################################################################################################################################################################
def format_table(dist_fit_T, Xi):
    """
    format_table is a function to format the output of vs.Stats[2] in order to show dist_fit: {params, AIC and BIC} for Xi resampling periods: Wk, Mo & Qt.
    Parameters:
    ----------
    dist_fit : list
        List of lists with output of vs.Stats[2].
    Xi : list
        Xi Selection from vs.Selection_data[3].index.values
    Returns:
    -------
    df : dataframe
        Formatted Dataframe with Xi values for resampling periods with rows Xi and cols. for periods.
    """
    pd.set_option('display.max_colwidth', 400)
    dist_fit_T = dist_fit.T
    dist_fit_T.apply(lambda row: pd.Series(row).drop_duplicates(keep='first'),axis='columns')
    dist_fit_T.columns = ["Wk", "Mo", "Qt"]
    dist_fit_T.index = Xi.index.values
    dist_fit_T.index.name = "{Params., AIC, BIC}"

    return dist_fit_T

############################################################################################################################################################################################################################################