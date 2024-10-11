import matplotlib.pyplot as plt
import numpy as np
import random
import yaml

# Slice Application class
class SliceApplication:
    def __init__(self, min_bandwidth, max_bandwidth, qos_class, delay_tolerance, client_weight):
        self.min_bandwidth = min_bandwidth  # Minimum bandwidth guaranteed (in bps)
        self.max_bandwidth = max_bandwidth  # Maximum bandwidth required (in bps)
        self.qos_class = qos_class          # QoS class (integer, higher means more priority)
        self.delay_tolerance = delay_tolerance  # Delay tolerance (in milliseconds)
        self.allocated_bandwidth = 0        # This will be set during allocation
        self.client_weight = client_weight  # Weight of clients subscribed to this slice
        self.usage_pattern = {"distribution": "randint", "params": [4000000, 800000000]}
        self.threshold = 0

# Various Slicing Algorithms:

#*1. Round Robin Algo:
def round_robin_allocation(applications, total_bandwidth):
    num_apps = len(applications)
    bandwidth_per_app = total_bandwidth // num_apps #Equal splitting of bandwidth between applications
    for app in applications:
        app.allocated_bandwidth = min(app.max_bandwidth, bandwidth_per_app)

#*2. Priority Based Algo:
def priority_based_allocation(applications, total_bandwidth):
    sorted_apps = sorted(applications, key=lambda x: (-x.qos_class, x.delay_tolerance)) #Allocate channels based on QoS class (higher first) and delay tolerance (lower first)
    for app in sorted_apps:
        if total_bandwidth == 0:
            break
        allocation = min(app.max_bandwidth, total_bandwidth)
        app.allocated_bandwidth = allocation #Allocate bandwidth to application
        total_bandwidth -= allocation

#*3. Proportional Fairness Algo:
def proportional_fairness_allocation(applications, total_bandwidth):
    total_required_bandwidth = sum(app.max_bandwidth for app in applications)
    for app in applications:
        app.allocated_bandwidth = (app.max_bandwidth / total_required_bandwidth) * total_bandwidth #Allocate bandwidth linearly proportional to max_bandwidth requirement 

#*4. Max-Min Fairness Algo:
def max_min_fairness_allocation(applications, total_bandwidth):
    sorted_apps = sorted(applications, key=lambda x: x.min_bandwidth)
    for app in sorted_apps:
        allocation = min(app.max_bandwidth, total_bandwidth / len(sorted_apps)) #Allocate minimum required bandwidth for each application that is fair to its requirements
        app.allocated_bandwidth = allocation

#*5. Weighted Fairness Algo:
def weighted_fair_queueing(applications, total_bandwidth):
    total_weight = sum(app.qos_class for app in applications)
    for app in applications:
        app.allocated_bandwidth = (app.qos_class / total_weight) * total_bandwidth #Allocation proportional to QoS class value relative to other applications

#*6. First Come First Served Algo:
def first_come_first_served(applications, total_bandwidth):
    for app in applications:
        if total_bandwidth == 0:
            break
        allocation = min(app.max_bandwidth, total_bandwidth)
        app.allocated_bandwidth = allocation
        total_bandwidth -= allocation

#*7. Latency-Aware Algo:
def latency_aware_allocation(applications, total_bandwidth):
    sorted_apps = sorted(applications, key=lambda x: x.delay_tolerance)
    for app in sorted_apps:
        allocation = min(app.max_bandwidth, total_bandwidth / len(sorted_apps)) #Using delay alone as a focus in priority
        app.allocated_bandwidth = allocation

#*8. Resource Reservation Algo:
def resource_reservation(applications, total_bandwidth):
    for app in applications:
        reserved = app.min_bandwidth
        if total_bandwidth >= reserved:
            app.allocated_bandwidth = reserved #Allocate upto channel availability only
            total_bandwidth -= reserved

#*9. Utility-Based Algo:
def utility_based_allocation(applications, total_bandwidth):
    utilities = [app.qos_class / app.max_bandwidth for app in applications] #Utility = ratio of QoS class to max bandwidth
    total_utility = sum(utilities)
    for app in applications:
        app.allocated_bandwidth = (app.qos_class / total_utility) * total_bandwidth #Based on utility metric for each application

#*10. Dynamic Adaptive Algo:
def dynamic_adaptive_allocation(applications, total_bandwidth):
    for app in applications:
        if total_bandwidth == 0:
            break
        real_time_bandwidth = random.uniform(app.min_bandwidth, app.max_bandwidth) #Allocate random value between min and max bandwidth through a normal distribuiton
        app.allocated_bandwidth = min(real_time_bandwidth, total_bandwidth)
        total_bandwidth -= app.allocated_bandwidth

