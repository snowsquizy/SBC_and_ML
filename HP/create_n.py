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
        W,
        b,
        n_lay,
        n_neurons,
        b_dim,
        place_holder,
        matmul,
        act_1,
        act_0):
    """
    Create the Layers for the Neural Network
    """
    # Create Random Weights and Biases for each Layer for starting
    for a in range(0, n_lay+1):
        layer_name = "layer{}".format(a)
        with tf.name_scope(layer_name):
            if (a == 0):
                W.append(
                    tf.Variable(place_holder([n_neurons, 3], 0, 0.5)))
                b.append(
                    tf.Variable(place_holder([3], 0, 0.5)))
            elif (a == n_lay):
                W.append(
                    tf.Variable(place_holder(
                        [b_dim * b_dim, n_neurons], 0, 0.5)))
                b.append(
                    tf.Variable(place_holder([n_neurons], 0, 0.5)))
            else:
                W.append(
                    tf.Variable(place_holder([n_neurons, n_neurons], 0, 0.5)))
                b.append(
                    tf.Variable(place_holder([n_neurons], 0, 0.5)))
    # Create Placeholder Variable for input
    x = tf.placeholder(tf.float32, [None, b_dim*b_dim])
    # Create Place holder for output
    y_ = tf.placeholder(tf.float32, [None, 3])
    # Create the Layers and Neurons
    for k in range(n_lay, -1, -1):
        if (k == n_lay):
            y = act_1(matmul(x, W[k]) + b[k])
        elif (k == 0):
            y = act_0(matmul(y, W[k]) + b[k])
        else:
            y = act_1(matmul(y, W[k]) + b[k])
    return W, b, x, y_, y


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
    summary_op,
    results_directory,
    u_cluster,
    global_step,
        preset_accu):
    """
    Train the Neural Network
    """
    # Placeholders for history plots
    batch_xs = []
    batch_ys = []
    cost_hist = []
    accu_hist = []
    time_hist = []
    curr_c = 0
    # curr_a = 0
    writer = tf.summary.FileWriter(
        results_directory+"/",
        graph=tf.get_default_graph())
    count = 0
    start_time = time.time()
    end_time = 0
    for a in range(t_epochs):
        timer1 = timeit.default_timer()
        # Process Batches of training Data
        for i in range(0, n_train-1, n_bs):
            batch_xs = g_b.x_train[i:i+n_bs]
            batch_ys = g_b.y_train[i:i+n_bs]
            if u_cluster:
                _, curr_c, summary, step = sess.run(
                    [train_step, cross_entropy, summary_op, global_step],
                    feed_dict={x: batch_xs, y_: batch_ys})
                writer.add_summary(summary, step)
            else:
                _, curr_c, summary = sess.run(
                    [train_step, cross_entropy, summary_op],
                    feed_dict={x: batch_xs, y_: batch_ys})
                writer.add_summary(summary, count)
                count += 1
        time_hist.append(timeit.default_timer()-timer1)
        # Determine Cost for epoch and add to History
        cost_hist.append(curr_c)
    # Close tensorflow Session
    end_time = time.time()
    final_accu = sess.run(
        accuracy,
        feed_dict={x: g_b.x_valid, y_: g_b.y_valid})
    sess.close()
    return {"cost": cost_hist,
            "accu": accu_hist,
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
            n_act,
            b_team,
            n_train,
            n_valid,
            n_test,
            n_lay,
            n_neurons,
            t_epochs,
            n_bs,
            t_cl,
            u_cpu,
            u_cluster,
            p_server,
            workers,
            node,
            results_directory,
            preset_accu,
            cluster,
            server):
        """
        Class Constructor for Neural Network
        Args:
            g_b[] (boards) : Game boards used for creating Neural Network.
            b_dim (int) : Board Side Dimensions.
            n_act (str) : Activation Function.
            b_team[] (str) : Team Identifiers.
            n_train (int) : Number of Boards to use for training.
            n_valid (int) : Number of Boards to use for Validation.
            n_test (int) : Number of Boards to use for Testing.
            n_lay (int) : Number of Neural Network layers.
            n_neurons (int) : Number of Neurons per layer.
            t_epochs (int) : Number of testing epochs.
            n_bs (int) : batch size used for training.
            t_cl (boolean) : Whether to Display Debug Code.
            u_cpu (boolean) : Whether to use CPU or GPU.
            u_cluster (boolean) : Whether to use cluster.
            p_server (string)[] : Parameter servers IP and Port Numbers
            workers (string)[] : Workers IP and port Numbers
            FLAGS (obj) : Type and index of hardware.
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
        # x training data
        # Weights
        self.W = []
        # Biases
        self.b = []
        # tensorflow matric multiplication
        matmul = tf.matmul
        # Softmax Regression Neural Network
        act_0 = tf.nn.softmax
        # Variable creation
        place_holder = tf.random_normal
        # setup Activation function for Layers
        if (n_act == "tanh"):
            act_1 = tf.tanh
        elif (n_act == "relu"):
            act_1 = tf.nn.relu
        elif (n_act == "sigmoid"):
            act_1 = tf.sigmoid
        if u_cluster:
            if t_cl:
                print("***     Worker      ****")
            with tf.device(tf.train.replica_device_setter(
                worker_device="/job:worker/task:%d" % node[1],
                    cluster=cluster)):
                global_step = tf.get_variable(
                    'global_step',
                    [],
                    initializer=tf.constant_initializer(0),
                    trainable=False)
                [self.W, self.b, x, y_, y] = create_layers(
                    self.W,
                    self.b,
                    n_lay,
                    n_neurons,
                    b_dim,
                    place_holder,
                    matmul,
                    act_1,
                    act_0)

        else:
            if not u_cpu:
                with tf.device("/gpu:1"):
                    [self.W, self.b, x, y_, y] = create_layers(
                        self.W,
                        self.b,
                        n_lay,
                        n_neurons,
                        b_dim,
                        place_holder,
                        matmul,
                        act_1,
                        act_0)
            else:
                [self.W, self.b, x, y_, y] = create_layers(
                    self.W,
                    self.b,
                    n_lay,
                    n_neurons,
                    b_dim,
                    place_holder,
                    matmul,
                    act_1,
                    act_0)
        with tf.name_scope('cross_entropy'):
            # this is our cost
            cross_entropy = tf.reduce_mean(
                -tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))
        with tf.name_scope('train'):
            # Training Steps Setup
            grad_op = tf.train.AdamOptimizer()
            if u_cluster:
                train_step = grad_op.minimize(
                    cross_entropy,
                    global_step=global_step)
            else:
                train_step = grad_op.minimize(
                    cross_entropy)

        with tf.name_scope('Accuracy'):
            # Correct Prediction of board winner
            correct_prediction = tf.equal(
                tf.argmax(y, 1), tf.argmax(y_, 1))
            # Accuracy Calculation
            accuracy = tf.reduce_mean(
                tf.cast(correct_prediction, tf.float32))
        tf.summary.scalar("cost", cross_entropy)
        tf.summary.scalar("accuracy", accuracy)
        summary_op = tf.summary.merge_all()
        init = tf.global_variables_initializer()
        if t_cl:
            print("Variables initialized ...")

        if u_cluster:
            sv = tf.train.Supervisor(
                is_chief=(node[1] == 0),
                global_step=global_step,
                init_op=init)
            with sv.prepare_or_wait_for_session(server.target) as sess:
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
                    summary_op,
                    results_directory,
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
                summary_op,
                results_directory,
                u_cluster,
                global_step,
                preset_accu)

        self.cost_hist = result["cost"]
        self.time_hist = result["time"]
        self.final_accu = result["fa"]
        self.start_time = result["st"]
        self.end_time = result["et"]
        if (t_cl):
            print("Final Accuracy {0:0.4f}".format(self.final_accu))
        self.t_time = timeit.default_timer() - start_time


def main():

    return 0

if __name__ == '__main__':
    main()
