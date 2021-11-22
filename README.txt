
Vizualizing Earthquake Data

Heidi Duus - hjoer14
Ronni Madsen - rmads17
Rasmus Vahlgreen - ravah17

Visualization Project 2020





Running the code:

This project has been written in Python, and the following packages must be installed before the code can run;


Pandas
pyproj
Bokeh (main visualization package)


Provided that the packages above have been installed, the visualization can be created by running the following command: bokeh serve vis.py --show --session-token-expiration 1000000
Notice that this will open a browser window on your computer.

Furthermore it is suggested to run in google chrome (will choose standard browser), since safari only allocates sufficiently amounts of ram if you keep the browser tap open.


Data:

Two datasets have been attached to this assignment. One contains all earthquakes from the 2018 and 2019, while the second one contains similar data from 2010-2020. We have been using the small one for testing, and the large on for our video. 

NOTICE that the script takes almost 15 minutes to run with the large dataset, but only approximately 5 minutes for the small one.

