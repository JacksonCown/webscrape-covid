Database Management - CSCI 4370
Term Project Submission

Manager: Matthew Kurien
Programmers: Jackson Cown, Arjun Kavungal

Project: Creating a COVID-19 visualizations web-app based on the Dash Framework

Components: 
cleaning.py:
- Scraping and cleaning data + munging/reformatting dataframes in pandas
- Generating subtables for Database
- Preparing data to prototype plots

plotTest.py:
- Prototyping interactive Plotly visualizations
- Preparing Visualizations to transfer to Dash web-app

app.py:
- Main Dash web-app component
- Executed to begin hosting the Dash app on local machine

To Run Demo:
Ensure you have the latest version of Dash and Pandas
1. Navigate to the project directory
2. Execute the command: "python app.py"
3. Visit http://127.0.0.1:8050/ from your web-browser

Note: There is a bug in the current implementation of the web-app that
prevents the multi-select prompt from clearing its memory. If the page stops
responding after you try to change the graph type, refresh and try again and
it should fix it.

Email me if you have any issues starting the demo:
jhc47191@uga.edu.

Thanks