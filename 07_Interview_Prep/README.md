# 26UAMPC204 Artificial Intelligence — Interview & Industry-Skills Handbook

> Practice questions written for this course, modelled on topics and formats commonly discussed for AI/ML and software-engineering interviews at product companies, AI labs, start-ups and IT-services / GCC firms. They are not verbatim questions from any specific company.

## Unit I: Introduction to AI and Intelligent Agents (CO204.1)

### 🚀 Top industry skills you gain

- Translating a vague business problem into an agent specification (PEAS)
- Classifying environments to pick a feasible AI approach
- Formulating problems as state spaces with clear actions, costs and goal tests
- Explaining AI history and limits clearly to non-technical stakeholders
- Comparing reflex, goal, utility and learning agent designs
- Reading problem statements critically before coding

**Tools:** Python, NetworkX, Jupyter, Draw.io / Excalidraw for agent diagrams  
**Job roles:** AI Product Analyst, Junior ML Engineer, Solutions Engineer  
**Portfolio output:** A one-page PEAS + architecture design doc for a real campus or city problem, with a state-space prototype in a notebook.

### 🎯 Interview questions with model answers

<details><summary><b>QI.01</b> [Concept · Easy · Product / Big Tech] What is a rational agent, and why is rational not the same as perfect?</summary>

A rational agent picks the action with the highest expected performance given its percepts and knowledge. It can still get a bad outcome because it cannot see the future or the full state; rationality is judged on the decision, not on luck.

</details>

<details><summary><b>QI.02</b> [Concept · Easy · IT Services / GCC] Write the PEAS description for a food-delivery app's rider-assignment agent.</summary>

Performance: delivery time, cost, rider utilisation, customer rating. Environment: city roads, traffic, restaurants, riders, customers. Actuators: assign order, re-route, notify. Sensors: GPS, order stream, traffic feed, rider status.

</details>

<details><summary><b>QI.03</b> [Concept · Medium · Robotics / Autonomy] Classify a warehouse robot's environment along the seven properties and say which property makes it hardest.</summary>

Partially observable, multi-agent, stochastic, sequential, dynamic, continuous, mostly known. Partial observability combined with other moving agents is hardest because the robot must track state it cannot see while others change it.

</details>

<details><summary><b>QI.04</b> [Concept · Medium · AI Research Lab] Is passing the Turing Test evidence of intelligence? Argue both sides briefly.</summary>

For: it is an operational, behaviour-based test that avoids defining 'thinking'. Against: it rewards imitation and deception, ignores grounding and understanding (Chinese Room), and modern LLMs can fool judges in short chats without reliable reasoning.

</details>

<details><summary><b>QI.05</b> [Concept · Medium · AI Startup] When would you choose a utility-based agent over a goal-based agent?</summary>

When goals conflict or outcomes are uncertain, e.g. a ride-hailing pricing agent trading off revenue, wait time and fairness. A utility function lets the agent rank partial successes and compute expected utility, which a binary goal cannot.

</details>

<details><summary><b>QI.06</b> [Coding · Easy · Product / Big Tech] Write a function that returns all valid successor states for the Water-Jug problem (capacities a, b).</summary>

Return fill-A, fill-B, empty-A, empty-B, pour A→B with d = min(x, b−y), pour B→A with d = min(y, a−x); drop any successor equal to the current state. O(1) per state.

</details>

<details><summary><b>QI.07</b> [Coding · Medium · Product / Big Tech] Given an 8-puzzle state, decide in O(n²) whether it is solvable.</summary>

Count inversions among the 8 tiles (ignore the blank). For a 3×3 board the state is solvable iff the inversion count is even. See the coding notebook for the implementation.

</details>

<details><summary><b>QI.08</b> [Coding · Medium · Gaming] Implement a simple-reflex vacuum agent and a model-based one; show where the reflex agent fails.</summary>

Reflex: if dirty Suck else move. In a world where it cannot sense location it loops; the model-based agent remembers which squares are clean and stops (NoOp) when all are clean, saving moves.

