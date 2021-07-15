import os 
import boto3

# Fetch instance wise statues from AWS console
client = boto3.client("ec2", region_name='us-east-2')
dict_ = client.describe_volumes()
status = {}

for item in dict_["Volumes"]:
    status[item['VolumeId']] = {'volumetype': item['VolumeType'], 
                                'ioops': item.get('Iops', "NULL"), 
                                'size': item['Size']}

print(status)

# Reading data from customer request 
f = open("customer_mainfile.txt", "r").readlines()
customer_input = []


for line in f:
    input_ = {}
    input_["--volume-id"] = line.replace("\n", "")
    customer_input.append(input_)


print("Checking current volumeType status of instances")
for item in customer_input:
    volume_id = item["--volume-id"]
    if volume_id in status:

        current_volume_type_status = status[volume_id]['volumetype']
        current_value_of_size = status[volume_id]['size']

        if current_value_of_size <= 1000:
            new_value_of_ioops = 3000
        else:
            new_value_of_ioops = min(current_value_of_size * 3, 16000)


        if current_volume_type_status == 'gp2':
            print(f"Status : {volume_id} {status[volume_id]['volumetype']} {status[volume_id]['ioops']} new ioops value {new_value_of_ioops}") 
            print(f"Changing volume type of volume_id : {volume_id} current size : {current_value_of_size} new value of ioops : {new_value_of_ioops}")
            command_to_run = f"aws ec2 modify-volume --volume-type gp3 --volume-id {volume_id} --iops {new_value_of_ioops}"
            print(f"Running : {command_to_run}")
            os.system(command_to_run)
            print("\n")
            




# print(customer_input)

"""
for line in f:
    temp = line.split()
    input_ = {}
    for index in range(len(temp) - 1):
        if '--' in temp[index]:
            item1 = temp[index]
            item2 = temp[index+1]
            input_[item1] = item2
    customer_input.append(input_)
print(customer_input)
"""


# print("Checking current volumeType status of instances")
# for item in customer_input:
#     volume_id = item["--volume-id"]
#     #print(volume_id)
#     if volume_id in status:
#         print(f"Status : {volume_id} {status[volume_id]['volumetype']} {status[volume_id]['ioops']}") 




