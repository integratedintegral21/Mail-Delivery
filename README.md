# Mail-Delivery
> A set of tools for scraping and processing mail delivery data 
 ## Table of contents
 * [General Info](#general-information)
 * [Technologies Used](#technologies-used)
 * [Features](#features)
 * [Setup](#setup)
 * [Usage](#usage)
 ## General Information
  - Subdirectories: <br/>
    -**data/** - contains files with data ready to be processed / fed to the neural network<br/>
    -**models/** - by default empty - save trained models and processing pipelines here<br/>
    -**predictor/** - a python library to be used in your programs (follows factory creational pattern)<br/>
    -**preprocess/** - scripts used for preproccessing data (cleaning, features selection, etc.)
    -**scraper/** - scraping scripts. Feel free to experiment with them if you need more data
    -**train/** - scripts resposible for rescaling data, training model and saving essential files to model/ directory
  - The repository provides features allowing user to estimate delivery time of a parcel or a letter to any place in Poland (default)<br/>
  - Users can provide their own data and train a new estimator with it<br/>
 ## Technologies Used
  - **Python 3.8**
  - **Pandas**
  - **Numpy**
  - **TensorFlow**
  - **Selenium**
 ## Features
  - Preparing provided data for training (about 30k records)
  - Training and saving a delivery time predictor
  - A user-friendly library using the predictor model
  - Scrapping new data specified by user
  - Evaluating distance and trip duration between 2 locations
  - Saving scrapped data to csv files
 
