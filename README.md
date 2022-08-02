# Scratchpad

This repository hosts notes/notebooks and one off explorations, so I can look them up easily. 

The posts are in reverse chronological order by the date they were added though a lot of them date back multiple years. 

## Index

**[Nicer SQL syntax using FunSQL](./jupyter-notebooks/against-sql.ipynb)**
* date: `2022-06-27`
* topic: Jupyter notebook that addresses some of the SQL syntax quirks mentioned in the [against-sql](https://www.scattered-thoughts.net/writing/against-sql/) post by Jamie Brandon. Uses the `FunSQL` python library. 
* tiny-notes: Using a DSL hosted in the language allows for richer abstractions. I really need to clean up the FunSQL library code though. 

<hr/>

**[VMSP algorithm](./jupyter-notebooks/vmsp-mining.ipynb)**
* date: `2022-06-02`
* topic: Implements the VMSP (Vertical Maximal Sequence Patterns) algorithm to find frequent subsequences in a collection of event logs. Based off the work [here](https://www.philippe-fournier-viger.com/spmf/VMSP.php). 
* tiny-notes: Could be used to surface frequent patterns when digging into event sequences. The [MAQUI](https://www.zcliu.org/maqui/) work for recursive event exploration uses it. Tabled for later when I try to replicate the full application. 

<hr/>

**[Metrics layer tools](./md-posts/metrics_layer.md)**
* date: `2020-04-20`
* topic: What I can understand from the pitch for `Metric layer` tools. 
* tiny-notes: Seems like a nice way to keep analytics disciplined. Not sure if it warrants a separate service though, maybe as a library that you can integrate with your existing analytics code. 

<hr/>

**[Writing a Recommendation System](./md-posts/reco_system.md)**
* date: `2021-11-01`
* topic: Describes the recommendation system behind an adaptive learning API platform for school students. 
* tiny-notes: The post never made it to the company blog, so stored here for posterity. 

<hr/>

**[Code from a Forth tutorial](./forth-snake/)**
* date: `2021-10-29`
* topic: What writing the Snake game in your calculator is like; following the tutorial at [link](https://skilldrick.github.io/easyforth/). 
* tiny-notes: Concatenative programming seems pretty cool. Time to dive into a language like APL. 

<hr/>

**[Change Data capture](./cdc/)**
* date: `2021-05-30`
* topic: How materialize does change data capture; original post on their [blog](https://materialize.com/change-data-capture-part-1/). 
* tiny-notes: pretty neat model, was easy enough to follow and write it up in python. 