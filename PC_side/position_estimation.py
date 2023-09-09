import numpy as np
from scipy.spatial.distance import euclidean

# Assuming you have a long list of tuples, each containing the angle (in degrees) and distance to a point/object
'''data = [
    (30.0, 3.5),
    (45.0, 5.0),
    (60.0, 4.2),
    (120.0, 2.8),
    (135.0, 6.0),
    (150.0, 4.5),
    # Add more data here
]'''



# Function to calculate the distance between two points in (angle, distance) space
def point_distance(point1, point2):
    return euclidean(point1, point2)

# DBSCAN clustering function
def dbscan_clustering(data, eps, min_samples):
    clusters = []
    visited = set()

    def expand_cluster(point_idx, neighbors, cluster):
        cluster.append(point_idx)
        visited.add(point_idx)

        while neighbors:
            next_point_idx = neighbors.pop()
            if next_point_idx not in visited:
                visited.add(next_point_idx)
                next_neighbors = region_query(next_point_idx)
                if len(next_neighbors) >= min_samples:
                    neighbors.extend(next_neighbors)
            if next_point_idx not in cluster:
                cluster.append(next_point_idx)

    def region_query(point_idx):
        return [idx for idx, point in enumerate(data) if point_distance(data[point_idx], point) <= eps]

    for point_idx, point in enumerate(data):
        if point_idx in visited:
            continue

        neighbors = region_query(point_idx)
        if len(neighbors) < min_samples:
            continue

        cluster = []
        expand_cluster(point_idx, neighbors, cluster)
        clusters.append(cluster)

    return clusters

def estimate_pos(data):

    # Convert angle from degrees to radians
    data_rad = [(angle * np.pi / 180.0, distance) for angle, distance in data]
    # Clustering parameters
    eps = 1.2  # Adjust as needed 1.5
    min_samples = 2  # Adjust as needed

    # Perform DBSCAN clustering
    clusters = dbscan_clustering(data_rad, eps, min_samples)

    # Estimate the positions of objects in each cluster
    estimated_positions = []
    for cluster in clusters:
        x_sum, y_sum = 0.0, 0.0
        for idx in cluster:
            x_sum += data_rad[idx][1] * np.cos(data_rad[idx][0])
            y_sum += data_rad[idx][1] * np.sin(data_rad[idx][0])
        num_points = len(cluster)
        estimated_x = int(x_sum / num_points)
        estimated_y = int(y_sum / num_points)
        estimated_distance = int(np.hypot(estimated_x, estimated_y))
        estimated_angle_deg = int(np.arctan2(estimated_y, estimated_x) * 180.0 / np.pi)
        estimated_positions.append((estimated_angle_deg, estimated_distance))
       
    
    #print("Estimated best positions:", estimated_positions)
    return estimated_positions
