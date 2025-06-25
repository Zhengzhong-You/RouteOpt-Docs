DeLuxing
====================

Introduction
---------------

Deep Lagrangian Underestimate Fixing (**DeLuxing**, :cite:p:`yang2024deluxing`) is a variable-fixing strategy designed for
column-generation (CG)-based exact methods in discrete optimization. It aims to remove unnecessary 
variables from large enumerated pools by leveraging linear programming (LP) dual solutions, thereby 
reducing problem size and significantly speeding up solver performance.


DeLuxing Controller Header Code and Parameters
--------------------------------------------------

.. code-block:: cpp

    /*
     * Copyright (c) 2025 Yu Yang & Zhengzhong (Ricky) You.
     * All rights reserved.
     * Software: RouteOpt
     * License: GPL-3.0
     *
     * @file deluxing.hpp
     * @brief Header file for the DeLuxingController class.
     *
     * This header defines the DeLuxingController class, which is used to perform the DeLuxing algorithm
     * to reduce the number of enumerated columns.
     */

    #ifndef ROUTE_OPT_DELUXING_HPP
    #define ROUTE_OPT_DELUXING_HPP

    #include <vector>
    #include "solver.hpp"

    namespace RouteOpt::DeLuxing {
        class DeLuxingController {
        public:
            static void deLuxing(Solver &solver, double UB, int NClust, int beta1, int beta2, std::vector<int> &Idxdel,
                                 double Timelimit,
                                 double Tolerance, bool Verbose);
        };
    }

    #endif

**Parameters**:

- ``UB``: Upper bound on the objective value (often from a known feasible solution).  
- ``NClust``: Number of clusters for grouping columns (variables).  
- ``beta1, beta2``: Thresholds controlling the aggressiveness of variable removal.  
- ``Idxdel``: A vector that returns the indexes of deleted (fixed) variables.  
- ``Timelimit``: Maximum allowed runtime for the procedure.  
- ``Tolerance``: A small value to handle floating-point comparisons when fixing variables.  
- ``Verbose``: If true, prints additional logs about the process.  

Example of Usage
----------------------
.. code-block:: cpp

    #include "deluxing.hpp"
    #include "solver.hpp"

    using namespace RouteOpt::DeLuxing;

    int main() {
        Solver solver;
        double UB = 100.0; // Example upper bound
        int NClust = 20; // Number of clusters
        int beta1 = 1000; // Threshold for variable removal
        int beta2 = 1000; // Another threshold for variable removal
        std::vector<int> Idxdel; // Vector to store deleted variable indexes
        double Timelimit = 3600.0; // 1 hour time limit
        double Tolerance = 1e-6; // Tolerance for floating-point comparisons
        bool Verbose = true; // Enable verbose output

        DeLuxingController::deLuxing(solver, UB, NClust, beta1, beta2, Idxdel, Timelimit, Tolerance, Verbose);

        return 0;
    }

Further Reading
------------------

For more detailed information, please refer to:

.. bibliography::
   :filter: key in {"yang2024deluxing"}

