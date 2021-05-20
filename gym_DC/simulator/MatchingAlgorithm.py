from collections import deque
import random
import datetime

class MatchingAlgorithm(object):
    def __init__(self, Sort_parameter):
        self.Sort_parameter = Sort_parameter


    def Matching_Model_1(self, Packets_List, SP_List, Storage):
        # create list of items
        DC_Storage_P_Packets = []
        DC_Unmatched_P_Packets = []
        DC_Sent_P_Packets = []


        SP_List = self.Sort_SP_Budget(SP_List)
        Packets_List = self.Sort_Packets_Budget(Packets_List)
        it = deque(Packets_List)
        while it:
            # Compute sizes
            # Get biggest item
            i = self.max_profit(it)
            it.remove(i)
            matched = False

            for index in range(len(SP_List)):
                if ( SP_List[index].capacity > i.weight ):
                    SP_List[index].capacity = SP_List[index-1].capacity - i.weight
                    i.status = SP_List[index].idsp
                    i.departure = SP_List[index].departure_time
                    #make sure notification is not sent before departure
                    if (i.deadline > i.departure + datetime.timedelta(days=3)):
                        random_days = 3
                    else:
                        random_days = 1
                    i.notification_time = i.deadline + datetime.timedelta(days=random.randint(random_days, 6))
                    DC_Sent_P_Packets.append(i)
                    matched = True
                    break
            if (matched==False):
                #There is No SP for this packet
                if (Storage.capacity>i.weight):
                    DC_Storage_P_Packets.append(i)
                else:
                    DC_Unmatched_P_Packets.add(i)
        return DC_Sent_P_Packets, DC_Storage_P_Packets, DC_Unmatched_P_Packets

    ################## Utility functions ####################
    def max_profit(self ,Packet_List):
        """ Return max profit packet using size attribute """
        Temp_List = self.Sort_Packets_Budget(Packet_List)
        return Temp_List[len(Temp_List)-1]


    #sort packets based on their budget
    def Sort_Packets_Budget(self ,Packets_List_ALL=[]):
        n = len(Packets_List_ALL)
        for i in range(n):
            already_sorted = True
            for j in range(n - i - 1):
                packet1_score = 0
                packet2_score = 0
                x, y = self.coeffient_hp(self.Sort_parameter)
                if (Packets_List_ALL[j].weight) > 0:
                    packet1_score = ( x * (Packets_List_ALL[j].budget / Packets_List_ALL[j].weight) ) - (y * Packets_List_ALL[j].penalty_late )
                if(Packets_List_ALL[j+1].weight) > 0:
                    packet2_score = ( x * (Packets_List_ALL[j+1].budget / Packets_List_ALL[j+1].weight) ) - (y * Packets_List_ALL[j+1].penalty_late )
                if packet1_score < packet2_score:
                    Packets_List_ALL[j], Packets_List_ALL[j + 1] = Packets_List_ALL[j + 1], Packets_List_ALL[j]
                    already_sorted = False
            if already_sorted:
                break
        Packets = Packets_List_ALL
        return Packets

    #sort SPs based on their price
    def Sort_SP_Budget(self, SP_List_ALL=[]):
        n = len(SP_List_ALL)
        for i in range(n):
            already_sorted = True
            for j in range(n - i - 1):
                loss_sp1 = 0
                loss_sp2 = 0
                if SP_List_ALL[j].total_packets > 0:
                    loss_sp1= 1 - (SP_List_ALL[j].delivered_packets / SP_List_ALL[j].total_packets)
                if SP_List_ALL[j+1].total_packets > 0:
                    loss_sp2 = 1 - (SP_List_ALL[j+1].delivered_packets / SP_List_ALL[j+1].total_packets)
                x , y = self.coeffient_hp(self.Sort_parameter)
                sp1_score = (x * SP_List_ALL[j].price_per_kg ) +  (y * loss_sp1 * 10 )
                sp2_score = (x * SP_List_ALL[j+1].price_per_kg ) + (y * loss_sp2 * 10 )
                if sp1_score > sp2_score:
                    SP_List_ALL[j], SP_List_ALL[j + 1] = SP_List_ALL[j + 1], SP_List_ALL[j]
                    already_sorted = False
            if already_sorted:
                break
        SP = SP_List_ALL
        return SP

    def coeffient_hp(self, HP):
        if (HP==0):
            x , y =1 , 0
        if (HP==1):
            x , y =15 , 5
        if (HP==2):
            x , y =1 , 1
        if (HP==3):
            x , y =-5 , -5
        if (HP==4):
            x , y =-1 , 0
        return x, y