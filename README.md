## VHDL/Verilog IP CORES Scripts

This repository contains few Python scripts capable to connect to the website 
opencores.org and download from it  approximately 4.5GB of VHDL/Verilor IP cores.
Downloaded data is saved locally and, in a second step, uploaded to github. An
index.html file containing an index of the available IP cores is generated.
 
All downloaded IP cores, once saved locally, are then uploaded on this 
guthub repository:
 
 https://github.com/fabriziotappero/ip-cores

The "ip-cores" repository accounts for approximately 1102 projects spread in 16 
categories. There is a branch for each IP project. Since the whole repository 
is around 4.47GB of data, you are advised to check out only the branch that you 
might interested in.

A searchable list of all projects is available at:

 www.freerangefactory.org/cores.html

Available Python scripts:

**opencores_scraper.py** downloads all opencores.org projects locally 
(in a local folder in your PC) and generate a n index file index.html.

**local2github.py** analyze a local folder and upload its content to the github
repository https://github.com/fabriziotappero/ip-cores


