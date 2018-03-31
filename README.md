# Detecting Community Structure in Scientific Networks

### Author: Yuan Huang

In this project, we will apply two clustering methods to detect the community structure in Physical Review citation network. We test the robustness of these two methods and check the significance of our results using the modularity measure. We apply both algorithms to the Physical Review citation network to resolve its major communities and the connections between them. We also visualize the structure of the individual communities.

## Prerequisites

This project is based on mongodb, pymongo, and D3 visualization library.

## Installing

The installation of mongodb on different operating systems can be found in [Installation](https://docs.mongodb.com/manual/installation/). Be sure to have a directory `/data/db` with read and write permission as the default mongodb dbpath.

The installation of pymongo can be done by
```
pip install pymongo
```

## Running the code

To run the code, you need to first install mongodb, create the directory `/data/db` and run the following commands to start a local mongod server:
```
mongod
```
Then run the following scripts to load the mongodb database and start the main code:
```
./run.sh
```
The code will print out some information about the simulation status. It will take 1.5 to 2 hours to finish. The code will write to some result files in `Data/` and plot some statistical figures to `Figures/`.

To see the interactive visualization on a webpage, you need to run the following script:
```
./visual.sh
```
and open webpage `localhost:8000` in your brower to get access to the visualizations. On the webpage, there are two links corresponding to the article network on the test data and the cluster network on the whole dataset.

## Dataset

The dataset is requested on the American Physical Society webpage [Dataset](https://journals.aps.org/datasets).
