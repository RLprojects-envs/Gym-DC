from dataclasses import dataclass
import datetime

"""
input parameters to generate data

"""
@dataclass
class Data_Parameters:
    __slots__ = ['start_date', 'mean_packet_weight', 'stddev_packet_weight', 'mean_packet_budget', 'stddev_packet_budget', 'mean_packet_penalty_late', 'stddev_packet_penalty_late', 'mean_packet_penalty_unmatched', 'stddev_packet_penalty_unmatched', 'mean_service_provider_price_per_kg', 'stddev_service_provider_price_per_kg', 'loss_service_provider_max', 'loss_service_provider_min', 'mean_service_provider_capacity', 'stddev_service_provider_capacity', 'mean_storage_price_per_kg', 'stddev_storage_price_per_kg', 'mean_storage_capacity', 'stddev_storage_capacity']
    start_date: datetime.date
    mean_packet_weight: int
    stddev_packet_weight: int
    mean_packet_budget: int
    stddev_packet_budget: int
    mean_packet_penalty_late: int
    stddev_packet_penalty_late: int
    mean_packet_penalty_unmatched: int
    stddev_packet_penalty_unmatched: int
    mean_service_provider_price_per_kg: int
    stddev_service_provider_price_per_kg: int
    loss_service_provider_max: float
    loss_service_provider_min: float
    mean_service_provider_capacity: int
    stddev_service_provider_capacity: int
    mean_storage_price_per_kg: int
    stddev_storage_price_per_kg: int
    mean_storage_capacity: int
    stddev_storage_capacity: int
