R1Cs: Coefficient Getter
=========================

Overview
--------
The file ``packages/rank1_cuts/coefficient_getter/include/rank1_coefficient_controller.hpp`` defines the ``Rank1CoefficientGetter`` class, which is responsible for calculating the coefficients of Rank-1 cuts within the RouteOpt software package. This class provides methods to compute these coefficients based on column sequence information and solver data (LP model), supporting both full memory and limited memory approaches.

License
^^^^^^^
This software is licensed under **GPL-3.0**.

File Contents
^^^^^^^^^^^^^
The header file ``rank1_coefficient_controller.hpp`` includes:

- **Rank1CoefficientGetter Class**

  - *Public Methods*:
    - ``getR1CCoeffs``: Computes the coefficients of Rank-1 cuts.
    - ``buildR1CEnuMatrix``: Builds the enumeration matrix for Rank-1 cuts.

  - *Private Methods*:
    - ``getFullMemR1CCoeffs``: Computes full memory coefficients of Rank-1 cuts.
    - ``getCoefficientExtendR1C``: Extends the coefficient states for Rank-1 cuts.
    - ``getLimitedR1CCoeffs``: Computes limited memory coefficients of Rank-1 cuts.
    - ``getLimitedR1CPre``: Prepares internal data structures for limited memory Rank-1 cut coefficient computation.

Rank1CoefficientGetter Class
----------------------------
The ``Rank1CoefficientGetter`` class is designed to calculate the coefficients of Rank-1 cuts. It utilizes both full memory and limited memory approaches to accommodate different computational scenarios.

Constructor
^^^^^^^^^^^
- **Rank1CoefficientGetter**

  *Input*: A reference to the shared Rank-1 cuts data object of type ``Rank1CutsDataShared``.

  **Meaning**: Initializes the coefficient getter with shared data necessary for computing Rank-1 cut coefficients.

Public Methods
^^^^^^^^^^^^^^
- **getR1CCoeffs**

  *Template Parameter*: ``MatrixType`` – The type of the matrix to store the coefficients.

  *Inputs*:
    - ``seq_info``: A vector of ``SequenceInfo`` objects representing sequence data.
    - ``cuts``: A vector of Rank-1 cuts.
    - ``solver``: A pointer to the ``Solver`` instance.
    - ``if_limit_mem``: A boolean flag indicating whether to use the limited memory approach.

  *Output*: ``mat`` – A matrix of type ``MatrixType`` to store the computed coefficients.

  **Meaning**: This templated method calculates the coefficients of Rank-1 cuts based on the provided sequence information, cuts, solver data, and memory limitation flag. The results are stored in the provided matrix.

  .. note::
     `solver` pointer is only used when `if_limit_mem` is false and can be `nullptr`. Then column sequence information is used to compute the coefficients.

- **buildR1CEnuMatrix**

  *Inputs*:
    - ``mat``: A sparse matrix representing the coefficients.
    - ``r1cs``: A vector of Rank-1 cuts.
    - ``start``: An integer representing the starting row index in the LP model for processing.
    - ``triplets``: A vector of ``Eigen::Triplet`` to store the non-zero entries.

  **Meaning**: This method constructs the enumeration matrix for Rank-1 cuts based on the provided sparse matrix, cuts, starting index, and triplets.

  .. note::
     retrieved `triplets`'s row index is the row index of the LP model - `start`.

Private Methods
^^^^^^^^^^^^^^^^^
- **getFullMemR1CCoeffs**

  *Template Parameter*: ``MatrixType`` – The type of the matrix to store the coefficients.

  *Inputs*:
    - ``seq_info``: A vector of ``SequenceInfo`` objects representing sequence data.
    - ``cuts``: A vector of Rank-1 cuts.

  *Output*: ``mat`` – A matrix of type ``MatrixType`` to store the computed coefficients.

  **Meaning**: This templated method calculates the coefficients of Rank-1 cuts using the full memory approach based on the provided sequence information, cuts, and matrix.

- **getCoefficientExtendR1C**

  *Inputs*:
    - ``states``: A vector representing the current states.
    - ``sparse_rep``: A vector representing the sparse representation.
    - ``cnt``: An unordered map counting occurrences of each state.
    - ``valid_sparse_num``: An integer reference to the number of valid sparse entries.
    - ``from``: An integer representing the starting customer index.
    - ``to``: An integer representing the ending customer index.

  **Meaning**: This method updates the states, sparse representation, count map, and valid sparse number based on the transition from one customer to another.

- **getLimitedR1CCoeffs**

  *Template Parameter*: ``MatrixType`` – The type of the matrix to store the coefficients.

  *Input*: ``seq_info`` – A vector of ``SequenceInfo`` objects representing sequence data.

  *Output*: ``mat`` – A matrix of type ``MatrixType`` to store the computed coefficients.

  **Meaning**: This templated method calculates the coefficients of Rank-1 cuts using the limited memory approach based on the provided sequence information and matrix.

- **getLimitedR1CPre**

  *Input*: ``cuts`` – A vector of Rank-1 cuts to be processed.

  **Meaning**: This method initializes and sets up the necessary internal data structures to facilitate the computation of Rank-1 cut coefficients in a limited memory environment. It processes the provided cuts to extract and organize information required for efficient coefficient calculation.

