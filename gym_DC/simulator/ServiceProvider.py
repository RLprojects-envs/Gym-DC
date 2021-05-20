from dataclasses import dataclass

@dataclass
class ServiceProvider:
    __slots__ = ['idsp', 'price_per_kg', 'capacity', 'departure_time', 'destination', 'loss_rate', 'delivered_packets', 'total_packets']
    idsp: int
    price_per_kg: int
    capacity: int
    departure_time: int
    destination: int
    loss_rate: float
    delivered_packets: int
    total_packets: int


    
    


    
    
    

