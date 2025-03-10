Candidate Selector
======================================

Overview
--------
The Candidate Selector module in RouteOpt is responsible for managing the candidate selection process during branching.
It is implemented through two primary components:

- **Macros and Constants**: Defined in ``packages/branching/candidate_selector/include/candidate_selector_macro.hpp``, these set the parameters for candidate selection,
  such as invalid index indicators, score adjustment ratios, and console output formatting. They also define an enumeration class
  for the various testing phases used during candidate evaluation.

- **Candidate Selector Controller**: Defined in ``packages/branching/candidate_selector/include/candidate_selector_controller.hpp``, this component encapsulates the candidate
  selection process via the templated **BranchingTesting** class. It manages different testing phases (LP, Heuristic, Exact)
  by applying user-defined processing functions to nodes and measuring execution times. Additionally, it provides interfaces
  to retrieve candidate score information and the best candidate branching decision.

License
-------
This software is licensed under **GPL-3.0**.

Candidate Selector Macros (candidate_selector_macro.hpp)
--------------------------------------------------------
This header file defines several key constants, macros, and an enumeration used for candidate selection:

- **``INVALID_INDEX``**

  Indicator for an invalid or uninitialized index.

- **``ADJUSTMENT_SCORE_RATIO``**

  A multiplier used to adjust candidate scores during selection.

- **``PRINT_COL_WIDTH``**

  Specifies the width of each column when printing candidate data in a tabular format.

- **``PRINT_NUM_COLS``**

  Defines the number of columns to display per row in console output.

- **TestingPhase Enumeration**

  Defines the phases used during candidate selection:
  
  - ``LP``: Testing using a Linear Programming approach.
  - ``Heuristic``: Testing using LP combined with heuristic Column Generation.
  - ``Exact``: Testing using LP combined with exact Column Generation.

- **Verbose Macros**

  The macro **``CANDIDATE_SELECTOR_VERBOSE``** enables verbose debugging. When defined, the macro
  **``CANDIDATE_SELECTOR_VERBOSE_EXEC(...)``** executes its code block to provide additional logging.


.. code-block:: cpp
   :caption: candidate_selector_macro.hpp (Clean Excerpt)

   /*
    * Copyright (c) 2025 Zhengzhong (Ricky) You.
    * All rights reserved.
    * Software: RouteOpt
    * License: GPL-3.0
    *
    * @file candidate_selector_macro.hpp
    * @brief Macros and constants for candidate selection in RouteOpt.
    *
    * This header defines constants, macros, and an enumeration class used in the candidate selection process.
    * It includes settings for invalid indices, score adjustment ratios, and console output formatting.
    */

   #ifndef ROUTE_OPT_CANDIDATE_SELECTOR_MACRO_HPP
   #define ROUTE_OPT_CANDIDATE_SELECTOR_MACRO_HPP

   namespace RouteOpt::Branching::CandidateSelector {
       constexpr int INVALID_INDEX = -1;
       constexpr double ADJUSTMENT_SCORE_RATIO = 3;
       constexpr int PRINT_COL_WIDTH = 10;
       constexpr int PRINT_NUM_COLS = 5;

       enum class TestingPhase {
           LP,
           Heuristic,
           Exact
       };

   #define CANDIDATE_SELECTOR_VERBOSE

   #ifdef CANDIDATE_SELECTOR_VERBOSE
   #define CANDIDATE_SELECTOR_VERBOSE_EXEC(...) __VA_ARGS__;
   #else
       CANDIDATE_SELECTOR_VERBOSE_EXEC();
   #endif
   } // namespace RouteOpt::Branching::CandidateSelector

   #endif // ROUTE_OPT_CANDIDATE_SELECTOR_MACRO_HPP


Candidate Selector Controller (candidate_selector_controller.hpp)
------------------------------------------------------------------
This header defines the **BranchingTesting** class template, which manages the candidate selection process during branching.
Key features include:

- **Constructor and Phase Configuration**

  The constructor accepts parameters for the number of tests in each phase (LP, Heuristic, Exact, and an additional phase)
  and user-defined testing functions. The testing functions are applied to nodes to measure performance and adjust scores.

- **Setters for Testing Phases**

  Methods such as ``setNumPhase0()``, ``setNumPhase1()``, ``setNumPhase2()``, and ``setNumPhase3()`` configure the number
  of tests for each respective phase.

- **Processing Function Setters**

  The class provides setters for the LP, Heuristic, and Exact testing functions, allowing you to customize the candidate evaluation process. Each testing function is defined as a parameter of type:

  ``const std::function<void(Node *, const BrCType &, double &, double &)> &``

  In this function:

  - The **first parameter** is a pointer to the current node.
  - The **second parameter** is the branching candidate.
  - The **third and fourth parameters** represent the improvements (or differences) in the objective value of the child LP compared to the LP of the current node, denoted as ``s_l`` (left side) and ``s_r`` (right side), respectively.

  The candidate score is then calculated using the product rule:

  .. math::
      \text{score} = s_l \times s_r

  This formulation allows the evaluation process to weigh both improvements multiplicatively, emphasizing candidates that yield balanced and significant improvements in both directions.


