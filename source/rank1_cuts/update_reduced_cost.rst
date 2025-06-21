R1Cs: RC Updater
===========================

Overview
--------
The file ``packages/rank1_cuts/chg_rc_getter/include/rank1_rc_controller.hpp`` defines the controller and utilities for managing Rank-1 cut pricing (in labeling) statistics and states within the RouteOpt software package.
This header is pivotal for updating reduced cost (RC) information, copying pricing statistics, updating state values, performing dominance checks, concatenating state information during the labeling process.


License
^^^^^^^
This software is licensed under **GPL-3.0**.

File Contents
^^^^^^^^^^^^^
This header file comprises the following key components:

- **Structures and Utility Functions**

  - **R1CPricingStat**

    Structure holding Rank-1 cut pricing statistics, including:

    - **num**

      Number of valid cuts.

    - **valid_cut_idx**

      Pointer to an array of valid cut indices.

    - **cut_map**

      Pointer to the complete cut map array.

    - **copyFrom()**

      Method to copy pricing statistics from another instance.

  - **R1CUseStates**

    Structure representing the usage states for Rank-1 cuts, including:

    - **union_map**

      Bitset representing the union (C+M) mapping (1 indicates presence of a cut).

    - **v_union_mem**

      Vector representing union memory for cuts.

    - **sparse**

      Sparse representation of states as a vector of pairs.

    - **sparse_map**

      Bitset for the sparse mapping (specific to C).

- **Controller: Rank1RCController**

  The ``Rank1RCController`` class provides functionality to:

  - Initialize label memory for pricing statistics via ``initializeLabel()``.

  - Retrieve Rank-1 dual values from the column generation (CG) process using ``getRank1DualsInCG()``.

  - Update Rank-1 cut states with ``updateR1CStates()``.

  - Check dominance between pricing statistics with ``doR1CDominance()``.

  - Concatenate state information via ``concatenateR1CStates()``.

  - Assign contiguous label memory to label objects using the templated method ``assignLabelMem()``.

Controller: Rank1RCController
-----------------------------
Constructor
^^^^^^^^^^^
- **data_shared**

  *Input*: A reference to a shared Rank-1 cuts data object of type ``Rank1CutsDataShared``.

  **Meaning**: Provides precomputed multipliers and metadata required for generating and updating Rank-1 cut states.

Member Functions
^^^^^^^^^^^^^^^^^^
- **initializeLabel()**

  *Static Method*
  Initializes the label fields of a given pricing statistic by filling the entire cut_map array with zeros.

- **getRank1DualsInCG()**

  *Functionality*: Update the dual map for a given set of Rank-1 cuts using a provided π-vector.

- **updateR1CStates()**

  *Functionality*: Updates the RC and produces new pricing statistics by transferring state information from a source customer to a target customer.

- **doR1CDominance()**

  *Functionality*: Checks whether the updated pricing statistics dominate the input statistics by comparing a computed gap value. Returns true if the dominance condition is satisfied.

- **concatenateR1CStates()**

  *Functionality*: Concatenates input state information into output pricing statistics based on a required value. This process is crucial for combining state information across different customers.

- **assignLabelMem()**

  *Templated Method*
  Assigns contiguous memory space for the cut_map and valid_cut_idx fields for an array of label objects.


Header Codes
--------------

Below is an excerpt from ``rank1_rc_controller.hpp`` that illustrates the structure and functionality of the Rank1RCController class:

.. code-block:: cpp

   #ifndef ROUTE_OPT_RANK1_RC_CONTROLLER_HPP
   #define ROUTE_OPT_RANK1_RC_CONTROLLER_HPP

   #include <algorithm>
   #include "rank1_macro.hpp"
   #include "route_opt_macro.hpp"

   namespace RouteOpt::Rank1Cuts::RCGetter {

       struct R1CPricingStat {
           int num{};
           int *valid_cut_idx{};
           int *cut_map{};

           void copyFrom(const R1CPricingStat &other) {
               num = other.num;
               std::copy_n(other.valid_cut_idx, num, valid_cut_idx);
               std::copy_n(other.cut_map, MAX_NUM_R1CS_IN_PRICING, cut_map);
           }
       };

       struct R1CUseStates {
           r1cIndex union_map{};
           std::vector<int> v_union_mem;
           std::vector<std::pair<int, int>> sparse;
           r1cIndex sparse_map{};
       };

       class Rank1RCController {
       public:
           explicit Rank1RCController(Rank1CutsDataShared &data_shared)
               : data_shared_ref(std::ref(data_shared)) {
           }

           static void initializeLabel(const R1CPricingStat &r1c) {
               std::fill_n(r1c.cut_map, MAX_NUM_R1CS_IN_PRICING, 0);
           }

           void getRank1DualsInCG(const std::vector<R1c> &cuts,
                                  const std::vector<double> &pi_vector);

           void updateR1CStates(double &rc, R1CPricingStat &out_states,
                                const R1CPricingStat &in_states,
                                int from,
                                int to);

           bool doR1CDominance(double &gap,
                               const R1CPricingStat &out_states,
                               const R1CPricingStat &in_states);

           bool concatenateR1CStates(double &rc, double req, R1CPricingStat &out_states,
                                     const R1CPricingStat &in_states, int out, int in);

           template<typename T, typename R1cPtr>
           void assignLabelMem(T *all_label, size_t label_assign, R1cPtr r1c_ptr) {
               if (all_label == nullptr)
                   THROW_RUNTIME_ERROR("all_label is nullptr");
               delete[] label_int_space;
               size_t constexpr label_int_space_len = MAX_NUM_R1CS_IN_PRICING + MAX_POSSIBLE_NUM_R1CS_FOR_VERTEX;
               label_int_space = new int[label_int_space_len * label_assign];
               size_t cut_map_beg = 0;
               for (size_t i = 0; i < label_assign; ++i) {
                   auto &r1c = all_label[i].*r1c_ptr;
                   r1c.cut_map = label_int_space + cut_map_beg;
                   cut_map_beg += MAX_NUM_R1CS_IN_PRICING;
                   r1c.valid_cut_idx = label_int_space + cut_map_beg;
                   cut_map_beg += MAX_POSSIBLE_NUM_R1CS_FOR_VERTEX;
               }
           }

           Rank1RCController() = delete;

           ~Rank1RCController() {
               delete[] label_int_space;
           }

       private:
           int *label_int_space{};
           std::vector<R1CUseStates> cg_v_cut_map{};
           std::vector<std::vector<std::vector<int>>> cg_v_v_use_states{};
           std::vector<int> cg_r1c_denominator{};
           std::vector<double> rank1_dual{};
           std::vector<double> revised_rank1_dual{};
           const std::reference_wrapper<Rank1CutsDataShared> data_shared_ref;
       };
   } // namespace RouteOpt::Rank1Cuts::RCGetter

   #endif // ROUTE_OPT_RANK1_RC_CONTROLLER_HPP


