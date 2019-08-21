# SMAP_FieldCampaign
Code for obtaining and visualizing Radiometer Data obtained in Harvard Forest as part of a NASA Field Campaign to verify SMAP's readings. Done at NOAA-CREST at CCNY

# How to use
- Install WinSCP for passive FTP on windows
- Install Anaconda and make a conda enviorment with the imported librarys used by electric.py
- Use the scripts in /Sync to download the data (WinSCP)
- Put the input files into Visualziation/input_files
- Run electric.py

## Directory Structure


```
.
+--README.md
+--Sync
|	+--MesDu-2019-`*`**.txt**
+--ProcData
|	+--MesDu-2019`*`**.csv**
+--Visualization
|	+--plotting.py
+--FTP
|	+--ftpcalled.bat
|	+--ftp.txt
+--Output
|	+--graph.png

## Directories Explained

- Sync (Synchronize)
  - This is folder is synchronized with the FTP server through the FTP script in ./FTP. 

