# DMR Prune Contacts

This is a simple Python application that takes a DMR contacts file (such as from RadioID.net), filters it based on selected countries, and writes an output file ready for loading to a DMR handset.

## Description

The total number of registered DMR IDs in the world exceeds the maximum number of entries allowed by many DMR handsets. Therefore it is necessary to filter down the list before loading it to the handset.

RadioID.net provides a subscription service that can do this easily on their website.

Alternatively, it is a simple matter to download the csv file and filter it using a spreadsheet (such as Excel).

As an exercise in programming, I chose to write a Python program to do the filtering by country. I'm a beginner at Python, so no doubt the program can be greatly improved - but it does what I want so I'm happy with it!

## Getting Started

### Dependencies

The program has been written in Python. It has been tested using Tcl and Tk version 8.6, on MacOS and Windows.

Testing has been with a Retevis RT-3S. It is currently untested with other handsets, and I will be interested in any user reports with other devices.

### Installing

You need a working Python environment. Download DMR_Prune_Contacts.py and place it in a working directory (such as "Documents"). 

### Executing program

First, get your long list of contacts from RadioID.net (or elsewhere). This can be found in the Database / Data Dumps part of the RadioID.net website, and the file is called "user.csv".

Place user.csv in the same working directory as the main program (although you can placed it elsewhere if you prefer).

Run the DMR_Prune_Contacts.py, which takes you through the three steps:

1. Choose the input file. Click the filename if you want to change the name and/or location of the input file. Click "Open". If successful, the status line at the bottom of the screen will show how many database entries have been loaded.

2. Select tickboxes corresponding to the countries found in the input file. The status line keeps a running total of the entries selected.

3. Write the output file. By default this is "contacts.csv" in the working directory, but this can be changed by clicking the filename box.

That's it!


## Limitations and future developments

Currently filtering is only by country. 

I would like to add "States" for USA. 

I would also like to save settings, so that the same selection can be used for the next run.

## Authors

Russell Whitworth G4CTP
russell_whitworth@hotmail.com


## License

This project is licensed under the GPLv3 Licence.