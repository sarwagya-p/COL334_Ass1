import argparse
import subprocess
import re

def getTracerouteArgs():
    argParser = argparse.ArgumentParser(description="implements traceroute using ping")

    argParser.add_argument("destination")
    argParser.add_argument("-6", "--ipv6", action="store_true")
    argParser.add_argument("-4", "--ipv4", action="store_true")

    argParser.add_argument("-m", "--max_ttl", action="store", default=30, type=int)
    argParser.add_argument("-q", "--nqueries", action="store", default='3', type=str)
    args = argParser.parse_args()

    return args

def outputStatus(output):
    if output.find("TTL expired in transit.") != -1:
        return "expired"
    
    if output.find("time=") != -1:
        return "reached"
    
    return "timed out"


def getIP(output):
    pattern = r"Reply from (?P<IP>\S*)"
    match = re.findall(pattern, output)

    if not match:
        return None
    return match[0][:-1]

def getLatency(output):
    match = re.findall(r"time=(\d)+ms", output)
    if not match:
        return match
    return match[0]+"ms"

def pingCall(args, ttl):
    command = ["ping", '-i', str(ttl), '-n', '1', args.destination]
    if args.ipv4:
        command.append('-4')
    elif args.ipv6:
        command.append('-6')

    output = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\r\n")[2]
    if outputStatus(output) == 'timed out':
        return ('timed out', "Request timed out", ['*']*int(args.nqueries))
    
    transitIP = getIP(output)

    command = ["ping", '-n', args.nqueries, transitIP]
    timeOutput = subprocess.run(command, stdout=subprocess.PIPE).stdout.decode("utf-8").split("\r\n")[2:-6]
    times = []

    for line in timeOutput:
        if outputStatus(line) == 'timed out':
            return ('timed out', transitIP, ['*']*int(args.nqueries))
        times.append(getLatency(line))
    
    return (outputStatus(output), transitIP, times)

def traceroute():
    args = getTracerouteArgs()
    if (args.ipv4 and args.ipv6):
        raise "Could not resolve IP format - too many arguments"

    ttl = 1
    i = 1

    print(f"Tracing route to {args.destination}, sending {args.nqueries} packets with max hops {args.max_ttl}")
    
    while ttl <= args.max_ttl:
        print()
        print(f"{i}.", end="\t")
        i += 1
        callOutput = pingCall(args, ttl)
        ttl += 1

        print('\t'.join(callOutput[2]), end='\t')
        print(callOutput[1], end='\t')

        if (callOutput[0] == 'reached'):
            break


if __name__ == "__main__":
    traceroute()