from .DataPreparation import *
from .Packet import P_Packet
from .DataParameters import Data_Parameters

class Network(object):
    def __init__(self, N_packets, N_sp, N_storage, N_days, N_departures_sp, N_destination, Data_Parameters):
        self.N_packets = N_packets
        self.N_sp = N_sp
        self.N_storage = N_storage
        self.N_days = N_days
        self.N_departures_sp = N_departures_sp
        self.N_destination = N_destination
        self.Data_Parameters = Data_Parameters

    #preparing data
    def Preparing_data(self):
        DC1 = DataPreparation(self.N_packets ,self.N_sp ,self.N_storage ,self.N_days ,self.N_departures_sp ,self.N_destination , self.Data_Parameters)
        P_Packetlist1 = DC1.P_Packet_list()
        SP_list1, SP_loss = DC1.SP_list()
        Storagelist = DC1.Storage_list()
        return P_Packetlist1, SP_list1, Storagelist, SP_loss

    #packets at time t
    def Packets_T(self ,time_T , Storagelist, P_PacketsList_ALL = [] ):
        P_Packet_T = []
        P_PacketsList_new = [] # remove packets at time T form list
        for index in range(len(P_PacketsList_ALL)):
            if P_PacketsList_ALL[index].arrival <= time_T:
                P_Packet_T.append(P_PacketsList_ALL[index])
            else:
                P_PacketsList_new.append(P_PacketsList_ALL[index])
        for index in range(len(Storagelist)):
            P_Packet_T.append(Storagelist[index])
        return P_Packet_T, P_PacketsList_new

    #Service providers at time t to t+7 days
    def SP_T(self ,Start_Time ,End_Time ,SPList_ALL = [] ):
        SP_T_Result = []
        for index in range(len(SPList_ALL)):
            if SPList_ALL[index].departure_time >= Start_Time and SPList_ALL[index].departure_time <= End_Time:
                SP_T_Result.append(SPList_ALL[index])
        return SP_T_Result

    #Split Packets based on their destination
    def Packets_for_Destinations(self ,Packets_List_ALL = [] ):
        Packets_for_destinations = {}
        for i in range(self.N_destination):
            Packets_for_destinations[i] = []
            for index in range(len(Packets_List_ALL)):
                if Packets_List_ALL[index].destination == i:
                    Packets_for_destinations[i] .append(Packets_List_ALL[index])
        return Packets_for_destinations

    #Split Service providers based on their destination
    def SP_for_Destinations(self ,SP_List_ALL = [] ):
        SPs_for_destinations = {}
        for i in range(self.N_destination):
            SPs_for_destinations[i] = []
            for index in range(len(SP_List_ALL)):
                if SP_List_ALL[index].destination == i:
                    SPs_for_destinations[i] .append(SP_List_ALL[index])
        return SPs_for_destinations

    #Update notifications for each packet at time = T
    def Update_Notifications(self ,Sent_P_Packets_list, SuDelivery_P_Packets, UNSuDelivery_P_Packets, Storage_P_Packets_list, Unmatched_P_Packets_list, SP_list, time, Budget, Penalty):
        # if packets in storage is expired we have to add it to list of unmatched packets
        DC_Storage_list_update = []
        for index in range(len(Storage_P_Packets_list)):
            if Storage_P_Packets_list[index].deadline == time:
                Unmatched_P_Packets_list.append(Storage_P_Packets_list[index])
                Penalty = Penalty + Storage_P_Packets_list[index].penalty_unmatched
            else:
                DC_Storage_list_update.append(Storage_P_Packets_list[index])
        #Check for notification time in time = T
        DC_Sent_P_Packets_list_update = []
        for index in range(len(Sent_P_Packets_list)):
            if Sent_P_Packets_list[index].notification_time == time:
                # get a sample form distribution
                if(random.uniform(0, 1) > SP_list[Sent_P_Packets_list[index].status].loss_rate):
                    #Successful delivery
                    SuDelivery_P_Packets.append(Sent_P_Packets_list[index])
                    SP_list[Sent_P_Packets_list[index].status].delivered_packets += 1
                    SP_list[Sent_P_Packets_list[index].status].total_packets += 1
                    Profit = Sent_P_Packets_list[index].budget - (Sent_P_Packets_list[index].weight * SP_list[Sent_P_Packets_list[index].status].price_per_kg)
                    Budget = Budget + Profit
                else:
                    #faild
                    UNSuDelivery_P_Packets.append(Sent_P_Packets_list[index])
                    SP_list[Sent_P_Packets_list[index].status].total_packets += 1
                    Penalty = Penalty + Sent_P_Packets_list[index].penalty_late
            else:
                #create a new list to save remained packets
                DC_Sent_P_Packets_list_update.append(Sent_P_Packets_list[index])
        return DC_Sent_P_Packets_list_update, SuDelivery_P_Packets, UNSuDelivery_P_Packets, DC_Storage_list_update, Unmatched_P_Packets_list, SP_list, Budget, Penalty
