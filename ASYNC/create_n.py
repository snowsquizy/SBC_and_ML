#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  create.py
#
#  Copyright 2017 Andrew Taylor <andrew@snowsquizy.id.au>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; version 3.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
""" Library Imports """
# Tensorflow
import tensorflow as tf
# For timing each run
import timeit
# For absolute Time
import time


def create_layers(
        b_dim,
        place_holder):
    """
    Create the Layers for the Neural Network
    Args:
        b_dim (int) : Board dimension along one side
        placeholder (obj) : tf.random_normal method
    Returns:
        W0 (tensor) : Input Layer random Weights
        W1 (tensor) : Hidden Layer random weights
        W2 (tensor) : Output Layer random weights
        b0 (tensor) : Input Layer zero Biases
        b1 (tensor) : Hidden Layer zero Biases
        b2 (tensor) : Output Layer zero Biases
        x (tensor) : Input data placeholder
        y_ (tensor) : Output data placeholder
        y (tensor) : Calculated Neural Network Output (softmax)
        z0 (tensor) : Input multiplied by input weights and biases layer
        z1 (tensor) : input weights & biases multiplied by hidden layer
        z2 (tensor) : hidden weights & biases multiplied by output layer
        a0 (tensor) : input layer multiplied by activation function
        a1 (tensor) : hidden layer multiplied by activation function
    """
    # Create Placeholder Variable for input
    x = tf.placeholder(tf.float32, [None, b_dim*b_dim])
    # Create Place holder for output
    y_ = tf.placeholder(tf.float32, [None, 3])

    # Create Random Weights for each Layer for starting
    W0 = tf.Variable(place_holder([b_dim * b_dim, 12], 0, 0.3))
    W1 = tf.Variable(place_holder([12, 12], 0, 0.3))
    W2 = tf.Variable(place_holder([12, 3], 0, 0.3))
    # Create zero value Biases for each Layer for starting
    b0 = tf.Variable(tf.zeros([12]))
    b1 = tf.Variable(tf.zeros([12]))
    b2 = tf.Variable(tf.zeros([3]))
    # Setup the Neural Network
    z0 = tf.nn.xw_plus_b(x, W0, b0)
    a0 = tf.nn.tanh(z0)
    z1 = tf.nn.xw_plus_b(a0, W1, b1)
    a1 = tf.nn.tanh(z1)
    z2 = tf.nn.xw_plus_b(a1, W2, b2)
    y = tf.nn.softmax(z2)
    # Return Variables
    return W0, W1, W2, b0, b1, b2, x, y_, y, z0, z1, z2, a0, a1


def train_network(
    sess,
    g_b,
    t_epochs,
    t_cl,
    accuracy,
    x,
    y_,
    n_bs,
    n_train,
    train_step,
    cross_entropy,
    u_cluster,
    global_step,
        preset_accu):
    """
    Train the Neural Network
    args:
        sess (obj) : tf session object
        g_b (obj) [] : Game boards object (train, valid, test)
        t_epoch (int) : Number of training epochs
        t_cl (boolean) : Displays debugging code
        accuracy (obj) : tf Accuracy operation
        x (tensor) : Input data placeholder
        y_ (tensor) : Output data Label placeholder
        n_bs (int) : batch size
        n_train (int) : total number of game boards for training
        train_step (obj) : tf Training operation
        cross_entropy (obj) : tf Cross Entropy calculation
        u_cluster (boolean) : Whether to use cluster or CPU/GPU
        global_step (obj) : tf tracking training steps across multiple devices
        preset_accu (float) : Preset Accuracy calculation for timing
    Returns:

    """
    batch_xs = []
    batch_ys = []
    cost_hist = []
    accu_hist = []
    time_hist = []
    curr_c = 0
    curr_a = 0
    count = 0
    start_time = time.time()
    end_time = 0
    for a in range(t_epochs):
        if (t_cl):
            # Display Current Progress
            print("Epoch: %d" % (a+1))
        timer1 = timeit.default_timer()
        # Process Batches of training Data
        for i in range(0, n_train-1, n_bs):
            batch_xs = g_b.x_train[i:i+n_bs]
            batch_ys = g_b.y_train[i:i+n_bs]
            if u_cluster:
                _, step = sess.run(
                    [train_step, global_step],
                    feed_dict={x: batch_xs, y_: batch_ys})
            else:
                sess.run(
                    [train_step],
                    feed_dict={x: batch_xs, y_: batch_ys})
                count += 1
        # Run Accuracy Test on Neural Network
        curr_a = sess.run(
            accuracy,
            feed_dict={x: g_b.x_valid, y_: g_b.y_valid})
        if (curr_a >= preset_accu):
            end_time = time.time()
            break
        # Determine Time for epoch and add to History
        time_hist.append(timeit.default_timer()-timer1)
        # Determine Cost for epoch and add to History
        cost_hist.append(curr_c)
        # Determine Accuracy for epoch  and add to History
        accu_hist.append(curr_a)
        if (t_cl):
            # Display current Metrics
            print("Time : {0:0.4f}".format(time_hist[-1]))
            # print("Cost : {0:0.4f}".format(cost_hist[-1]))
            print("Accu : {0:0.4f}".format(accu_hist[-1]))
        # else:
        #     if ((a+1) % 5 == 0):
        #         print("Time : {0:0.4f}".format(time_hist[-1]))
        #         print("Cost : {0:0.4f}".format(cost_hist[-1]))
        #         print("Accu : {0:0.4f}".format(accu_hist[-1]))
    # Close tensorflow Session
    final_accu = sess.run(
        accuracy,
        feed_dict={x: g_b.x_test, y_: g_b.y_test})
    sess.close()
    return {"accu": accu_hist,
            "time": time_hist,
            "fa": final_accu,
            "st": start_time,
            "et": end_time}


