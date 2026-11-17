# 26UAMPC204 Artificial Intelligence — Project Portfolio (50 projects)

Mini = individual, 2 weeks. Major = team of 3–4, 6 weeks. Rubric: formulation 15, implementation 30, experiments 25, demo 15, documentation & ethics 15.

## Unit I: Introduction to AI and Intelligent Agents (CO204.1)

| ID | Project | Type | Problem | Tools | Deliverables |
|---|---|---|---|---|---|
| PI.01 | **Smart Campus PEAS Designer** | Mini | Build a web form that takes any agent idea and generates its PEAS table and seven-property environment classification with explanations. | Python, Streamlit | App, 10 sample agents, report |
| PI.02 | **Vacuum-World Agent Simulator** | Mini | Simulate simple-reflex, model-based and random agents in an n×n vacuum world and compare performance scores over 1000 runs. | Python, NumPy, Matplotlib | Simulator, comparison plots |
| PI.03 | **Water-Jug State-Space Visualiser** | Mini | Generate and draw the full reachable state graph for arbitrary jug capacities and highlight the shortest solution. | Python, NetworkX | Graph images, GIF of path |
| PI.04 | **Turing Test Chat Arena** | Major | Run a blinded Turing-style experiment: students chat with a human or an LLM and guess which; analyse detection accuracy. | Python, Flask, any LLM API | Web app, experiment report, statistics |
| PI.05 | **AI Timeline Explorer** | Mini | Interactive timeline of AI history (1943–today) with filters by era, approach and application. | HTML/JS, D3 or Plotly | Hosted page, dataset CSV |
| PI.06 | **Traffic-Signal Reflex vs Model Agent** | Major | Simulate a 4-way junction; compare a fixed-timer reflex agent with a model-based agent that counts queues. | Python, SimPy / Pygame | Simulation, average wait-time analysis |
| PI.07 | **8-Puzzle Problem Formulator** | Mini | Generate random solvable 8-puzzle states, check solvability by inversion parity and export as search problems. | Python | Library, unit tests |
| PI.08 | **Agent Architecture Playground** | Major | Implement all five agent types for the Wumpus-lite grid and visualise their decision process step by step. | Python, Pygame | Game, demo video, report |
| PI.09 | **Missionaries and Cannibals Solver** | Mini | Formulate and solve M&C with BFS; animate the boat crossings. | Python, Matplotlib animation | Solver, animated GIF |
| PI.10 | **AI Applications Survey Dashboard** | Mini | Survey 50 Indian AI applications (agri, health, fintech) and classify by agent type and environment. | Python, Pandas, Plotly | Dashboard, survey dataset |

## Unit II: Problem Solving by Search (CO204.2)

| ID | Project | Type | Problem | Tools | Deliverables |
|---|---|---|---|---|---|
| PII.01 | **Pathfinding Visualiser** | Major | Grid-based visualiser for BFS, DFS, UCS, Greedy and A* with walls, weights and step-by-step animation. | Python, Pygame or JS Canvas | App, benchmark table |
| PII.02 | **Pune Metro Route Planner** | Mini | Model Pune/Mumbai metro stations as a graph and find shortest-time routes with UCS and A*. | Python, NetworkX, Folium | Route planner, map output |
| PII.03 | **Sudoku Solver with AC-3** | Mini | Solve Sudoku using backtracking + MRV + AC-3; compare node counts with plain backtracking. | Python | Solver, performance chart |
| PII.04 | **Unbeatable Tic-Tac-Toe** | Mini | Minimax with alpha–beta and a GUI; log nodes searched with and without pruning. | Python, Tkinter | Game, pruning statistics |
| PII.05 | **Connect-Four AI** | Major | Depth-limited alpha–beta with a heuristic evaluation function; tune weights by self-play. | Python, NumPy | Game, evaluation study |
| PII.06 | **N-Queens: Hill Climbing vs SA vs GA** | Mini | Compare success rate and time of three local-search methods for n = 8…64. | Python, Matplotlib | Experiment notebook, plots |
| PII.07 | **Exam Timetable CSP** | Major | Schedule exams with room capacity and no-clash constraints using CSP techniques. | Python, OR-Tools (optional) | Timetable generator, report |
| PII.08 | **TSP with Genetic Algorithm** | Mini | Optimise a tour through 30 Indian cities; animate the best tour each generation. | Python, Matplotlib | GIF, convergence curve |
| PII.09 | **8-Puzzle Heuristic Study** | Mini | Measure effective branching factor of IDS, A*(h1), A*(h2) and a pattern-database heuristic. | Python | Results table, analysis |
| PII.10 | **Map-Colouring of Indian States** | Mini | Colour the map of Indian states with minimum colours using backtracking with forward checking. | Python, GeoPandas | Coloured map image |

## Unit III: Knowledge Representation and Reasoning (CO204.3)

