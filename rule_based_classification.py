import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

"""
THE CASE: 

A MOBILE GAME DEV COMPANY WANTS TO CREATE LEVEL BASED NEW CUSTOMERS DEFINITIONS (PERSONA)
BY USING USER DATA AND CREATE NEW SEGMENTS ACCORDING TO THESE NEW DEFINITIONS
LASTLY WANTS KNOW HOW MUCH MONEY AN UPCOMING USER WILL PAY. 

"""

# LOAD DATASET
def load_dataset():
    df = pd.read_csv("persona.csv")
    return df

df = load_dataset()


# CHECK DF
def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(df)

# UNIQUE SOURCES AND FREQUENCIES

sources_and_freq = pd.DataFrame({"SOURCES" : df["SOURCE"].unique() , "FREQUENCIES" : df["SOURCE"].value_counts()})

# UNIQUE PRICES

df["PRICE"].nunique()

# HOW MANY SALES MADE FROM WHICH PRICE

df["PRICE"].value_counts()

# HOW MANY SALES MADE FROM WHICH COUNTRY

df["COUNTRY"].value_counts()

# HOW MUCH MONEY WAS MADE FROM EACH COUNTRY

df["PRICE"].groupby(df["COUNTRY"]).sum()
df.groupby("COUNTRY").agg({"PRICE" : "sum"})

# NUMBER OF SALES MADE BY SOURCES

df.groupby("SOURCE").agg({"PRICE" : "sum"})

# MEAN OF PRICES BY COUNTRY

df.groupby("COUNTRY")["PRICE"].mean()
df.groupby("COUNTRY").agg({"PRICE" : "mean"})

# MEAN OF PRICES BY SOURCES
df.groupby("SOURCE").agg({"PRICE" : "mean"})

# MEAN OF PRICES BY COUNTRY AND SOURCE

df.groupby(["SOURCE","COUNTRY"]).agg({"PRICE" : "mean"})

# MEAN OF PRICES BY COUNTRY, SOURCE, AGE, SEX

df.groupby(["COUNTRY","SOURCE","AGE","SEX"]).agg({"PRICE" : "mean"})

# SORT VALUES BY PRICE

agg_df = df.groupby(["COUNTRY","SOURCE","AGE","SEX"]).agg({"PRICE" : "mean"}).sort_values(by = "PRICE", ascending=True)

agg_df.head()

agg_df = agg_df.reset_index()

# SET AGE AS CATEGORICAL AND MAKE IT NEW COLUMN

bins = [0, 19, 24, 31, 41, agg_df["AGE"].max()]

# SET LABELS
mylabels = ['0_18', '19_24', '24_30', '30_40', '40_' + str(agg_df["AGE"].max())]

agg_df["CAT_AGE"] = pd.cut(df["AGE"], bins , labels = mylabels)

# CREATE CUSTOMER LEVEL BASED ROWS

agg_df["CUSTOMER_LEVEL_BASED"] = [row[0].upper() + "_" + row[1].upper() + "_" + row[3].upper() + "_" + row[-1].upper() for row in agg_df.values]
agg_df.head()

agg_df = agg_df[["CUSTOMER_LEVEL_BASED","PRICE"]]

agg_df["CUSTOMER_LEVEL_BASED"].value_counts()

# GROUP BY LEVELS

agg_df = agg_df.groupby("CUSTOMER_LEVEL_BASED").agg({"PRICE" : "mean"})
agg_df = agg_df.reset_index()

# SEGMENTATION BY PRICE

agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, ["D","C","B","A"])

# SOME STATISTICS ABOUT SEGMENTS
agg_df.groupby("SEGMENT").agg({"PRICE" : ["mean","max","sum"]})

agg_df[agg_df["SEGMENT"] == "C"]

# WHICH SEGMENT DOES A 33 YEARS OLD TURKISH WOMAN USING ANDROID BELONG TO ?

new_user = "TUR_ANDROID_FEMALE_30_40"
agg_df[agg_df["CUSTOMER_LEVEL_BASED"] == new_user]

# WHICH SEGMENT DOES A 35 YEARS OLD FRENCH WOMAN USING IOS BELONG TO ?
new_user = "FRA_IOS_FEMALE_30_40"
agg_df[agg_df["CUSTOMER_LEVEL_BASED"] == new_user]

agg_df.head()






