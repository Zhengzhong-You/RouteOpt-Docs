General Questions
=================

**Q:** Does RouteOpt support non-commercial solvers like SCIP? Are there plans to support it in the future?

**A:** Not yet, but we plan to support SCIP in a future release, probably in the next version. In addition, we may also provide support for other solvers like MindOpt. Currently, RouteOpt supports only Gurobi and CPLEX, with a strong preference for Gurobi due to its excellent performance.

**Q:** Where are parameters defined in RouteOpt?

**A:** They are all defined in files named ``xxx_macro.hpp``. According to their functionality, these macros are divided into several files, including those for pricing, branching, cutting, and more.