#*11. Hybrid Dynamic Algo:
def NoStarvation_priority_roundRHybrid_allocation(applications, total_bandwidth):
    total_bandwidth_remaining = total_bandwidth
    delay_since_last_allocated = [app.delay_tolerance for app in applications]

    for time in range(100):  # Simulation over time (e.g., 100 time slots)
        ctr = 0.6
        Increment = 1 / (len(applications) * 2)
        i = 0

        for app in applications:
            if total_bandwidth_remaining == 0:
                # Adjust priorities for unmet SLAs
                for j in applications:
                    if j.allocated_bandwidth == 0:
                        j.qos_class = min(2 + j.qos_class, 12)  # Increment priority for starvation cases
                break

            real_time_bandwidth = random.uniform(app.min_bandwidth, app.max_bandwidth)

            # Ensure slice gets at least its minimum bandwidth for SLA satisfaction
            if real_time_bandwidth > total_bandwidth_remaining:
                app.allocated_bandwidth = min(app.min_bandwidth, total_bandwidth_remaining)
            else:
                app.allocated_bandwidth = min(real_time_bandwidth, total_bandwidth_remaining)

            total_bandwidth_remaining -= app.allocated_bandwidth

            # Increment priority for slices close to delay expiration
            if delay_since_last_allocated[i] / app.delay_tolerance < 0.3:
                ctr = 1  # Boost priority if nearing delay tolerance threshold

            if app.allocated_bandwidth < real_time_bandwidth:
                delay_since_last_allocated[i] -= 1  # Reduce delay tolerance as it waits longer
                app.qos_class = min(2 + app.qos_class, 12)  # Increase QoS to avoid starvation

            i += 1

        # Sort applications by QoS class for the next round
        applications.sort(key=lambda x: x.qos_class, reverse=True)

# Performance Metrics

#*1 Bandwidth utilization:
def calculate_bandwidth_utilization(applications, total_bandwidth):
    allocated_bandwidth = sum(app.allocated_bandwidth for app in applications)
    return allocated_bandwidth / total_bandwidth #ratio of application to total bandwidth


#*2 Jain Fairness Index:
def calculate_jain_fairness_index(applications):
    allocations = [app.allocated_bandwidth for app in applications]
    numerator = (sum(allocations)) ** 2
    denominator = len(allocations) * sum(x ** 2 for x in allocations)
    return numerator / denominator if denominator != 0 else 0

#*3 SLA Satisfaction:
def calculate_sla_satisfaction(applications):
    satisfied_apps = sum(1 for app in applications if app.allocated_bandwidth >= app.min_bandwidth)
    return satisfied_apps / len(applications)

#*4 Delay Satisfaction:
def calculate_delay_satisfaction(applications):
    satisfied_apps = sum(1 for app in applications if app.delay_tolerance >= random.randint(0, 500))  # Simplified random delay modeling
    return satisfied_apps / len(applications)

#*5 Over Provisioning:
def calculate_over_provisioning(applications):
    over_provisioned_apps = sum(1 for app in applications if app.allocated_bandwidth > app.min_bandwidth)
    return over_provisioned_apps / len(applications)

#*6 Under Provisioning:
def calculate_under_provisioning(applications):
    under_provisioned_apps = sum(1 for app in applications if app.allocated_bandwidth < app.min_bandwidth)
    return under_provisioned_apps / len(applications)

#*7 Bandwidth Variance:
def calculate_bandwidth_variance(applications):
    allocations = [app.allocated_bandwidth for app in applications]
    return np.var(allocations)

#*8 Max Allocation Ratio:
def calculate_max_allocation_ratio(applications, total_bandwidth):
    max_alloc = max(app.allocated_bandwidth for app in applications)
    return max_alloc / total_bandwidth

#*9 Client Saturation Index:
def calculate_client_saturation_index(applications):
    return sum(app.allocated_bandwidth / app.max_bandwidth for app in applications) / len(applications)

#*10 Weighted Efficiency:
def calculate_weighted_efficiency(applications):
    weighted_sum = sum((app.allocated_bandwidth / app.max_bandwidth) * app.qos_class for app in applications)
    total_weight = sum(app.qos_class for app in applications)
    return weighted_sum / total_weight if total_weight > 0 else 0

#* All Performance Metrics:
def calculate_metrics(applications, total_bandwidth):
    utilization = calculate_bandwidth_utilization(applications, total_bandwidth)
    fairness = calculate_jain_fairness_index(applications)
    sla_satisfaction = calculate_sla_satisfaction(applications)
    delay_satisfaction = calculate_delay_satisfaction(applications)
    over_provisioning = calculate_over_provisioning(applications)
    under_provisioning = calculate_under_provisioning(applications)
    allocation_variance = calculate_bandwidth_variance(applications)
    max_allocation_ratio = calculate_max_allocation_ratio(applications, total_bandwidth)
    client_saturation = calculate_client_saturation_index(applications)
    weighted_efficiency = calculate_weighted_efficiency(applications)

    return {
        "utilization": utilization,
        "fairness": fairness,
        "sla_satisfaction": sla_satisfaction,
        "delay_satisfaction": delay_satisfaction,
        "over_provisioning": over_provisioning,
        "under_provisioning": under_provisioning,
        "allocation_variance": allocation_variance,
        "max_allocation_ratio": max_allocation_ratio,
        "client_saturation": client_saturation,
        "weighted_efficiency": weighted_efficiency
    }

