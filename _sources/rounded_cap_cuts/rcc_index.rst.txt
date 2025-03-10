Rounded Capacity Cuts
======================================

Rounded Capacity Cuts, referred to as RCCs, are a type of cutting plane used in capacity constrained vehicle routing problems to improve the
lower bound of the linear programming (LP) relaxation.

In this section, we will discuss the RCC package used in RouteOpt. It provides the following functionalities:

1. **Easy call CVRPSEP**.
     RouteOpt does not implement the RCC separation package itself, but instead calls the CVRPSEP package :cite:p:`lysgaard2004new`, which is a C library for solving the Capacitated Vehicle Routing Problem (CVRP) using cutting planes.

2. **Updating the reduced cost (RC) associated with RCCs** during the labeling algorithm.

3. **Calculating the coefficients of the constraint matrix** associated with RCCs.

The following are details of the functionalities provided by the RCC package.
I highly recommend reading the rest of this page before going through the following sections to understand how to use the package.

.. toctree::
   :maxdepth: 1

   rcc_common
   separation
   update_reduced_cost
   calculate_coefficients

Definition
----------

The following formulas describe the general form of the RCC:

1. **Basic Constraint for a Set** :math:`S`:

.. math::

   x(S:S) \leq |S| - k(S)

- :math:`x(S:S)` represents the total flow that starts and ends within the customer set :math:`S`.
- :math:`|S|` denotes the total number of customers in :math:`S`.
- :math:`k(S)` is the lower bound on the number of vehicles required to serve the customers in :math:`S`.

2. **Constraint for the Complement Set** :math:`\bar{S}`:

.. math::

   x(\bar{S}:\bar{S}) + \frac{1}{2}\,x(\{0\}:\bar{S}) - \frac{1}{2}\,x(\{0\}:S) \leq |\bar{S}| - k(S)

- :math:`x(\bar{S}:\bar{S})` represents the total flow among customers within the complement set :math:`\bar{S}`.
- :math:`x(\{0\}:\bar{S})` denotes the flow from the depot (represented by 0) to customers in :math:`\bar{S}`.
- :math:`x(\{0\}:S)` denotes the flow from the depot to customers in :math:`S`.

3. **Strengthened Constraint in the Enumeration State:**

.. math::

   \sum_{p \in P} I\{(|p \cap S| \geq 1)\}\, x_p \geq k(S)

- :math:`\sum_{p \in P}` indicates summation over a set of routes.
- :math:`I\{(|p \cap S| \geq 1)\}` is the indicator function that equals 1 if path :math:`p` includes at least one customer from :math:`S`, and 0 otherwise.
- :math:`x_p` is the decision variable associated with path :math:`p`.

Further Reading
---------------

For more detailed information, please refer to:

.. bibliography::
   :filter: key in {"lysgaard2004new"}



