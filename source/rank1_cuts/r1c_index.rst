Rank-1 Cuts
======================================

Chvátal-Gomory Rank-1 Cuts, referred to as Rank-1 cuts, are a type of cutting plane used in integer programming (IP) to improve the solution of linear programming (LP) problems.

In this section, we will discuss the Rank-1 cuts package used in RouteOpt. It provides the following functionalities:

1. **Separating Rank-1 cuts and identifying optimal memory set** (node-based or arc-based) with proper cut selection. This ensures that Rank-1 cuts are effective and do not degrade the performance of the pricing problem.
2. **Updating the reduced cost (RC) associated with Rank-1 cuts** during the labeling algorithm. You do not need to maintain any information about these non-robust cuts.
3. **Calculating the coefficients of the constraint matrix** associated with Rank-1 cuts. This eliminates the need to implement your own functor to determine the coefficients, which can be complex when using limited-memory techniques.

The following are details of the functionalities provided by the Rank-1 cuts package.
I highly recommend reading the rest of this page before going through the following sections to understand how to use the package.

.. toctree::
   :maxdepth: 1

   rank1_common
   separation
   update_reduced_cost
   calculate_coefficients


Definition
--------------------------------------

Rank-1 cuts have the following form:

.. math::

   \sum_{r\in \Omega} \left\lfloor \sum_{i\in C} p_i a_i^r \right\rfloor x_r \leq \left\lfloor \sum_{i \in C} p_i \right\rfloor

where:

- :math:`\Omega` is the set of all columns,

- :math:`C` is the cut set, a subset of :math:`N`, where :math:`N` is the set of all customers, excluding the depot,

- :math:`p_i` is the (optimal) multiplier for each :math:`i\in C`. Here, optimal means that the cut obtained using this multiplier is the most violated one. From the perspective of polyhedral theory, it defines a facet of the LP polytope, denoted as :math:`\operatorname{CSPP}_{\leq}(n)`,

- :math:`a_i^r` is the number of times route :math:`r` visits customer :math:`i`.

The polyhedral representation of :math:`\operatorname{CSPP}_{\leq}(n)` is given by:

.. math::

   \operatorname{CSPP}_{\leq}(n)=\operatorname{Conv}\left\{ \sum_{j=1}^{2^n-1} b^j x_j \leq \mathbf{1}, x \in\{0,1\}^{2^n-1} \right\},

where :math:`b^j` represents the column associated with the binary representation of :math:`j`.


Advanced Speed-Up Techniques
-----------------------------

The most advanced techniques related to general cutting for speeding up exact routing solvers include:

1. Using Rank-1 cuts with higher dimensions (larger :math:`C`).
2. Using them efficiently with **limited memory techniques**.

Limited memory techniques, as introduced in :cite:`pecin2017limited`,
make the pricing subproblem tractable even after adding hundreds of Rank-1 cuts.

For simplicity, we first discuss **Rank-1 cuts with full memory** before introducing limited memory approaches.

Optimal Multipliers for Rank-1 Facets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Based on the beautiful work by :cite:t:`bulhoes2018complete`:

We have the following optimal multipliers defining the rank-1 facets of the LP polytope (Theorem 2 of the paper, and :math:`n:=|C|`):

 **Plan 0:** :math:`\left(\frac{1}{2}, \frac{1}{2}, \dots, \frac{1}{2}\right)`, if :math:`n` is odd.

 **Plan 1:** :math:`\left(\frac{1}{3}, \frac{1}{3}, \dots, \frac{1}{3}\right)`, if :math:`n = 3k + 2, k \geq 1`.

 **Plan 2:** :math:`\left(\frac{n-3}{n-2}, \frac{n-3}{n-2}, \frac{2}{n-2}, \frac{1}{n-2}, \dots, \frac{1}{n-2}\right)`, for :math:`n \geq 5`.

 **Plan 3:** :math:`\left(\frac{n-2}{n-1}, \frac{n-2}{n-1}, \frac{2}{n-1}, \frac{2}{n-1}, \frac{1}{n-1}, \dots \right)`, for :math:`n \geq 5`.

 **Plan 4:** :math:`\left(\frac{n-3}{n-1}, \frac{2}{n-1}, \frac{1}{n-1}, \frac{1}{n-1}, \dots, \frac{1}{n-1}\right)`, for :math:`n \geq 5`.

 **Plan 5:** :math:`\left(\frac{n-2}{n-1}, \frac{1}{n-1}, \frac{1}{n-1}, \dots, \frac{1}{n-1}\right)`, for :math:`n \geq 4`.

 **Plan 6:** :math:`\left(\frac{n-2}{n}, \frac{2}{n}, \frac{2}{n}, \frac{1}{n}, \dots, \frac{1}{n}\right)`, for :math:`n \geq 5`.

