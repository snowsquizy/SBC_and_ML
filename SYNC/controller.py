#!/usr/bin/env python3

"""
Asynchronous Tic Tac Toe Solver
Andrew Taylor 2017
UNSW - Engineering Project

Adjust Variables to suit the hardware to be run on
then:-
    For use with CPU just run with python3 controller.py
    For use with GPU just run with python3 controller.py
    For use with Cluster run the following on each type:-
        Parameter Server
        python3 controller.py --job_name="ps" --task_index=0
        Worker
        python3 controller.py --job_name="worker" --task_index=0

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

"""

""""
Library Imports
"""
# Tensorflow Machine Learning
import tensorflow as tf
# For Getting the Current Date Time
import datetime
# For Creating Directories
import os
# Creating Tic Tac Toe Games
import create_b
# Creating Neural Network
import create_n
# Loading Tic Tac Toe Games
import load_b
# Saving Tic Tac Toe Games
import save_b
# Command Line Arguments
import sys
# Pre Processing of Tic Tac Toe Games
import pre_process


"""
Global Variables
"""
# Format for Date & Time File Names
format_long = "%Y_%m_%d_%H_%M"
# Format for Date only File Names
format_short = "%Y_%m_%d"
# Get the Current Data and Time
today = datetime.datetime.today()
# Parse it into a String long version
file_name_long = today.strftime(format_long)
# Parse it into a String short version
file_name_short = today.strftime(format_short)
# Result Directory Name
results_directory = "results/" + file_name_long + "/"
# Board Directory Name
board_directory = "boards/"
# Removes Incorrect CPU type warning
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

""" Use a Cluster for Machine Learner """
use_cluster = False

""" Use CPU or GPU """
use_cpu = True

""" Debugging Display on """
debug_code = False

""" Accuracy Percentage to Time """
preset_accu = 0.95

"""
Tic Tac Toe Variables
"""

""" Create New Tic Tac Toe Boards """
board_create = True

""" Number of Boards """
board_number = 100000

""" Board Dimensions """
board_dimensions = 3

# Board File Name
board_filename = board_directory + file_name_short + ".ttt"
# Board Teams
board_teams = ["X", "O"]

"""
Neural Network Variables
"""

""" Number of Layers """
layers_number = 2

""" Number of Neurons """
neurons_layer = 12

# Training Percentage
training_percentage = 0.7
# Validation Percentage
validation_percentage = 0.2
# Testing Percentage
testing_percentage = 0.1

""" Epochs to be run in Training """
epoch_number = 40

""" Activation Function """
activation = "tanh"

""" Batch Size to be Used """
batch_size = 2500

# Neural Network Save File Name
nn_filename = results_directory + "nn"

"""
Raspberry Pi Cluster Setup
"""
# Parameter Server IP Address and Port Number
p_server = [
    "localhost:2222",
    "localhost:2223"]

# Worker Ip Address and Port Number
workers = [
    "localhost:2224",
    "localhost:2225"]

# input flags
tf.app.flags.DEFINE_string(
    "job_name", "", "Either 'ps' or 'worker'")
tf.app.flags.DEFINE_integer(
    "task_index", 0, "Index of task within the job")
FLAGS = tf.app.flags.FLAGS
if (len(sys.argv) < 2):
    FLAGS.job_name = "worker"
    FLAGS.task_index = 0

node = []
node.append(FLAGS.job_name)
node.append(FLAGS.task_index)

cluster = tf.train.ClusterSpec(
    {"ps": p_server, "worker": workers})
server = tf.train.Server(
    cluster,
    job_name=node[0],
    task_index=node[1])

if node[0] == "ps":
    if debug_code:
        print("*** Parameter Server ***")
    server.join()

"""
Main Program Block
"""

"""
Check / Create Directories for Files Created
"""
# Check if results directory name exists
if not os.path.exists(results_directory):
    # Create results directory
    os.makedirs(results_directory)
# Check if board directory name exists
if not os.path.exists(board_directory):
    # Create board directory
    os.makedirs(board_directory)

"""
Tic Tac Toe Boards creation or loading
"""

if debug_code:
    # Display Current Process
    print("Program Start")
if (board_create):
    if (debug_code):
        # Display Current Process
        print("Creating Boards")
    # Create new Game Boards
    g_b = create_b.get_game_boards(
        board_number, board_dimensions, board_teams)
    if (debug_code):
        # Display Current Process
        print("Saving Boards")
    # Save newly created Game Boards
    save_b.save_boards(g_b, board_filename)
    if (debug_code):
        # Display Current Process
        print("Boards Saved")

else:
    if (debug_code):
        # Display Current Process
        print("Loading Boards")
    # Load Boards from filename
    g_b = load_b.get_game_boards(board_filename)
    # Update board Dimensions
    board_dimensions = int(len(g_b[0].board)**(1/2))
    # Update Board Number
    board_number = len(g_b)
    if (debug_code):
        # Display Current Process
        print("Boards Loaded")


"""
Pre Process Tic Tac Toe Boards for training, validation and testing
"""
ttt = pre_process.process_input(
    g_b,
    board_teams,
    training_percentage,
    validation_percentage,
    testing_percentage)


"""
Create Neural Network for training
"""
if (debug_code):
    # Display Current Process
    print("Creating NN")
N_N = create_n.neural_network(
    ttt,
    board_dimensions,
    activation,
    board_teams,
    int(training_percentage*board_number),
    int(validation_percentage*board_number),
    int(testing_percentage*board_number),
    layers_number,
    neurons_layer,
    epoch_number,
    batch_size,
    debug_code,
    use_cpu,
    use_cluster,
    p_server,
    workers,
    node,
    results_directory,
    preset_accu,
    cluster,
    server)

"""
Display Run Results Data
"""
print(str(N_N.start_time)+","+str(N_N.end_time)+","+str(N_N.final_accu))
