Usage Tips
==========

This section provides useful tips and configurations for efficiently running and customizing RouteOpt, especially for CVRP and VRPTW applications.

1. **Solve Root LP Only**

In ``src/main/src/call_pricing.cpp``, locate the function:

.. code-block:: cpp

    void CVRPSolver::callPricingAtBeg(BbNode *node) {
        setEnv(node);
        if constexpr (ml_type == ML_TYPE::ML_GET_DATA_1 || ml_type == ML_TYPE::ML_GET_DATA_2) {
            GetTrainingData<BbNode, std::pair<int, int>, PairHasher>::checkIfStopGeneratingData(
                node->getTreeSize(), node->refIfTerminate());
            if (node->getIfTerminate()) return;
        }
        double eps;
        callPricing(node, std::numeric_limits<float>::max(), eps);
        if (node->getIfRootNode() && app_type == APPLICATION_TYPE::VRPTW)
            augmentNGRound(node, pricing_controller.refNG());

        // Add the following line here to disable branching after root LP
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