</details>

<details><summary><b>QI.09</b> [Design · Medium · AI Startup] Design an agent that schedules campus classrooms. Give the state space and the performance measure.</summary>

State: partial assignment of (course, room, slot). Actions: assign or move a course. Goal: all courses placed with no clash and capacity met. Performance: hard-constraint violations (must be 0) plus soft penalties such as gaps or room changes. Solve as a CSP with local repair.

</details>

<details><summary><b>QI.10</b> [Design · Hard · Robotics / Autonomy] Design a learning agent for an autonomous shuttle on a university campus. What are the critic and the problem generator?</summary>

Performance element: perception + planning stack. Critic: compares behaviour against a safety and comfort standard (near-misses, jerk, delays). Learning element: updates policies or cost weights from logged drives. Problem generator: proposes safe exploratory scenarios in simulation, not on real roads.

</details>

<details><summary><b>QI.11</b> [Design · Medium · IT Services / GCC] A bank wants 'AI' to reduce loan-processing time. How do you turn this into a well-defined AI problem?</summary>

Clarify the decision (approve / refer / reject), the data available, the performance measure (time, default rate, fairness), constraints (regulation, explainability) and the human-in-the-loop points. Then choose the agent type and formulate inputs, actions and evaluation.

</details>

<details><summary><b>QI.12</b> [Scenario · Easy · HealthTech] A hospital asks for an 'omniscient' triage AI. How do you set expectations?</summary>

Explain that the agent acts on available evidence, so it will sometimes be wrong; define a measurable performance target, keep clinicians in the loop, and design for safe failure such as escalation when confidence is low.

</details>

<details><summary><b>QI.13</b> [Scenario · Medium · Product / Big Tech] Your agent's performance measure is 'number of tickets closed'. What can go wrong?</summary>

Reward hacking: the agent closes tickets without solving them. Measure what you actually want (resolved without reopen, customer satisfaction) and add guard-rails; design the performance measure around the desired environment state, not agent behaviour.

</details>

<details><summary><b>QI.14</b> [Scenario · Medium · AI Research Lab] How would you explain to a manager why AI had 'winters', and what that means for today's projects?</summary>

Hype outran capability (combinatorial explosion, brittle expert systems, limited compute and data). The lesson is to scope projects to proven capability, measure value early and avoid over-promising.

</details>

<details><summary><b>QI.15</b> [Scenario · Hard · AI Startup] Customers want a fully autonomous AI agent that sends emails on their behalf. What design safeguards do you propose?</summary>

Least-privilege actions, confirmation for irreversible or external actions, audit logs, rate limits, clear undo paths, and monitoring for prompt-injection from incoming content. Start with a draft-and-approve mode before full autonomy.

</details>

## Unit II: Problem Solving by Search (CO204.2)

### 🚀 Top industry skills you gain

- Implementing BFS, DFS, UCS, IDS and A* from scratch with clean, tested code
- Designing admissible heuristics and reasoning about complexity
- Using priority queues, hash maps and visited sets correctly
- Applying local search / metaheuristics to optimisation problems
- Building game agents with Minimax and alpha–beta
- Modelling scheduling/allocation as CSPs and using solvers

**Tools:** Python heapq / collections, NetworkX, Google OR-Tools, Pygame (visualisers)  
**Job roles:** Software Engineer (algorithms), Routing / Logistics Engineer, Game AI Developer, Operations Research Analyst  
**Portfolio output:** A path-finding visualiser (BFS / A*) and a Sudoku or timetable CSP solver on GitHub with benchmarks.

### 🎯 Interview questions with model answers

<details><summary><b>QII.01</b> [Concept · Easy · Product / Big Tech] Compare BFS and DFS on time, space, completeness and optimality.</summary>

BFS: O(b^d) time and space, complete, optimal for unit costs. DFS: O(b^m) time, O(bm) space, not complete in infinite or cyclic spaces without checks, not optimal.

</details>

