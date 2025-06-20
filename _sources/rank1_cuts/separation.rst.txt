R1Cs: Separation
=========================

Overview
--------
The files ``packages/rank1_cuts/separation/include/rank1_separation_macro.hpp`` and ``packages/rank1_cuts/separation/include/rank1_separation_controller.hpp`` define the macro definitions, type aliases, and the controller class used for the separation of Rank-1 cuts within the RouteOpt software package. These files provide the parameters for tolerances, memory settings, and generator parameters, as well as the implementation of the Rank-1 separation controller which integrates cut generation, memory finding, and cut selection modules.

License
^^^^^^^
This software is licensed under **GPL-3.0**.

File Contents
^^^^^^^^^^^^^
The separation module is composed of two main components:

- **Macro Definitions and Type Aliases**

  The file ``rank1_separation_macro.hpp`` defines constants, type aliases, and helper macros used in the Rank-1 separation process.

- **Separation Controller**

  The file ``rank1_separation_controller.hpp`` defines the ``Rank1SeparationController`` class, which manages the separation process for Rank-1 cuts.

Macro Definitions and Type Aliases
-----------------------------------
The file ``rank1_separation_macro.hpp`` provides several key definitions:

- **RANK1_SEPARATION_VERBOSE**

  Verbosity flag for debugging the separation process.

- **SOL_X_RANK1_TOLERANCE**

  Tolerance for solution x values in Rank-1 separation.

- **MAX_CUT_MEM_FACTOR**

  Factor to control the maximum memory size for cut generation.

- **INITIAL_RANK_1_MULTI_LABEL_POOL_SIZE**

  Initial size for the pool of Rank-1 multi-labels.

- **FIND_MEM_USE_ENUMERATION_OR_MIP**

  Threshold to decide whether to use enumeration or MIP (Mixed-Integer Programming) for memory finding.

- **MAX_NUMBER_SEGMENT_FOR_ONE_COLUMN**

  Maximum number of segments allowed for a single column in the separation process.

- **MAX_UNDETERMINED_ARC_NUMBER**

  Maximum number of undetermined arcs.

- **MAX_LABELS**

  Maximum number of labels allowed.

- **MAX_HEURISTIC_SEP_ROW_RANK1**

  Maximum number of neighbor customers for separating Rank-1 cuts.

- **MIN_CUTS_ADDED_PER_ROUND**

  Minimum number of cuts to be added per separation round.

- **TIME_LIMIT_FOR_MIP_FIND_MEM**

  Time limit (in seconds) for MIP-based memory finding.

- **CUT_VIO_FACTOR**

  Violation factor for cuts.

- **RANK1_ROW_DENSITY**

  Estimated density for Rank-1 cuts.

- **SOL_KEEPER_LIMIT**

  Limit for keeping solution routes in memory.

- **MemoryType**

  Enumeration specifying the memory mode used in separation:

  - **NO_MEMORY**

    No memory is used.

  - **NODE_MEMORY**

    Node-based memory is applied.

  - **ARC_MEMORY**

    Arc-based memory is applied.

- **VectorHashInRank1**

  Custom hash functor for a vector of integers, used in unordered containers.

- **arcBit**

  A bitset type representing undetermined arcs.

- **cutLong**

  Alias for the custom long bitset type used in cut representations.

- **sparseRowMatrixXI** and **sparseRowVectorXI**

  Type aliases for row-major sparse matrices and vectors using the Eigen library.

- **RouteInfo**

  Structure containing route information, including:

  - **frac_x**

    The fractional value associated with the route (e.g., LP solution value).

  - **col_seq**

    The sequence of customer indices representing the route.

  - **forward_concatenate_pos**

    The position used for forward concatenation during route merging.

- **RANK1_VERBOSE_EXEC**

  Macro for conditionally executing a statement based on the verbosity flag.

Separation Controller: Rank1SeparationController
------------------------------------------------
The file ``rank1_separation_controller.hpp`` defines the ``Rank1SeparationController`` class, which manages the separation of Rank-1 cuts. Key functionalities include:

Constructor
^^^^^^^^^^^^^^^^^^^^^^^^^
- **rank1CutsDataShared**

  *Input*: A reference to a shared Rank-1 cuts data object of type ``Rank1CutsDataShared``.

  **Meaning**: Provides precomputed multipliers and metadata required for generating Rank-1 cuts.

- **max_row_rank1**

  *Input*: An integer representing the maximum row dimension for Rank-1 cuts.

  **Meaning**: Limits the maximum size (or depth) of cuts based on the number of customers (:math:`|C|`).

