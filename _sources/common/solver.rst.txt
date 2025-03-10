Solver Interface
=========================

Overview
--------
The solver interface of RouteOpt provides a unified abstraction layer for interacting with various optimization solvers
such as Gurobi, CPLEX, and MindOpt (under development). This interface hides the complexity of each backend behind a consistent API,
enabling model creation, updating, optimization, and solution retrieval in a solver-agnostic manner.
The selection of the backend solver is controlled by the ``SOLVER_TYPE`` macro.
Much like the ``route_opt_macro.hpp`` file, this solver interface is a foundational
component utilized across all RouteOpt packages, promoting consistency and modularity throughout the project.

License
^^^^^^^
This software is licensed under **GPL-3.0**.

File Contents
^^^^^^^^^^^^^
The solver interface is organized into several key files:

Shared Files
~~~~~~~~~~~~
- **``packages/common/solver_interface/include/solver_macro.hpp``**

  This header defines macros and utility functions essential for the RouteOpt solver interface. Key components include:

  - **``SOLVER_TYPE``**: A macro that selects the optimization solver backend.
  - **``SAFE_SOLVER``**: A macro that wraps solver API calls to handle errors by printing detailed error messages (including file and line information) and terminating the program if a call fails.

- **``packages/common/solver_interface/include/solver.hpp``**

  This header declares the unified **``Solver``** class, which abstracts the interactions with different optimization solvers. It provides a comprehensive set of methods for:

  - Creating, updating, and deleting models.
  - Adding and removing constraints and variables.
  - Performing optimization (both continuous and mixed-integer programming).
  - Retrieving solution information such as objective values, duals, slacks, and basis details.

  Please refer to the **``Solver``** class documentation for detailed descriptions of each method and its parameters.

Solver-Specific Files (Gurobi Example)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- **``packages/common/solver_interface/include/solver_grb.hpp``**

  This file implements the solver interface for Gurobi. It maps generic solver types and constants to the corresponding Gurobi C API constructs. Notable mappings include:

  - **Type Aliases**:

    - ``SOLVERmodel`` is defined as **``GRBmodel``**.
    - ``SOLVERenv`` is defined as **``GRBenv``**.

  - **Solver Constants**:

    - Constants such as **``SOLVER_EQUAL``**, **``SOLVER_GREATER_EQUAL``**, **``SOLVER_BINARY``**, etc., are mapped to the Gurobi-specific API values.

  - **Status Codes and Methods**:

    - Definitions for solver status codes like **``SOLVER_OPTIMAL``**, **``SOLVER_MIP_INFEASIBLE``**, etc., are provided to interpret the results of optimization calls.

Usage Example
-------------
Below is an example illustrating how to use the unified solver interface in RouteOpt:

.. code-block:: cpp

    #include <iostream>
    #include "solver.hpp"

    int main() {
        // Create a Solver instance.
        RouteOpt::Solver solver{};

        // Load the solver environment.
        SAFE_SOLVER(solver.loadEnv(nullptr))

        // Create a new optimization model.
        // (Assuming numVars, obj, lb, ub, vtype, and varnames are defined appropriately.)
        int status = solver.newModel("MyModel", numVars, obj, lb, ub, vtype, varnames);
        if (status != 0) {
            std::cerr << "Error creating model." << std::endl;
            return status;
        }

        // Alternatively, you can use SAFE_SOLVER to automatically check for errors.
        SAFE_SOLVER(solver.newModel("MyModel", numVars, obj, lb, ub, vtype, varnames));

        // Optimize the model.
        status = solver.optimize();
        if (status != 0) {
            std::cerr << "Error during optimization." << std::endl;
            return status;
        }

        // Alternatively, you can use SAFE_SOLVER to automatically check for errors.
        SAFE_SOLVER(solver.optimize());

        // Retrieve and display the optimal objective value.
        double objVal;
        status = solver.getObjVal(&objVal);
        if (status == 0) {
            std::cout << "Optimal objective value: " << objVal << std::endl;
        } else {
            std::cerr << "Error retrieving objective value." << std::endl;
        }

        // Alternatively, you can use SAFE_SOLVER to automatically check for errors.
        SAFE_SOLVER(solver.getObjVal(&objVal));

        // Clean up resources.
        SAFE_SOLVER(solver.freeModel());
        SAFE_SOLVER(solver.freeEnv());

        return 0;
    }

Conclusion
----------
The RouteOpt solver interface encapsulates the complexities of different optimization solvers behind a unified API.
This design allows for easy switching between solver backends by simply modifying the ``SOLVER_TYPE`` macro,
without requiring changes to the core application logic. Consequently,
RouteOpt maintains flexibility and robustness across various optimization environments.


Further Reading
---------------
For additional details, refer to the official documentation of the respective solvers:

- **Gurobi C API Documentation**:
  `Gurobi C API Reference <https://www.gurobi.com/documentation/current/refman/c_api_overview.html>`_

- **IBM ILOG CPLEX Optimization Studio C API Documentation**:
  `CPLEX C API Documentation <https://www.ibm.com/docs/en/cofz/12.10.0?topic=v12100-cplex-callable-library-c-api-reference-manual>`_

- **MindOpt C API Documentation**:
  `MindOpt C API Documentation <https://opt.aliyun.com/doc/latest/en/html/testing/compile-c.html>`_
