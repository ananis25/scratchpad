# Node and Wire editors

This was prompted by looking at multiple tools for data exploration and analytics, ex - [Datablocks](https://datablocks.pro/), [Basis Data](https://www.getbasis.com/) and more. I looked at similar products and noted down the good bits.  

## Interesting ideas in the apps

### Nodes as execution primitive

* Nodes have structured input and output, and thus correspond to specific actions/transforms. This would make sharing code across projects easier, and also dial down the friction when starting a new analysis. 
Notebook cells lack this constraint, so it is hard to tell what each one does.
* Structured I/O allows for isolation between execution of each node. The flow of data between nodes can be realized by serializing the output, maybe even in process using a format like Arrow.
* **Feature I'd like** - A spotlight style search bar that surfaces other nodes to pass the output of current leaf nodes in. Knowing the data schema adds more context for suggestions.

### Visual workflow

- Nodes joined together to form a directed graph make the dataflow explicit.
- Flows are also a better medium for communication. And for someone to play with the analysis without digging into the code. Jupyter notebooks have been great for reproducible analysis but trying to parse the intent from a code document is still difficult.
- **Features I'd like**
    - Flow editors don't feel as good a tool for iterative work, if you don't have the entire pipeline in your head already. Notebooks leak global state, but feel more interactive. Could you solve this by launching a separate python kernel for each node, with the input data injected by the runtime?
    - Ability to switch between different views. 
        - Graph: look at the full workflow; get a joint view of alternative methods, or the same method with different parameters.
        - Linear/single-node: at development time, when following a single chain of operations.

### Shared modules of functionality

- Data products generally have low-level(?) integrations that abstract over storage - object stores (S3 and GCS buckets), or relational databases (MySQL, Postgres, Snowflake).
- Custom code support means connectors to applications and service providers can be written exactly once and so can simple modules to process them. Everyone has Stripe transactions to analyze and everyone uses Google analytics. This means you can reuse a lot of code easily. Though, of course you can already do that with open source libraries for each thing; the harder problem is to surface the relevant modules when needed. 
- **Features I'd like**
    - Writing adapters for specific data origins allows more conveniences. Like, schema and data quality checks, or carrying over metadata from the source.
    - Use the data model to create synthetic data sets, so you work on your analysis in isolation and deal with setting up data inflow later.

## Things I am curious about

- _How do you keep the product open source or open core?_
Is an open core as useful as interoperability? I would rather like the ability to export my analysis to an open runtime, like python or DAG executors like airflow. Though how does it work if I am using community/application provided modules, say like a sanitizer function for Stripe data?

- _How do you trade off performance with isolation?_
The start-up time for a python interpreter is non trivial. and so is loading third party libraries. But you also want to execute each node separately (push down query to warehouse, execute on GPU, security reasons).

## Similar projects in data land

### Zapier

- link - [https://zapier.com/](https://zapier.com/)

- No-code tool for automated workflows, of the if-this-then-that kind. The platform provides a lot of integrations and action blocks to connect together and create flows.

- **Notes**
    - Zapier doesn't seem to be focused on data heavy workloads.
    - One of the use-cases of the newer apps points at actions/triggers based on the output of some nodes. That pretty much overlaps with Zapier.
    - So, Zapier with data integrations and a lot of `transform` nodes?

### Notebook products

- Examples
    - **Deepnote** - python + SQL
    - **Hexdata** - python + SQL
    - **Observable** - javascript + SQL
    - **Runkit** - javascript

- Each of them builds improvements on the Jupyter notebook workflow, while retaining a `cell` as the execution primitive. Features include -
    - database integrations
    - better version control
    - cell dependency graphs
    - pre-installed universe of packages
    - input and visualization widgets
    - widgets to transform notebooks into applications

- Generally, not open source.

- Hexdata is interesting and pretty close to the existing standard, Jupyter notebooks. 
    - Dependency graph is exposed to the user, and makes the logic explicit.
    - The runtime also leverages it to make execution reactive - when a cell is updated, downstream cells are re-run.

- **Notes**
    - I am not fond of reactive execution. A lot of times, I could be doing multiverse analysis - compare output downstream for different values of an input parameter. So, you also need the ability to _gather_ a cell's output before it gets automatically re-evaluated.
    - Cells are not a good primitive even when supported by a dependency checker ala Hex. Errors like a cell mutating a value in another cell could still creep in.

### Workflow tools

- Examples
    - **DBT** - data pipelines in SQL
    - **Prefect** - general purpose python workflow engine
    - **Dagster** - data pipelines in python

- Each of them require you to model the data pipeline as a DAG, generally explicitly. You either write python scripts or declarative YAML files and register with the workflow engine, which then schedules and executes the graph.

- Generally open-core, with open source integrations to common data sources and typical tasks. The companies make proprietary IDEs to profile the graph execution, debug workflows, query run status, etc.

- **Notes**
    - These feel similar to the node-and-wire workflow, although those usually have a visual graph builder while these workflows are described in code.
    - I'd imagine the node editors implements a similar engine to manage graph execution.

### ML Ops tools

- Examples
    - Pachyderm
    - DVC

- These projects are more of the bolt-on to your code repository kind, managing version control for your entire project and datasets. Also, schedule experiments and deploy applications.

- **Notes**
    - More like CI/CD for ML projects. Very little overlap.

### Enso

- link: [https://enso.org/](https://enso.org/)

- Open source visual programming environment, focused on data analysis. You create nodes using the functional Enso language, but can also import R/Python/Javascript code. The runtime JIT compiles the entire flow to keep interop costs minimal.

- **Notes**
    - Super ambitious, they bring a compiler to a UI/library fight. It feels a lot like MIT Scratch, with the focus on visual data flow.
    - However, the UI and the graph navigation is very finicky on macOS. Projects often fail to initialize, citing service errors. They plan for a web application too, maybe that improve stability?
    - Also curious how many UX features can be realized without inventing a new language and just a regular python backend. 

### VizierDB

- link: [https://vizierdb.info/](https://vizierdb.info/)
- Not really a product but an open-source university project.
- Features
    - Provides a notebook interface but cells must produce outputs that can be serialized, like files, datasets, config parameters.
    - Each cell execution is a new process and does not share state with other cells.
    - Cells also provide multiple interaction modalities. For example, when working with a table, you can write pandas/sql code, or use a spreadsheet editor.
- **Notes**
    - This is my favorite of the lot. The only things I want to improve are
        - swapping the linear notebook layout with a flow-like editor
        - make forking the data flow or rolling back changes, easier to understand.
    - Would have been nicer if I didn't need to learn Scala to work on it.