| ID | Project | Type | Problem | Tools | Deliverables |
|---|---|---|---|---|---|
| PIII.01 | **Family Tree Reasoner in Prolog** | Mini | Encode a 4-generation family and answer grandparent, cousin, uncle queries. | SWI-Prolog / PySwip | KB, query log |
| PIII.02 | **Propositional Logic Toolkit** | Mini | Parse formulas, build truth tables, check validity/satisfiability and convert to CNF. | Python | Library, CLI, tests |
| PIII.03 | **Resolution Theorem Prover** | Major | Implement FOL resolution with unification and occurs check; prove classic textbook problems. | Python | Prover, proof traces |
| PIII.04 | **Wumpus World Logical Agent** | Major | A KB agent that infers safe squares using propositional inference and explores the cave. | Python, Pygame | Agent, visual demo |
| PIII.05 | **Forward-Chaining Rule Engine** | Mini | Generic forward-chaining engine with conflict resolution strategies and explanation trace. | Python | Engine, sample KBs |
| PIII.06 | **Department Ontology** | Mini | Build an OWL ontology for the AI&DS department and query it with SPARQL. | Protégé, rdflib | OWL file, SPARQL queries |
| PIII.07 | **Semantic Network Visualiser** | Mini | Draw a semantic network from triples and support inheritance-based queries. | Python, NetworkX | Tool, examples |
| PIII.08 | **Course Prerequisite Advisor** | Mini | Backward-chaining advisor that tells a student whether they can register for a course. | Prolog or Python | Advisor, test cases |
| PIII.09 | **English-to-FOL Helper** | Major | Use pattern rules (and optionally an LLM) to translate simple English sentences into FOL, with validation. | Python, spaCy | Tool, accuracy evaluation |
| PIII.10 | **Legal Rules Knowledge Base** | Mini | Encode a small set of Indian traffic rules and infer penalties for given scenarios. | Python / Prolog | KB, scenario report |

## Unit IV: Planning and Reasoning under Uncertainty (CO204.4)

| ID | Project | Type | Problem | Tools | Deliverables |
|---|---|---|---|---|---|
| PIV.01 | **Blocks-World STRIPS Planner** | Mini | Forward and backward STRIPS planners with a visual of each plan step. | Python | Planner, animation |
| PIV.02 | **PDDL Robot Delivery** | Major | Model a campus delivery robot in PDDL and solve using an off-the-shelf planner. | PDDL, Fast Downward / pyperplan | Domain & problem files, plans |
| PIV.03 | **Medical Diagnosis Bayesian Network** | Major | Build a BN for respiratory illnesses, perform inference and sensitivity analysis. | Python, pgmpy | Model, inference report |
| PIV.04 | **Naïve Bayes SMS Spam Filter** | Mini | Implement Naïve Bayes from scratch on the SMS Spam Collection; compare with scikit-learn. | Python, scikit-learn | Notebook, metrics |
| PIV.05 | **Bayes' Theorem Visual Calculator** | Mini | Interactive tool showing how prior, sensitivity and specificity change the posterior. | Streamlit / HTML | App |
| PIV.06 | **Fuzzy Washing-Machine Controller** | Mini | Mamdani controller with dirt and load inputs; plot the control surface. | Python, scikit-fuzzy | Controller, 3D surface |
| PIV.07 | **Fuzzy Traffic-Signal Timing** | Major | Fuzzy controller that sets green time from queue length and arrival rate; simulate against fixed timing. | Python, scikit-fuzzy, SimPy | Simulation, comparison |
| PIV.08 | **Partial-Order Planner** | Major | Implement POP with causal links and threat resolution; solve shoe-sock and tea-making domains. | Python | Planner, plan graphs |
| PIV.09 | **Monte-Carlo Bayesian Inference** | Mini | Compare enumeration, rejection sampling and likelihood weighting on the burglary network. | Python | Convergence plots |
| PIV.10 | **Crop Irrigation Fuzzy Advisor** | Mini | Fuzzy system using soil moisture and temperature to recommend irrigation duration for farmers. | Python, scikit-fuzzy | Advisor, rule base |

## Unit V: Learning, Expert Systems and Applications of AI (CO204.5)

| ID | Project | Type | Problem | Tools | Deliverables |
|---|---|---|---|---|---|
| PV.01 | **Decision Tree from Scratch** | Mini | Implement ID3 with entropy/information gain, visualise the tree and extract rules. | Python, Graphviz | Library, Play-Tennis demo |
| PV.02 | **Student Placement Predictor** | Major | Predict placement from academic features with decision trees; explain predictions and audit bias. | Python, scikit-learn, SHAP | Model, fairness report |
| PV.03 | **Perceptron Playground** | Mini | Animate perceptron learning on AND/OR/XOR and show why XOR fails; add a 2-layer MLP. | Python, Matplotlib animation | GIFs, notebook |
| PV.04 | **Crop Disease Expert System** | Major | Rule-based expert system with certainty factors and explanation for common Maharashtra crops. | Python / CLIPS (clipspy) | Expert system, consultation logs |
| PV.05 | **College Admission Chatbot** | Major | Intent-matching chatbot answering admission FAQs with fallback and logging. | Python, NLTK / Rasa | Chatbot, evaluation |
| PV.06 | **Handwritten Digit Recogniser** | Mini | Train a simple neural network on MNIST and deploy a drawing canvas for live prediction. | Python, PyTorch / Keras | App, accuracy report |
| PV.07 | **Sentiment Analyser for Reviews** | Mini | Classify product reviews (English/Marathi-English) with Naïve Bayes and a small neural net. | Python, scikit-learn | Notebook, confusion matrix |
| PV.08 | **Line-Following Robot Simulator** | Mini | Simulate a robot with sensors and a rule-based controller; extend with a learned controller. | Python, Pygame | Simulator, demo |
| PV.09 | **Q-Learning Grid World** | Mini | Reinforcement learning agent learning to reach a goal; plot reward curves and learned policy. | Python, NumPy | Notebook, policy heat-map |
| PV.10 | **Responsible-AI Audit Toolkit** | Major | Audit a trained classifier for bias, robustness and explainability; produce a model card. | Python, Fairlearn, SHAP | Toolkit, model card |
