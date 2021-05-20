import gym
from ..simulator.Simulator import Simulator
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np


class DCGymEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):

        self.num_packets = 0
        self.num_sp = 0
        self.num_storage = 0
        self.num_days = 0
        self.num_departures_sp = 0
        self.num_destination = 0
        self.Budget = 0
        self.Penalty = 0
        self.HP = 0
        #self.action_space = spaces.Discrete(num_actions)

        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Tuple((spaces.Discrete(100), spaces.Discrete(100), spaces.Discrete(100), spaces.Discrete(100))) # percentage of delayed packet, percentage of unmatched packet , percentage of budget/profit

    def step(self, action, num_packets, num_sp, num_storage, num_days, num_departures_sp, num_destination, Budget, Penalty, Data_Parameters):
        self.num_packets = num_packets
        self.num_sp = num_sp
        self.num_storage = num_storage
        self.num_days = num_days
        self.num_departures_sp = num_departures_sp
        self.num_destination = num_destination
        self.Budget = Budget
        self.Penalty = Penalty
        HP = action
        simulator = Simulator(self.num_packets, self.num_sp, self.num_storage, self.num_days, self.num_departures_sp, self.num_destination, self.Budget, self.Penalty, HP, Data_Parameters)
        profit, penalty, rate_of_successful, rate_of_delayed, rate_of_unmatched = simulator.Simulation_Period()
        reward = 0
        if profit > 0:
            reward = int(rate_of_successful*profit/100)
        state = (reward, rate_of_successful, rate_of_delayed, rate_of_unmatched)
        return reward, state

    def reset(self, num_packets, num_sp, num_storage, num_days, num_departures_sp, num_destination, Budget, Penalty, HP, Data_Parameters):
        simulator = Simulator(num_packets, num_sp, num_storage, num_days, num_departures_sp, num_destination, Budget, Penalty, HP, Data_Parameters)
        profit, penalty, rate_of_successful, rate_of_delayed, rate_of_unmatched = simulator.Simulation_Period()
        state = (rate_of_successful, rate_of_delayed, rate_of_unmatched)
        reward = 0
        if profit > 0:
            reward = int(rate_of_successful*profit/100)
        return reward, state

    def render(self, mode='human'):
        print()

