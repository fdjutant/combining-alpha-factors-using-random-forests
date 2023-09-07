import numpy as np

def sigmoid_fn(x):
    return 1 / (1 + np.exp(-x))

def simple_entropy_fn(m,n):
    sum = m + n
    return (-m * np.log2(m/sum) - n * np.log2(n/sum)) / (m+n)

def entropy_fn(event):
    
    entropy = 0
    total_event = sum(event)
    for i in range(len(event)):
        p = event[i] / total_event
        entropy += -p * np.log2(p)

    return entropy

print(simple_entropy_fn(4,10))
print(entropy_fn([8, 3, 2]))