- **max_num_r1c3_per_round**

  *Input*: An integer specifying the maximum number of R1C cuts with dimension 3 to be generated per separation round.

  **Meaning**: Restricts the number of specific types of cuts (dimension 3).

- **max_num_r1c_per_round**

  *Input*: An integer specifying the maximum number of Rank-1 cuts (with dimensions other than 3) to be generated per round.

  **Meaning**: Ensures that the total number of generated cuts remains within a manageable limit.

- **solver**

  *Input*: A reference to the IP solver object.

  **Meaning**: Provides access to the underlying solver to integrate new cuts into the LP/MIP model.

- **cost_mat4_vertex**

  *Input*: A two-dimensional vector of doubles representing the cost matrix for vertices.

  **Meaning**: Used to evaluate the cost associated with transitions between vertices in the routing problem.

updateInfo()
^^^^^^^^^^^^^^^^^^^^^^^^^
- **limited_memory_type**

  *Input*: A value of the enumeration ``MemoryType``.

  **Meaning**: Determines the memory mode to apply during separation (e.g., NO_MEMORY, NODE_MEMORY, ARC_MEMORY).

- **pricing_hard_level**

  *Input*: A value of the enumeration ``PRICING_HARD_LEVEL``.

  **Meaning**: Indicates the complexity of the pricing subproblem, guiding the cut generation strategy.

- **if_collect_sol**

  *Input*: A boolean flag.

  **Meaning**: Specifies whether the current solution routes should be collected for further processing or analysis.

- **sol**

  *Input*: A vector of ``RouteInfo`` structures.

  **Meaning**: Represents the current solution routes obtained from the LP/MIP, each containing route details such as fractional value and customer sequence.

- **old_cuts**

  *Input*: A vector of existing Rank-1 cuts (``R1c`` structures).

  **Meaning**: Contains previously generated cuts that may be used for comparison or updating during the separation process.

separateRank1Cuts()
^^^^^^^^^^^^^^^^^^^^^^^^^
- **cuts**

  *Input/Output*: A vector of ``R1c`` structures.

  **Meaning**: On input, may contain existing cuts; on output, will include newly generated or updated Rank-1 cuts.

- **if_mem**

  *Input*: A boolean flag.

  **Meaning**: Indicates whether memory-based search strategies should be applied during the separation process.

  .. note::
     When call this function in ``enumeration`` state, ``if_mem`` should be set to ``false`` to avoid redundant memory search.

- **if_select_cuts**

  *Input*: A boolean flag.

  **Meaning**: Determines whether cut selection strategies should be executed to filter or prioritize generated cuts.

  .. note::
     When call this function ``enumeration`` state, ``if_select_cuts`` should be set to ``false`` to avoid giving up cuts
     that are bad for labeling but have no impact on the pricing problem in ``enumeration`` state, i.e., inspection algorithm.

convert2ArcMemory()
^^^^^^^^^^^^^^^^^^^^^^^^^
- **existing_cuts**

  *Input/Output*: A vector of ``R1c`` structures.

  **Meaning**: Contains cuts in a node-memory representation which will be converted to an arc-memory representation for improved pricing performance.


Header Codes
-------------
Below is an excerpt from ``rank1_separation_macro.hpp`` that illustrates key macro definitions and type aliases:

