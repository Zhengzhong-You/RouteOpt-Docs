RCCs: Coefficient Getter
===============================================

Overview
--------
The file ``packages/rounded_cap_cuts/coefficient_getter/include/rcc_coefficient_controller.hpp``
defines the ``RCCCoefficientController`` class, which is responsible for computing the
coefficient matrix for Rounded Cap Cuts (RCCs) in the RouteOpt software package.
This class provides static methods to compute these coefficients based on sequence information
and RCC cut data, as well as to build the RCC enumeration matrix using a sparse matrix
representation.

License
^^^^^^^
This software is licensed under **GPL-3.0**.

File Contents
^^^^^^^^^^^^^
The header file ``rcc_coefficient_controller.hpp`` includes:

- **RCCCoefficientController Class**

  - *Public Methods*:

    - ``getCoefficientRCC``: A templated static method that computes the coefficient matrix
      for RCCs. It supports an option to compute an elementary coefficient matrix (using form 3 of RCC).

    - ``buildRCCEnuMatrix``: A static method that constructs the RCC enumeration matrix from a given
      sparse matrix (with dimension dim-1 rows) and RCC cuts.

    - ``recoverRCCsInEnum``: A static method that recovers/strengthens RCCs to form 3 for just entering enumeration state.

RCCCoefficientController Class
------------------------------
The ``RCCCoefficientController`` class provides static methods for the computation of
RCC coefficient matrices and for building the enumeration matrix required in optimization
models involving Rounded Cap Cuts.

Constructor
^^^^^^^^^^^
- **RCCCoefficientController**

  *Meaning*: As a static utility class, it does not require initialization of internal data.
  The default constructor is provided, but its functionality is based solely on its static methods.

Public Methods
^^^^^^^^^^^^^^
- **getCoefficientRCC**

  *Template Parameter*: ``MatrixType`` – The type of the matrix to store the coefficients (e.g., Eigen::MatrixXd).

  *Inputs*:
    - ``seq_info``: A vector of ``SequenceInfo`` objects representing sequence data.
    - ``cuts``: A vector of RCC cuts.
    - ``if_elementary``: A boolean flag indicating whether the computation should follow the elementary coefficient matrix formulation (form 3 of RCC).
    - ``mat``: A matrix of type ``MatrixType`` to be computed and updated with the RCC coefficients.

  **Meaning**: This static templated method computes the RCC coefficient matrix based on the provided
  sequence information and RCC cuts. The flag ``if_elementary`` determines whether the computation
  follows the elementary coefficient formulation.

- **buildRCCEnuMatrix**

  *Inputs*:
    - ``mat``: A sparse matrix (with dim-1 rows) representing the base coefficient matrix used in the enumeration.
    - ``rccs``: A vector of RCC cuts used in the enumeration process.
    - ``start``: An integer representing the starting row index in the LP model (to offset the enumeration).
    - ``triplets``: A vector of ``Eigen::Triplet<double>`` to store the non-zero entries of the enumeration matrix.

  **Meaning**: This static method constructs the enumeration matrix for RCCs by converting the given sparse matrix
  into a list of triplets. The provided starting index offsets the row indices according to the LP model's structure.

.. note::
   If you choose to compute the elementary coefficient matrix (form 3 of RCC), the ``if_elementary`` flag should be set to true.
   However, setting this flag to true will require the vector of RCC to be all form 3, and if not, the program will throw an error.
   Therefore, you should call the method recoverRCCsInEnum to recover/strengthen the RCCs, i.e., set them to form 3.

- **recoverRCCsInEnum**
    *Inputs*:
        - ``rccs``: A vector of RCC cuts to be recovered or strengthened.
        - ``cols``: A vector of ``SequenceInfo`` objects representing the columns of the LP model.
        - ``solver``: An instance of the ``Solver`` class used for solving the LP model.

    **Meaning**: This static method recovers or strengthens the RCCs to form 3, ensuring that they are suitable for
    entering the enumeration state. It uses the provided sequence information and solver instance to perform this operation.

