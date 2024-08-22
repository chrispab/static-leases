import csv

with open('telnet-static-leases.txt', 'r') as in_file:
    # stripped = (line.strip() for line in in_file)
    lines = (line.split() for line in in_file if line)
    # print(lines)
    with open('host-details-table.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerow(('mac', 'host_name', 'ip', 'time'))
        for row in lines:
            # print(row)
            terms = (term.split('=') for term in row if term)
            for term in terms:
                print(term)
                writer.writerow(term)
