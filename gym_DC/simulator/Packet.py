from dataclasses import dataclass

@dataclass
class P_Packet:
    __slots__ = ['idp', 'budget', 'weight', 'arrival', 'deadline', 'destination', 'penalty_late', 'penalty_unmatched', 'status', 'departure', 'notification_time', 'delivery_report']
    idp: int
    budget: int
    weight: int
    arrival: int
    deadline: int
    destination: int
    penalty_late: int
    penalty_unmatched: int
    status: int
    # 0 = On the arrival    1 = queue list
    departure: int
    notification_time: int
    delivery_report: int
    # 0 = unsuccessful      1 = successful




    


    
    
    