Header Code
-----------
Below is an excerpt from ``rcc_coefficient_controller.hpp`` illustrating the definition of the ``RCCCoefficientController`` class:

.. code-block:: cpp
   :caption: rcc_coefficient_controller.hpp

   /*
    * Copyright (c) 2025 Zhengzhong (Ricky) You.
    * All rights reserved.
    * Software: RouteOpt
    * License: GPL-3.0
    *
    * @file rcc_coefficient_controller.hpp
    * @brief Controller for RCC coefficient generation in RouteOpt.
    *
    * This header defines the RCCCoefficientController class, which provides static methods to
    * compute coefficient matrices and build enumeration matrices for Rounded Cap Cuts (RCCs).
    */

   #ifndef ROUTE_OPT_RCC_COEFFICIENT_CONTROLLER_HPP
   #define ROUTE_OPT_RCC_COEFFICIENT_CONTROLLER_HPP


   #include <Eigen/Sparse>
   #include "route_opt_macro.hpp"
   #include "rcc_macro.hpp"
   #include "solver.hpp"

   namespace RouteOpt::RCCs::CoefficientGetter {
       class RCCCoefficientController {
       public:
           template<typename MatrixType>
           static void getCoefficientRCC(const std::vector<SequenceInfo> &seq_info,
                                         const std::vector<Rcc> &cuts,
                                         bool if_elementary,
                                         MatrixType &mat);


           static void buildRCCEnuMatrix(
               const Eigen::SparseMatrix<double> &mat,
               const std::vector<Rcc> &rccs,
               int start,
               std::vector<Eigen::Triplet<double> > &triplets
           );

           static void recoverRCCsInEnum(std::vector<Rcc> &rccs,
                                      const std::vector<SequenceInfo> &cols,
                                      Solver &solver);

           RCCCoefficientController() = default;
           ~RCCCoefficientController() = default;
       };
   }

   #include "get_rcc_coefficient.hpp"
   #endif // ROUTE_OPT_RCC_COEFFICIENT_CONTROLLER_HPP

Usage Example
-------------
Below is an example demonstrating how to use the ``RCCCoefficientController`` class to compute
the RCC coefficient matrix and build the enumeration matrix.

.. code-block:: cpp

   #include <vector>
   #include <iostream>
   #include "rcc_coefficient_controller.hpp"
   #include "solver.hpp"

   using namespace RouteOpt::RCCs::CoefficientGetter;

   int main() {
       // Prepare dummy sequence information.
       std::vector<SequenceInfo> seqInfo;
       // Populate seqInfo with relevant data...

       // Define a matrix type (e.g., using Eigen's MatrixXd for a dense matrix).
       Eigen::MatrixXd coeffMatrix;

       // Compute the RCC coefficient matrix.
       // 'if_elementary' flag determines the coefficient formulation.
       RCCCoefficientController::getCoefficientRCC(seqInfo, /*cuts=*/{}, /*if_elementary=*/true, coeffMatrix);

       // Define a sparse matrix for enumeration (with dim-1 rows).
       Eigen::SparseMatrix<double> baseMatrix;
       // Initialize baseMatrix accordingly...

       // Vector to store the enumeration triplets.
       std::vector<Eigen::Triplet<double>> triplets;

       // Build the RCC enumeration matrix with a given starting row index.
       RCCCoefficientController::buildRCCEnuMatrix(baseMatrix, /*rccs=*/{}, /*start=*/0, triplets);

       std::cout << "RCC coefficient matrix computed and enumeration matrix built." << std::endl;
       return 0;
   }

Conclusion
----------
The ``RCCCoefficientController`` module in RouteOpt is essential for computing the coefficient matrix
and constructing the enumeration matrix for Rounded Cap Cuts (RCCs). By providing flexible,
static methods for 3 forms of RCCs, it enables effective integration of RCCs into optimization models.
