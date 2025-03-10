Common Header
===============
Overview
--------
The ``packages/branching/include/branching_macro.hpp`` header provides a collection of macros, 
constants, and custom data structures used in the RouteOpt branching module. 
These definitions include settings for branch score validation, tolerances for candidate comparisons, 
and discount factors for the branching process. 
Additionally, the header defines several templated data structures to record branching history, 
store candidate score information, and manage shared branching data.

File Contents
^^^^^^^^^^^^^
This file contains the following key components:

- **Constants and Macros**

  - ``INVALID_BR_SCORE``: Represents an invalid branch score.
  - ``CANDIDATE_TOLERANCE``: Tolerance for candidate comparisons during branching decisions.
  - ``PSEUDO_FRAC``: Pseudo-fraction value used for fractional branching decisions.
  - ``INITIAL_CUTTING_BRANCHING_RATIO``: Initial ratio for cutting improvement / branching improvement.
  - ``R_DISCOUNT``: Discount factor used in the branching process :cite:p:`you2023two`.

  The header also defines the verbose macro ``BRANCHING_VERBOSE`` and its associated execution macro ``BRANCHING_VERBOSE_EXEC(...)``, which conditionally compiles debugging code.

- **Templated Data Structures**

  - **BranchingHistory**: Records branching history by storing maps for exact, heuristic, and LP testing improvements, as well as branch choice counts and depth increases.

  - **CandidateScoreInfo**: Stores information related to candidate scores, including the candidate candidate, score differences (left and right), the overall score, a ratio (max/min score), and a flag indicating if the right side is maximal.

  - **BranchingBound**: Represents the upper and lower bounds for a branch.

  - **BranchingDataShared**: Maintains shared branching data including the instance dimension, branch pairs, and a candidate map that links candidate candidates to their associated values.

Clean Excerpts
^^^^^^^^^^^^^^^

.. code-block:: cpp
   :caption: branching_macro.hpp (Clean Excerpt)

   #ifndef ROUTE_OPT_BRANCHING_MACRO_HPP
   #define ROUTE_OPT_BRANCHING_MACRO_HPP

   #include <unordered_map>
   #include <functional>

   namespace RouteOpt::Branching {
       constexpr double INVALID_BR_SCORE = -1.;
       constexpr double CANDIDATE_TOLERANCE = 1e-4;
       constexpr double PSEUDO_FRAC = 0.5;
       constexpr double INITIAL_CUTTING_BRANCHING_RATIO = 0.2;
       constexpr double R_DISCOUNT = 0.72;

   #define BRANCHING_VERBOSE

   #ifdef BRANCHING_VERBOSE
   #define BRANCHING_VERBOSE_EXEC(...) __VA_ARGS__;
   #else
       BRANCHING_VERBOSE_EXEC();
   #endif

       template<typename BrCType, typename Hasher>
       class BranchingDataShared;

       template<typename BrCType, typename Hasher>
       struct BranchingHistory {
           std::unordered_map<BrCType, std::pair<double, int>, Hasher> exact_improvement_up{};
           std::unordered_map<BrCType, std::pair<double, int>, Hasher> exact_improvement_down{};
           std::unordered_map<BrCType, std::pair<double, int>, Hasher> heuristic_improvement_up{};
           std::unordered_map<BrCType, std::pair<double, int>, Hasher> heuristic_improvement_down{};
           std::unordered_map<BrCType, std::pair<double, int>, Hasher> lp_testing_improvement_up{};
           std::unordered_map<BrCType, std::pair<double, int>, Hasher> lp_testing_improvement_down{};
           std::unordered_map<BrCType, int, Hasher> branch_choice{};
           std::vector<std::pair<std::pair<double, int>, std::pair<double, int> > > increase_depth{};

           void recordExactPerScore(const BrCType &candidate, double old_val, double now_val, bool dir, int tree_level);
           double tellBranchingIncreaseVal(int tree_level);
           void initialScreen(BranchingDataShared<BrCType, Hasher> &branching_data_shared, int num);
           bool isRecordedCandidate(const BrCType &candidate) const;
           bool isOnceBranched(const BrCType &candidate) const;
       };

       template<typename BrCType>
       struct CandidateScoreInfo {
           BrCType brc{};
           double dif1{}, dif2{};
           double score{};
           double ratio{1.};
           bool if_right_max{};
       };

       struct BranchingBound {
           double ub{};
           double lb{};
       };

       template<typename BrCType, typename Hasher>
       class BranchingDataShared {
       public:
           explicit BranchingDataShared(int dim) : dim(dim) { }
           [[nodiscard]] int getDim() const { return dim; }
           auto &refCandidateMap() { return candidate_map; }
           const auto &getCandidate() const { return candidate_map; }
           const auto &getBranchPair() const { return branch_pair; }
           auto &refBranchPair() { return branch_pair; }
           BranchingDataShared() = delete;
           ~BranchingDataShared() = default;
       private:
           int dim{};
           std::vector<BrCType> branch_pair{};
           std::unordered_map<BrCType, double, Hasher> candidate_map{};
       };
   } // namespace RouteOpt::Branching

   #endif // ROUTE_OPT_BRANCHING_MACRO_HPP

Conclusion
----------
The ``branching_macro.hpp`` file provides foundational elements for the RouteOpt branching module, including constants,
macros, and templated data structures that facilitate candidate evaluation,
branching history tracking, and shared data management.
These components are essential for implementing efficient and robust branch-and-bound algorithms in RouteOpt.


Further Reading
----------------
For more detailed information, please refer to:

.. bibliography::
   :filter: key in {"you2023two"} and cited