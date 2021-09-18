import matplotlib.pyplot as plt
'''
Standard markers and colors
'''

markers = ['o', '^', 's', '*', 'D']
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

def getMarker(index):
    return markers[index % len(markers)]

def getColor(index):
    return colors[index // len(markers)]