Special Case: Subset Row Cuts
"""""""""""""""""""""""""""""""

One of the most popular cutting planes, subset row cuts :cite:p:`jepsen2008subset`: takes the following form:

.. math::

   \sum_{r\in \Omega} \left\lfloor \frac{1}{2} a^r_i + \frac{1}{2} a^r_j + \frac{1}{2} a^r_k \right\rfloor \leq 1

It is easy to see that subset row cuts are a special case of Rank-1 cuts, where :math:`p_i = \frac{1}{2}` for all :math:`i\in C`, i.e., :math:`p=(\frac{1}{2}, \frac{1}{2}, \frac{1}{2})` and :math:`C=\{i,j,k\}`.


Higher-Dimensional Cuts
"""""""""""""""""""""""""""""""

All other higher-dimensional cuts (i.e., :math:`|C| > 3`) correspond to distinct facets of the LP polytope and they enhance the lower bound of the LP relaxation by the same idea.
Therefore, if subset row cuts are beneficial for your problem, it is advisable to consider higher-dimensional cuts collectively in your implementation.


Limited Memory Techniques
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Inspired by the Ng-Route relaxation :cite:p:`baldacci2011new`, which introduces a memory technique to accelerate the pricing problem through state-space relaxation (yielding a stronger dominance rule at the cost of a slightly weaker bound),
the **limited memory technique** is employed to achieve similar performance enhancements.

Memory Definition
"""""""""""""""""""""""""""""""
The limited memory technique associates a memory set with each Rank-1 cut:

- **Node Memory**: A memory set :math:`M_n \subseteq N`, where :math:`N` denotes the set of customers.
- **Arc Memory**: A memory set :math:`M_a \subseteq A`, where :math:`A` denotes the set of arcs.

Mechanism
"""""""""""""""""""""""""""""""

Full Memory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In a full memory scenario, the process is as follows:

1. When a route :math:`r` visits a customer :math:`i \in C`, the state corresponding to the cut is incremented by a multiplier :math:`p_i`.
2. If the cumulative state exceeds 1, the coefficient of the cut is increased by 1, and the state is reduced by 1.
3. After the label extension completes (i.e., once the route returns to the depot), the computed coefficient corresponds exactly to :math:`a^r_i` as defined in the formulation.

With Limited Memory Techniques
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
With limited memory, an additional check is introduced during the extension phase:

- When extending from node :math:`i` to node :math:`j`, perform the following:

  - For **node memory**, verify whether :math:`j \in M_n`.
  - For **arc memory**, verify whether :math:`(i, j) \in M_a`.

- If the node or arc is present in the memory set, the current state remains unchanged.
- Otherwise, the state is reset to 0.


Effect on Dominance Rule
"""""""""""""""""""""""""""""""

The dominance condition is given by:

.. math::

   \bar{c}(L) - \sum_{c \in C: s_{c}(L) > s_{c}(L^\prime)} \pi_{c} \leq \bar{c}(L^\prime)

where :math:`\bar{c}(L)` denotes the reduced cost of label :math:`L`, :math:`s_{c}(L)` is the state of the cut associated with label :math:`L`, and :math:`\pi_{c}\leq 0` represents the dual variable corresponding to cut :math:`c` in the set :math:`C`.

By implying limited memory technique, if a customer or arc is not included in the memory set :math:`M`, the state is reset to 0. Consequently, the dominance condition becomes relaxed, making it easier to satisfy. This trade-off leads to computational efficiency gains at the expense of a slightly weaker bound, which aligns with the principles of the Ng-Route relaxation.

How to Find the Optimal Memory
"""""""""""""""""""""""""""""""

Determining the optimal memory is itself an optimization problem. Given a set of fractional solutions, the objective is to identify a memory set of minimal size (i.e., minimizing :math:`|M_a|` for arc memory or :math:`|M_n|` for node memory) such that all coefficients of the columns in the solution are computed exactly the same as under full memory.

In the implementation of RouteOpt, two approaches are employed:

1. **Dynamic Programming**

2. **Integer Programming Model:**
   An IP model is built to determine the memory set (applicable only for node memory). This approach is used only when the dynamic programming method is unlikely to succeed within the available time constraints.

Further Reading
---------------

For more detailed information, please refer to:

.. bibliography::
   :filter: key in {"baldacci2011new", "bulhoes2018complete", "jepsen2008subset", "pecin2017limited"} and cited



