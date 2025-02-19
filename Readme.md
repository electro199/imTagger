# Image Classification App

This Python-based Image Classification App allows you to label images for machine learning models. It supports various input such as folders and CSV file, shortcuts for labeling and  provides progress files for saving progress.

## Features

- **Light** ImTagger is simple app for simple job
- **Shortcuts** Use ctrl+1-9 for fast labeling
- **Folder Input:** Load images directly from a specified folder.
- **CSV Input:** Use a CSV file to specify image paths and additional metadata.
- **Progress Tracking:** Keep track of your progress with a progress file.
- **Autosave** saving every changes into progress file automatically.
- **AutoLabelling** (Beta) Builitin support for auto lable prediction model running with transformers.

## Installation

To install and set up the Image Classification App, follow these steps:

1. **Clone the repository:**
``` bash
git clone https://github.com/electro199/imTagger.git
cd imTagger
```


Install requirements

Python version 3.10 and 3.11 are recommended.

windows :
```bash
pip install -r requirements.txt
```
Unix :
```bash
pip3 install -r ./requirements.txt
```

## Auto Labelling

This Feature is in beta to use in app set `AUTO_LABELER_ENABLED` to True in `main.py` and install dependency:

```
pip install transformers
```


## Usage :

On windows click `run.bat` or in cmd `run.bat`

On unix in terminal `python3 main.py`


# Contributing
Pull requests are more than welcome! If you are planning to contribute a large patch, please create an issue first to get any upfront questions or design decisions out of the way first.