- **Time Counters and Edge Score Information**

  It maintains time counters for each testing phase and collects edge score information during candidate evaluation.

- **Retrieving the Best Candidate**

  The method ``getBestCandidate()`` executes all testing phases, measures execution times, updates internal counters,
  and finally selects and returns the best candidate branching decision based on the processed data.

- **Update of BKF Times**

  The function ``updateBKFtime()`` is provided to update the BKF controllers with measured testing and node processing times,
  ensuring that the candidate selection process is tightly integrated with overall branching operations.


.. code-block:: cpp
   :caption: candidate_selector_controller.hpp (Clean Excerpt)

   /*
    * Copyright (c) 2025 Zhengzhong (Ricky) You.
    * All rights reserved.
    * Software: RouteOpt
    * License: GPL-3.0
    *
    * @file candidate_selector_controller.hpp
    * @brief CandidateSelectorController class for managing candidate selection in RouteOpt.
    *
    * This header defines the BranchingTesting class, which encapsulates the candidate selection process
    * during branching in the RouteOpt framework. It manages different testing phases (LP, Heuristic, Exact)
    * by applying user-defined processing functions on nodes, and measuring the corresponding execution times.
    */

   #ifndef ROUTE_OPT_CANDIDATE_SELECTOR_CONTROLLER_HPP
   #define ROUTE_OPT_CANDIDATE_SELECTOR_CONTROLLER_HPP

   #include <unordered_map>
   #include <vector>
   #include <functional>
   #include "route_opt_macro.hpp"
   #include "candidate_selector_macro.hpp"
   #include "branching_macro.hpp"

   namespace RouteOpt::Branching::CandidateSelector {
       template<typename Node, typename BrCType, typename Hasher>
       class BranchingTesting {
       public:
           BranchingTesting(int num_phase0, int num_phase1, int num_phase2, int num_phase3,
                            const std::function<void(Node *, const BrCType &, double &, double &)> &
                            processLPTestingFunction,
                            const std::function<void(Node *, const BrCType &, double &, double &)> &
                            processHeurTestingFunction,
                            const std::function<void(Node *, const BrCType &, double &, double &)> &
                            processExactTestingFunction) {
               setNumPhase0(num_phase0);
               setNumPhase1(num_phase1);
               setNumPhase2(num_phase2);
               setNumPhase3(num_phase3);
               setProcessLPTestingFunction(processLPTestingFunction);
               setProcessHeurTestingFunction(processHeurTestingFunction);
               setProcessExactTestingFunction(processExactTestingFunction);
           }

           void setNumPhase0(int num) {
               num_phase0 = num;
           }

           void setNumPhase1(int num) {
               num_phase1 = num;
           }

           void setNumPhase2(int num) {
               num_phase2 = num;
           }

           void setNumPhase3(int num) {
               num_phase3 = num;
           }

           void setProcessLPTestingFunction(const std::function<void(Node *, const BrCType &, double &, double &)> &func) {
               processLPTestingFunction = func;
           }

           void setProcessHeurTestingFunction(
               const std::function<void(Node *, const BrCType &, double &, double &)> &func) {
               processHeurTestingFunction = func;
           }

           void setProcessExactTestingFunction(
               const std::function<void(Node *, const BrCType &, double &, double &)> &func) {
               processExactTestingFunction = func;
           }

           const std::vector<EdgeScoreInfo<BrCType> > &getEdgeInfo() const {
               return edge_info;
           }

           [[nodiscard]] int getNumPhase0() const {
               return num_phase0;
           }

           [[nodiscard]] int getNumPhase1() const {
               return num_phase1;
           }

           [[nodiscard]] int getNumPhase2() const {
               return num_phase2;
           }

           [[nodiscard]] int getNumPhase3() const {
               return num_phase3;
           }

           auto &refLPTimeCnt() {
               return lp_time_cnt;
           }

           auto &refHeuristicTimeCnt() {
               return heuristic_time_cnt;
           }

           auto &refExactTimeCnt() {
               return exact_time_cnt;
           }

           const BrCType &getBestCandidate(Node *node,
                                           BranchingHistory<BrCType, Hasher> &branching_history,
                                           BranchingDataShared<BrCType, Hasher> &branching_data_shared,
                                           const std::unordered_map<BrCType, double, Hasher> &candidate_map) {
               branching_data_shared.refCandidateMap() = candidate_map;
               branching_history.initialScreen(branching_data_shared, num_phase0);
               lp_time_cnt.first = TimeSetter::measure([&]() {
                   testing(node, branching_history, branching_data_shared, TestingPhase::LP);
               });
               lp_time_cnt.second = num_phase0 == 1 ? 0 : 2 * num_phase0;
               heuristic_time_cnt.first = TimeSetter::measure([&]() {
                   testing(node, branching_history, branching_data_shared, TestingPhase::Heuristic);
               });
               heuristic_time_cnt.second = num_phase1 == 1 ? 0 : 2 * num_phase1;
               exact_time_cnt.first = TimeSetter::measure([&]() {
                   testing(node, branching_history, branching_data_shared, TestingPhase::Exact);
               });
               exact_time_cnt.second = num_phase2 == 1 ? 0 : 2 * num_phase2;
               return branching_data_shared.refBranchPair().front();
           }

           void testing(
               Node *node,
               BranchingHistory<BrCType, Hasher> &branching_history,
               BranchingDataShared<BrCType, Hasher> &branching_data_shared,
               TestingPhase phase);

           void updateBKFtime(double eps, std::vector<BKF::BKFController> &bkf_controllers) const {
               for (int i = 0; i < bkf_controllers.size(); ++i) {
                   auto &bkf = bkf_controllers[i];
                   if (i == 0) {
                       bkf.setTestingTime(lp_time_cnt.first, lp_time_cnt.second);
                       bkf.setNodeTime(eps + (heuristic_time_cnt.first + exact_time_cnt.first) / 2);
                   } else if (i == 1) {
                       bkf.setTestingTime(heuristic_time_cnt.first, heuristic_time_cnt.second);
                       bkf.setNodeTime(eps + (exact_time_cnt.first + lp_time_cnt.first) / 2);
                   } else if (i == 2) {
                       bkf.setTestingTime(exact_time_cnt.first, exact_time_cnt.second);
                       bkf.setNodeTime(eps + (lp_time_cnt.first + heuristic_time_cnt.first) / 2);
                   } else
                       THROW_RUNTIME_ERROR("BKFController only supports 3 phases, but got " + std::to_string(i));
               }
           }

           BranchingTesting() = delete;
           ~BranchingTesting() = default;

       private:
           int num_phase0{};
           int num_phase1{};
           int num_phase2{};
           int num_phase3{};
           std::pair<double, int> lp_time_cnt{};
           std::pair<double, int> heuristic_time_cnt{};
           std::pair<double, int> exact_time_cnt{};
           std::vector<EdgeScoreInfo<BrCType> > edge_info{};
           std::function<void(Node *, const BrCType &, double &, double &)> processLPTestingFunction{};
           std::function<void(Node *, const BrCType &, double &, double &)> processHeurTestingFunction{};
           std::function<void(Node *, const BrCType &, double &, double &)> processExactTestingFunction{};
           void reviseExtremeUnbalancedScore(BranchingHistory<BrCType, Hasher> &branching_history,
                                             TestingPhase phase);
       };
   }

   #include "candidate_testing.hpp"
   #include "initial_screen.hpp"
   #endif // ROUTE_OPT_CANDIDATE_SELECTOR_CONTROLLER_HPP


