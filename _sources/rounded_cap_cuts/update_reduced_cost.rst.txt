RCCs: RC Updater
========================

Overview
--------
The file ``packages/rounded_cap_cuts/chg_rc_getter/include/rcc_rc_controller.hpp`` defines the
``RCCRCController`` class, which is responsible for pricing Rounded Capacity Cuts (RCCs) and updating
the reduced cost (RC) information in the RouteOpt software package. This header is pivotal for
updating the change in the cost matrix for customers based on RCC pricing, using dual values
obtained from the LP relaxation.

License
^^^^^^^
This software is licensed under **GPL-3.0**.

File Contents
^^^^^^^^^^^^^
The header file ``rcc_rc_controller.hpp`` comprises the following key components:

- **Controller: RCCRCController**

  The ``RCCRCController`` class provides a static method to:

  - Price RCCs using a given vector of RCCs and a dual price vector.
  - Update the change cost matrix for customers based on the RCC pricing process.

RCCRCController Class
---------------------
The ``RCCRCController`` class is responsible for pricing RCCs by utilizing dual values from the LP
relaxation. Its static method, ``priceRCC``, computes the change in cost for each customer based on the
provided RCCs and dual prices.

Static Method: priceRCC
^^^^^^^^^^^^^^^^^^^^^^^^^
- **priceRCC**

  *Inputs*:

  - **rccs**: A vector of RCCs used in the pricing process.
  - **pi_vector**: A vector of dual prices from the LP relaxation.

  *Output*:

  - **chg_cost_mat4_vertex**: A matrix (2D vector of doubles) representing the change in cost for customers, which is updated based on the RCC pricing.
    If no non-robust cuts are added, then the RC of route :math:`\mathcal{P} = \{(0,i_1), (i_1,i_2), \cdots, (i_j,0)\}` is calculated by

  .. math::

     \sum_{(i,j) \in \mathcal{P}} \text{chg_cost_mat4_vertex}[i][j]

Header Code
-----------
Below is an excerpt from ``rcc_rc_controller.hpp`` illustrating the key definitions:

.. code-block:: cpp
   :caption: rcc_rc_controller.hpp

   #ifndef ROUTE_OPT_RCC_RC_CONTROLLER_HPP
   #define ROUTE_OPT_RCC_RC_CONTROLLER_HPP

   namespace RouteOpt::RCCs::RCGetter {
       class RCCRCController {
       public:
           static void priceRCC(const std::vector<Rcc> &rccs,
                                const std::vector<double> &pi_vector,
                                std::vector<std::vector<double>> &chg_cost_mat4_vertex);
           RCCRCController() = default;
           ~RCCRCController() = default;
       };
   } // namespace RouteOpt::RCCs::RCGetter

   #endif // ROUTE_OPT_RCC_RC_CONTROLLER_HPP

Usage Example
-------------
Below is an example demonstrating how to use the ``RCCRCController`` to price RCCs and update the change
cost matrix for customers.

.. code-block:: cpp

   #include <vector>
   #include <iostream>
   #include "rcc_rc_controller.hpp"
   #include "rcc_macro.hpp"         // header for RCC definitions
   #include "solver.hpp"            // header for the Solver class

   using namespace RouteOpt::RCCs::RCGetter;

   int main() {
       // Prepare a dummy vector of RCCs.
       std::vector<Rcc> rccs;
       // (Populate rccs with RCC objects as required.)

       // Prepare a dummy dual price vector from the LP relaxation.
       std::vector<double> pi_vector = {1.0, 0.8, 0.5, 0.3, 0.2};

       // Define a change cost matrix for customers (e.g., for 5 customers).
       std::vector<std::vector<double>> chg_cost_mat4_vertex(5, std::vector<double>(5, 1.0));

       // Price the RCCs and update the change cost matrix.
       RCCRCController::priceRCC(rccs, pi_vector, chg_cost_mat4_vertex);

       // Output the updated cost matrix.
       std::cout << "Updated Change Cost Matrix:" << std::endl;
       for (const auto &row : chg_cost_mat4_vertex) {
           for (double cost : row) {
               std::cout << cost << " ";
           }
           std::cout << std::endl;
       }

       return 0;
   }

Conclusion
----------
The RCCRCController module in RouteOpt provides an effective mechanism for mapping the duals of Rounded Capacity Cuts (RCCs)
to the change cost matrix for customers, and thus facilitates the update of reduced costs (RCs) in the labeling algorithm.
