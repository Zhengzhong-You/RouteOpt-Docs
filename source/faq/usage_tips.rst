Usage Tips
==========

This section provides useful tips and configurations for efficiently running and customizing RouteOpt, especially for CVRP and VRPTW applications.

1. **Solve Root LP Only**

In ``src/main/src/call_pricing.cpp``, find the function:

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

3. **Update Parameters via Templates**

To conveniently update key parameters, use the provided Python script:

In `RouteOpt/packages/application/cvrp/`, prepare a template file `xxx.txt` (examples in the `templates` folder), and then run:

.. code-block:: bash

    python3 inspect_code.py xxx.txt

This automatically modifies key parameters initialized with braces `{}` in your source code.

**Note:**
Only parameters initialized using `{}` can be modified by this script. Parameters initialized using `=` cannot be changed automatically.
