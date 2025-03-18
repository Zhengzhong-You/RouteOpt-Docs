Workflow
=========================================

Overview
--------
The file ``packages/branching/bbt/include/workflow.hpp`` is part of the RouteOpt branching module. It implements the
``solve`` function of the ``BBTController`` class template, which performs a branch-and-bound
tree search to solve the optimization problem. This function processes nodes from the tree,
applies pricing and cutting operations, and utilizes BKF controllers along with branching testers
to determine the best branching candidate. In essence, it drives the exploration of the branch-and-bound
tree until termination criteria are met.

License
^^^^^^^
This software is licensed under **GPL-3.0**.

File Contents
^^^^^^^^^^^^^
The header file ``workflow.hpp`` includes the following key components:

- **Branch-and-Bound Tree Solver**

  - *Function*:

    - **solve(Node *root_node)**:
      Performs the branch-and-bound tree search. It:

      - Adds the root node to the tree and optionally reads additional node information.
      - Iteratively processes nodes by:
        - Removing the first node from the tree.
        - Printing the current tree details.
        - Extracting node values and branching candidate details.
        - Performing pricing and cutting operations, measuring their execution time.
        - Updating branching history and BKF controller information.
        - Determining the best branching candidate via either a custom function or the default tester.
        - Imposing the branching decision to generate child nodes and adding them to the tree.
        - Updating global bounds and bookkeeping for nodes explored.
      - Continues this process until the tree is empty.

Workflow Description
--------------------
The ``solve`` function implements a comprehensive workflow for exploring the branch-and-bound tree:

- **Initialization**:
  The root node is added to the tree, and if available, external node details are read using the
  provided callback.

- **Node Processing Loop**:
  The function enters a loop that continues until no nodes remain in the tree. For each node:

  - **Tree Update**:
    The node is removed from the tree, and the current tree details are printed for monitoring.

  - **Node Evaluation**:
    The node's value and branching candidate information are extracted. Pricing and cutting
    operations are performed on the node, with their execution times measured.

  - **Branching Decision**:
    If the node is still active (i.e., not terminated), the function uses BKF controllers to update
    candidate values, selects the best branching candidate, and updates branching history.

  - **Child Node Generation**:
    The selected branching decision is imposed, generating child nodes that are then added to the tree.
    For each child node, additional BKF updates and external outputs (if configured) are handled.

  - **Cleanup and Bound Update**:
    Terminated nodes are deleted, and the lower bound of the tree is updated based on the remaining nodes.

- **Termination**:
  The loop terminates when the tree is empty, signifying that the branch-and-bound process is complete.

Header Code
--------------------
Below is an excerpt from ``workflow.hpp`` that illustrates the implementation of the ``solve``
function within the ``BBTController`` class template:

.. code-block:: cpp
   :caption: Excerpt from workflow.hpp

   template<typename Node, typename BrCType, typename Hasher>
   void BBTController<Node, BrCType, Hasher>::solve(Node *root_node) {

       if (tryReadNodeIn != nullptr)
           tryReadNodeIn(root_node, branching_history, bkf_data_shared);

       // Add the root node to the tree.
       addNode(root_node);

       while (!tree.empty()) {
           // Select and remove the first node from the tree.
           auto node = *tree.begin();
           tree.erase(node);
           printTreeDetail();

           auto val = valueExtractor(node);
           auto [edge, dir, tree_level] = lastBrcExtractor(node);

           // Perform pricing on the node.
           auto eps = TimeSetter::measure([&]() {
               pricing(node);
           });

           if (!isTerminate(node) && tree_level != 0) {
               branching_history.recordExactPerScore(edge, val, valueExtractor(node), dir, tree_level);
               brcValueOutput(node) = branching_history.tellBranchingIncreaseVal(tree_level);
           }

           // Perform cutting on the node.
           eps += TimeSetter::measure([&]() {
               cutting(node);
           });

           if (!isTerminate(node)) {
               if (tree_level != 0) {
                   if (!bkf_controllers.empty()) {
                       bkf_data_shared.calculateRStar(valueExtractor(node) - val, tree_level, dir,
                                                      idxExtractor(node), bkf_controllers[0]);
                   }
               }

               BrCType brc;
               std::vector<int> bst_ks(bkf_controllers.size());
               for (int i = 0; i < bst_ks.size(); ++i) {
                   bkf_controllers[i].setIfB4(!enuStateExtractor(node));
                   bst_ks[i] = bkf_controllers[i].getBestK(bkf_data_shared, ub_ref.get(), valueExtractor(node));
                   if (i == 0)
                       branching_tester.setNumPhase0(bst_ks[i]);
                   else if (i == 1)
                       branching_tester.setNumPhase1(bst_ks[i]);
                   else if (i == 2)
                       branching_tester.setNumPhase2(bst_ks[i]);
                   else
                       THROW_RUNTIME_ERROR("BKFController only supports 3 phases, but got " + std::to_string(i));
               }

               if (getBestCandidateBySelfDefined) {
                   brc = getBestCandidateBySelfDefined(node, branching_history, branching_data_shared,
                                                       branching_tester);
               } else {
                   brc = branching_tester.getBestCandidate(node, branching_history, branching_data_shared,
                                                           getBranchingCandidates(node));
               }

               if (!bkf_controllers.empty()) {
                   branching_tester.updateBKFtime(eps, bkf_controllers);
                   for (auto &bkf: bkf_controllers) {
                       bkf.updateTimeMeasure(bkf_data_shared);
                   }
                   enuStateExtractor(node) ? bkf_data_shared.increaseNodeAf() : bkf_data_shared.increaseNodeB4();
               }

               ++branching_history.branch_choice[brc];
               std::vector<Node *> children;
               imposeBranching(node, brc, children);

               for (auto &child: children) {
                   if (child != node && tryWriteNodeOut != nullptr) {
                       tryWriteNodeOut(child, branching_history, bkf_data_shared);
                       if (isTerminate(child)) {
                           delete child;
                           continue;
                       }
                   }
                   addNode(child);
                   for (int i = 0; i < bst_ks.size(); ++i) {
                       bkf_controllers[i].updateOptK(bst_ks[i], idxExtractor(child));
                   }
               }
           } else {
               if (!bkf_controllers.empty()) {
                   bkf_data_shared.updateF(ub_ref.get() - valueExtractor(node));
               }
               delete node;
           }
           ++num_nodes_explored;
           updateBounds();
       }
   }

Usage Example
-------------
The following example demonstrates how the ``solve`` function is used within the branch-and-bound
workflow. This example assumes that all necessary callback functions and type definitions have been provided:

.. code-block:: cpp

   #include "workflow.hpp"
   #include <iostream>

   int main() {
       // Assume that a valid root node pointer is obtained and callback functions are defined.
       auto root_node = /* obtain pointer to root node */;

       // Instantiate the BBTController (template parameters omitted for brevity).
       RouteOpt::Branching::BBT::BBTController</* Node */, /* BrCType */, /* Hasher */> bbtController(/* constructor parameters */);

       // Start solving the branch-and-bound tree.
       bbtController.solve(root_node);

       std::cout << "Total nodes explored: " << bbtController.getNumNodesExplored() << std::endl;
       std::cout << "Current tree size: " << bbtController.getNumNodes() << std::endl;
       std::cout << "Current lower bound: " << bbtController.getLowerBound() << std::endl;

       return 0;
   }

Conclusion
----------
The ``workflow.hpp`` header implements the core logic for the branch-and-bound tree search in RouteOpt.
By integrating pricing, cutting, and advanced branching strategies with dynamic updates to the tree structure,
the ``solve`` function enables automatically managing the exploration of the optimization problem space.
