# Camtrap Data Package Python Library

The Camtrap Data Package Python Library is a Python library for working with the [Camtrap Data Package](https://camtrap-dp.tdwg.org/) version 1.0 format.

### Read an Deployments CSV file

```python
from camtrapdp import Deployment

# Read a deployments CSV file
deployments = Deployment.from_csv('deployments.csv')

# Print the first deployment
print(deployments[0])
```

### Write a Deployments CSV file

```python
from camtrapdp import Deployment

# Create a deployment
deployments = [
    Deployment(...),
    Deployment(...)
]

# Write a deployments CSV file
Deployment.to_csv(deployments, 'deployments.csv')
```