.. code-block:: cpp

   /*
    * Copyright (c) 2025 Zhengzhong (Ricky) You.
    * All rights reserved.
    * Software: RouteOpt
    * License: GPL-3.0
    */

   /*
    * @file rank1_separation_macro.hpp
    * @brief Macro definitions and type aliases for Rank-1 separation in RouteOpt.
    *
    * This header defines various constants, type aliases, and helper macros that are used
    * in the Rank-1 separation process.
    */

   #ifndef ROUTE_OPT_RANK1_SEPARATION_MACRO_HPP
   #define ROUTE_OPT_RANK1_SEPARATION_MACRO_HPP

   #include <bitset>
   #include <Eigen/Sparse>
   #include <vector>
   #include "route_opt_macro.hpp"

   namespace RouteOpt::Rank1Cuts::Separation {
       constexpr bool RANK1_SEPARATION_VERBOSE = false;

       constexpr double SOL_X_RANK1_TOLERANCE = 1e-3;

       constexpr double MAX_CUT_MEM_FACTOR = 0.15;

       constexpr int INITIAL_RANK_1_MULTI_LABEL_POOL_SIZE = 2048;

       constexpr int FIND_MEM_USE_ENUMERATION_OR_MIP = 1000;

       constexpr int MAX_NUMBER_SEGMENT_FOR_ONE_COLUMN = 16;

       constexpr int MAX_UNDETERMINED_ARC_NUMBER = 128;

       constexpr int MAX_LABELS = 1024;

       constexpr int MAX_HEURISTIC_SEP_ROW_RANK1 = 16;

       constexpr int MIN_CUTS_ADDED_PER_ROUND = 50;

       constexpr double TIME_LIMIT_FOR_MIP_FIND_MEM = 0.2;

       constexpr double CUT_VIO_FACTOR = 0.1;

       constexpr double RANK1_ROW_DENSITY = 0.1;

       constexpr int SOL_KEEPER_LIMIT = 20;

       enum class MemoryType {
           NO_MEMORY = 0,
           NODE_MEMORY = 1,
           ARC_MEMORY = 2
       };

       struct RouteInfo {
           double frac_x{};
           std::vector<int> col_seq{};
           int forward_concatenate_pos{};
       };

       struct VectorHashInRank1 {
           size_t operator()(const std::vector<int> &v) const {
               std::size_t hash = 0;
               for (const int num: v) {
                   hash ^= std::hash<int>{}(num) + 0x9e3779b9 + (hash << 6) + (hash >> 2);
               }
               return hash;
           }
       };

       using arcBit = std::bitset<MAX_UNDETERMINED_ARC_NUMBER>;
       using cutLong = routeOptLong;
       using sparseRowMatrixXI = Eigen::SparseMatrix<int, Eigen::RowMajor>;
       using sparseRowVectorXI = Eigen::SparseVector<int, Eigen::RowMajor>;

   #define RANK1_VERBOSE_EXEC(stmt) do { \
       if (RANK1_SEPARATION_VERBOSE) { \
           stmt; \
       } \
   } while (0);
   } // namespace RouteOpt::Rank1Cuts::Separation

   #endif // ROUTE_OPT_RANK1_SEPARATION_MACRO_HPP

Below is an excerpt from ``rank1_separation_controller.hpp`` that demonstrates the interface of the separation controller:

.. code-block:: cpp

   /*
    * Copyright (c) 2025 Zhengzhong (Ricky) You.
    * All rights reserved.
    * Software: RouteOpt
    * License: GPL-3.0
    *
    * @file rank1_separation_controller.hpp
    * @brief Rank-1 Separation Controller for handling the generation, updating, and processing of Rank-1 cuts.
    *
    * This header defines the Rank1SeparationController class which coordinates the separation process for Rank-1 cuts.
    * It integrates shared Rank-1 cuts data, cut generation, memory finding, and cut selection modules,
    * and interfaces with the underlying solver and vertex cost matrix.
    */

   #ifndef ROUTE_OPT_RANK1_SEPARATION_CONTROLLER_HPP
   #define ROUTE_OPT_RANK1_SEPARATION_CONTROLLER_HPP

   #include "rank1_data_shared.hpp"
   #include "rank1_cuts_generator.hpp"
   #include "rank1_memory_finder.hpp"
   #include "rank1_cuts_selector.hpp"
   #include "solver.hpp"

   namespace RouteOpt::Rank1Cuts::Separation {
       class Rank1SeparationController {
       public:
           Rank1SeparationController(const Rank1CutsDataShared &rank1CutsDataShared,
                                     int max_row_rank1,
                                     int max_num_r1c3_per_round,
                                     int max_num_r1c_per_round,
                                     Solver &solver,
                                     const std::vector<std::vector<double>> &cost_mat4_vertex);

           void updateInfo(MemoryType limited_memory_type,
                           PRICING_HARD_LEVEL pricing_hard_level,
                           bool if_collect_sol,
                           const std::vector<RouteInfo> &sol,
                           const std::vector<R1c> &old_cuts);

           void separateRank1Cuts(std::vector<R1c> &cuts,
                                  bool if_mem = true,
                                  bool if_select_cuts = true);

           void convert2ArcMemory(std::vector<R1c> &existing_cuts);

           [[nodiscard]] auto getIfOnceUseNoSymmetryMem() const {
               return if_once_use_no_symmetry_mem;
           }

           Rank1SeparationController() = delete;
           ~Rank1SeparationController() = default;

       private:
           std::vector<std::vector<RouteInfo>> sol_vec{};
           std::reference_wrapper<const Rank1CutsDataShared> rank1CutsDataShared_ref;
           DataShared sharedData;
           CutGenerator cutGen;
           MemGenerator memGen;
           CutSelector cutSelector;
           bool if_once_use_no_symmetry_mem{false};

           void cleanData() {
               sharedData.cleanData();
               cutGen.cleanData();
               memGen.cleanData();
               cutSelector.cleanData();
           }

           void setRhs(std::vector<R1c> &cuts);
       };
   } // namespace RouteOpt::Rank1Cuts::Separation

   #endif // ROUTE_OPT_RANK1_SEPARATION_CONTROLLER_HPP


