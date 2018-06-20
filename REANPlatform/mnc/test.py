import re
input_data = 'default_12345'
data = re.findall(r'-?\d+\.?\d*',input_data)
print("Data value::")
print(data)