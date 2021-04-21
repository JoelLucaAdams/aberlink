# Using shelve in Python

## Reviewing data in file

```python
import shelve

file = shelve.open("/home/joa38/aberlink/src/AberLinkDiscord/shelve_file")
my_keys = list(file.keys())
for key in my_keys:
    print(key, file[key])
```

## Deleting keys from file

```python
import shelve

file = shelve.open("/home/joa38/aberlink/src/AberLinkDiscord/shelve_file")
del file["<key_value>"]
```
