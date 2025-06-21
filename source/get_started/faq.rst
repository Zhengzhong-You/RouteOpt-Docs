FAQ
===

**Q**: Does RouteOpt support some non-commercial solvers like SCIP now? Or do you have plans to support it in the future?

**A**: Not yet, but we are planning to support it in a future release, probably in the next version. By then, we will also likely provide support for other solvers like MindOpt. Currently, RouteOpt supports only Gurobi and CPLEX, with a strong preference for Gurobi due to its performance.

**Q**: Where are parameters defined in RouteOpt?

**A**: They are all in `xxx_macro.hpp` files. According to their functionality, they are divided into several files, including pricing, branching, and others.
