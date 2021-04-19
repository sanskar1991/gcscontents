# gcscontents

It aims to a be a transparent, drop-in replacement for Jupyter standard filesystem-backed storage system.
With this implementation of a Jupyter Contents Manager you can save all your notebooks, regular files, directories

## Installation

```
$ pip install s3contents
```

## Jupyter config

Edit `~/.jupyter/jupyter_notebook_config.py` based on the backend you want to
based on the examples below. Replace credentials as needed.



## GCP Cloud Storage

```python
from GCScontents import GCloudContentsManager

c = get_config()

c.NotebookApp.contents_manager_class = GCloudContentsManager
c.GCloudContentsManager.project = "{{ your-project }}"
c.GCloudContentsManager.token = "~/.config/gcloud/application_default_credentials.json"
c.GCloudContentsManager.bucket = "{{ GCP bucket name }}"
```

Note that the file `~/.config/gcloud/application_default_credentials.json` assumes a posix system
when you did `gcloud init`