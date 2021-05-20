from .Packet import P_Packet
from .ServiceProvider import ServiceProvider
from .DataParameters import Data_Parameters
from .Storage import Storage
from typing import List
from random import normalvariate,randint
import datetime
import random
import numpy as np

class DataPreparation(object):
    def __init__(self,  N_packets, N_sp, N_storage, N_days, N_departures_sp, N_destination, Data_Parameters):
        """
        Parameters
        ----------
        N_packets : int
            Number of packets in the network
        N_sp : int
            Number of service providers in the network
        N_sp : int
            Number of storages in the network
        """
        self.N_packets = N_packets
        self.N_sp = N_sp
        self.N_storage = N_storage
        self.N_days = N_days
        self.N_departures_sp = N_departures_sp
        self.N_destination = N_destination
        self.start_date = Data_Parameters.start_date
        self.mean_packet_weight = Data_Parameters.mean_packet_weight
        self.stddev_packet_weight = Data_Parameters.stddev_packet_weight
        self.mean_packet_budget = Data_Parameters.mean_packet_budget
        self.stddev_packet_budget = Data_Parameters.stddev_packet_budget
        self.mean_packet_penalty_late = Data_Parameters.mean_packet_penalty_late
        self.stddev_packet_penalty_late = Data_Parameters.stddev_packet_penalty_late
        self.mean_packet_penalty_unmatched = Data_Parameters.mean_packet_penalty_unmatched
        self.stddev_packet_penalty_unmatched = Data_Parameters.stddev_packet_penalty_unmatched
        self.mean_service_provider_price_per_kg = Data_Parameters.mean_service_provider_price_per_kg
        self.stddev_service_provider_price_per_kg = Data_Parameters.stddev_service_provider_price_per_kg
        self.loss_service_provider_max = Data_Parameters.loss_service_provider_max
        self.loss_service_provider_min = Data_Parameters.loss_service_provider_min
        self.mean_service_provider_capacity = Data_Parameters.mean_service_provider_capacity
        self.stddev_service_provider_capacity = Data_Parameters.stddev_service_provider_capacity
        self.mean_storage_price_per_kg = Data_Parameters.mean_storage_price_per_kg
        self.stddev_storage_price_per_kg = Data_Parameters.stddev_storage_price_per_kg
        self.mean_storage_capacity = Data_Parameters.mean_storage_capacity
        self.stddev_storage_capacity = Data_Parameters.stddev_storage_capacity

    def P_Packet_list(self):
        # Set parameters for lists
        # packets
        P_PacketsList = []
        # assigning values to lists
        # assigning values to P_PacketsList
        for index in range(self.N_packets ):
            budget = int(normalvariate(self.mean_packet_budget * self.mean_packet_weight, self.stddev_packet_budget) + 0.5)
            weight = int(normalvariate(self.mean_packet_weight, self.stddev_packet_weight) + 0.5) + 1
            arrival= self.start_date + datetime.timedelta(days=random.randrange(self.N_days))
            deadline = arrival + datetime.timedelta(days=random.randrange(10))
            destination = int(random.uniform(0, self.N_destination))
            penalty_late = int(normalvariate(self.mean_packet_penalty_late, self.stddev_packet_penalty_late) + 0.5)
            penalty_unmatched = int(normalvariate(self.mean_packet_penalty_unmatched, self.stddev_packet_penalty_unmatched) + 0.5)
            status = 99
            departure = 0
            notification_time = 0
            delivery_report = 0
            random_P_Packet = P_Packet(index, budget, weight, arrival, deadline, destination, penalty_late, penalty_unmatched, status, departure, notification_time, delivery_report)
            P_PacketsList.append(random_P_Packet)
        return P_PacketsList

    def SP_list(self):
        # Service Providers
        ServiceProvidersList = []
        SP_loss  = []
        # assigning values to ServiceProvidersList
        for index in range(self.N_sp):
            loss_rate = random.uniform(self.loss_service_provider_min, self.loss_service_provider_max)
            #If loss rate is small then price will be higher
            #price_per_kg = int(normalvariate(self.mean_service_provider_price_per_kg, self.stddev_service_provider_price_per_kg) + 0.5)
            price_per_kg = int( (1-loss_rate) * self.mean_service_provider_price_per_kg)
            SP_loss.append(ServiceProvider(index, price_per_kg, 0, 0, 0, loss_rate, 0, 0))
            for index_departure in range(self.N_departures_sp):
                departure_time = self.start_date + datetime.timedelta(days=random.randrange(self.N_days))
                capacity = int(normalvariate(self.mean_service_provider_capacity, self.stddev_service_provider_capacity) + 0.5)
                destination = int(random.uniform(0, self.N_destination))
                random_sp = ServiceProvider(index, price_per_kg, capacity, departure_time, destination, loss_rate, 0, 0)
                ServiceProvidersList.append(random_sp)
        return ServiceProvidersList, SP_loss

    def Storage_list(self):
        # Storage
        StorageList = []
        # assigning values to StorageList
        for index in range(self.N_storage):
            price_per_kg = int(normalvariate(self.mean_storage_price_per_kg, self.stddev_storage_price_per_kg) + 0.5)
            capacity = int(normalvariate(self.mean_storage_capacity, self.stddev_storage_capacity) + 0.5)
            random_storage = Storage(index, price_per_kg, capacity)
            StorageList.append(random_storage)
        return StorageList

