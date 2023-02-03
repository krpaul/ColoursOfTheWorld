# The World in Colour
McHacks 2023 Project @ McGiil University. Coded in 24 hours on Jan 28 2023.

### YouTube Video Demo
[![YouTube Video Demo](https://user-images.githubusercontent.com/34616839/216401894-0c680c51-41bb-4b96-ad7e-4ae1c09f387b.png)](https://youtu.be/3khhzTuc1d4)

# Inspiration
We were inspired by sentiment analysis in the news, as well as crisis trackers. We decided to use co:here to run our own sentiment analysis for current events to pick out petitions one might want to sign!

# What it does
Our project aims to visualise global turmoil for the user through news headlines. Heatmaps are established based on negative headlines and the user can navigate to anywhere on the world to take action and sign petitions that our model generates.

Displays a globe with a heat map which visualises countries which have the most negative recent news articles
Allows the user to select an area of turmoil and do relevant to helping this region
How we built it
In order to implement the heatmaps for our globe, we needed to create a ratio between negative and positive news articles in order to gauge if a country was in a state of turmoil/had many negative headlines. To do this, we had to train cohere's NLP model so that we can identify the sentiment of an article - whether it was positive or negative. In order to do this, we used a news search API in order to pull recent news articles from a variety of countries and then created a program so that we could script through these headlines and descriptions manually and quickly decide whether they are positive or negative, thus creating a database to use to train cohere.

Once we had a gauge of the negative to positive headlines in countries, we created the heat map which identifies the most contentious countries at the moment. In order to promote the user to take action in certain countries that may appear to be in turmoil, we used change.org's searching to automatically search and display the most relevant few charitable initiatives within the selected countries.

# Challenges we ran into
One of the biggest challenges during our project was classifying our news articles into negative or positive - this was particularly difficult because of the various nuances a news article's headline and description have, making it often difficult to fit into a strict category. We therefore needed to train coshare's model in order to identify what kinds of news articles were negative or positive.

# Accomplishments that we're proud of
We are proud of being able to produce a globe with the heat map that implements the relative "negativity" of news articles

# What we learned
3D modelling on the web browser is a lot harder than it needs to be :/ Sentiment analysis has a long way to go. There is an upper limit for caffeine saturation in the human body

# How to run
Simply close the repository and run `flask run` 

If you would like to redownload and reanalyze news sources, regard the heatmap/ directory for related scripts.

This project has not been edited since it was submitted to the Hackathon at the end of the 24 hours.

## What's next for The World in Colour
From the beginning our overarching aim was for The World in Colour to implement a chatbot that can guide the user through the experience

## Built With
- Flask Backend
- Pure HTML/CSS/JS Frontend
- [Three.JS](https://threejs.org/) rendering library
- [cohere.ai](https://cohere.ai) NLP AI Model
- Python for scripting 

## Devpost
https://devpost.com/software/the-world-in-colour