Usage Example
-------------
Below is a simple C++ example demonstrating how to use the candidate selector module within RouteOpt.

.. code-block:: cpp
   :caption: Example: Using the Candidate Selector Module

   #include <iostream>
   #include "candidate_selector_macro.hpp"
   #include "candidate_selector_controller.hpp"

   // Define a simple dummy node structure for demonstration.
   struct DummyNode {
       int id;
       double score;
       DummyNode(int id, double score) : id(id), score(score) {}
   };

   // Dummy testing functions for each phase.
   auto processLPTesting = [](DummyNode* node, const int &brc, double &dif1, double &dif2) {
       dif1 = 1; dif2 = 2;
   };

   auto processHeurTesting = [](DummyNode* node, const int &brc, double &dif1, double &dif2) {
       dif1 = 0.1; dif2 = 0.2;
   };

   auto processExactTesting = [](DummyNode* node, const int &brc, double &dif1, double &dif2) {
       dif1 = 0.01; dif2 = 0.02;
   };

   int main() {
       // Create a BranchingTesting instance for candidate selection.
       // Template parameters:
       //   - Node type: DummyNode
       //   - Branching candidate type: int (for simplicity)
       //   - Hasher: std::hash<int>
       RouteOpt::Branching::CandidateSelector::BranchingTesting<DummyNode, int, std::hash<int>> tester(
           2, 2, 2, 1,  // Number of tests for phases LP, Heuristic, Exact, and an extra phase.
           processLPTesting,
           processHeurTesting,
           processExactTesting
       );

       // Retrieve the number of tests configured for the LP phase.
       std::cout << "Number of LP phase tests: " << tester.getNumPhase0() << std::endl;

       // Further candidate selection logic would involve:
       //   - Applying the testing functions on a given node.
       //   - Measuring the execution times.
       //   - Updating candidate scores.
       //   - Selecting and returning the best candidate.
       // For simplicity, this example only demonstrates the configuration.

       return 0;
   }

Conclusion
----------
The Candidate Selector module in RouteOpt provides essential macros, constants, and a flexible controller class to
manage candidate selection during branching. By customizing the testing functions and configuring the number of tests
per phase, users can tailor the candidate selection process to their specific optimization problem. This module is
integrated into the overall RouteOpt framework, ensuring that candidate selection is performed consistently across
different branching scenarios.

Further Reading
---------------
For more details on the candidate selection process and its integration into the RouteOpt branching framework,
please refer to the source code in the application of CVRP located in ``packages/application/cvrp/src/``, or simply
ask your question in the RouteOpt Slack/Wechat channel, and I may update the documentation accordingly.