#* Save Slice Data into a YAML file: (NOTE: base_stations.py used to generate base station data as YAML file):
def save_applications_to_yaml(applications, filename="slice_data.yaml"):
    slices_data = {"slices": {}}
    
    for i, app in enumerate(applications):
        slice_name = f"slice_{i+1}"
        slices_data["slices"][slice_name] = {
            "delay_tolerance": app.delay_tolerance,
            "qos_class": app.qos_class,
            "bandwidth_guaranteed": app.min_bandwidth,
            "bandwidth_max": app.max_bandwidth,
            "client_weight": app.client_weight,
            "threshold": app.threshold,
            "usage_pattern": app.usage_pattern
        }
    
    with open(filename, "w") as file:
        yaml.dump(slices_data, file)

# Simulate the network slicing and metrics calculation
def simulate_and_evaluate(num_apps, total_bandwidth, allocation_strategy):
    applications = [
        SliceApplication(min_bandwidth=random.randint(5000000, 20000000),
                         max_bandwidth=random.randint(20000000, 100000000),
                         qos_class=random.randint(1, 5),
                         delay_tolerance=random.randint(10, 500),
                         client_weight=random.uniform(0.01, 0.1))
        for _ in range(num_apps)
    ]
    allocation_strategy(applications, total_bandwidth)
    metrics = calculate_metrics(applications, total_bandwidth)
    save_applications_to_yaml(applications)
    
    return metrics

#* Main simulation and scaling
def simulate_scaling(num_apps_list, total_bandwidth, allocation_strategy):
    all_metrics = []
    for num_apps in num_apps_list:
        metrics = simulate_and_evaluate(num_apps, total_bandwidth, allocation_strategy)
        all_metrics.append(metrics)
    return all_metrics




#* Actual simulation of different slicing algos:

total_bandwidth = 5000000000  # 5 Gbps total bandwidth
num_apps_list = [50, 100, 200, 500, 1000]  # Simulating different numbers of applications


import os

# Create folder to store plots:
output_dir = "plots"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Dictionary of algorithms:
algorithms = {
    'Round Robin': round_robin_allocation,
    'Priority-Based': priority_based_allocation,
    'Proportional Fairness': proportional_fairness_allocation,
    'Max-Min Fairness': max_min_fairness_allocation,
    'Weighted Fair Queueing': weighted_fair_queueing,
    'First-Come First-Served': first_come_first_served,
    'Latency-Aware': latency_aware_allocation,
    'Resource Reservation': resource_reservation,
    #!'Utility-Based': utility_based_allocation,
    'Dynamic Adaptive': dynamic_adaptive_allocation,
    'Hybrid Dynamic': NoStarvation_priority_roundRHybrid_allocation
}

# List of metrics to plot:
metric_names = ["utilization", "fairness", "sla_satisfaction", "delay_satisfaction", 
                "over_provisioning", "under_provisioning", "allocation_variance", 
                "max_allocation_ratio", "client_saturation", "weighted_efficiency"]

from itertools import cycle
# Function to plot all algorithms on one graph for each metric:
def plot_all_algorithms_on_one_graph(metrics_dict, num_apps_list):
    for metric in metric_names:
        plt.figure(figsize=(10, 6))

        #! Use a colormap with more than 10 colors, like 'tab20'
        #!colors = plt.get_cmap('tab20').colors  # tab20 has 20 colors
        #!color_cycle = cycle(colors)  # Create a cycle from the colormap

        for alg_name, metrics in metrics_dict.items():
            metric_values = [m[metric] for m in metrics]
            #!plt.plot(num_apps_list, metric_values, label=alg_name, color=next(color_cycle), marker='o')
            plt.plot(num_apps_list, metric_values, label=alg_name, marker='o')


        plt.xlabel("Number of Applications")
        plt.ylabel(metric.replace('_', ' ').title())
        plt.title(f"{metric.replace('_', ' ').title()} vs. Number of Applications (All Algorithms)")
        plt.legend()
        plt.grid(True)

        # Save the plot
        plot_filename = os.path.join(output_dir, f"all_algorithms_{metric}.png")
        plt.savefig(plot_filename)
        plt.show()
        plt.close()

# Run simulations for all algorithms and store their metrics
all_algorithms_metrics = {}

for alg_name, alg_func in algorithms.items():
    print(f"Running simulation for {alg_name}...")
    all_algorithms_metrics[alg_name] = simulate_scaling(num_apps_list, total_bandwidth, alg_func)

# Plot all algorithms on one graph for each metric
plot_all_algorithms_on_one_graph(all_algorithms_metrics, num_apps_list)
