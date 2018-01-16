import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# -----------------------------------------------------------------------------------------------------------------
# -------------------- read in the text files (read in column names before the text file) -------------------------
# -----------------------------------------------------------------------------------------------------------------
# Our data
df = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/IRTF_SpeX (SRMP) - SpeX_Jul4.tsv", sep="\t", comment="#", header=0)
df1 = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/IRTF_SpeX (SRMP) - Feb28.tsv", sep="\t", comment="#", header=0)
df2 = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/IRTF_SpeX (SRMP) - Dec_1224.tsv", sep="\t", comment="#", header=0)

dfmar05 = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/IRTF_SpeX (SRMP) - March 05.tsv", sep="\t", comment="#", header=0)
dfmar06 = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/IRTF_SpeX (SRMP) - March 06.tsv", sep="\t", comment="#", header=0)
# Comparisons
column_names_BDKP3A = ["nmn", "Lgn", "sptn", "Total Proper Motion", "J", "Jerr", "H", "Herr", "K", "Kerr", "w1", "w1err",
                      "w2", "w2err", "w3", "w3err", "w4", "w4err"]
dfBDKP3A = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/BDKP3A.txt", sep="\s+", comment="#", names=column_names_BDKP3A,
                       header=None)
# dfBDKP3B = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/BDKP3B.txt", sep="\t", comment="#")  # not using now
column_namesLSPMWISE = ["name", "Total Proper Motion", "w1", "w1err", "w2", "w2err", "w3", "w3err", "w4", "w4err",
                         "J", "Jerr", "H", "Herr", "K", "Kerr"]
dfLSPMWISE = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/LSPM-WISE-Table.txt", sep="\t", comment="#",
                         names=column_namesLSPMWISE)
# Read in comparisons (these are the old text files, not using)
# how to tell python that you have multiple columns as opposed to just one
# column_names = ['RA', 'DEC', 'J', 'K', 'PMRA', 'PMDEC', 'Vtan', 'SpT']
# df3 = pd.read_csv("/Users/nina/Dropbox/SRMP_shared/BDKP.txt", sep="\s+", header=0, names=column_names,
#                   error_bad_lines=False)  # error bad lines gets rid of the rows that had too many value
# column_names1 = ['_RAJ2000', '_DEJ2000', 'pm', 'pmRA', 'pmDE', 'Jmag', 'Kmag']
# df4=pd.read_csv("/Users/nina/Dropbox/SRMP_shared/LSPM2.txt", sep="\s+", comment="#", header=2)

# -----------------------------------------------------------------------------------------------------------------
# ------------------------------------Combining our data into one dataframe----------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# creating 3 new data frames with only the values you need from the old df's(apparent magnitudes, total proper motion)
df_rpm = df[['NAME', 'J', "J_err", 'H', "H_err", "K", "K_err", "W1", "W1_err", 'Total Proper Motion']]
df_rpm1 = df1[['NAME', 'J', "J_err", 'H', "H_err", "K", "K_err", "W1", "W1_err", 'Total PM b']]
df_rpm2 = df2[['NAME', 'J', "J_err", 'H', "H_err", "K", "K_err", "W1", "W1_err", 'Total Proper Motion']]
dfmar05 = dfmar05[['NAME', 'J', 'J_err', 'H', 'H_err', 'K', 'K_err', 'W1', 'W1_err', 'Total Proper Motion']]
dfmar06 = dfmar06[['NAME', 'J', 'J_err', 'H', 'H_err', 'K', 'K_err', 'W1', 'W1_err', 'Total Proper Motion']]

# change column names to match each other
df_rpm1.columns = ['NAME', 'J', "J_err", 'H', "H_err", "K", "K_err", "W1", "W1_err", "Total Proper Motion"]
df4 = pd.read_csv('/Users/nina/Dropbox/SRMP_shared/LSPM2.txt', sep="\s+", comment='#', header=2,
                  names=['RA', 'DEC', 'pm', 'pmRA','pmDEC','J', 'K'])
# use concatinate function to stack new data frames
frames = [df_rpm, df_rpm1, df_rpm2]
result = pd.concat(frames, ignore_index=True)


# -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------Adding RPM and J-K color columns------------------------------------------
# -----------------------------------------------------------------------------------------------------------------
# Reduced Proper Motion Equation, H = m + 5 log(μ) + 5

# how to add column to dataframes
result["RPM_W1"] = result["W1"]+5*np.log10(result["Total Proper Motion"]/1000)+5
result["RPM_J"] = result["J"]+5*np.log10(result["Total Proper Motion"]/1000)+5
result["J-K color"] = result["J"]-result["K"]

dfmar05["RPM_W1"] = dfmar05["W1"]+5*np.log10(dfmar05["Total Proper Motion"]/1000)+5
dfmar05["RPM_J"] = dfmar05["J"]+5*np.log10(dfmar05["Total Proper Motion"]/1000)+5
dfmar05["J-K color"] = dfmar05["J"]-dfmar05["K"]