<details><summary><b>QII.02</b> [Concept · Medium · Product / Big Tech] What makes a heuristic admissible and consistent? Give an example that is admissible but not consistent.</summary>

Admissible: never overestimates the true cost. Consistent: h(n) ≤ c(n,n′) + h(n′). Example: on a path S→A→G with costs 1 and 1, h(S)=2, h(A)=0, h(G)=0 is admissible but violates consistency because h(S) > c(S,A) + h(A).

</details>

<details><summary><b>QII.03</b> [Concept · Medium · AI Research Lab] Why is iterative deepening not much slower than BFS?</summary>

Most nodes are at the deepest level; re-expanding shallower levels adds only a constant factor (about b/(b−1)). Total work stays O(b^d) while memory is only O(bd).

</details>

<details><summary><b>QII.04</b> [Concept · Medium · Gaming] How does move ordering affect alpha–beta pruning?</summary>

Searching the best moves first tightens α and β early, so more branches are pruned. With perfect ordering the effective branching factor drops to about √b, roughly doubling search depth for the same time.

</details>

<details><summary><b>QII.05</b> [Concept · Hard · AI Research Lab] Why does simulated annealing escape local optima while hill climbing does not?</summary>

It accepts worse moves with probability e^(ΔE/T). At high temperature it explores widely; as T falls it settles. A slow enough cooling schedule converges to a global optimum with high probability.

</details>

<details><summary><b>QII.06</b> [Coding · Medium · Product / Big Tech] Find the shortest path in a grid with obstacles (4-directional). Return its length or −1.</summary>

BFS from the start with a visited set; each layer is one step. O(R·C) time and space. Use A* with Manhattan distance for large grids.

</details>

<details><summary><b>QII.07</b> [Coding · Medium · Product / Big Tech] Implement Dijkstra / uniform-cost search with a heap and explain the stale-entry trick.</summary>

Push (cost, node); when popping, skip the entry if its cost is larger than the best known distance (lazy deletion). O((V+E) log V).

</details>

<details><summary><b>QII.08</b> [Coding · Hard · Product / Big Tech] Solve N-Queens and return the number of solutions for N = 8.</summary>

Backtracking column by column with sets for used rows and both diagonals (r−c, r+c). There are 92 solutions for N = 8; bitmasks make it faster.

</details>

<details><summary><b>QII.09</b> [Coding · Medium · Gaming] Write Minimax with alpha–beta for Tic-Tac-Toe and report nodes visited.</summary>

Recursive max/min with α, β; return utility at terminals. From the empty board plain Minimax visits about 550k nodes, alpha–beta about 18k. See the lab Experiment 4.

</details>

<details><summary><b>QII.10</b> [Design · Hard · Product / Big Tech] Design the route engine for a ride-hailing app serving a city of 10 million people.</summary>

Pre-process the road graph (contraction hierarchies or hub labels) for fast shortest paths, use live traffic as edge weights updated by stream, A* or bidirectional search for queries, caching for frequent pairs, and sharding by region. Measure p99 latency and ETA error.

</details>

<details><summary><b>QII.11</b> [Design · Medium · IT Services / GCC] Design an exam-timetabling system for a university.</summary>

Model as a CSP: variables are exams; domains are (slot, room) pairs; constraints cover student clashes, capacity and invigilators. Use MRV + forward checking, then local search (min-conflicts) to optimise soft constraints. Provide a manual override UI.

</details>

<details><summary><b>QII.12</b> [Design · Hard · FinTech] How would you optimise delivery routes for 200 vans each morning?</summary>

It is a vehicle-routing problem (NP-hard): start with a constructive heuristic, improve with local search or metaheuristics (2-opt, simulated annealing, GA), or use OR-Tools; respect time windows and capacities; re-plan incrementally during the day.

</details>

<details><summary><b>QII.13</b> [Scenario · Medium · Product / Big Tech] Your A* search is slow on a large map. What do you check first?</summary>

