import re

def read_trace(filename):
    ''' Open the file and return its raw lines '''
    with open(filename, 'r') as file:
        raw_files = file.readlines()

    return raw_files

def main():
    lines = read_trace('my_trace.csv')
    # your code here

    line_lst = []
    for i in range(len(lines)):
        lines[i].strip('"')
        line = lines[i].split(',')
        line_lst.append(line)

    count_ip = num_unique_IP(line_lst)
    protocols = unique_protocols(line_lst)
    total_bytes = bytes_captured(line_lst)
    median = median_bytes(line_lst)


    # you may write other functions but keep this same structure to help me
    # test your solution

    # print your results using the following
    print("Number of unique IP addresses:", count_ip)
    print("Unique protocols observed:", protocols)
    print("Number of packets captured:", len(line_lst)-1)
    print("Total bytes captured:", total_bytes)
    print("Average number of bytes per packet:", total_bytes//(len(line_lst)-1))
    print("Median bytes per packet:", median)
    
def num_unique_IP(lines):
    u_ips = []
    for i in range(len(lines[1:])):
        if i == 0:
            continue
        if lines[i][2] not in u_ips:
            u_ips.append(lines[i][2])
    return len(u_ips)

def unique_protocols(lines):
    u_protocols = ""
    for i in range(len(lines[1:])):
        if i == 0:
            continue
        if lines[i][4] not in u_protocols:
            u_protocols += (lines[i][4]+",")
    return u_protocols[:-1].replace('"', "")


def bytes_captured(lines):
    total = 0
    for line in lines[1:]:
        total += (int(line[5].strip('"')))
    return total


def median_bytes(lines):
    sort = []
    for line in lines[1:]:
        sort.append(int(line[5].strip('"')))
    sort.sort()
    return (sort[len(sort)//2])

if __name__ == '__main__':
    main()
