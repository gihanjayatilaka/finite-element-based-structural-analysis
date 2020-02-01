# Finite Element Based Structural Analysis


## Introduction ##
This is an attempt to implement a CLI tool for the following paper.

*M.C.M. Rajapakse, K.K. Wijesundara, R. Nascimbene, C.S. Bandara, R. Dissanayake, **Accounting axial-moment-shear interaction for force-based fiber modeling of RC frames, Engineering Structures**, Volume 184, 2019, Pages 15-36,ISSN 0141-0296,
https://doi.org/10.1016/j.engstruct.2019.01.075.*


**People:** [Gihan Jayatilaka](https://gihan.me), [Suren Sritharan](https://github.com/suren3141) and [Harshana Weligampola](https://github.com/harshana95)

**Advised by:** [Dr. Kushan Wijesundara](http://eng.pdn.ac.lk/civil/people/drKKWijesundara.php) and [Dr. Janaka Alawathugoda](http://www.ce.pdn.ac.lk/academic-staff/janaka-alawatugoda/)


## Project summary ##
[**Project Report**](https://github.com/gihanjayatilaka/finite-element-based-structural-analysis/blob/dev/Documentation/CO328-project-report.pdf), [**Project Presentation**](https://github.com/gihanjayatilaka/finite-element-based-structural-analysis/blob/dev/Documentation/CO328-project-presentation.pdf)

* Civil engineering structure modelling
  * Elementwise local stiffness matrix calculation generation.
  * Structure's global stiffnexx matrix calculation.
  * Load matrix generation.
* Lieanr system oprations.
  * Linear system representation : dense and sparse
  * Linear system solving: Gauss ellimination on dense and sparse matrices, iterative numerical techniques.
* Backtracking to translate the linear system solution to civil engineering structure.

The main objective of this project was to find the **time and memroy efficient** way of computing the results.


## Please note ##
This work was done as a partial requirement for [CO328 Software Engineering](http://www.ce.pdn.ac.lk/undergraduate-courses/)) course. **This implementation consists of the linear elastic region analysis only.**


This work will be continued by at [https://github.com/pubuduudara/finite-element-based-structural-non-linear-analysis/](https://github.com/pubuduudara/finite-element-based-structural-non-linear-analysis/). Please contact [pubuduudara7@gmail.com](pubuduudara7@gmail.com) if the repository is private. Their work **might** have backward compatibility for input format but they will **not** be using the code from this project.