Usage Example
-------------
Below is an example demonstrating how to use the Rank1RCController in RouteOpt. This example shows how to initialize shared data, prepare dummy pricing statistics, retrieve dual values, update states, and perform dominance and concatenation checks.

.. code-block:: cpp

   #include <vector>
   #include <iostream>
   #include "rank1_rc_controller.hpp"
   #include "rank1_macro.hpp"
   #include "solver.hpp"

   using namespace RouteOpt::Rank1Cuts;
   using namespace RouteOpt::Rank1Cuts::RCGetter;

   int main() {
       // Initialize shared Rank-1 cuts data with an instance dimension (e.g., 5)
       Rank1CutsDataShared sharedData(5);

       // Create an instance of the Rank1RCController with the shared data
       Rank1RCController rcController(sharedData);

       // assign label memory for a vector of labels (e.g., 10 labels), assuming Label is a struct with r1c as a member
       auto all_label = new Label[10];
       rcController.assignLabelMem(all_label, 10, &Label::r1c);

       // Prepare a dummy R1CPricingStat for demonstration
       R1CPricingStat pricingStat;
       // Allocate memory for valid_cut_idx and cut_map as needed, for example:
       // pricingStat.valid_cut_idx = new int[some_length];
       // pricingStat.cut_map = new int[MAX_NUM_R1CS_IN_PRICING];

       // Initialize the label fields of pricingStat (set all values in cut_map to zero)
       Rank1RCController::initializeLabel(pricingStat);

       // Prepare a dummy π-vector (dual prices)
       std::vector<double> piVector = {1.0, 0.5, 0.2, 0.8, 0.3};

       // Assume an empty vector of Rank-1 cuts for demonstration
       std::vector<R1c> cuts;

       // Retrieve dual values from the column generation process
       rcController.getRank1DualsInCG(cuts, piVector);

       // Update Rank-1 cut states (e.g., transfer state from customer 1 to customer 2)
       double rc = 0.0;
       R1CPricingStat newPricingStat;
       // Ensure newPricingStat is allocated and initialized appropriately.
       rcController.updateR1CStates(rc, newPricingStat, pricingStat, 1, 2);

       // Perform a dominance check between the updated and original pricing statistics
       double gap = -10.0; // Example gap value
       bool isDominant = rcController.doR1CDominance(gap, newPricingStat, pricingStat);
       std::cout << "Dominance check result: "
                 << (isDominant ? "Dominant" : "Not Dominant") << std::endl;

       // Concatenate state information with a required value (example: 1.5)
       bool concatenated = rcController.concatenateR1CStates(rc, 1.5, newPricingStat, pricingStat, 2, 1);
       std::cout << "State concatenation "
                 << (concatenated ? "succeeded" : "failed") << std::endl;



       // Clean up any dynamically allocated memory if necessary.
       // The destructor of rcController will automatically free label_int_space.

       return 0;
   }

.. note::
   For a deeper understanding of the Rank-1 RC Controller, explore the application source code under
   ``packages/application/cvrp/src`` using an IDE such as CLion.

   If you have any questions, please feel free to contact me at `you.z@ufl.edu <mailto:you.z@ufl.edu>`_ or reach out via Group Chat.

Conclusion
----------
The Rank1RCController module in RouteOpt offers a comprehensive framework for managing Rank-1 cut pricing statistics and states.
By providing functionality for dual value retrieval, state updates, dominance checks, state concatenation, and memory assignment, this module enables effective management of reduced cost information during the labeling process in complex routing problems.
