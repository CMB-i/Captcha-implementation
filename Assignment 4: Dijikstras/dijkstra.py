import heapq

# Graph of Indian cities with road distances (in km)
graph = {
    "Delhi": [("Jaipur", 281), ("Lucknow", 555), ("Ahmedabad", 950)],
    "Jaipur": [("Delhi", 281), ("Ahmedabad", 657), ("Mumbai", 1148)],
    "Lucknow": [("Delhi", 555), ("Kolkata", 991)],
    "Ahmedabad": [("Delhi", 950), ("Jaipur", 657), ("Mumbai", 524), ("Pune", 660)],
    "Mumbai": [("Ahmedabad", 524), ("Jaipur", 1148), ("Pune", 148), ("Hyderabad", 709)],
    "Pune": [("Mumbai", 148), ("Ahmedabad", 660), ("Hyderabad", 560), ("Bengaluru", 842)],
    "Hyderabad": [("Mumbai", 709), ("Pune", 560), ("Bengaluru", 569), ("Chennai", 627)],
    "Bengaluru": [("Pune", 842), ("Hyderabad", 569), ("Chennai", 346)],
    "Chennai": [("Bengaluru", 346), ("Hyderabad", 627), ("Kolkata", 1660)],
    "Kolkata": [("Lucknow", 991), ("Chennai", 1660)]
}

def dijkstra(graph, start):
    distances = {city: float("inf") for city in graph}
    parent = {city: None for city in graph}

    distances[start] = 0
    pq = [(0, start)]

    while pq:
        current_distance, current_city = heapq.heappop(pq)

        if current_distance > distances[current_city]:
            continue

        for neighbor, weight in graph[current_city]:
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                parent[neighbor] = current_city
                heapq.heappush(pq, (new_distance, neighbor))

    return distances, parent

def get_path(parent, target):
    path = []
    while target is not None:
        path.append(target)
        target = parent[target]
    return path[::-1]


# ---------------- MAIN ----------------

start = input("Enter source city: ")
end = input("Enter destination city: ")

# Validation
if start not in graph or end not in graph:
    print(" Invalid city name. Please check spelling.")
else:
    distances, parent = dijkstra(graph, start)

    if distances[end] == float("inf"):
        print(f"⚠️ No path exists from {start} to {end}")
    else:
        path = get_path(parent, end)

        print("\n Shortest Path Found!")
        print(f"Distance: {distances[end]} km")
        print("Path:", " -> ".join(path))