Heuristic quality (too weak → near-Dijkstra), duplicate states in the frontier, an inefficient priority queue, no closed set, memory pressure. Then consider bidirectional search, hierarchical maps or pre-computed landmarks (ALT).

</details>

<details><summary><b>QII.14</b> [Scenario · Medium · Gaming] An opponent AI is 'too perfect' and players quit. What do you change?</summary>

Limit search depth, add randomness among near-best moves, use a weaker evaluation function by difficulty level, and tune against player-retention metrics. Perfect play is not the product goal; fun is.

</details>

<details><summary><b>QII.15</b> [Scenario · Hard · AI Startup] A greedy heuristic gives good routes 95% of the time but occasionally terrible ones. How do you decide whether to ship it?</summary>

Quantify the tail (worst-case cost and frequency), assess business impact, add a fallback such as a time-bounded A* or a sanity check, and monitor in production. Ship with guard-rails if the tail is detectable and recoverable.

</details>

## Unit III: Knowledge Representation and Reasoning (CO204.3)

### 🚀 Top industry skills you gain

- Encoding domain rules as logic and knowledge graphs
- Implementing unification, forward and backward chaining
- Writing and debugging Prolog / rule-engine style programs
- Designing ontologies and querying them (RDF, SPARQL)
- Combining symbolic knowledge with LLMs (knowledge-grounded answers)
- Explaining why a system reached a conclusion (traceability)

**Tools:** SWI-Prolog / PySwip, rdflib, Protégé, Neo4j (knowledge graphs)  
**Job roles:** Knowledge Engineer, Knowledge-Graph Engineer, Conversational AI Engineer, Compliance-tech Developer  
**Portfolio output:** A small knowledge graph (e.g. department courses and prerequisites) with SPARQL queries and a rule-based Q&A layer.

### 🎯 Interview questions with model answers

<details><summary><b>QIII.01</b> [Concept · Easy · IT Services / GCC] Differentiate propositional logic and first-order logic with an example.</summary>

Propositional logic uses atomic true/false symbols (Rain → WetGround). FOL adds objects, predicates, functions and quantifiers (∀x Student(x) ⇒ Person(x)), so one sentence covers many cases.

</details>

<details><summary><b>QIII.02</b> [Concept · Medium · Product / Big Tech] What is unification? Unify Knows(John, x) with Knows(y, Mother(y)).</summary>

Unification finds a substitution that makes two expressions identical. Here θ = {y/John, x/Mother(John)}.

</details>

<details><summary><b>QIII.03</b> [Concept · Medium · AI Research Lab] Forward vs backward chaining — when do you prefer each?</summary>

Forward chaining is data-driven and suits monitoring and alerts where new facts arrive. Backward chaining is goal-driven and suits answering specific queries or diagnosis, avoiding irrelevant derivations.

</details>

<details><summary><b>QIII.04</b> [Concept · Medium · AI Startup] What is the difference between a knowledge graph and a relational database?</summary>

A knowledge graph stores entities and typed relationships as a graph with a flexible schema and supports traversal and inference; a relational database stores fixed-schema tables optimised for joins and transactions.

</details>

<details><summary><b>QIII.05</b> [Concept · Hard · AI Research Lab] Why is resolution refutation-complete but FOL entailment only semi-decidable?</summary>

If KB ⊨ α, resolution on KB ∧ ¬α will eventually derive the empty clause. If not entailed, the search may never terminate because FOL can generate infinitely many clauses.

</details>

<details><summary><b>QIII.06</b> [Coding · Medium · Product / Big Tech] Implement a truth-table checker that decides whether KB entails α.</summary>

Enumerate all 2^n assignments; whenever KB is true, α must also be true. Return False on the first counter-model. O(2^n · |KB|).

</details>

<details><summary><b>QIII.07</b> [Coding · Medium · IT Services / GCC] Write a forward-chaining engine for Horn rules and report derived facts.</summary>

Keep a fact set; loop over rules and fire those whose premises are all present; stop at a fixed point. Use a count-of-unsatisfied-premises agenda for linear time.