Usage Example
----------------

Below is an example demonstrating how to use the Rank-1 separation module in RouteOpt. This example shows how to initialize the shared data,
create a solver instance, define a cost matrix, and then use the Rank1SeparationController to update information and generate new Rank-1 cuts.

.. code-block:: cpp


   #include <vector>
   #include <iostream>
   #include "rank1_data_shared.hpp"
   #include "rank1_separation_controller.hpp"
   #include "solver.hpp"

   using namespace RouteOpt::Rank1Cuts;
   using namespace RouteOpt::Rank1Cuts::Separation;

   int main() {
       // Initialize shared Rank-1 cuts data with an instance dimension (e.g., 4)
       Rank1CutsDataShared sharedData(4);

       // Create an instance of the IP solver
       Solver solver{};

       // Define a sample cost matrix for vertices (e.g., for 4 vertices)
       std::vector<std::vector<double>> costMatrix = {
           {0.0, 10.0, 20.0, 30.0},
           {10.0, 0.0, 15.0, 25.0},
           {20.0, 15.0, 0.0, 35.0},
           {30.0, 25.0, 35.0, 0.0}
       };

       // Instantiate the Rank1SeparationController with parameters:
       // - max_row_rank1: Maximum Rank-1 row dimension (e.g., 4)
       // - max_num_r1c3_per_round: Maximum number of R1C3 cuts per separation round (e.g., 50)
       // - max_num_r1c_per_round: Maximum number of R1C cuts (dimension != 3) per round (e.g., 100)
       // This is one time call
       Rank1SeparationController separationController(
           sharedData,
           4,
           50,
           100,
           solver,
           costMatrix
       );

       // Prepare dummy solution routes (RouteInfo) for the update
       std::vector<RouteInfo> solutionRoutes;
       RouteInfo route;
       route.frac_x = 0.75;
       route.col_seq = {1, 2};
       route.forward_concatenate_pos = 1;
       solutionRoutes.push_back(route);
       // Add other routes as needed...

       // Prepare the cut vector for old cuts (if not have, give empty vector)
       std::vector<R1c> oldCuts;

       // Update the controller with the current solution and existing cuts.
       // You need to call this function each cutting round
       separationController.updateInfo(
           MemoryType::NODE_MEMORY,   // Using node-based memory
           PRICING_HARD_LEVEL::EASY,   // Pricing difficulty level: EASY
           true,                       // Collect current solution
           solutionRoutes,
           oldCuts
       );

       // Container to hold the new generated Rank-1 cuts
       std::vector<R1c> newCuts;

       // Perform the separation process to generate new cuts
       // You need to call this function each cutting round
       separationController.separateRank1Cuts(newCuts, true, true);

       // Optionally, convert node-memory-based cuts to arc-memory-based cuts
       separationController.convert2ArcMemory(newCuts);

       // Output the number of new cuts generated (for demonstration)
       std::cout << "Number of new Rank-1 cuts generated: " << newCuts.size() << std::endl;

       return 0;
   }

.. note::
   The new cuts obtained may contain some of the old cuts, but definitely with larger memory set, and thus,
   make the these old cuts no longer tight. Therefore, it is recommended to identify the duplicated cuts in old cuts set,
   and remove them from the old cuts set before/after you add new cuts to the LP model.

.. note::
   The Rank-1 separation module offers a myriad of interesting and useful features that are not fully covered in this document.
   For a deeper understanding, I recommend exploring the function usages directly in the source code located under ``packages/application/cvrp/src`` using an IDE such as CLion.

   Reviewing the source code of the CVRP application related to the Rank-1 separation module will provide valuable insights into how to use these features effectively.

   If you have any questions, please feel free to contact me at `you.z@ufl.edu <mailto:you.z@ufl.edu>`_ or send your question in Group Chat.

Conclusion
----------
The Rank-1 separation module in RouteOpt provides a robust framework for generating, updating, and managing Rank-1 cuts. By leveraging detailed macro definitions for parameter settings and a dedicated controller for the separation process, users can effectively integrate advanced cut separation strategies into their routing solvers.
