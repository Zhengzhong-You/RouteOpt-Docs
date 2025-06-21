Best K Formula
===================

Overview
--------
The Best K Formula, known as **BKF** :cite:p:`you2023two`, module in RouteOpt provides constants, macros, and classes that
facilitate **dynamic testing number determination** for branching selection, achieving the best trade-off
between testing time and candidate quality. This module consists of two main files:

- **``packages/branching/bkf/include/bkf_macro.hpp``**: Defines constants, macros, and configuration parameters used by the BKF algorithm.
- **``packages/branching/bkf/include/bkf_controller.hpp``**: Declares the **``BKFController``** class and a supporting **``BKFDataShared``** class
  to manage BKF branching operations, parameter estimation, and time measurements.

License
^^^^^^^
This software is licensed under **GPL-3.0**.

File Contents
^^^^^^^^^^^^^
1. **bkf_macro.hpp**  
   - **Constants**:

     - **``BOOST_TOLERANCE_BIT``**: Bit-level tolerance used in Boost operations.
     - **``MAX_ITERATION``**: Maximum number of iterations for equation solving in BKF.
     - **``R_DISCOUNT``**: Discount factor applied to parameter “R” during BKF calculations.
     - **``MAX_ALPHA``**: Maximum alpha value allowed in BKF computations.

   - **Macros**:

     - **``BKF_VERBOSE``**: Enables verbose execution for debugging.
     - **``BKF_VERBOSE_EXEC(...)``**: Executes the code block only if **BKF_VERBOSE** is defined.

2. **bkf_controller.hpp**  
   - **``BKFDataShared``** class:

     - Stores shared data used by **BKFController**, including counters for nodes before/after enumeration,
       the current best “f” value, and vectors to store **r_star** information.
     - Provides methods to update **f**, manage node counters, and calculate **r_star** values.

   - **``BKFController``** class:

     - Manages BKF branching operations, parameter estimation, time measurement, and best K determination.
     - Provides methods for setting estimated parameters (**m** and **n**), updating testing times, tracking node solving times,
       and retrieving the best **k** values.

BKF Macros and Constants (bkf_macro.hpp)
----------------------------------------
Below is an excerpt from **``bkf_macro.hpp``**:

.. code-block:: cpp
   :caption: bkf_macro.hpp

   #ifndef ROUTE_OPT_BKF_MACRO_HPP
   #define ROUTE_OPT_BKF_MACRO_HPP

   namespace RouteOpt::Branching::BKF {
       constexpr int BOOST_TOLERANCE_BIT = 6;
       constexpr int MAX_ITERATION = 1000;
       constexpr double R_DISCOUNT = 0.72;
       constexpr double MAX_ALPHA = 0.8;

       #define BKF_VERBOSE

       #ifdef BKF_VERBOSE
       #define BKF_VERBOSE_EXEC(...) __VA_ARGS__;
       #else
       BKF_VERBOSE_EXEC();
       #endif
   } // namespace RouteOpt::Branching::BKF

   #endif // ROUTE_OPT_BKF_MACRO_HPP

BKFDataShared Class (bkf_controller.hpp)
----------------------------------------
The **``BKFDataShared``** class holds shared data for BKF branching operations:

.. code-block:: cpp
   :caption: BKFDataShared Excerpt

   class BKFDataShared {
   public:
       double getF() const { return f; }
       void updateF(double f) { ... }
       int getNodeB4() const { return num_node_b4; }
       int getNodeAf() const { return num_node_af; }
       void increaseNodeB4() { ++num_node_b4; }
       void increaseNodeAf() { ++num_node_af; }
       double getCurrentRBest() const { return current_r_best; }
       void calculateRStar(double lift, int tree_level, bool dir, int node_idx, BKFController &controller);
       const auto &getRStarDepth() const { return r_star_depth; }
       auto &refRStarDepth() { return r_star_depth; }

   private:
       int num_node_b4{};
       int num_node_af{};
       double f{};
       double current_r_best{};
       std::vector<std::pair<std::pair<double, int>, std::pair<double, int> > > r_star_depth{};
   };

**Key Methods**:

- **``updateF``**: Updates the best **f** value if a higher one is found.
- **``increaseNodeB4``** / **``increaseNodeAf``**: Increments counters for nodes before/after enumeration.
- **``calculateRStar``**: Uses **lift** and **tree_level** to update **r_star** values for BKF computations.

BKFController Class (bkf_controller.hpp)
----------------------------------------
The **``BKFController``** class manages BKF branching operations:

.. code-block:: cpp
   :caption: BKFController Excerpt

   class BKFController {
   public:
       void setMN(int m, int n) { ... }
       void setIfB4(bool if_b4) { ... }
       void setTestingTime(double t, int n) { ... }
       void setNodeTime(double t) { ... }
       void updateTimeMeasure(BKFDataShared &sharedData) { ... }
       int getBestK(const BKFDataShared &sharedData, double ub, double lb);
       void updateOptK(int k, int node_idx) { ... }
       double getOptK(int node_idx) { ... }
       double getAlpha() const { return alpha; }

   private:
       bool if_init{};
       double tmp_single_testing_time{};
       double tmp_single_node_time{};
       bool tmp_if_b4{};
       double alpha{};
       double all_n{};
       double est_m{};
       std::unordered_map<int, double> opt_k{};
       double t_for_one_testing_b4{};
       double c_for_node_b4{};
       double t_for_one_testing_af{};
       double c_for_node_af{};
       void evaluateM1();
   };