</details>

<details><summary><b>QIII.08</b> [Coding · Hard · AI Research Lab] Implement unification with the occurs check.</summary>

Recursively walk variable bindings; bind a variable unless it occurs in the other term; unify compound terms argument by argument. See lab Experiment 7.

</details>

<details><summary><b>QIII.09</b> [Coding · Medium · AI Startup] Given parent(x, y) facts, write a query for all cousins of a person.</summary>

cousin(a, b) if parent(p, a), parent(q, b), sibling(p, q), with sibling(p, q) if parent(g, p), parent(g, q), p ≠ q. Implement with dictionaries or as Prolog rules.

</details>

<details><summary><b>QIII.10</b> [Design · Hard · Product / Big Tech] Design a knowledge graph to power product search for an e-commerce site.</summary>

Entities: product, brand, category, attribute, user intent; relations: is-a, has-attribute, compatible-with. Build from catalogue plus extraction; use it for query expansion and faceting; keep it fresh with pipelines and quality checks.

</details>

<details><summary><b>QIII.11</b> [Design · Hard · AI Startup] How would you reduce hallucinations in an LLM chatbot for university regulations?</summary>

Retrieval-augmented generation over the official rule documents, plus a rule base / knowledge graph for hard facts (fees, dates), citations in answers, refusal when no source is found, and evaluation on a curated question set.

</details>

<details><summary><b>QIII.12</b> [Design · Medium · FinTech] Design a rule engine for transaction compliance checks.</summary>

Declarative rules (IF amount > limit AND country in list THEN flag), versioning and testing of rules, Rete-style matching for speed, an explanation trail for auditors, and a path for analysts to update rules without code deploys.

</details>

<details><summary><b>QIII.13</b> [Scenario · Medium · HealthTech] A clinical rule system gives a wrong recommendation. How do you debug it?</summary>

Trace the inference path (which facts fired which rules), check fact quality, look for conflicting or outdated rules and their priority, add a regression test, and review with domain experts.

</details>

<details><summary><b>QIII.14</b> [Scenario · Medium · IT Services / GCC] The client's domain experts disagree on rules. How do you build the knowledge base?</summary>

Capture both views with provenance, find the scope where each applies, use certainty factors or priorities, and agree a governance process for resolution; never silently pick one.

</details>

<details><summary><b>QIII.15</b> [Scenario · Hard · AI Research Lab] When would you still choose symbolic AI over a neural model today?</summary>

When you need guaranteed constraints, auditability, small data, or exact reasoning (tax rules, safety interlocks). Hybrids are common: neural models for perception or language, symbolic layers for rules and verification.

</details>

## Unit IV: Planning and Reasoning under Uncertainty (CO204.4)

### 🚀 Top industry skills you gain

- Writing planning domains (STRIPS / PDDL) and reading planner output
- Reasoning with Bayes' rule and avoiding base-rate errors
- Building and querying Bayesian networks
- Quantifying uncertainty in model predictions
- Designing fuzzy controllers for embedded systems
- Communicating probabilistic results to decision makers

**Tools:** pyperplan / Fast Downward, pgmpy, scikit-fuzzy, NumPy / SciPy  
**Job roles:** Data Scientist, Robotics Planning Engineer, Risk / Fraud Analyst, Embedded AI Engineer  
**Portfolio output:** A diagnostic Bayesian network with a written sensitivity analysis, plus a fuzzy controller with its control-surface plot.

### 🎯 Interview questions with model answers

<details><summary><b>QIV.01</b> [Concept · Easy · FinTech] State Bayes' theorem and explain prior, likelihood and posterior.</summary>

P(H|E) = P(E|H)P(H)/P(E). The prior is belief before evidence, the likelihood is how probable the evidence is if H holds, and the posterior is the updated belief.

</details>

<details><summary><b>QIV.02</b> [Concept · Medium · HealthTech] A test is 99% sensitive with a 1% false-positive rate; prevalence is 0.1%. What is P(disease | +)?</summary>

