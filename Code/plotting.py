import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

def plot_histogram(data, methodname="Modularity_Maximization", label="test"):

    plt.figure(figsize=(6,4))  #6x4 is the aspect ratio for the plot
    n, bins, patches = plt.hist(data, 50, normed=1, facecolor='green', alpha=0.75)

    plt.title("Cluster Size Histogram")
    plt.xlabel("Cluster Size")
    plt.ylabel("Proportion of Clusters")
    plt.yscale("log")
    plt.legend([methodname], loc="best")

    #Make sure labels and titles are inside plot area
    plt.tight_layout()
    plt.savefig("./Figures/"+methodname+"_cluster_size_"+label+".pdf")

def plot_line(x, testscore, methodname="Modularity_Maximization", paraname="Number of Clusters", label="test"):
    #Plot a line graph
    plt.figure(figsize=(6,4))  #6x4 is the aspect ratio for the plot
    plt.plot(x, testscore,'sb-', linewidth=3) #Plot the first series in blue with square marker

    #This plots the data
    plt.grid(True) #Turn the grid on
    plt.ylabel("Modularity") #Y-axis label
    plt.xlabel(paraname) #X-axis label
    plt.title("Modularity vs "+paraname) #Plot title
    plt.xlim(0.0, max(x)+0.1) #set x axis range
    plt.ylim(0.0, 1.0) #set yaxis range
    plt.legend([methodname],loc="best")

    #Make sure labels and titles are inside plot area
    plt.tight_layout()
    plt.savefig("./Figures/"+methodname+"_modularity_score_"+label+".pdf")

