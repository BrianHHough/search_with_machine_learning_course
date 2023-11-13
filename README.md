# Welcome to Search with Machine Learning

Search with Machine Learning is a four week class taught by Grant Ingersoll and Daniel Tunkelang and is focused on helping students
quickly get up to speed on search best practices by first teaching the basics of search and then extending those basics with machine learning.  

Students will learn indexing, querying, aggregations and text analysis, as well as how to use machine learning for ranking, content classification and query understanding.

The class is a hands-on project-driven course where students will work with real data and the [Opensearch](https://opensearch.com)/Elasticsearch ecosystem along with libraries like [FastText](https://fasttext.cc/), [XG Boost](https://xgboost.readthedocs.io/en/stable/) and [OpenSearch Learning to Rank](https://github.com/aparo/opensearch-learning-to-rank).

# Class code layout (e.g. where the projects are)

For our class, we have four weekly projects.  Each project
is a standalone Python application that interacts with an OpenSearch server (and perhaps other services).  

You will find these four projects in the directories below them organized in the following way:

- Week 1:
    - week1 -- The unfinished template for the week's project, annotated with instructions.
- Week 2:
    - week2 -- The unfinished template for the week's project, annotated with instructions.
- Week 3 and 4: you get the picture

Our instructor annotated results for each project will be provided during the class.  Please note, these represent our way of doing the assignment and may differ from your results, as there is often more than one way of doing things in search.

You will also find several supporting directories and files for [Logstash](https://opensearch.org/docs/latest/clients/logstash/), Docker and Gitpod.

# Prerequisites

1. For this class, you will need a Kaggle account and a [Kaggle API token](https://www.kaggle.com/docs/api).
1. No prior search knowledge is required, but you should be able to code in Python or Java (all examples are in Python)
1. You will need a [Gitpod](https://gitpod.io) account.

# Working in Gitpod (Officially Supported)

*NOTE*: The Gitpod free tier comes with 50 hours of use per month.  We expect our work will be done in less time than that.  However, you may wish to conserve time on the platform by being sure to stop your workspace when you are done with it.  Gitpod will time you out (don't worry, your work will be saved), but that may take longer to detect.

The following things must be done each time you create a new Gitpod Workspace (unfortunately, we can't automate this)

1. Fork this repository.
1. Launch a new Gitpod workspace based on this repository.  This will automatically start OpenSearch and OpenSearch Dashboards.
    1. Note: it can take a few minutes for OpenSearch and the dashboards to launch.        
1. You should now have a running Opensearch instance (port 9200) and a running Opensearch Dashboards instance (port 5601)
1. Login to the dashboards at `https://5601-<$GITPOD_URL>/` with default username `admin` and password `admin`. This should popup automatically as a new tab, unless you have blocked popups.  Also note, that in the real world, you would change your password.  Since these ports are blocked if you aren't logged into Gitpod, it's OK.

        $GITPOD_URL is a placeholder for your ephemeral Gitpod host name, e.g. silver-grasshopper-8czadqyn.ws-us25.gitpod.io     

# Downloading the Best Buy Dataset

1. Run the install [Kaggle API token](https://www.kaggle.com/docs/api) script and follow the instructions:

        ./install-kaggle-token.sh
1. Accept all of the [kaggle competition rules](https://www.kaggle.com/c/acm-sf-chapter-hackathon-big/rules) then run the download data script:

        ./download-data.sh

1. To index the data, open up a virtual environment and then run:

```
./index-data.sh
```


### 🐞 Debugging: `./counter-tracker.sh` logs 0 results for Queries and Products

I ran `./index-data.sh` and then saw this output as expected:
```bash
mkdir: cannot create directory ‘/workspace/logs’: File exists
Running python scripts from /workspace/search_with_machine_learning_course/utilities
++ '[' '' '!=' --annotate ']'
++ echo 'Creating index settings and mappings'
Creating index settings and mappings
++ '[' -f /workspace/search_with_machine_learning_course/conf/bbuy_products.json ']'
++ echo ' Product file: /workspace/search_with_machine_learning_course/conf/bbuy_products.json'
 Product file: /workspace/search_with_machine_learning_course/conf/bbuy_products.json
++ curl -k -X PUT -u admin https://localhost:9200/bbuy_products -H 'Content-Type: application/json' -d @/workspace/search_with_machine_learning_course/conf/bbuy_products.json
Enter host password for user 'admin':
{"acknowledged":true,"shards_acknowledged":true,"index":"bbuy_products"}++ '[' 0 -ne 0 ']'
++ '[' -f index_products.py ']'
++ echo 'Indexing product data in /workspace/datasets/product_data/products and writing logs to /workspace/logs/index_products.log'
Indexing product data in /workspace/datasets/product_data/products and writing logs to /workspace/logs/index_products.log
++ '[' 0 -ne 0 ']'
++ '[' -f /workspace/search_with_machine_learning_course/conf/bbuy_queries.json ']'
++ echo ''

++ echo ' Query file: /workspace/search_with_machine_learning_course/conf/bbuy_queries.json'
 Query file: /workspace/search_with_machine_learning_course/conf/bbuy_queries.json
++ nohup python index_products.py -s /workspace/datasets/product_data/products
++ curl -k -X PUT -u admin https://localhost:9200/bbuy_queries -H 'Content-Type: application/json' -d @/workspace/search_with_machine_learning_course/conf/bbuy_queries.json
Enter host password for user 'admin':nohup: redirecting stderr to stdout

{"acknowledged":true,"shards_acknowledged":true,"index":"bbuy_queries"}++ '[' 0 -ne 0 ']'
++ '[' -f index_queries.py ']'
++ echo 'Indexing queries data and writing logs to /workspace/logs/index_queries.log'
Indexing queries data and writing logs to /workspace/logs/index_queries.log
++ '[' 0 -ne 0 ']'
++ nohup python index_queries.py -s /workspace/datasets/train.csv
++ '[' '' == --annotate ']'
nohup: redirecting stderr to stdout
```

Then, when I ran `./count-tracker.sh`, I saw this output:
```bash
Queries:
1699818839 19:53:59 0
Products:
1699818839 19:53:59 0
Queries:
1699818899 19:54:59 0
Products:
1699818899 19:54:59 0
```

I needed to investigate why that was the case. I cd'ed to `/workspace/logs` and then found there were two files in there:
```bash
index_products.log  index_queries.log
```

I vim'ed into one of them with `vim index_products.log` and saw this output:

```bash
Traceback (most recent call last):
  File "/workspace/search_with_machine_learning_course/utilities/index_products.py", line 2, in <module>
    import opensearchpy
ModuleNotFoundError: No module named 'opensearchpy'
```

This was showing that there wasn't a specific package I needed, meaning pyenv was not being leveraged to run these indexing commands.

1. First, set up the virtual env:
```bash
pyenv activate search_with_ml
```

2. Next, ensure that there are no indices already created for `bbuy_products` and `bbuy_queries`. Running `DELETE /bbuy_products` might not be enough, as you might need to `PUT` a number_of_replicas as 0 first before running the `DELETE`.

```bash
DELETE /bbuy_products
DELETE /bbuy_queries

PUT /bbuy_products/_settings
{
  "index" : {
      "number_of_replicas" : 0
  }
}

PUT /bbuy_queries/_settings
{
  "index" : {
      "number_of_replicas" : 0
  }
}
```

3. To confirm this, get the indeces running in the local environment:
```bash
curl -k -X GET -u admin:admin "https://localhost:9200/_cat/indices"
```

The output should be free of `bbuy_products` and `bbuy_queries` like this:
```bash
green  open .kibana_-152937574_admintenant_1          kUnDXzogTjShsBI7mcUV0g 1 0     1 0   5.1kb   5.1kb
yellow open searchml_ltr                              ZK8Dp78IT7GhBdQr69KOBw 1 1     8 0  42.2kb  42.2kb
yellow open security-auditlog-2023.11.12              WHoHckngTsGpAffh4CpUwA 1 1    16 0 120.5kb 120.5kb
green  open .kibana_92668751_admin_1                  ZLgmJA-2TWCALeNAxfomcg 1 0    59 0  34.1kb  34.1kb
yellow open security-auditlog-2023.10.30              J1X6D2nUTBKdR3jK6rOVeA 1 1    64 0 277.3kb 277.3kb
green  open opensearch_dashboards_sample_data_flights 3mSunE6pTnyVgx04c1fRrQ 1 0 13059 0   5.9mb   5.9mb
yellow open searchml_test                             apOikCLeSnyrTpOzW2o17g 1 1     4 0   6.3kb   6.3kb
yellow open security-auditlog-2023.11.05              ggC-f_6QTLyb2_tWoRX86w 1 1    11 0  50.6kb  50.6kb
yellow open search_fun_test                           EzBEA4GxQECOcbgZH-N-qA 1 1     4 0   6.9kb   6.9kb
green  open .opendistro_security                      iln1t4KNQHC2PeYBnbzgtw 1 0    10 0  71.7kb  71.7kb
green  open .kibana_1                                 GvnZo_00TL2H8Typ3ucrJQ 1 0     1 0   4.2kb   4.2kb
yellow open security-auditlog-2023.11.06              A-wsBDysRiS_XxhOhbpr-g 1 1    47 0  93.5kb  93.5kb
```

^ If either of those indexes are still there, do the PUT command and then the DELETE and it should clear it out.

4. Set up the Python virtual environment:

Discover the available virtual envs to choose:
```bash
pyenv virtualenvs
```

This should return 2 options:
- `3.9.7/envs/search_with_ml (created from /home/gitpod/.pyenv/versions/3.9.7)`
- `search_with_ml (created from /home/gitpod/.pyenv/versions/3.9.7)`\
    - We want this one

Select the `search_with_ml` virtualenv and activate it with this command:
```bash
pyenv activate search_with_ml
```

The terminal should now look like this: `(search_with_ml) gitpod /workspace/search_with_machine_learning_course (main) $`

5. Run the `index-data.sh` file in the virtual environment:

```bash
./index-data.sh
```




# Exploring the OpenSearch Sample Dashboards and Data

1. Login to OpenSearch and point your browser at `https://5601-<$GITPOD_URL>/app/opensearch_dashboards_overview#/`
1. Click the "Add sample data" link
1. Click the "Add Data" link for any of the 3 projects listed. In the class, we chose the "Sample flight data", but any of the three are fine for exploration.

# Running the Weekly Project

At the command line, do the following steps to run the example.  

1. Activate your Python Virtual Environment.  We use `pyenv` (Pyenv website)[https://github.com/pyenv/pyenv] and `pyenv-virtualenv` (Pyenv Virtualenv)[https://github.com/pyenv/pyenv-virtualenv].
    1. `pyenv activate search_with_ml` -- Activate the Virtualenv. 
1. Optional: You can run `ipython` if you like.
    
# Working locally (Not supported, but may work for you. YMMV)

To run locally, you will need a few things:

1. [Pyenv](https://github.com/pyenv/pyenv) and [Pyenv-Virtualenv](https://github.com/pyenv/pyenv-virtualenv) with Python 3.9.7 installed
1. [Docker](https://docker.com/)
1. A [Git](https://git-scm.com/) client

Note: these have only been tested on a Mac running OS 12.2.1.  YMMV.  Much of what you will need to do will be similar to what's in `.gitpod.Dockerfile`

1.  Install [GraphViz](https://www.graphviz.org/)
1. `pyenv install 3.9.7`
1. `pip install` all of the libraries you see in `.gitpod.Dockerfile`
1. Setup your weekly python environments per the "Weekly Project" above.
1. Install [Fasttext](https://fasttext.cc/)  
1. Run OpenSearch: 
    1. `cd docker`
    1. `docker-compose up`
1. Note: most of the scripts and projects assume the data is in `/workspace/datasets`, but have overrides to specify your own directories. You will need to download and plan accordingly.  
1. Do your work per the Weekly Project     
    