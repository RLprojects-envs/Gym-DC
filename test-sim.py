import argparse
import sys
import time
import math
import numpy as np
import datetime
from numpy.random.mtrand import RandomState
from gym import wrappers, logger
from gym_DC.simulator.DataParameters import Data_Parameters
#from gym_DC.DCgym_Env import DCGymEnv
import matplotlib.pyplot as plt
import numpy as np
from gym_DC.simulator.Simulator import Simulator



if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--env', default = 'DCgym-v0')
    parser.add_argument('--num_packets', type = int, default = 10000)
    parser.add_argument('--num_sp', type = int, default = 10)
    parser.add_argument('--num_storage', type = int, default = 1)
    parser.add_argument('--num_days', type = int, default = 100)
    parser.add_argument('--num_departures_sp', type = int, default = 80)
    parser.add_argument('--num_destination', type = int, default = 6)
    parser.add_argument('--Budget', type = int, default = 2000)
    parser.add_argument('--Penalty', type = int, default = 0)
    parser.add_argument('--num_actions', type=int, default=10)
    parser.add_argument('--HP', type = int, default = 3 )
    parser.add_argument('--start_date', type = datetime.date, default = datetime.date(2020, 1, 1))
    parser.add_argument('--mean_packet_weight', type = int, default = 8)
    parser.add_argument('--stddev_packet_weight', type = int, default = 2)
    parser.add_argument('--mean_packet_budget', type = int, default= 8)
    parser.add_argument('--stddev_packet_budget', type = int, default = 3)
    parser.add_argument('--mean_packet_penalty_late', type = int, default = 6)
    parser.add_argument('--stddev_packet_penalty_late', type = int, default = 2)
    parser.add_argument('--mean_packet_penalty_unmatched', type = int, default = 2)
    parser.add_argument('--stddev_packet_penalty_unmatched', type = int, default = 1)
    parser.add_argument('--mean_service_provider_price_per_kg', type = int, default = 10)
    parser.add_argument('--stddev_service_provider_price_per_kg', type = int, default = 2)
    parser.add_argument('--loss_service_provider_max', type = float, default = 0.6)
    parser.add_argument('--loss_service_provider_min', type = float, default = 0.1)
    parser.add_argument('--mean_service_provider_capacity', type = int, default = 200)
    parser.add_argument('--stddev_service_provider_capacity', type = int, default = 15)
    parser.add_argument('--mean_storage_price_per_kg', type = int, default = 1)
    parser.add_argument('--stddev_storage_price_per_kg', type = int, default = 1)
    parser.add_argument('--mean_storage_capacity', type = int, default = 5000)
    parser.add_argument('--stddev_storage_capacity', type = int, default = 50)
    parser.add_argument('--seed', type=int, default=0)
    parser.add_argument('--epsilon', type=float, default = 0.4)

    args = parser.parse_args()
    env = args.env
    num_packets = args.num_packets
    num_sp = args.num_sp
    num_storage = args.num_storage
    num_days = args.num_days
    num_departures_sp = args.num_departures_sp
    num_destination = args.num_destination
    Budget = args.Budget
    Penalty = args.Penalty
    num_actions = args.num_actions
    HP = args.HP
    Data_Params = Data_Parameters(args.start_date, args.mean_packet_weight, args.stddev_packet_weight, args.mean_packet_budget, args.stddev_packet_budget, args.mean_packet_penalty_late, args.stddev_packet_penalty_late, args.mean_packet_penalty_unmatched, args.stddev_packet_penalty_unmatched, args.mean_service_provider_price_per_kg, args.stddev_service_provider_price_per_kg, args.loss_service_provider_max, args.loss_service_provider_min, args.mean_service_provider_capacity, args.stddev_service_provider_capacity, args.mean_storage_price_per_kg, args.stddev_storage_price_per_kg, args.mean_storage_capacity, args.stddev_storage_capacity)

    data_x_axis = []
    data_y_axis = []

    HP=0
    for index in range (100):
        simulator = Simulator(num_packets, num_sp, num_storage, num_days, num_departures_sp, num_destination, Budget, Penalty, HP, Data_Params)
        profit, penalty, rate_of_successful, rate_of_delayed, rate_of_unmatched = simulator.Simulation_Period()
        reward = 0
        if profit > 0:
            reward = int(rate_of_successful * profit / 100)
        state = (reward, rate_of_successful, rate_of_delayed, rate_of_unmatched)
