import csv


def telnet_leases_to_csv():
    """Read the telnet static leases file and create a CSV file of host info."""
    with open("input/telnet-static-leases.txt", encoding="utf-8") as input_file:
        with open("input/host-details-table.csv", "w", encoding="utf-8") as output_file:
            writer = csv.writer(output_file)
            writer.writerow(["mac", "host_name", "ip", "time"])
            for line in input_file:
                if not line.strip():
                    continue
                terms = [term.split("=") for term in line.split()]
                for term in terms:
                    writer.writerow(term)


def create_static_leases_str():
    with open("input/host-details-table.csv", "r", encoding="utf-8") as in_file:
        # stripped = (line.strip() for line in in_file)
        file = in_file
        # lines = (line.split() for line in file if line)
        lines_store = list(line.split() for line in file if line)
        lines_store.sort(key=get_last_octet)
        # print(lines)
        with open(
            "output/static-leases-op-string.txt", "w", encoding="utf-8"
        ) as out_file:
            # writer = csv.writer(out_file)
            # writer.writerow(('mac', 'host_name', 'ip', 'time'))
            # lines.next()
            staticLeaseStr = ""
            # number of host entries
            # hostEntries =sum(1 for dummy in lines_store)
            hostEntries = lines_store.__len__() - 1
            # hostEntries = 44
            # rrr = print("nvram set static_leasenum=", hostEntries, "", sep="")
            out_file.write("nvram set static_leasenum=" + str(hostEntries) + "\n")
            print('nvram set static_leases="', end="")
            out_file.write('nvram set static_leases="')
            # reset lines pointer
            # file = in_file
            # lines_store = (line.split() for line in file if line)
            # lines.seek(0)
            # sort the list using last octet of ip

            for row in lines_store:
                # print(row)
                idx = lines_store.index(row)
                terms = (term.split(",") for term in row if term)
                # nvram set static_leasenum=38
                # nvram set static_leases="00:00:00:00:00:00:=Comp01=192.168.1.101= \
                # 00:00:00:00:00:00:=Comp02=192.168.1.102= \
                # 00:00:00:00:00:00:=Comp03=192.168.1.103= \
                # ...
                # 00:00:00:00:00:00:=Comp26=192.168.1.138="
                for term in terms:
                    mac = term.pop(0)
                    if mac == "mac" or mac == "MAC":
                        staticLeaseStr = ""
                        continue
                    host_name = term.pop(0)
                    ip = term.pop(0)
                    time = term.pop(0)
                    staticLeaseItem = (
                        mac + "=" + host_name + "=" + ip + "=" + time + " \\\n"
                    )

                    # if last row, format diff ending
                    if idx == hostEntries:
                        staticLeaseItem = (
                            mac + "=" + host_name + "=" + ip + "=" + time + '"'
                        )
                    # staticLeaseStr = staticLeaseStr + staticLeaseItem
                    staticLeaseStr = staticLeaseItem
                if staticLeaseStr:
                    print(staticLeaseStr, end="")
                    out_file.write(staticLeaseStr)
                    # print("\\")
                    # print(mac,host_name,ip,time)

                    # writer.writerow(term)
            print("")
            out_file.write("\n")


def create_custom_list():
    with open("input/host-details-table.csv", "r", encoding="utf-8") as in_file:
        file = in_file
        lines_store = list(line.split() for line in file if line)
        # add custom hosts for pihole use
        #read in additional pihole hosts
        with open("input/additional-pihole.txt", encoding="utf-8") as input_file:
            # add lines to lines_store list
            lines_store2 = list(line.split() for line in input_file if line)
            # for line in input_file:
            #     if not line.strip():
            #         continue
            #     terms = [term.split("=") for term in line.split()]
            #     for term in terms:
            #         lines_store.append(term)
            # add lines_store2 to lines_store list
        lines_store.extend(lines_store2)
            # lines_store..extend(lines_store2)
        # sort the list using last octet of ip

        lines_store.sort(key=get_last_octet)

        with open("output/custom.list", "w", encoding="utf-8") as out_file:

            staticLeaseStr = ""

            domain = "lan"

            for row in lines_store:

                terms = (term.split(",") for term in row if term)

                for term in terms:
                    mac = term.pop(0)
                    if mac == "mac" or mac == "MAC":
                        staticLeaseStr = ""
                        continue
                    host_name = term.pop(0)
                    ip = term.pop(0)
                    # time = term.pop(0)
                    customListItem = ip + " " + host_name + "." + domain + "\n"

                    staticLeaseStr = customListItem
                if staticLeaseStr:
                    print(staticLeaseStr, end="")
                    out_file.write(staticLeaseStr)

            print("")
            out_file.write("\n")


def get_last_octet(e):
    """
    Returns the last octet of the IP address in the given tuple `e`. If the last character of the last octet is a comma, it is removed.

    Args:
        e (tuple): A tuple containing an IP address and additional information.

    Returns:
        int: The last octet of the IP address as an integer.
    """
    # get last octet of ip
    order = e[0].split(".")[-1]
    # if last char in order is a comma remove it
    intorder = 0
    if order[-1] == ",":
        intorder = int(order[:-1])
    return intorder


telnet_leases_to_csv()
create_static_leases_str()
create_custom_list()
