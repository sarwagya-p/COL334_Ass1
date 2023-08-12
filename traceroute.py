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


def pingCall(args, ttl):
    command = ["ping", '-i', str(ttl), '-n', args.nqueries, args.destination]

    if args.ipv4:
        command.append('-4')
    elif args.ipv6:
        command.append('-6')

    output = subprocess.run(command, stdout=subprocess.PIPE)
    return output.stdout.decode("utf-8").split("\r\n")[2:-4]

def outputStatus(output):
    if output.find("TTL expired in transit.") != -1:
        return "expired"
    
    if output.find("time=") != -1:
        return "reached"
    
    return "timed out"


def getIP(output):
    pattern = r"Reply from (?P<IP>\S*) *"
    match = re.compile(pattern).match(output)

    if match is None:
        return None
    return match.groupdict()["IP"][:-1]

def getLatency(output):
    pattern = r"*?time=(?P<time>/d+)*"
    match = re.compile(pattern).match(output)

    if match is None:
        return None 
    return match.groupdict()["time"]


def traceroute():
    args = getTracerouteArgs()
    if (args.ipv4 and args.ipv6):
        raise "Could not resolve IP format - too many arguments"

    transitIPs = []
    ttl = 1
    i = 1

    print(f"Tracing route to {args.destination}, sending {args.nqueries} packets with max hops {args.max_ttl}")
    
    while ttl <= args.max_ttl:
        print()
        print(f"{i}.", end="\t")
        i += 1
        callOutput = pingCall(args, ttl)
        IPs = []

        for packet_output in callOutput:
            if outputStatus(packet_output) == "timed out":
                print("Request timed out.", end="\t")
                break
            elif outputStatus(packet_output) == "reached":
                IPs.append(getIP(packet_output))
                ttl = args.max_ttl+1
            
            else:
                IPs.append(getIP(packet_output))
        else:
            ttl += 1
            for ip in IPs:
                print(ip, end="\t")


if __name__ == "__main__":
    traceroute()