# 26UAMPC204 Artificial Intelligence — BTL Question Bank

30 questions per unit (5 per Bloom's level). Marks: L1 = 2, L2–L3 = 5, L4–L6 = 10.

## Unit I: Introduction to AI and Intelligent Agents (CO204.1)

| # | Question | BTL | Marks |
|---|---|---|---|
| 1 | Define Artificial Intelligence. State any two definitions from the four categories proposed by Russell and Norvig. | L1 – Remember | 2 |
| 2 | What is the Turing Test? List the four capabilities a machine needs to pass it. | L1 – Remember | 2 |
| 3 | Define an agent, a percept sequence and an agent function. | L1 – Remember | 2 |
| 4 | Expand PEAS and state what each component specifies. | L1 – Remember | 2 |
| 5 | List the five components of a well-defined search problem. | L1 – Remember | 2 |
| 6 | Explain the four approaches to AI (thinking/acting, humanly/rationally) with one example each. | L2 – Understand | 5 |
| 7 | Describe the major milestones in the history and evolution of AI from 1943 to the present. | L2 – Understand | 5 |
| 8 | Explain the concept of rationality. Why is a rational agent not the same as an omniscient agent? | L2 – Understand | 5 |
| 9 | Discuss the contributions of mathematics, economics, neuroscience and psychology to the foundations of AI. | L2 – Understand | 5 |
| 10 | Explain the structure of a learning agent with a neat diagram, describing the role of the critic and problem generator. | L2 – Understand | 5 |
| 11 | Write the PEAS description for (a) an automated taxi driver and (b) an online English tutor. | L3 – Apply | 5 |
| 12 | Classify the task environment of (a) crossword puzzle, (b) poker and (c) medical diagnosis along all seven properties. | L3 – Apply | 5 |
| 13 | Formulate the 8-puzzle problem as a state-space search problem. How many states are reachable? | L3 – Apply | 5 |
| 14 | Formulate the Water-Jug problem (4 L and 3 L jugs, goal 2 L) and give one solution path. | L3 – Apply | 5 |
| 15 | Write the agent function in tabular form for the two-square vacuum-cleaner world. | L3 – Apply | 5 |
| 16 | Compare simple-reflex, model-based, goal-based and utility-based agents in terms of internal state, knowledge required and flexibility. | L4 – Analyse | 10 |
| 17 | Analyse why a simple-reflex agent may loop forever in a partially observable environment and how randomisation or a model helps. | L4 – Analyse | 10 |
| 18 | Distinguish between a state and a node in a search tree. Analyse how repeated states inflate the Water-Jug search tree. | L4 – Analyse | 10 |
| 19 | Differentiate episodic vs sequential and static vs dynamic environments with examples from Indian application domains (UPI fraud detection, traffic signals). | L4 – Analyse | 10 |
| 20 | Analyse the Missionaries-and-Cannibals problem: identify states, legal actions and illegal states. | L4 – Analyse | 10 |
| 21 | Evaluate the Turing Test as a criterion of machine intelligence in the light of Searle's Chinese Room argument and modern LLMs. | L5 – Evaluate | 10 |
| 22 | Critically assess whether a self-driving car should be designed as a goal-based or a utility-based agent. Justify your choice. | L5 – Evaluate | 10 |
| 23 | Judge the suitability of a performance measure 'amount of dirt cleaned' for a vacuum agent. Propose and defend a better measure. | L5 – Evaluate | 10 |
| 24 | Evaluate the claim that 'any AI problem can be solved if it is formulated as a state-space search'. Give supporting and counter examples. | L5 – Evaluate | 10 |
| 25 | Assess the impact of AI applications in Indian healthcare and agriculture, citing benefits and risks. | L5 – Evaluate | 10 |
| 26 | Design a complete PEAS specification and agent architecture for a smart campus energy-management agent at Sanjivani University. | L6 – Create | 10 |
| 27 | Propose a learning-agent design for a personalised tutoring system; identify the performance element, critic, learning element and problem generator. | L6 – Create | 10 |
| 28 | Formulate a real-world exam-timetabling problem as a well-defined search problem, specifying all five components. | L6 – Create | 10 |
| 29 | Develop a taxonomy chart that maps ten everyday AI applications to environment properties and suitable agent types. | L6 – Create | 10 |
| 30 | Create a state-space representation for a delivery-drone routing problem in a city, including action costs and goal test. | L6 – Create | 10 |

## Unit II: Problem Solving by Search (CO204.2)

| # | Question | BTL | Marks |
|---|---|---|---|
| 1 | Define branching factor, depth of solution and maximum depth of a search tree. | L1 – Remember | 2 |
| 2 | State the data structure used for the frontier in BFS, DFS and UCS. | L1 – Remember | 2 |
| 3 | Define an admissible heuristic and a consistent heuristic. | L1 – Remember | 2 |
| 4 | What is a constraint satisfaction problem? State its three components. | L1 – Remember | 2 |
| 5 | State the evaluation function used by Greedy Best-First Search and A*. | L1 – Remember | 2 |
| 6 | Explain Iterative-Deepening Search and why its overhead is small compared to BFS. | L2 – Understand | 5 |
| 7 | Explain the problems of local maxima, ridges and plateaux in hill climbing and the remedies. | L2 – Understand | 5 |
| 8 | Describe simulated annealing and the role of temperature in accepting worse moves. | L2 – Understand | 5 |
| 9 | Explain the working of a genetic algorithm with selection, crossover and mutation for the 8-queens problem. | L2 – Understand | 5 |
| 10 | Explain bidirectional search and state when it cannot be applied. | L2 – Understand | 5 |
| 11 | Apply BFS and DFS to a given graph (A–G) and write the order of node expansion and the path found. | L3 – Apply | 5 |
| 12 | Apply A* on the Romania map from Arad to Bucharest using straight-line distance and show f, g, h for each expansion. | L3 – Apply | 5 |
| 13 | Compute h1 (misplaced tiles) and h2 (Manhattan distance) for a given 8-puzzle start state. | L3 – Apply | 5 |
| 14 | Apply Minimax to a given 3-ply game tree and find the value of the root and the best move. | L3 – Apply | 5 |
| 15 | Solve the Australia map-colouring CSP using backtracking with MRV and forward checking. | L3 – Apply | 5 |
| 16 | Compare BFS, DFS, DLS, IDS, UCS and bidirectional search on completeness, optimality, time and space complexity. | L4 – Analyse | 10 |
| 17 | Analyse why A* with a consistent heuristic never re-expands a node, while an inadmissible heuristic may return a sub-optimal path. | L4 – Analyse | 10 |
| 18 | Apply alpha–beta pruning to a given game tree; identify pruned branches and analyse how move ordering affects pruning. | L4 – Analyse | 10 |
| 19 | Differentiate global search (A*) from local search (hill climbing) with respect to memory, optimality and application domains. | L4 – Analyse | 10 |
| 20 | Analyse AC-3 on a small CSP and show the domain reductions after each arc revision. | L4 – Analyse | 10 |
| 21 | Evaluate which search strategy is best suited for a GPS navigation app with millions of nodes. Justify with complexity arguments. | L5 – Evaluate | 10 |
| 22 | Judge whether the heuristic h(n) = 2 × Manhattan distance is acceptable for the 8-puzzle; discuss the speed–optimality trade-off. | L5 – Evaluate | 10 |
| 23 | Critically compare simulated annealing and genetic algorithms for solving the Travelling Salesperson Problem. | L5 – Evaluate | 10 |
| 24 | Assess the limitations of Minimax for real games such as chess and Go and evaluate how MCTS overcomes them. | L5 – Evaluate | 10 |
| 25 | Evaluate the effectiveness of MRV, degree and LCV heuristics on Sudoku solving. | L5 – Evaluate | 10 |
| 26 | Design an admissible heuristic for a robot path-planning problem on a grid with diagonal moves and prove its admissibility. | L6 – Create | 10 |
| 27 | Develop a complete Tic-Tac-Toe agent using Minimax with alpha–beta pruning; write the pseudocode and evaluation function. | L6 – Create | 10 |
| 28 | Formulate the university exam-scheduling problem as a CSP and propose a solving strategy. | L6 – Create | 10 |
| 29 | Design a genetic algorithm (encoding, fitness, operators) for a class-timetable optimisation problem. | L6 – Create | 10 |
| 30 | Create a comparative experiment plan to benchmark BFS, IDS and A* on randomly generated 8-puzzle instances. | L6 – Create | 10 |

## Unit III: Knowledge Representation and Reasoning (CO204.3)

| # | Question | BTL | Marks |
|---|---|---|---|
| 1 | What is a knowledge base? State the two operations of a knowledge-based agent. | L1 – Remember | 2 |
| 2 | Define entailment, validity and satisfiability. | L1 – Remember | 2 |
| 3 | List the connectives of propositional logic in order of precedence. | L1 – Remember | 2 |
| 4 | Define unification and the most general unifier. | L1 – Remember | 2 |
| 5 | What is a frame? Name its main components. | L1 – Remember | 2 |
| 6 | Explain the architecture of a knowledge-based agent with the KB-AGENT algorithm. | L2 – Understand | 5 |
| 7 | Explain the difference between propositional logic and first-order logic with examples. | L2 – Understand | 5 |
| 8 | Explain universal and existential quantifiers and the duality between them. | L2 – Understand | 5 |
| 9 | Describe semantic networks with an example showing inheritance through is-a links. | L2 – Understand | 5 |
| 10 | Explain what an ontology is and describe the role of RDF and OWL. | L2 – Understand | 5 |
| 11 | Construct the truth table to prove that (P ⇒ Q) ≡ (¬P ∨ Q). | L3 – Apply | 5 |
| 12 | Convert the sentence (A ⇔ B) ⇒ C to Conjunctive Normal Form, showing each step. | L3 – Apply | 5 |
| 13 | Translate into FOL: (a) All students who study pass. (b) Some birds cannot fly. (c) Every person has a mother. | L3 – Apply | 5 |
| 14 | Find the MGU of Knows(John, x) and Knows(y, Mother(y)); and of P(x, f(y)) and P(a, f(g(z))). | L3 – Apply | 5 |
| 15 | Represent the Hotel-Room domain using frames with slots, default values and procedures. | L3 – Apply | 5 |
| 16 | Apply forward chaining to the Colonel West crime knowledge base and show each iteration. | L4 – Analyse | 10 |
| 17 | Apply backward chaining to prove Criminal(West) and draw the proof tree. | L4 – Analyse | 10 |
| 18 | Compare forward and backward chaining with respect to direction, efficiency and application domains. | L4 – Analyse | 10 |
| 19 | Analyse the common errors in translating English to FOL involving ∀ with ∧ and ∃ with ⇒. | L4 – Analyse | 10 |
| 20 | Distinguish between semantic networks, frames and ontologies on expressiveness and reasoning support. | L4 – Analyse | 10 |
| 21 | Prove using resolution: Given ∀x Man(x) ⇒ Mortal(x) and Man(Socrates), prove Mortal(Socrates); justify each step. | L5 – Evaluate | 10 |
| 22 | Evaluate the soundness and completeness of resolution as an inference procedure. | L5 – Evaluate | 10 |
| 23 | Assess the limitations of propositional logic for representing the Wumpus World and justify the need for FOL. | L5 – Evaluate | 10 |
| 24 | Critically evaluate rule-based (logic) knowledge representation against neural representations used in LLMs. | L5 – Evaluate | 10 |
| 25 | Judge whether the sentence ∀x ∃y Loves(x,y) entails ∃y ∀x Loves(x,y). Justify with a model. | L5 – Evaluate | 10 |
| 26 | Design a family-relationship knowledge base in FOL (parent, grandparent, sibling, cousin) and pose three queries. | L6 – Create | 10 |
| 27 | Develop a Prolog program for a university course-prerequisite knowledge base and trace a query. | L6 – Create | 10 |
| 28 | Create an ontology (classes, properties, individuals) for the AI & DS department using RDF triples. | L6 – Create | 10 |
| 29 | Construct a complete resolution refutation proof for a given knowledge base about 'Marcus' (Rich & Knight). | L6 – Create | 10 |
| 30 | Design a semantic network for an Indian railway reservation system showing inheritance and attributes. | L6 – Create | 10 |

## Unit IV: Planning and Reasoning under Uncertainty (CO204.4)

| # | Question | BTL | Marks |
|---|---|---|---|
| 1 | State the components of a planning system. | L1 – Remember | 2 |
| 2 | What does STRIPS stand for? List the parts of a STRIPS action schema. | L1 – Remember | 2 |
| 3 | State Bayes' theorem and name each term. | L1 – Remember | 2 |
| 4 | Define a Bayesian network and a conditional probability table. | L1 – Remember | 2 |
| 5 | Define a fuzzy set and a membership function. | L1 – Remember | 2 |
| 6 | Explain forward (progression) and backward (regression) state-space planning. | L2 – Understand | 5 |
| 7 | Explain partial-order planning with causal links, ordering constraints and threats. | L2 – Understand | 5 |
| 8 | Describe the sources of uncertainty faced by an intelligent agent. | L2 – Understand | 5 |
| 9 | Explain conditional independence and how it makes Bayesian networks compact. | L2 – Understand | 5 |
| 10 | Explain the steps of a Mamdani fuzzy inference system with a block diagram. | L2 – Understand | 5 |
| 11 | Write STRIPS operators for PickUp, PutDown, Stack and Unstack in the Blocks World. | L3 – Apply | 5 |
| 12 | A disease has prevalence 1%; a test has 90% sensitivity and 5% false-positive rate. Compute P(Disease | +). | L3 – Apply | 5 |
| 13 | Using the burglary network, compute P(j, m, a, ¬b, ¬e). | L3 – Apply | 5 |
| 14 | Draw triangular membership functions for Cold, Warm and Hot temperature and find the membership of 18 °C. | L3 – Apply | 5 |
| 15 | Compute P(cavity | toothache) from the given full joint distribution table. | L3 – Apply | 5 |
| 16 | Generate a plan for a given Blocks World problem using goal-stack planning and analyse the Sussman anomaly. | L4 – Analyse | 10 |
| 17 | Compare total-order and partial-order planning with an example (putting on shoes and socks). | L4 – Analyse | 10 |
| 18 | Compare probability theory and fuzzy logic for handling uncertainty and vagueness, with examples. | L4 – Analyse | 10 |
| 19 | Analyse inference by enumeration for P(Burglary | JohnCalls, MaryCalls) and comment on its complexity. | L4 – Analyse | 10 |
| 20 | Apply the fuzzy operators union, intersection, complement and the hedge 'very' on two given fuzzy sets. | L4 – Analyse | 10 |
| 21 | Evaluate the base-rate fallacy using the medical test example and its implications for AI diagnosis tools. | L5 – Evaluate | 10 |
| 22 | Assess the assumptions of classical planning and judge whether they hold for a Mars rover. | L5 – Evaluate | 10 |
| 23 | Critically evaluate Naïve Bayes for spam filtering: when does the independence assumption fail? | L5 – Evaluate | 10 |
| 24 | Judge whether exact or approximate inference should be used in a 100-node medical Bayesian network. | L5 – Evaluate | 10 |
| 25 | Evaluate the effect of different defuzzification methods (centroid, mean-of-max) on a fan-speed controller. | L5 – Evaluate | 10 |
| 26 | Design STRIPS/PDDL operators and a plan for a robot that delivers parcels between rooms. | L6 – Create | 10 |
| 27 | Construct a Bayesian network for diagnosing a laptop that does not boot; give the structure and CPTs. | L6 – Create | 10 |
| 28 | Design a complete fuzzy controller (inputs, rules, outputs) for an automatic washing machine. | L6 – Create | 10 |
| 29 | Propose a partial-order plan for preparing tea and identify all causal links and threats. | L6 – Create | 10 |
| 30 | Develop a probabilistic model for a crop-disease advisory system for farmers in Maharashtra. | L6 – Create | 10 |

## Unit V: Learning, Expert Systems and Applications of AI (CO204.5)

| # | Question | BTL | Marks |
|---|---|---|---|
| 1 | Define machine learning as given by Tom Mitchell. | L1 – Remember | 2 |
| 2 | List the three forms of learning with one example each. | L1 – Remember | 2 |
| 3 | Define entropy and information gain. | L1 – Remember | 2 |
| 4 | What is a perceptron? Write its output equation. | L1 – Remember | 2 |
| 5 | List the components of an expert system. | L1 – Remember | 2 |
| 6 | Explain supervised, unsupervised and reinforcement learning with suitable examples. | L2 – Understand | 5 |
| 7 | Explain how a decision tree is learned using the ID3 algorithm. | L2 – Understand | 5 |
| 8 | Explain the perceptron learning rule and the perceptron convergence theorem. | L2 – Understand | 5 |
| 9 | Explain the architecture of an expert system with a neat diagram. | L2 – Understand | 5 |
| 10 | Explain the knowledge acquisition process and why it is called a bottleneck. | L2 – Understand | 5 |
| 11 | Compute the entropy of a dataset with 9 positive and 5 negative examples. | L3 – Apply | 5 |
| 12 | Compute the information gain of attribute Outlook for the Play Tennis dataset. | L3 – Apply | 5 |
| 13 | Train a perceptron for the AND function (η = 1, initial weights 0) for two epochs; show all updates. | L3 – Apply | 5 |
| 14 | Apply forward chaining on a given medical rule base with certainty factors and compute the final CF. | L3 – Apply | 5 |
| 15 | Illustrate the stages of an NLP pipeline for the sentence 'Sanjivani University is in Kopargaon'. | L3 – Apply | 5 |
| 16 | Analyse why a single perceptron cannot learn XOR and how a multilayer network solves it. | L4 – Analyse | 10 |
| 17 | Compare decision trees and neural networks on interpretability, data requirement and accuracy. | L4 – Analyse | 10 |
| 18 | Compare forward-chaining and backward-chaining expert systems with examples (XCON, MYCIN). | L4 – Analyse | 10 |
| 19 | Analyse overfitting in decision trees and compare pre-pruning and post-pruning. | L4 – Analyse | 10 |
| 20 | Differentiate the AI techniques used in NLP, computer vision and robotics. | L4 – Analyse | 10 |
| 21 | Evaluate the ethical issues of bias and fairness in AI-based hiring or loan approval systems. | L5 – Evaluate | 10 |
| 22 | Assess the advantages and limitations of expert systems compared to machine-learning systems. | L5 – Evaluate | 10 |
| 23 | Critically evaluate the use of facial recognition by public authorities in India with reference to privacy laws. | L5 – Evaluate | 10 |
| 24 | Judge the need for explainability (XAI) in medical AI and evaluate LIME/SHAP-style explanations. | L5 – Evaluate | 10 |
| 25 | Evaluate the EU AI Act's risk-based approach and its relevance to Indian AI policy. | L5 – Evaluate | 10 |
| 26 | Design a rule-based expert system (at least 10 rules) for crop-disease diagnosis and show a sample consultation. | L6 – Create | 10 |
| 27 | Build a decision tree by hand for a given student-placement dataset and extract IF–THEN rules. | L6 – Create | 10 |
| 28 | Propose a responsible-AI checklist for a student-performance prediction system at a university. | L6 – Create | 10 |
| 29 | Design an AI-based chatbot for college admissions: architecture, NLP components and evaluation plan. | L6 – Create | 10 |
| 30 | Develop a reinforcement-learning formulation (states, actions, rewards) for a smart traffic-signal controller. | L6 – Create | 10 |