**Key Methods**:

- **``setMN``**: Sets the estimated parameters **m** and **n**.
- **``setTestingTime``** / **``setNodeTime``**: Records testing and node processing times.
- **``updateTimeMeasure``**: Updates average testing/node times based on the number of processed nodes.
- **``getBestK``**: Determines the best **k** value given the shared data, upper bound, and lower bound.
- **``updateOptK``** / **``getOptK``**: Manages a per-node best **k** value, removing it once retrieved.

Usage Example
-------------

Below is a simple C++ example demonstrating how to use the BKF module within RouteOpt.

.. note::
   Although the default RouteOpt workflow automatically calls this module under the hood, if you wish to use it directly,
   I highly recommend reviewing the source code of CVRP and ``workflow.hpp`` to understand when and how to invoke the functions to update your data.

This example utilizes the constants and functions defined in ``bkf_macro.hpp`` and the classes declared in ``bkf_controller.hpp``. The workflow aligns with the overall BKF process employed in RouteOpt's branch-and-bound operations.

.. code-block:: cpp
   :caption: Simple BKF Module Usage Example

   #include <iostream>
   #include "bkf_macro.hpp"
   #include "bkf_controller.hpp"

   using namespace RouteOpt::Branching::BKF;

   int main() {
       // Instantiate shared BKF data.
       BKFDataShared bkfData;

       // Create a BKFController instance.
       BKFController controller;

       // Set estimated parameters (m, n) for BKF computations.
       // Here, 'm' is the estimated parameter and 'n' is the total number of elements.
       controller.setMN(5, 20);

       // Simulate some node states by incrementing counters for before (B4) and after (Af) enumeration.
       bkfData.increaseNodeB4();

       // Calculate the RStar values for a node with index 1.
       // Here, 'lift' is a parameter used in BKF calculations, and 'tree_level' is the current level in the tree.
       double lift = 1.5;
       int tree_level = 2;
       bool dir = true; // Direction of the node (true/false).
       int node_idx = 1;
       controller.calculateRStar(lift, tree_level, dir, node_idx, bkfData);

       // Update time measures:
       // - Set the current state to B4 (true indicates B4 state).
       // - Set the testing time (0.5 seconds for 2 tests).
       // - Set the processing time for a single node (0.3 seconds).
       controller.setIfB4(false);
       controller.setTestingTime(0.5, 2);
       controller.setNodeTime(0.3);
       controller.updateTimeMeasure(bkfData);

       // Suppose we want to determine the best K value for a node given an upper bound and a lower bound.
       double ub = 100.0;
       double lb = 50.0;
       int bestK = controller.getBestK(bkfData, ub, lb);
       std::cout << "Best K: " << bestK << std::endl;

       // Update and retrieve the per-node best K value.
       // Here, we update the best K for a node with index 1.
       controller.updateOptK(bestK, 1);
       double retrievedK = controller.getOptK(1);
       std::cout << "Retrieved K for node 1: " << retrievedK << std::endl;

       return 0;
   }

Explanation
-----------
1. **BKFDataShared Initialization**

   The BKFDataShared object holds shared data for BKF computations, including node counters
   and the current best "f" value. In this example, we simulate node state changes by calling
   `increaseNodeB4()` once.

2. **BKFController Setup**

   The BKFController is initialized and configured using `setMN(5, 20)`, where `5` represents the
   estimated parameter (m) and `20` represents the total number of elements (n).

3. **Time Measurement Configuration**

   - `setIfB4(false)` sets the current state to "before enumeration" (B4).
   - `setTestingTime(0.5, 2)` simulates a total testing time of 0.5 seconds over 2 tests.
   - `setNodeTime(0.3)` sets the node processing time to 0.3 seconds.
   - `updateTimeMeasure(bkfData)` uses the provided times to update internal timing statistics.

4. **Determining the Best K Value**

   The `getBestK()` function is called with upper bound (`ub`) 100.0 and lower bound (`lb`) 50.0,
   returning the best candidate K value for the node based on the shared BKF data.

5. **Per-Node Best K Management**

   The example updates the best K value for a specific node (node index 1) using `updateOptK()`
   and then retrieves it using `getOptK()`. This demonstrates how the controller tracks and updates
   per-node best K values during the branch-and-bound process.


Conclusion
----------
The BKF module in RouteOpt provides a specialized approach for “Best K” parameter management
in branch-and-bound algorithms. Through **bkf_macro.hpp** and **bkf_controller.hpp**, you can
configure BKF-related constants, track node information, measure testing times, and determine
optimal **k** values for branching decisions. This modular design ensures flexibility and clarity
when integrating BKF into the broader RouteOpt framework.

Further Reading
----------------
For more detailed information, please refer to:

.. bibliography::
   :filter: key in {"you2023two"} and cited