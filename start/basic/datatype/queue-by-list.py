#!/usr/bin/python3
from collections import deque

queue = deque(["Eric", "John", "Michael"])
queue.append("Terry")           # Terry arrives
queue.append("Graham")          # Graham arrives

queue.popleft()                 # The first to arrive now leaves
queue.popleft()                 # The second to arrive now leaves

print(queue)