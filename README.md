### README.MD

This is a repo for the *EG AI 2020* project.

To recreate the environment in which the code for this repo was created, run the **environment.yml** file.

For the folders **'.shp', 'measurements' and 'network'**, it is quite clear from their names what kind of files are in them.
Therefore, I would focus on the folder **'code'**, and provide some details about the files there.

So, here's a brief explanation of the files in the folder **'code'** (more detailed explanations of the 
inner workings of the files is provides inside of them):

1. **libs_and_funcs.py** - this file contains the libraries and functions that need to be imported in the script app_v1.py
2. **files_to_read.py** - in this file we read all the files we need in app_v1.py; we read the files here only to make the 
   code in app_v1.py clearer
3. **pp_plot_data_generation.py** - this script generates the bus and line geodata for the pandapower plot; we don't have 
   to call this script anymore, because we've already created this bus and line geodata; nevertheless, I thought it 
   might be useful to see how the data was generated and maybe improve this data generation
4. **plotly_plot_data_generation.py** - this script generates data for the 'plotly_plot'; this script has also been 
   executed, so the data has been generated, but still I thought it would be useful to post the code here
5. **app_v1.py** - this file represents the Dash app for the project EG AI 2020; so, here we have all the code for the 
   web application, i.e. the code for the CSS and HTML parts, plus some functions which enable user interactivity
   
Note: We plot our electrical network in 2 ways: 'plotly_plot' and 'pandapower_plot'. As we are not sure yet which way is 
faster, we've retained both types of plotting so far. Of course, later on we should use only one of them.

I hope this info is a good start. In case, you need extra code or data related to this project, you can check the 
Sharepoint folder on the following [link](https://ovdes.sharepoint.com/sites/2020egai/Shared%20Documents/Forms/AllItems.aspx?viewid=5d4f50f3%2D122b%2D4a5c%2Db61b%2Ddd41b6ca8b4a&id=%2Fsites%2F2020egai%2FShared%20Documents%2Fproject%20%2D%20demo).

For any questions or problems with the repo, write to this e-mail: *dimitar.stefanov@ovdes.onmicrosoft.com*. 