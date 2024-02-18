2024-gold-and-silver-dashboard
==============================

Data fetched with API's like yahoo finance and NBP. Dashboard was created with Dash. Tools: Dash, API's, Docker.

Project Organization
------------


    ├── README.md          <- The top-level README for developers using this project.
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── src                <- Source code for use in this project.
    │   ├── data           <- Scripts to download or generate data
    │   │   └── make_dataset.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    ├── docker.*           <- Docker files to contarizate app   
    │
    ├── terraform          <- Terraform to create IaC on Google Cloud 
    │
    └── ansible            <- Ansible to automate configuration of software on infrastructure cretaed with Terraform 


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
