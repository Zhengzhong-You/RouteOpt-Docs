Usage Tips
==========

This section provides useful tips and configurations for efficiently running and customizing RouteOpt, especially for CVRP and VRPTW applications.

1. **Solve Root LP Only**

In ``src/main/src/call_pricing.cpp``, locate the function:

.. code-block:: cpp

    void CVRPSolver::callPricingAtBeg(BbNode *node) {
        // Original function code here

        // Add the following line at the end to disable branching after root LP
        node->refIfTerminate() = true;
    }


2. **Disable Cutting**

In ``src/main/src/call_cutting.cpp``, find the function:

.. code-block:: cpp

    void CVRPSolver::callCutting(BbNode *node) {
        // Add the following line at the very beginning of this function to disable cutting
        return;

        // Original function code follows...
    }
