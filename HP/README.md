# Hyper Parameter Sweep Code

A Hyper Parameter sweep is used to determine the most efficient Artificial Neural Network setup by sweeping a range of layers and neuron values.  This is done for a fixed number of training epochs with the time taken and the final accuracy noted.

This code will run the 54 different hyper parameter combinations with the XX being replaced by the number of Raspberry Pi clusters to use.  On the Desktop and the K40 set the XX to 1 to run through the list sequentially.
```shell
parallel -j XX project {} {} {} ::: 1 2 3 ::: 9 18 27 36 45 54 63 72 81 ::: tanh sigmoid
``` 
