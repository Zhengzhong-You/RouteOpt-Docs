Install
=======

This guide is for building RouteOpt on Linux only.

Prerequisites
-------------
Before proceeding, ensure you have the following installed:

- A C/C++ compiler.
- **Ninja** build system. Install it using:

  .. code-block:: bash

      sudo apt-get install ninja-build

  Ninja is used (for example, with Xgboost).

- **Gurobi**: Make sure Gurobi is installed and note its installation path. This path will be used in the following steps.
  **Important**: Enter the full path to the Linux64 folder (e.g., ``/home/yzz/gurobi1000/linux64``), not just the parent directory.

Installation Steps
------------------
1. **Clone the Repository**
   Open a terminal and run:

   .. code-block:: bash

      git clone https://github.com/Zhengzhong-You/RouteOpt.git

2. **Change Directory**
   Navigate to the cloned repository:

   .. code-block:: bash

      cd RouteOpt

3. **Build RouteOpt**
   Run the build script:

   .. code-block:: python

      python build.py

4. **Specify Gurobi Path**
   When prompted, enter the full path to your Gurobi installation, for example:

      /home/yzz/gurobi1000/linux64

5. **Build RouteOpt**
   The build process may take about 3 minutes to complete. Once finished, you should see the message:

   ``Build process completed successfully.``

   This indicates that all packages have been built successfully.

Building CVRP or TW Solver
---------------------------
If you want to use our CVRP or TW solver:

1. Change directory to the application package:

   .. code-block:: bash

      cd packages/application/cvrp

2. Run the build script:

   .. code-block:: bash

      sh build.sh

3. The script will compile the CVRP or TW solver and run a small test instance (P-n20-k2.vrp). If the test succeeds, you are all set!

Build Your Own Solver
----------------------

After completing the build steps, dependencies are already installed, allowing you to create your own solver utilizing packages provided by RouteOpt. To accomplish this, you need to configure your own CMake project.

The following dependencies are required and also already installed, so you only need to link them in your CMake project:

- **Boost** (header-only; include directories required)
- **Eigen** (header-only; include directories required)
- **CVRPSEP** (include directories and libraries)
- **Gurobi** (include directories and libraries)
- **XGBoost** (include directories and libraries)

You can integrate the following packages into your CMake project:

- **external**: External packages required by RouteOpt

  (added via: ``add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../external external_build)``)
- **common**: Shared utilities and include files

  (added via: ``add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../common common_build)``)
- **branching**: Branching strategies

  (added via: ``add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../branching branching_build)``)
- **rounded_cap_cuts**: Packages for rounded cap cuts

  (added via: ``add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../rounded_cap_cuts rcc_build)``)
- **rank1_cuts**: Packages for rank1 cuts

  (added via: ``add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../rank1_cuts rank1_cuts_build)``)

Include the following directories and libraries in your CMake project configuration:

.. code-block:: cmake

    include_directories(
        ${BOOST_INCLUDE_DIRS}       # Boost include directories
        ${EIGEN_INCLUDE_DIRS}       # Eigen include directories
        ${CVRPSEP_INCLUDE_DIRS}
        ${GUROBI_INCLUDE_DIRS}
        ${XGB_INCLUDE_DIRS}
        # Additional directories can be included as needed
    )

    # Link external libraries to the project
    target_link_libraries(${PROJECT_NAME}
        PRIVATE
        COMMON_INCLUDES
        BRANCHING_INCLUDES
        ROUNDED_CAP_CUTS_INCLUDES
        RANK1_CUTS_INCLUDES
        ${GUROBI_LIBRARIES}
        ${CVRPSEP_LIBRARIES}
        ${XGB_LIBRARIES}
        ${HGS_LIBRARIES}
        # Additional libraries can be linked as needed
    )

Once these steps are completed, your solver is successfully configured.

CMake Configuration Example
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below is a complete example of a ``CMakeLists.txt`` file configuring a CVRP application using RouteOpt packages:

.. code-block:: cmake

    cmake_minimum_required(VERSION 3.10)
    project(cvrp VERSION 3.0)

    set(CMAKE_CXX_STANDARD 17)
    set(CMAKE_CXX_STANDARD_REQUIRED ON)

    if (NOT CMAKE_BUILD_TYPE)
        set(CMAKE_BUILD_TYPE Release)
    endif ()

    option(ENABLE_VALGRIND_MEM_CHECK "Enable Valgrind Memory Check" OFF)

    if (ENABLE_VALGRIND_MEM_CHECK)
        add_compile_definitions(VALGRIND_MEM_CHECK)
    endif ()

    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/bin)

    # Add subdirectories for external packages and common utilities
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../external external_build)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../common common_build)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../branching branching_build)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../rounded_cap_cuts rcc_build)
    add_subdirectory(${CMAKE_CURRENT_SOURCE_DIR}/../../rank1_cuts rank1_cuts_build)

    # Extend the CMake module path if needed
    list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/lib/cmake_modules")

    # Find required packages
    find_package(HGS REQUIRED)
    find_package(ZLIB REQUIRED)

    # Include directories for external dependencies (Boost and Eigen are header-only)
    include_directories(
        ${BOOST_INCLUDE_DIRS}       # Boost include directories
        ${EIGEN_INCLUDE_DIRS}       # Eigen include directories
        ${CVRPSEP_INCLUDE_DIRS}
        ${GUROBI_INCLUDE_DIRS}
        ${XGB_INCLUDE_DIRS}
        ${HGS_INCLUDE_DIRS}
    )

    # Project-specific include directories
    include_directories(
        ${CMAKE_CURRENT_SOURCE_DIR}/src/main/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/vrptw/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/add_column/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/cuts/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/pricing/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/l2b/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/read_data/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/heuristics/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/initial/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/node/include
        ${CMAKE_CURRENT_SOURCE_DIR}/src/two_stage/include
    )

    # Gather source files
    file(GLOB_RECURSE CVRP_SOURCES
        ${CMAKE_CURRENT_SOURCE_DIR}/src/main/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/vrptw/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/add_column/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/cuts/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/pricing/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/l2b/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/read_data/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/heuristics/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/initial/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/node/src/*.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp
        ${CMAKE_CURRENT_SOURCE_DIR}/src/two_stage/src/*.cpp
    )

    # Create the executable target
    add_executable(${PROJECT_NAME} ${CVRP_SOURCES})

    # Link external libraries to the project
    target_link_libraries(${PROJECT_NAME}
        PRIVATE
        COMMON_INCLUDES
        BRANCHING_INCLUDES
        ROUNDED_CAP_CUTS_INCLUDES
        RANK1_CUTS_INCLUDES
        ${GUROBI_LIBRARIES}
        ${CVRPSEP_LIBRARIES}
        ${XGB_LIBRARIES}
        ${HGS_LIBRARIES}
        ZLIB::ZLIB
    )


Conclusion
----------
After following these steps, RouteOpt and all required packages should be built successfully.
Enjoy optimizing your routing problems with RouteOpt!
