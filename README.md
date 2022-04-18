### README.MD

This is a repo for the Dash app developed during the *EG AI 2020* project.

To recreate the environment in which the code for this repo was created, run:
```
conda create env -f environment.yml
```

Short description of contents of the folders ```.shp```, ```measurements``` and ```network```:

- ```.shp```: files containing GIS coordinates about the various network elements,
- ```measurements```: files containing measurements at the various network elements,
- ```network```: files containing metadata about the various network elements.

The folder ```code``` requires more detailed explanations about the files in it:

1. ```libs_and_funcs.py``` - this file contains the libraries and functions that need to be imported in the script app_v1.py
2. ```files_to_read.py``` - in this file we read all the files we need in app_v1.py; we read the files here only to make the 
   code in app_v1.py clearer
3. ```pp_plot_data_generation.py``` - this script generates the bus and line geodata for the pandapower plot; we don't have 
   to call this script anymore, because we've already created this bus and line geodata; nevertheless, I thought it 
   might be useful to see how the data was generated and maybe improve this data generation
4. ```plotly_plot_data_generation.py``` - this script generates data for the 'plotly_plot'; this script has also been 
   executed, so the data has been generated, but still I thought it would be useful to post the code here
5. ```app_v1.py``` - this file represents the Dash app for the project EG AI 2020; so, here we have all the code for the 
   web application, i.e. the code for the CSS and HTML parts, plus some functions which enable user interactivity
   
Note: Our electrical network can be plotted using 2 different functions: ```plotly_plot``` and ```pandapower_plot```. 

---
### Update
The data in the folders ```.shp```, ```measurements``` and ```network``` has been removed. In case you would like to test the
workings of the Dash app with these data, write an e-mail to: *dimitarstefanov46@gmail.com*. All other 
questions, requests or suggestions for this repo should also be forwarded to the e-mail above.
