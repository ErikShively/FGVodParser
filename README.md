# PyVodParser

## Summary and Motivation
I wanted to explore relating machine learning to computer vision, and I thought video games would be a neat way to contextualize the learning process. I aimed to solve a relatively niche problem within a subgenre of competitive video games. This genre, known as 'Fighting Games,' sees 2 players playing head-to-head using 2 different characters. These characters are usually identified by a portrait in a fixed position as part of the game's UI, and this project provides the tools to generate a training set and learning model to classify the two characters on screen at once. It also marks the start and end times of character appearance.
For more information on the specific problem I was attempting to address, read below:

## Purpose
People want to watch footage of fighting games, and they do so for a number of reasons. There are a lot of videos of fighting games, but there are surprisingly few places where you can easily search by character or player. Seraching on Youtube directly is a wildcard, since consistent and reliable sources of footage can slip under the radar. Some channels are more popular than others, so it can make it difficult finding footage unless you know exactly what to look for. There are a few databases per game, but they're maintained by a sizable community effort.
This project aims to parse videos and return information about them. This is in an effort to contribute toward something to make video databases easier to maintain.

## Usage
There are three scripts: modelgen.py, vidparse.py and compressor.py. modelgen.py produces a model, vidparse.py loads the model and uses it to parse a video, and compressor.py looks at the training data, clones and compresses it. This is done to try and account for video compression.

### modelgen.py
This script will generate a model for use in vidparse.py.
**Usage:**
`python3 modelgen.py <game> <modeltype> [-c config] [-o output] [-j json]`
| Positional Argument | Description |
| --- | --- |
| game | The game to build the model from |
| modelType | The ML model to use. Currently supports GNB safely. |

| Optional Arguments | Description |
| --- | --- |
| --config | The config file to load |
| --output | The handle to save the trained model. Automatically appends extention. |
| --json | Saves model as a JSON file instead of a pickle file. Safer but less consistent. |

**Setup:**
modelgen.py is the most involved to set up, but it can basically be broken up into two steps: the config file and the training data.
See configs/config.ini for an example on how to set up the config file. Most of the values are very straightforward.
charDict_L and charDict_R are the least intuitive and they're involved with the training data. These values point to a dictionary file that tell the script where the training images are. charDict_L is a dictionary where the specified character appears on the left. charDict_R the is the dictionary file where they appear on the right.
See configs/CharacterPaths/L_EXAMPLEGAME.txt for an example. The way this is structured, there will be redundant images.

**Notes:**
JSON is considered a safe format, while pickle is not. Unfortunately, SKLearn models don't play too friendly with JSON. Using the pickle format is perfectly safe when not distributing models, but be aware the JSON is the safest choice. Source: https://docs.python.org/3/library/pickle.html


### vidparse.py
**Usage:**
`python3 vidparse.py <modelFile> <game> <video> [-c config]`
| Positional Argument | Description |
| --- | --- |
| modelFile | The trained model file to load |
| game | The game in the processed video |
| video | The video to parse |

| Optional Argument | Description |
| --- | --- |
| --config | The config file to load (This program needs one too.) |

**Notes:**
This script currently prints out the prediction results as the model sees them.

### compressor.py
**Usage:**
`python3 compressor.py <dictionaryFile>`
| Positional Argument | Description |
| --- | --- |
| directoryFile | The same kind of dictionary file used to specify training data locations |
