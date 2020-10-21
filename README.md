🚫 Note: All lines that start with 🚫 are instructions and should be deleted before this is posted to your portfolio. This is intended to be a guideline, feel free to add your own flare to it.

# Human Rights First Police Use of Force Map

You can find the deployed project at [Human Rights First Police Brutality](https://main.d17v0exvwwwzgz.amplifyapp.com/).

## Contributors


|                                                      [Griffin Wilson](https://github.com/Griffinw15/)                                                       |                                                       [Kristine Wang](https://github.com/KristineYW/)                                                        |                                                      [Daniel Benson](https://github.com/Daniel-Benson-Poe/)                                                       |                                                                                                               |                                                                                                             |
| :-----------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------: |
| [<img src="https://media-exp1.licdn.com/dms/image/C5603AQHBdRMfl70c0g/profile-displayphoto-shrink_200_200/0?e=1608163200&v=beta&t=x2kjIpS9INPLMSyc_NNT59uie5td6BOL-3dWae1MCGk" width = "200" />](https://github.com/Griffinw15/) | [<img src="https://media-exp1.licdn.com/dms/image/C5603AQHShEFoe32Lnw/profile-displayphoto-shrink_800_800/0?e=1608163200&v=beta&t=w431sI40V39B3yLsBZguHh8FyW8ybAbw-uAcFL1OXZ0" width="200" />](https://github.com/KristineYW/) | [<img src="https://avatars1.githubusercontent.com/u/55222213?s=400&u=81a5f3241df5769fd8fc5dd5d0c416ed3112f018&v=4" width = "200" />](https://github.com/Daniel-Benson-Poe/) |
|                                [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Griffinw15/)                                |                            [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/KristineYW/)                             |                          [<img src="https://github.com/favicon.ico" width="15"> ](https://github.com/Daniel-Benson-Poe/)                           ||
|                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/griffinwilson15/)                |                 [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/kristine-w-lambdads/)                 |                [ <img src="https://static.licdn.com/sc/h/al2o9zrvru7aqj8e1x2rzsrca" width="15"> ](https://www.linkedin.com/in/daniel-benson-dsaopls/)                |                

<br>
<br>

![fastapi](https://img.shields.io/badge/fastapi-0.60.1-blue)
![pandas](https://img.shields.io/badge/pandas-1.1.0-blueviolet)
![plotly](https://img.shields.io/badge/plotly-4.9.0-brightgreen)
![uvicorn](https://img.shields.io/badge/uvicorn-0.11.8-ff69b4)
![praw](https://img.shields.io/badge/praw-7.1.0-red)
![python-dotenv](https://img.shields.io/badge/python--dotenv-0.14.0-green)
![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4-4.9.1-orange)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0.23.2-yellow)
![spacy](https://img.shields.io/badge/spacy-2.3.2-lightgrey)
![newspaper3k](https://img.shields.io/badge/newspaper3k-0.2.8-9cf)
![fastapi-utils](https://img.shields.io/badge/fastapi--utils-0.2.1-informational)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-11.3.20-yellowgreen)

## Project Overview

[Trello Board](https://trello.com/b/QWXanExQ/team-c-2009)

[Product Canvas](https://whimsical.com/8sQcpjw3K2XdAiM9aeMkft)

Our team is developing an interactive map that identifies potential instances of police use of force across the United States of America for Human Rights First, an independent advocacy and action organization.

We're pulling data from similiar APIs(All locations V2 - https://raw.githubusercontent.com/2020PB/police-brutality/data_build/all-locations-v2.json, 846- https://api.846policebrutality.com/api/incidents) and from Twitter and Reddit. We want to identify aggregate these instances.

### Key Features

- User can browse incident map
- User can view specific instances with original source links
- User can view map with various filters

## Tech Stack

### Data Science API built using:

- Python
- Docker
- FastAPI
- AWS Elastic Beanstalk

### Why we made our tech stack decisions:

- Wanted to gain insight to AWS
- Docker makes environments easier
- FastAPI has been gaining traction over Flask

### Libraries used:

- Pandas
- Seaborn
- spacy
- nltk
- PRAW
- Plotly
- spacy
- newspaper3k

#### Data Science API deployed to AWS

#### [Back end](https://github.com/Lambda-School-Labs/Labs27-C-HRF-BE/blob/main/README.md) built using:

- point one
- point two
- point three

# APIs

## Data Science API

We are sending json objects to the backend with information about instances of police use of force. This information includes location data (city, state, and geocode) and relevant details about the incident, like the type of force that was used.

## PRAW

PRAW, The Python Reddit API Wrapper, makes it easy for users to analyze Reddit data. We used PRAW to scrape Reddit for potential instances of police of force.

# Environment Variables

In order for the app to function correctly, the user must set up their own environment variables. There should be a .env file containing the following:

    *  PRAW_CLIENT_ID  - keys for Reddit API
    *  PRAW_CLIENT_SECRET - keys for Reddit API
    *  PRAW_USER_AGENT - keys for Reddit API

# Content Licenses

| Image Filename | Source / Creator | License                                                                      |
| -------------- | ---------------- | ---------------------------------------------------------------------------- |
| name1.svg      | Griffin Wilson   | [MIT](https://github.com/SamHerbert/SVG-Loaders)                             |

# Testing

We tested the classifier on sets of 100-1000 incidents at a time, our aim was in precision as to minimize false incidents included. 

# Installation Instructions

We used Docker for ease of use when dealing with environmental dependancies 

## Scripts

    Get AWS credentials
    
    Get your AWS access keys
    
    Install AWS Command Line Interface
    
    * aws configure -> configures AWS CLI
    * pip install pipx -> installs pipx
    * pipx install awsebcli -> installs AWS Elastic BeanStalk CLI
    
    Follow AWS EB docs: Use Docker to build the image locally, test it locally, then push it to Docker Hub
    
    * docker build -f project/Dockerfile -t YOUR-DOCKER-HUB-ID/YOUR-IMAGE-NAME ./project 
    * docker login 
    * docker push YOUR-DOCKER-HUB-ID/YOUR-IMAGE-NAME 
    
    Edit the image name in Dockerrun.aws.json then replace YOUR-DOCKER-HUB-ID/YOUR-IMAGE-NAME with your values
    
    Then use the EB CLI:
    
    * git add --all 
    * git commit -m "Your commit message" 
    * eb init -p docker YOUR-APP-NAME --region us-east-1 
    * eb create YOUR-APP-NAME 
    * eb open 
    
    Then use AWS Route 53 to set up a domain name with HTTPS for your DS API
    
    Redeploy:
    
    * git commit ... 
    * docker build ... 
    * docker push ... 
    * eb deploy 
    * eb open 

# Contributing

When contributing to this repository, please first discuss the change you wish to make via issue, email, or any other method with the owners of this repository before making a change.

Please note we have a [code of conduct](./CODE_OF_CONDUCT.md). Please follow it in all your interactions with the project.

## Issue/Bug Request

**If you are having an issue with the existing project code, please submit a bug report under the following guidelines:**

- Check first to see if your issue has already been reported.
- Check to see if the issue has recently been fixed by attempting to reproduce the issue using the latest master branch in the repository.
- Create a live example of the problem.
- Submit a detailed bug report including your environment & browser, steps to reproduce the issue, actual and expected outcomes, where you believe the issue is originating from, and any potential solutions you have considered.

### Feature Requests

We would love to hear from you about new features which would improve this app and further the aims of our project. Please provide as much detail and information as possible to show us why you think your new feature should be implemented.

### Pull Requests4

If you have developed a patch, bug fix, or new feature that would improve this app, please submit a pull request. It is best to communicate your ideas with the developers first before investing a great deal of time into a pull request to ensure that it will mesh smoothly with the project.

Remember that this project is licensed under the MIT license, and by submitting a pull request, you agree that your work will be, too.

#### Pull Request Guidelines

- Ensure any install or build dependencies are removed before the end of the layer when doing a build.
- Update the README.md with details of changes to the interface, including new plist variables, exposed ports, useful file locations and container parameters.
- Ensure that your code conforms to our existing code conventions and test coverage.
- Include the relevant issue number, if applicable.
- You may merge the Pull Request in once you have the sign-off of two other developers, or if you do not have permission to do that, you may request the second reviewer to merge it for you.

### Attribution

These contribution guidelines have been adapted from [this good-Contributing.md-template](https://gist.github.com/PurpleBooth/b24679402957c63ec426).

## Documentation

See [Backend Documentation](https://github.com/Lambda-School-Labs/Labs27-C-HRF-BE/blob/main/README.md) for details on the backend of our project.