0.99×0.001 / (0.99×0.001 + 0.01×0.999) ≈ 0.090, so about 9%. Low prevalence dominates; confirmatory testing is needed.

</details>

<details><summary><b>QIV.03</b> [Concept · Medium · Robotics / Autonomy] What is STRIPS? Write the Move(x, from, to) action for a robot.</summary>

STRIPS describes actions by precondition, add and delete lists. Move: PRE At(x, from) ∧ Clear(to); ADD At(x, to), Clear(from); DEL At(x, from), Clear(to).

</details>

<details><summary><b>QIV.04</b> [Concept · Medium · AI Research Lab] Why is a Bayesian network more compact than a full joint table?</summary>

It uses conditional independence: each variable depends only on its parents, so storage is about n·2^k numbers instead of 2^n for n Boolean variables with at most k parents.

</details>

<details><summary><b>QIV.05</b> [Concept · Medium · IT Services / GCC] Probability vs fuzzy logic — what does each model?</summary>

Probability models uncertainty about whether a crisp event happens. Fuzzy logic models vagueness, i.e. the degree to which a property holds (how 'hot' 32 °C is).

</details>

<details><summary><b>QIV.06</b> [Coding · Easy · FinTech] Implement Naïve Bayes for spam detection from word counts.</summary>

Estimate P(class) and P(word|class) with Laplace smoothing; score log P(c) + Σ log P(w|c); choose the larger. Use log-probabilities to avoid underflow.

</details>

<details><summary><b>QIV.07</b> [Coding · Medium · AI Research Lab] Compute P(Burglary | JohnCalls, MaryCalls) by enumeration.</summary>

Sum the joint over the hidden variables Earthquake and Alarm for B = true and B = false, then normalise. Result ≈ 0.284. See lab Experiment 8.

</details>

<details><summary><b>QIV.08</b> [Coding · Medium · Robotics / Autonomy] Write a triangular membership function and fuzzify 18 °C into Cold/Warm/Hot.</summary>

μ(x; a, b, c) = max(min((x−a)/(b−a), (c−x)/(c−b)), 0). With Cold(−∞,10,20), Warm(10,25,40), Hot(30,40,∞): Cold 0.2, Warm 0.53, Hot 0.

</details>

<details><summary><b>QIV.09</b> [Coding · Hard · Product / Big Tech] Simulate a Monte-Carlo estimate of a posterior and show its convergence.</summary>

Use rejection sampling or likelihood weighting; plot the running estimate vs sample count; error falls roughly as 1/√N.

</details>

<details><summary><b>QIV.10</b> [Design · Hard · FinTech] Design a real-time fraud-scoring system that must explain its decisions.</summary>

Streaming features (velocity, device, geography), a calibrated probabilistic model or gradient-boosted trees with reason codes, rules for hard blocks, thresholds tuned to business cost, human review queue, and drift monitoring.

</details>

<details><summary><b>QIV.11</b> [Design · Hard · Robotics / Autonomy] Design the task planner for a hospital delivery robot.</summary>

PDDL domain (rooms, lifts, doors, items), a classical planner for task order, a motion planner for paths, replanning on failure, and probabilistic handling of busy lifts. Add safety constraints and logging.

</details>

<details><summary><b>QIV.12</b> [Design · Medium · AI Startup] How would you add uncertainty estimates to a model's predictions shown to users?</summary>

Use calibrated probabilities (Platt or isotonic), ensembles or MC-dropout for variance, prediction intervals for regression, and UI that shows confidence plus 'why'; abstain when uncertainty is high.

</details>

<details><summary><b>QIV.13</b> [Scenario · Medium · HealthTech] Doctors over-trust a model's 0.9 'probability'. What do you check and change?</summary>

Check calibration on held-out data from the same hospital; recalibrate if needed; display risk with context (base rate, intervals); train users; monitor outcomes.

</details>

<details><summary><b>QIV.14</b> [Scenario · Medium · Robotics / Autonomy] Your plan works in simulation but fails in the real warehouse. Why?</summary>