class neural_network:
    """
    Neural Network Object
    """

    def __init__(
            self,
            g_b,
            b_dim,
            n_train,
            n_valid,
            n_test,
            t_epochs,
            n_bs,
            t_cl,
            u_cpu,
            u_cluster,
            p_server,
            workers,
            node,
            preset_accu,
            cluster,
            server):
        """
        Class Constructor for Neural Network
        Args:
            g_b[] (boards) : Game boards used for training Neural Network.
            b_dim (int) : Board Side Dimensions.
            n_train (int) : Number of Boards to use for training.
            n_valid (int) : Number of Boards to use for Validation.
            n_test (int) : Number of Boards to use for Testing.
            t_epochs (int) : Number of testing epochs.
            n_bs (int) : batch size used for training.
            t_cl (boolean) : Whether to Display Debug Code.
            u_cpu (boolean) : Whether to use CPU or GPU.
            u_cluster (boolean) : Whether to use cluster or single CPU.
            p_server (string)[] : Parameter servers IP and Port Numbers
            workers (string)[] : Workers IP and port Numbers
            node (obj)[] : Type and index of hardware.
            preset_accu (float) : Accuracy Value used for timing
            cluster (obj) [] : The tf object defining all hardware
            server (obj) [] : The tf distributed hardware setup
        Returns:
            none.
        """
        tf.reset_default_graph()
        # Commence timer
        start_time = timeit.default_timer()
        # Total Time
        self.t_time = []
        # Board Dimensions
        self.dim = b_dim
        # Variable creation
        place_holder = tf.random_normal
        if u_cluster:
            if t_cl:
                print("***     Worker      ****")
            with tf.device(tf.train.replica_device_setter(
                worker_device="/job:worker/task:{}".format(node[1]),
                # ps_device="/job:ps/cpu:0",
                ps_strategy=tf.contrib.training.GreedyLoadBalancingStrategy(
                    len(p_server), tf.contrib.training.byte_size_load_fn),
                # merge_devices=True,
                    cluster=cluster)):
                """
                ps_tasks=len(p_server),
                ps_device="/job:ps",
                merge_devices=True,
                worker_device="/job:worker/task:{}".format(node[1]),
                ps_strategy=tf.contrib.training.GreedyLoadBalancingStrategy(
                    2, tf.contrib.training.byte_size_load_fn),
                """
                global_step = tf.Variable(
                    0, name="global_step", trainable=False)
                [W0, W1, W2, b0, b1, b2, x, y_, y,
                    z0, z1, z2, a0, a1] = create_layers(
                    b_dim,
                    place_holder)

        else:
            if not u_cpu:
                with tf.device("/gpu:1"):
                    [W0, W1, W2, b0, b1, b2, x,
                        y_, y, z0, z1, z2, a0, a1] = create_layers(
                        b_dim,
                        place_holder)
            else:
                [W0, W1, W2, b0, b1, b2, x, y_, y,
                    z0, z1, z2, a0, a1] = create_layers(
                    b_dim,
                    place_holder)
        # this is our cost
        cross_entropy = tf.reduce_mean(
            -tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        # Training Steps Setup
        grad_op = tf.train.AdamOptimizer()
        if u_cluster:
            train_step = grad_op.minimize(
                cross_entropy,
                global_step=global_step)
        else:
            train_step = grad_op.minimize(
                cross_entropy)
        # Correct Prediction of board winner
        correct_prediction = tf.equal(
            tf.argmax(y, 1), tf.argmax(y_, 1))
        # Accuracy Calculation
        accuracy = tf.reduce_mean(
            tf.cast(correct_prediction, tf.float32))
        init = tf.global_variables_initializer()
        if t_cl:
            print("Variables initialized ...")

        if u_cluster:
            sv = tf.train.Supervisor(
                is_chief=(node[1] == 0),
                global_step=global_step,
                logdir="/tmp/logdir",
                recovery_wait_secs=1,
                init_op=init)
            sess_config = tf.ConfigProto(
                allow_soft_placement=True,
                log_device_placement=False,
                device_filters=[
                    "/job:ps", "/job:worker/task:{}".format(node[1])])
            with sv.prepare_or_wait_for_session(
                server.target,
                    config=sess_config) as sess:
                result = train_network(
                    sess,
                    g_b,
                    t_epochs,
                    t_cl,
                    accuracy,
                    x,
                    y_,
                    n_bs,
                    n_train,
                    train_step,
                    cross_entropy,
                    u_cluster,
                    global_step,
                    preset_accu)
        else:
            global_step = 0
            # Create a Tensorflow Session
            sess = tf.Session()
            # Add global variables to Session
            sess.run(init)
            result = train_network(
                sess,
                g_b,
                t_epochs,
                t_cl,
                accuracy,
                x,
                y_,
                n_bs,
                n_train,
                train_step,
                cross_entropy,
                u_cluster,
                global_step,
                preset_accu)

        self.accu_hist = result["accu"]
        self.time_hist = result["time"]
        self.final_accu = result["fa"]
        self.start_time = result["st"]
        self.end_time = result["et"]
        if (t_cl):
            print("Final Accuracy {0:0.4f}".format(self.final_accu))
        self.t_time = timeit.default_timer() - start_time
