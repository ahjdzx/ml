#!/usr/bin/python3

bytes_data = b'this is a message'
print(type(bytes_data))
print(bytes_data)

# 方法一：
str_data = str(bytes_data, encoding='utf-8')
print(type(str_data))
print(str_data)

# 方法二：
str_data = bytes_data.decode('utf-8')
print(type(str_data))




str_data = 'this is a message'
print(type(str_data))
print(str_data)
# 方法一：
bytes_data = bytes(str_data, encoding='utf-8')
print(type(bytes_data))
print(bytes_data)
# 方法二：
bytes_data = str_data.encode('utf-8')
print(type(bytes_data))
print(bytes_data)