Classical assumptions break: actions are not deterministic, the state is partially observable, the world changes. Add execution monitoring, replanning, probabilistic models and sensor checks.

</details>

<details><summary><b>QIV.15</b> [Scenario · Hard · FinTech] A fraud model flags many legitimate transactions from one region. How do you respond?</summary>

Measure false-positive rates by region, inspect features acting as proxies, re-weight or adjust thresholds, add review, document the fix, and monitor; consider the fairness and regulatory implications.

</details>

## Unit V: Learning, Expert Systems and Applications of AI (CO204.5)

### 🚀 Top industry skills you gain

- Training, evaluating and interpreting decision-tree models
- Explaining overfitting, bias–variance and validation strategy
- Building a perceptron / small neural network and debugging training
- Designing rule-based expert systems and chatbots with fallbacks
- Auditing models for bias, privacy and explainability
- Mapping NLP, vision and robotics problems to the right technique

**Tools:** scikit-learn, PyTorch / Keras, SHAP / Fairlearn, Rasa or simple intent classifiers  
**Job roles:** ML Engineer, Data Scientist, Conversational AI Developer, Responsible-AI Analyst  
**Portfolio output:** An end-to-end classifier with a model card (data, metrics, fairness checks, limitations) and a deployed demo.

### 🎯 Interview questions with model answers

<details><summary><b>QV.01</b> [Concept · Easy · IT Services / GCC] Explain supervised, unsupervised and reinforcement learning with one industry example each.</summary>

Supervised: credit-risk scoring from labelled defaults. Unsupervised: customer segmentation by clustering. Reinforcement: dynamic pricing or robot control learned from rewards.

</details>

<details><summary><b>QV.02</b> [Concept · Medium · Product / Big Tech] How does a decision tree choose a split? Compare entropy and Gini.</summary>

It picks the split with the largest impurity reduction. Entropy uses −Σp log p; Gini uses 1 − Σp². They usually give similar trees; Gini is slightly cheaper to compute.

</details>

<details><summary><b>QV.03</b> [Concept · Medium · AI Research Lab] Why can't a single perceptron learn XOR?</summary>

XOR is not linearly separable; a perceptron draws one line. A hidden layer creates a non-linear boundary, so a 2-layer MLP solves it.

</details>

<details><summary><b>QV.04</b> [Concept · Medium · Product / Big Tech] What is overfitting and how do you detect and prevent it?</summary>

The model fits noise: training accuracy is high, validation accuracy is low. Detect with validation curves; prevent with more data, regularisation, pruning or max depth, early stopping and cross-validation.

</details>

<details><summary><b>QV.05</b> [Concept · Medium · HealthTech] Precision vs recall — which matters more for cancer screening?</summary>

Recall, because missing a cancer (false negative) is costly; precision is then improved with follow-up tests. Report both with the threshold chosen for clinical needs.

</details>

<details><summary><b>QV.06</b> [Coding · Easy · Product / Big Tech] Compute entropy and information gain for a split from scratch.</summary>

H = −Σ p log₂ p over class proportions; Gain = H(parent) − Σ (n_child/n) H(child). For Play Tennis, Outlook gives 0.247.

</details>

<details><summary><b>QV.07</b> [Coding · Medium · Product / Big Tech] Train a perceptron for AND/OR and print the final weights.</summary>

Initialise weights to 0; for each sample update w += η(y − ŷ)x until no errors. AND converges to a boundary such as x₁ + x₂ ≥ 2.

</details>

<details><summary><b>QV.08</b> [Coding · Medium · AI Startup] Write an intent classifier for a chatbot with a fallback.</summary>

Use TF-IDF + logistic regression (or keyword rules for a baseline), predict the intent with its probability, and return the fallback when the max probability is below a threshold; log misses for retraining.

</details>

<details><summary><b>QV.09</b> [Coding · Medium · IT Services / GCC] Build a decision tree with scikit-learn and extract human-readable rules.</summary>