dfmar06["RPM_W1"] = dfmar06["W1"]+5*np.log10(dfmar06["Total Proper Motion"]/1000)+5
dfmar06["RPM_J"] = dfmar06["J"]+5*np.log10(dfmar06["Total Proper Motion"]/1000)+5
dfmar06["J-K color"] = dfmar06["J"]-dfmar06["K"]

# dropping last 4 rows of dfBDKP3A because their TPM = 0
dfBDKP3A = dfBDKP3A.drop(dfBDKP3A.index[[1199,1200,1201, 1202]])
dfmar05 = dfmar05.drop(dfmar05.index[[5,6,7]])




dfBDKP3A["RPM_W1"] = dfBDKP3A["w1"] + 5 * np.log10(dfBDKP3A["Total Proper Motion"])+5
dfBDKP3A["J-K color"] = dfBDKP3A["J"]-dfBDKP3A["K"]

# dropping one row because its TPM < 0
dfLSPMWISE = dfLSPMWISE[dfLSPMWISE["Total Proper Motion"] > 0]


dfLSPMWISE["RPM_W1"] = dfLSPMWISE["w1"] + 5 * np.log10(dfLSPMWISE["Total Proper Motion"])+5
dfLSPMWISE["J-K color"] = dfLSPMWISE["J"]-dfLSPMWISE["K"]

# added three new columns to dataframes (TPM, RPM, and J-K color) to be able to graph!

# df3["Total Proper Motion"] = np.sqrt(np.square(df3['PMRA'])+np.square(df3['PMDEC']))
# df3["J-K color"] = df3["J"]-df3["K"]
# df3["RPM_J"] = df3["J"]+5*np.log10(df3["Total Proper Motion"])+5
#
# df4["Total Proper Motion"] = np.sqrt(np.square(df4['pmRA'])+np.square(df4['pmDEC']))
# df4["J-K Color"] = df4["J"]-df4["K"]
# df4["RPM_J"] = df4["J"]+5*np.log10(df4["Total Proper Motion"])+5


# how to actually plot this information
# our data (w1)
plt.scatter(result["J-K color"], result["RPM_W1"], c="red", zorder=2)
plt.ylabel("Reduced Proper Motion")
plt.xlabel('J-K color')
plt.ylim([4, 22])
plt.xlim([0, 3])

# our data (J)
plt.scatter(result["J-K color"], result["RPM_J"], c="red", zorder=2)
plt.ylabel("Reduced Proper Motion (J)")
plt.xlabel("J-K color")
plt.ylim([22, 4])
plt.xlim([0, 3])

# plot for df3 # not using
# plt.scatter(df3["J-K color"], df3["RPM_J"], c="green", s=1.5, zorder=1)
# plt.ylabel("Reduced Proper Motion (J)")
# plt.xlabel("J-K color")
# plt.ylim([22, 4])
# plt.xlim([-4, 4])
#
# # plot for df4 # not using
# plt.scatter(df4["J-K Color"], df4["RPM_J"], c="green", s=1.5, zorder=1)
# plt.ylabel("Reduced Proper Motion (J)")
# plt.xlabel("J-K Color")
# plt.ylim([22, 4])
# plt.xlim([-4, 4])

# plot for dfBDKP3A (w1)
plt.scatter(dfBDKP3A["J-K color"], dfBDKP3A["RPM_W1"])
plt.ylabel("Reduced Proper Motion (w1)")
plt.xlabel("J-K color")
plt.ylim([25,0])

# plot for dfBDKP3A (J)

# plot for dfLSPMWISE (w1)




# plot for dfLSPMWISE (J)

# how to save plot
plt.savefig('Reduced Proper Motion J.png')
plt.savefig('Reduced Proper Motion (w1)')

# how to search for data points that are outliers in your code; define x and make it find the weird values
# x = df4[(df4['J-K Color'] < -15)]
# x1 = df3[(df3['J-K color'] > 10)]
# x2 = dfBDKP3A [(dfBDKP3A['w1'] != -100)] # not using when doing j data
x3 = dfBDKP3A[(dfBDKP3A['J'] != -100)]
x4 = dfBDKP3A [(dfBDKP3A['K'] != -100)]
x5 = dfLSPMWISE [(dfLSPMWISE["Total Proper Motion"] < 0)]


# how to delete those outliers if they're useless (i.e. if they don't have a necessary value)
# df3 = df3.drop(df3.index[[425, 594, 682]])
# df4 = df4[df4.K != 27.77]
# dfBDKP3A = dfBDKP3A[dfBDKP3A.w1 != -100]
dfLSPMWISE = dfLSPMWISE[dfLSPMWISE.w1 != -100]






