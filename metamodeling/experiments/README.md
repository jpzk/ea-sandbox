# SVC metamodel experiments

15+100 EA with tangent constraint on sphere function, best fitness is minimum. A local SVC metamodel is used to approximate the tangent constraint. Before n-fold crossvalidation, training and testing standardscore scaling is applied. N-fold crossvalidation is used on the best fitness feasibles and infeasibles for feature selection and parameter C and gamma adjustment. RBF kernel is used. In the following different approaches have been tested.

## Constant stepsize

![](http://i.imgur.com/qsUJh.png)

![](http://i.imgur.com/RfuIp.png)
