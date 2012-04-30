# Constraint SVC metamodel experiments

15+100 EA with tangent constraint on sphere function, best fitness is minimum. A local SVC metamodel is used to approximate the tangent constraint. These experiments only use the default (sklearn-svc) C and gamma values for the SVC parameterization. In the following different metamodel integration approaches have been tested.

## Experiment A

![plot](http://i.imgur.com/1tDcW.png)

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 20 samples per method. Methods: WithoutMetaModel with Death Penalty and SVCBestWeighted with beta = 0.5.

## Experiment B

![plot](http://i.imgur.com/YDQLJ.png)

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 50 samples per method. Methods: WithoutMetaModel with Death Penalty and SVCSlidingWeighted with Sliding Window Size = 50 and SVCBestWeighted with beta = 0.5.

## Experiment C 

![plot](http://i.imgur.com/qyam0.png)

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 200 samples per method. Methods: WithoutMetaModel with Death Penalty and SVCSlidingWeighted with Sliding Window Size = 50, beta = 0.5 and SVCBestWeighted with beta = 0.5.

## Experiment D 

![plot](http://i.imgur.com/DalKj.png)

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 200 samples per method. Methods: WithoutMetaModel with Death Penalty and SVCSlidingWeighted with Sliding Window Size = 50, beta = 0.75 and SVCBestWeighted with beta = 0.75.

## Experiment E 

![plot](http://i.imgur.com/zlQDp.png)

15+100 EA with tangent constraint on sphere function, best fitness is minimum. 200 samples per method. Methods: WithoutMetaModel with Death Penalty and SVCSlidingWeighted with Sliding Window Size = 50, beta = 0.90 and SVCBestWeighted with beta = 0.90.


