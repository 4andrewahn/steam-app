# **Steam Game Recommendation App**
![Application Homepage](/homepage.jpg)

---
## **Overview** 
### *About the project*
Built as a final group project, this application was built as a tool to help Steam users find new games to play as well as provide insight into the popularity of each title. Through this web application, users are able to search for new games by keywords or attribute filters as well as add new game titles to the database. Basic game information is displayed for each title with the option to view a game description.  

### *Technical details*
The original dataset used in this application can be found [here](https://data.world/craigkelly/steam-game-data). The 78 attributes in this dataset were split into 4 tables (Categories, ComputerRequirements, GameCommunity, and SteamGames) and uploaded to a Google Cloud Platform (GCP) MySQL server. The Ajax library was used to interact with the GCP server. The Flask library was used to handle HTML routing with Javascript to handle the dynamically updating front-end. 

---
## **Getting Started**
### Setting up
To get a local copy up and running, setup the project environment with the following steps. 
1. Open a new terminal/command prompt and navigate to the project directory
2. Create a virtual Python environment using `python -m venv .venv`
3. Activate the virtual environment using `source .venv/bin/activate`
4. Install the required libraries into the environment by running `pip install -r requirements.txt`

### Running the application
To run the Flask app, complete the following steps in the same terminal/command prompt. 
1. To specificy that the Flask app module is the `app` folder, enter `export FLASK_APP=app`
2. To tell the Flask app to reload the server on change, enter `export FLASK_DEBUG=1`
3. Run the Flask app using `flask run`

---
## **Usage** 
Click on the Youtube thumbnail below to watch a brief demonstration of the Steam Recommendation App and its functionality. 

<a href="https://youtu.be/eztPFbncCXY">
  <img src="https://img.youtube.com/vi/eztPFbncCXY/0.jpg" alt="Project Demo on YouTube">
</a>

