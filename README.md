# ASKI - Semantic Search Evaluation 

> NOTE: Curently only supports Elasticsearch, ColBERT (unstable)

The goal of ASKI is to **make the lives of data scientists easier**, filling-in a required niche. 
ASKI will allow plug-and-play for *models, datasets, tasks, and other parameters*. Users can 
quickly see how their model performs, identify what works and what doesn't, and compare their 
model to other models. Here's ASKI's current functionalities:

- **Custom Question-Answering** (ColBERT, Elasticsearch) 
  - Can use SQUAD texts (ex. 1973 Oil Crisis) or upload custom files (`.txt` support)
  - Allows users to enter questions, displays model's output
  - Gives latency, still need to update accuracy card (bottom right) 


- **Solo SQUAD Benchmarking** (ColBERT, Elasticsearch) 
  - Can only use SQUAD texts (goes through ALL questions of chosen dataset) 
  - Gives latency (avg time/question, as well as generates real-time graph)
  - Gives accuracy (num correct, num total, % correct, % progress) 
  - Displays incorrect questions 

- **Model Comparison on SQUAD** (ColBERT, Elasticsearch)
  - Goes through all questions of chosen dataset on both models
  - Gives latency, accuracy, incorrect questions for both 
  - Allows for side-by-side comparison of performance 

> NOTE: Solo SQUAD Benchmarking and Model Comparison are a *little unstable*. Will be fixed in next commit! 


Over the coming weeks, this dashboard will be further fleshed out with more exciting features 😄. 

&nbsp;&nbsp;

![Custom](./auxmedia/custom_qna.PNG)

&nbsp;&nbsp;

![Comparison](./auxmedia/model_comparison.png)

&nbsp;&nbsp;

> As a reminder, Solo Benchmarking and Model Comparison are unstable! (will be fixed in next commit)

&nbsp;&nbsp;

## Installation & Usage 

First, clone this repository. Next, create your conda environment with 

`conda env create -f aski_env.yml`

Then, acivate your conda environment with `conda activate aski-benchmark`

Ensure that your elasticsearch client is up and running. For more information, see 
"Supported Models" section. Finally, run the dashboard with `python app_callbacks.py`.

Now, a link should appear (ex. `Dash is running on http://127.0.0.1:5000/`). Click on it to open the dashboard! 

&nbsp;&nbsp;

A few heads up, there are **several edge-cases** that are currently being ironed out! 
- If something stops working, try restarting the dashboard and navigating to that page from fresh
- Make sure to **check the outputs of cmd** (helpful debugging info that might not be shown on the Dash)


&nbsp;&nbsp;

## Supported Models 

***Installing Elasticsearch***

Navigate to [Elasticsearch Installation](https://www.elastic.co/downloads/past-releases/elasticsearch-7-0-0) and 
follow the instructions according to your specific setup. 

> NOTE: ASKI does **not currently support** Elasticsearch 8 or higher! 

In order to launch elasticsearch, open a new terminal, navigate to the elasticsearch directory, and run either of the following: 
- `./bin/elasticsearch` (Linux/Mac)
- `.\bin\elasticsearch.bat` (Windows)

Now, leave this terminal window open! 

&nbsp;&nbsp;

***Installing ColBERT***

Clone the following [GitHub Repo (new-api branch)](https://github.com/stanford-futuredata/ColBERT/tree/new_api) into the `ColBERT` folder. 

> NOTE: There might be some issues with environments, these will be resolved by next commit! 

Once downloading the ColBERT files, make sure to uncomment the three lines near the top 
of the file `ColBERTSearch.py`. More instructions are detailed at the top of this file. 

After this, navigate to the `get_sidebar()` function in `app_elements.py` and make sure to 
toggle the "Disabled" option next to ColBERT. You should be good to go now! 

&nbsp;&nbsp;

***Installing Knowledge Graph***

Stay tuned, support for this is coming soon! 

&nbsp;&nbsp;