fit DecisionTreeClassifier(max_depth=3), then export_text(model, feature_names). Validate on a held-out split and report a confusion matrix. See lab Experiment 9.

</details>

<details><summary><b>QV.10</b> [Design · Hard · Product / Big Tech] Design a content-moderation system for a social platform in Indian languages.</summary>

Multilingual text and image classifiers, policy taxonomy, thresholds per category, human review for borderline cases, appeal flow, feedback loop for retraining, and metrics per language to catch bias.

</details>

<details><summary><b>QV.11</b> [Design · Hard · HealthTech] Design an expert-system-plus-ML assistant for rural primary-health workers.</summary>

Rule-based triage protocol for safety-critical decisions, an ML model for risk ranking, offline-first mobile app, local-language voice UI, escalation to doctors, and audit logs; validate with clinicians.

</details>

<details><summary><b>QV.12</b> [Design · Medium · AI Startup] How would you deploy and monitor a model in production?</summary>

Package with versioned data and model, serve behind an API, track latency and errors, monitor input drift and prediction drift, collect labels to measure live accuracy, and keep a rollback path.

</details>

<details><summary><b>QV.13</b> [Scenario · Medium · Product / Big Tech] A hiring model rates women lower for the same CV. What do you do?</summary>

Stop using it for decisions, audit features and training data for proxies, measure group metrics, retrain with mitigation, add human review, document in a model card, and involve legal/HR.

</details>

<details><summary><b>QV.14</b> [Scenario · Medium · AI Research Lab] Your model is 98% accurate on a dataset with 2% positives. Is it good?</summary>

Not necessarily: predicting all negatives also gives 98%. Use precision, recall, F1, PR-AUC and the confusion matrix, and compare with a baseline.

</details>

<details><summary><b>QV.15</b> [Scenario · Hard · AI Startup] A client wants face recognition for classroom attendance. What do you advise?</summary>

Assess necessity and consent, privacy law (DPDP Act 2023), data retention, accuracy across demographic groups, and security; propose less intrusive alternatives (QR or app check-in) or opt-in with clear policies.

</details>

## 💻 Solved coding problems

See [Interview_Coding_Solutions.ipynb](Interview_Coding_Solutions.ipynb) for executed solutions with tests.

1. **8-puzzle solvability check** (Unit I) — Given a 3×3 8-puzzle state as a tuple (0 = blank), return True if it can reach 1-2-3/4-5-6/7-8-_ . Target: O(n²) or better.
2. **Water-Jug: minimum steps** (Unit I) — Jugs of capacity a and b litres; return the minimum number of operations to measure exactly t litres in either jug, or −1.
3. **Shortest path in a grid with obstacles** (Unit II) — Grid of 0 (free) and 1 (wall). Return the length of the shortest 4-directional path from top-left to bottom-right, or −1.
4. **Count N-Queens solutions with bitmasks** (Unit II) — Return the number of ways to place N non-attacking queens. Must handle N = 12 quickly.
5. **Propositional entailment by model checking** (Unit III) — Given a KB and a query as Python functions over a model, decide whether KB ⊨ query and return a counter-model if not.
6. **Unification with occurs check** (Unit III) — Implement unify(x, y) for terms written as nested tuples; variables start with '?'. Return the substitution or None.
7. **Naïve Bayes spam filter from scratch** (Unit IV) — Train a multinomial Naïve Bayes classifier with Laplace smoothing on a tiny corpus and classify new messages.
8. **Bayes' rule calculator with sequential evidence** (Unit IV) — Write posterior(prior, sensitivity, false_positive_rate) and apply it twice for two independent positive tests.
9. **Entropy and information gain** (Unit V) — Given labels and a candidate attribute, compute entropy and information gain from scratch; verify on Play Tennis (Outlook).
10. **Intent classifier with a confidence fallback** (Unit V) — Build a small chatbot intent classifier (TF-IDF + logistic regression) that returns a fallback when confidence is low.