Header Code
-----------
Below is an excerpt from ``rank1_coefficient_controller.hpp`` that illustrates the definition of the ``Rank1CoefficientGetter`` class:

.. code-block:: cpp
   :caption: rank1_coefficient_controller.hpp

   /*
    * Copyright (c) 2025 Zhengzhong (Ricky) You.
    * All rights reserved.
    * Software: RouteOpt
    * License: GPL-3.0
    *
    * @file rank1_coefficient_controller.hpp
    * @brief Rank-1 Coefficient Getter for calculating coefficients of Rank-1 cuts.
    *
    * This header defines the Rank1CoefficientGetter class, which provides methods to
    * compute the coefficients of Rank-1 cuts in the context of sequence information
    * and solver data. It supports both full memory and limited memory approaches
    * for coefficient calculation.
    */

   #ifndef ROUTE_OPT_RANK1_COEFFICIENT_CONTROLLER_HPP
   #define ROUTE_OPT_RANK1_COEFFICIENT_CONTROLLER_HPP

   #include <vector>
   #include <unordered_map>
   #include <Eigen/Sparse>
   #include "rank1_macro.hpp"
   #include "route_opt_macro.hpp"
   #include "solver.hpp"

   namespace RouteOpt::Rank1Cuts::CoefficientGetter {
       class Rank1CoefficientGetter {
       public:
           explicit Rank1CoefficientGetter(Rank1CutsDataShared &data_shared)
               : data_shared_ref(std::ref(data_shared)) {
           }

           template<typename MatrixType>
           void getR1CCoeffs(
               const std::vector<SequenceInfo> &seq_info,
               const std::vector<R1c> &cuts,
               const Solver *solver,
               bool if_limit_mem,
               MatrixType &mat);

           void buildR1CEnuMatrix(
               const Eigen::SparseMatrix<double, Eigen::RowMajor> &mat,
               const std::vector<R1c> &r1cs,
               int start,
               std::vector<Eigen::Triplet<double> > &triplets
           ) const;

           void recoverR1CsInEnum(std::vector<R1c> &r1cs,
                               const std::vector<SequenceInfo> &cols,
                               Solver &solver);

           Rank1CoefficientGetter() = delete;
           ~Rank1CoefficientGetter() = default;

       private:
           std::vector<std::pair<std::vector<int>, std::vector<int> > > lp_v_cut_map{};
           std::vector<std::vector<r1cIndex> > lp_v_v_use_states{};
           std::vector<int> lp_r1c_denominator{};

           const std::reference_wrapper<Rank1CutsDataShared> data_shared_ref;

           template<typename MatrixType>
           void getFullMemR1CCoeffs(
               const std::vector<SequenceInfo> &seq_info,
               const std::vector<R1c> &cuts,
               MatrixType &mat);

           template<typename MatrixType>
           void getFullMemR1CCoeffs(
               const Solver *solver,
               const std::vector<R1c> &cuts,
               MatrixType &mat);

           void getCoefficientExtendR1C(std::vector<int> &states,
                                        std::vector<int> &sparse_rep,
                                        std::unordered_map<int, int> &cnt,
                                        int &valid_sparse_num,
                                        int from,
                                        int to);

           template<typename MatrixType>
           void getLimitedR1CCoeffs(const std::vector<SequenceInfo> &seq_info,
                                    MatrixType &mat);

           void getLimitedR1CPre(const std::vector<R1c> &cuts);
       };
   }

   #include "r1c_coeffs_getter.hpp"
   #include "full_r1c_coeffs_getter.hpp"
   #endif // ROUTE_OPT_RANK1_COEFFICIENT_CONTROLLER_HPP

Usage Example
-------------
Below is an example demonstrating how to use the ``Rank1CoefficientGetter`` class to compute the coefficients of Rank-1 cuts using a limited memory approach.

.. code-block:: cpp

   #include <vector>
   #include <iostream>
   #include "rank1_coefficient_controller.hpp"
   #include "solver.hpp"

   using namespace RouteOpt::Rank1Cuts::CoefficientGetter;

   int main() {
       // Initialize shared Rank-1 cuts data with an instance dimension (e.g., 4)
       Rank1CutsDataShared sharedData(4);

       // Create an instance of the Rank1CoefficientGetter with the shared data
       Rank1CoefficientGetter coeffGetter(sharedData);

       // Prepare dummy sequence information
       std::vector<SequenceInfo> seqInfo;
       // Populate seqInfo with relevant data...

       // Define a matrix type (for example, using Eigen's SparseMatrix)
       Eigen::SparseMatrix<double, Eigen::RowMajor> coeffMatrix;

       // Compute the coefficients using the limited memory approach
       coeffGetter.getR1CCoeffs(seqInfo, /*cuts=*/{}, /*solver=*/nullptr, /*if_limit_mem=*/true, coeffMatrix);

       // Output the number of non-zero entries in the coefficient matrix (for demonstration)
       std::cout << "Computed coefficients matrix has "
                 << coeffMatrix.nonZeros() << " non-zero entries." << std::endl;

       return 0;
   }

Conclusion
----------
The ``Rank1CoefficientGetter`` module in RouteOpt is essential for calculating the coefficients of Rank-1 cuts. It offers flexible methods for coefficient computation under both full and limited memory scenarios, enabling efficient integration of Rank-1 cuts into optimization models.
