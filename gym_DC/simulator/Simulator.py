
from .Network import *
from .MatchingAlgorithm import *
from .DataParameters import Data_Parameters

class Simulator(object):
    def __init__(self, num_packets, num_sp, num_storage, num_days, num_departures_sp, num_destination, Budget, Penalty, HP, Data_Parameters):
        self.num_packets = num_packets
        self.num_sp = num_sp
        self.num_storage = num_storage
        self.num_days = num_days
        self.num_departures_sp = num_departures_sp
        self.num_destination = num_destination
        self.Budget = Budget
        self.Penalty = Penalty
        self.HP = HP
        self.Data_Parameters = Data_Parameters
        self.DC_P_Packetlist = []
        self.DC_Current_P_Packets = []
        self.DC_Storagelist = []
        self.DC_SPlist = []
        #Different lists for service providers
        self.SP_list = [] # store the loss value for service providers to use later for notification
        self.DC_Storage_P_Packets_list = []
        self.DC_Sent_P_Packets_list = []
        self.DC_Unmatched_P_Packets_list = []
        self.DC_SuDelivery_P_Packets = [] # list of successful delivery P_Packets
        self.DC_UNSuDelivery_P_Packets = [] # list of unsuccessful delivery P_Packets
        

          
        self.start_date = datetime.date(2020, 1, 1)

        self.DC_Network=self.Preparing_data()
        
        
        
    #preparing data
    def Preparing_data(self):
        Network_obj = Network(self.num_packets, self.num_sp, self.num_storage, self.num_days, self.num_departures_sp, self.num_destination, self.Data_Parameters)
        self.DC_P_Packetlist, self.DC_SPlist, self.DC_Storagelist, self.SP_list = Network_obj.Preparing_data()
        return Network_obj
    	
    # Packet and Service providers at T
    def Data_for_state_T(self, day):
        DC_Current_P_Packets, self.DC_P_Packetlist = self.DC_Network.Packets_T(day, self.DC_Storage_P_Packets_list, self.DC_P_Packetlist)
        # Service Providers in the range time = t to time = t + 7 days
        End_day = day + datetime.timedelta(days=7)
        DC_Current_SP = self.DC_Network.SP_T(day, End_day, self.DC_SPlist)
        # Separete Packets and SP based on the destination
        Packets = self.DC_Network.Packets_for_Destinations(DC_Current_P_Packets)
        SPs = self.DC_Network.SP_for_Destinations(DC_Current_SP)
        return Packets, SPs


    def Simulation_T(self, Packets, SPs, time):
        # Send list for matching process at time = T
        DC_Matching = MatchingAlgorithm(self.HP)
        for index in range(len(Packets)):
            DC_Sent_P_Packets_Temp, DC_Storage_P_Packets_Temp, DC_Unmatched_P_Packets_Temp = DC_Matching.Matching_Model_1(Packets[index], SPs[index], self.DC_Storagelist[0])
            self.DC_Sent_P_Packets_list.extend(DC_Sent_P_Packets_Temp)
            self.DC_Storage_P_Packets_list=DC_Storage_P_Packets_Temp #we add storage packets to P_Packet list before
            self.DC_Unmatched_P_Packets_list.extend(DC_Unmatched_P_Packets_Temp)
        self.DC_Sent_P_Packets_list, self.DC_SuDelivery_P_Packets, self.DC_UNSuDelivery_P_Packets, self.Storage_P_Packets_list, self.Unmatched_P_Packets_list, self.SP_list, self.Budget, self.Penalty= self.DC_Network.Update_Notifications(self.DC_Sent_P_Packets_list, self.DC_SuDelivery_P_Packets, self.DC_UNSuDelivery_P_Packets, self.DC_Storage_P_Packets_list, self.DC_Unmatched_P_Packets_list, self.SP_list, time, self.Budget, self.Penalty)

    def Simulation_Period(self):
        First_budget = self.Budget
        number_of_packets = len(self.DC_P_Packetlist)
        for index in range(self.num_days + 10):
            day = self.start_date + datetime.timedelta(days=index)
            Packets_day, SPs_day = self.Data_for_state_T(day)
            self.Simulation_T(Packets_day, SPs_day, day)

        current_budget = self.Budget
        penalty = self.Penalty
        profit = current_budget - First_budget -penalty
        if profit < 0:
           profit = 0
        rate_of_unmatched = int (100*len(self.DC_Unmatched_P_Packets_list)/number_of_packets)
        rate_of_delayed = int (100*len(self.DC_UNSuDelivery_P_Packets)/number_of_packets)
        rate_of_successful = int (100*len(self.DC_SuDelivery_P_Packets)/number_of_packets)

        return profit, penalty, rate_of_successful, rate_of_delayed, rate_of_unmatched


