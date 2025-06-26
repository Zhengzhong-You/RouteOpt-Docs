Troubleshooting
===============

This section addresses common issues encountered when using the CVRP solver and provides solutions.

Memory Allocation Error
-----------------------

**Issue**:

When running the CVRP solver test instance (e.g., ``P-n20-k2.vrp``), a fatal memory allocation error occurs, despite successful compilation:

.. code-block:: console

   [FATAL ERROR] Label assigned=8000000 failed in reallocateLabel. Not enough memory.

**Cause**:

The default setting for ``LABEL_ASSIGN`` (8,000,000) is designed for systems with large memory (e.g., 128 GB RAM). On systems with lower memory, this value leads to allocation errors.

**Solution**:

Reduce the ``LABEL_ASSIGN`` parameter to match your system’s available RAM:

1. Open the file:

   .. code-block:: bash

      packages/application/cvrp/src/pricing/include/pricing_macro.hpp

2. Modify ``LABEL_ASSIGN``:

   .. code-block:: cpp

      constexpr int LABEL_ASSIGN = 800000; // Example value; adjust according to your RAM capacity

3. Rebuild the solver:

   .. code-block:: bash

      cd packages/application/cvrp
      sh build.sh

This adjustment should resolve the issue, allowing the solver to run successfully.
