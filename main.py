import math
def parse_process_file(file_path):
    processes = []

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            pid = int(parts[0])
            arrival_time = int(parts[1])
            priority = int(parts[2])
            burst_sequence = parts[3:]
            parsed_bursts = []
            for burst in burst_sequence:
                burst = burst.strip()
                if burst.startswith("CPU"):
                    # Parse CPU bursts
                    cpu_content = burst[5:-1]
                    if cpu_content:
                        parsed_bursts.append({"type": "CPU", "details": [int(x) if x.isdigit() else x for x in map(str.strip, cpu_content.split(", "))]})
                elif burst.startswith("IO"):
                    # Parse IO bursts
                    io_content = burst[3:-1]
                    if io_content:
                        parsed_bursts.append({"type": "IO", "details": [int(x) if x.isdigit() else x for x in map(str.strip, io_content.split(", "))]})
            processes.append({
                "PID": pid,
                "Arrival Time": arrival_time,
                "Priority": priority,
                "Burst Sequence": parsed_bursts
            })
    return processes
#########################################################################################
def round_robin_scheduling(processes, time_quantum, resources, time):
    queue = []
    waiting_queue = []
    if processes or processes:
        current_PID = processes[0]['PID']
        current_priority = processes[0]['Priority']
        current_arrival = processes[0]['Arrival Time']
    while processes or queue:
        while processes and processes[0]['Arrival Time'] <= time:
            queue.append(processes.pop(0))
        if queue:
            current_process = queue.pop(0)
            if current_PID not in process_dict:
                process_dict[current_PID] = {
                    'Arrival Time': current_process['Arrival Time'],
                    'Arrival Time_withoutIO': current_process['Arrival Time'],
                    'Start Time': None,
                    'End CPU Time': None,
                    'Waiting Time': 0,
                    'Turnaround Time': 0
                }
            burst_sequence = current_process['Burst Sequence']
            if burst_sequence:
                burst = burst_sequence[0]
                burst_type = burst['type']
                burst_details = burst['details']
                i = 0
                if burst_type == "CPU":
                    while i < len(burst_details):
                        if burst_details:
                            if burst_details[0] in resources:
                                resource_value = resources[burst_details[0]]
                                if not resource_value:
                                    waiting_queue.append(current_process)
                                    deadlock_detected, waiting_processes = detect_deadlock(processes, resources,  waiting_queue)
                                    if deadlock_detected:
                                        aborted_process,queue=handle_deadlock(waiting_queue, resources,queue)
                                        for process in queue:
                                            if process['PID'] == aborted_process['PID']:
                                                process['Arrival Time'] += 10
                                                print(f"Aborted process PID {aborted_process['PID']} arrival time updated to {process['Arrival Time']}")
                                                process_dict[aborted_process['PID']]['Arrival Time'] = process['Arrival Time']
                                        aborted_process['Burst Sequence']=burst_sequence
                                        round_robin_scheduling(queue, time_quantum, resources, time)
                                    if not deadlock_detected:
                                          burst_details.pop(0)
                                else:
                                    resources[burst_details[0]] = 0
                                    var=burst_details.pop(0)
                                    if burst_details and burst_details[0] in resources:
                                        next_resource = burst_details[0]
                                        if resources[next_resource] == 0:
                                            waiting_queue.append(current_process)
                                            deadlock_detected, waiting_processes = detect_deadlock(processes, resources,waiting_queue)
                                            if deadlock_detected:
                                                burst['details'].append(var)
                                                aborted_process,queue = handle_deadlock(waiting_queue, resources,queue)
                                                burst['details'].remove(var)
                                                for process in ready_queue:
                                                    if process['PID'] == aborted_process['PID']:
                                                        process['Arrival Time'] += 10
                                                        print(f"Aborted process PID {aborted_process['PID']} arrival time updated to {process['Arrival Time']}")
                                                        process_dict[aborted_process['PID']]['Arrival Time'] = process['Arrival Time']
                                                        break
                                                aborted_process['Burst Sequence'] = burst_sequence

                                                round_robin_scheduling(queue, time_quantum, resources, time)
                                        else:
                                            resources[next_resource] = 0
                                            burst_details.pop(0)
                            burst_time = burst_details[0] if burst_details else None
                            while burst_details and burst_details[0] in ["F[1]", "F[2]"]:
                                burst_time = burst_details[0]
                                if burst_time == "F[1]":
                                    resources['R[1]'] = 1
                                    burst_details.pop(0)
                                elif burst_time == "F[2]":
                                    resources['R[2]'] = 1
                                    burst_details.pop(0)
                            if burst_details:
                                burst_time = burst_details[0]
                                if burst_time is not None:
                                    if burst_time <= time_quantum:
                                        print(f"PID {current_process['PID']} executes CPU burst for {burst_time} units (time: {time} to {time + burst_time})")
                                        burst_details.pop(0)
                                        if burst_sequence:
                                            queue.append(current_process)
                                            if not burst_details:
                                                burst_sequence.pop(0)
                                        time += burst_time
                                        break
                                    else:
                                        print(f"PID {current_process['PID']} executes CPU burst for {time_quantum} units (time: {time} to {time + time_quantum})")
                                        time += time_quantum
                                        burst_details[0] -= time_quantum
                                        queue.append(current_process)
                                        break
                        else:
                            break
                elif burst_type == "IO":
                    io_burst = burst_details[0]
                    io_time = io_burst
                    end_io_time = io_time + time
                    burst_sequence.pop(0)
                    print(f"PID {current_process['PID']} performs IO burst for {io_time} units (time: {time} to {end_io_time})")
                    if current_process and current_process['Burst Sequence']:
                        queue.append(current_process)
                    if queue:
                        if queue[0] != current_process:
                            current_process['Arrival Time'] = end_io_time
                            round_robin_scheduling(queue, time_quantum, resources, time)
                        else:
                            current_process['Arrival Time'] = end_io_time
                            round_robin_scheduling(queue, time_quantum, resources, end_io_time)
                    else:
                        print("Error: ready_queue is empty!")

        else:
            time += 1
#########################################################################################
def simulate_priority_round_robin(processes, time_quantum, time, ready_queue, process_dict, resources):
    processes.sort(key=lambda p: (p['Arrival Time'], p['Priority']))
    completed_processes = []
    waiting_queue = []
    while processes or ready_queue:
        RRlist = []
        while processes and processes[0]['Arrival Time'] <= time:
            ready_queue.append(processes.pop(0))
        ready_queue.sort(key=lambda p: (p['Arrival Time'], p['Priority']))
        if ready_queue:
            current_PID = ready_queue[0]['PID']
            current_priority = ready_queue[0]['Priority']
            current_arrival = ready_queue[0]['Arrival Time']
            for process in ready_queue:
                if process['Priority'] == current_priority and process['Arrival Time'] == current_arrival:
                    RRlist.append(process)
            if len(RRlist) > 1:
                round_robin_scheduling(RRlist, time_quantum, resources, time)
            current_process = ready_queue.pop(0)
            if current_PID not in process_dict:
                process_dict[current_PID] = {
                    'Arrival Time': current_process['Arrival Time'],
                    'Arrival Time_withoutIO': current_process['Arrival Time'],
                    'Start Time': None,
                    'End CPU Time': None,
                    'Waiting Time': 0,  # Initialize Waiting Time to 0
                    'Turnaround Time': 0  # Initialize Turnaround Time to 0
                }
            burst_sequence = current_process['Burst Sequence']
            i = 0
            while i < len(burst_sequence):
                seq = burst_sequence[i]
                burst_type = seq['type']
                burst_details = seq['details']
                if (len(burst_details) == 0):
                    burst_sequence.pop(0)
                    continue
                if burst_type == "CPU":
                    while i < len(burst_details):
                        if burst_details:
                            if burst_details:
                                if burst_details[0] in resources:
                                    resource_value = resources[burst_details[0]]
                                    if not resource_value:
                                        waiting_queue.append(current_process)
                                        deadlock_detected, waiting_processes = detect_deadlock(processes, resources,waiting_queue)
                                        if deadlock_detected:
                                            aborted_process,ready_queue=handle_deadlock(waiting_queue, resources,ready_queue)
                                            for process in ready_queue:
                                                if process['PID'] == aborted_process['PID']:
                                                    process['Arrival Time'] += 10
                                                    print(
                                                        f"Aborted process PID {aborted_process['PID']} arrival time updated to {process['Arrival Time']}")
                                                    process_dict[aborted_process['PID']]['Arrival Time'] = process[
                                                        'Arrival Time']
                                                    break
                                        if not deadlock_detected:
                                            burst_details.pop(0)
                                    else:
                                        resources[burst_details[0]] = 0
                                        burst_details.pop(0)
                                        if burst_details and burst_details[0] in resources:
                                            next_resource = burst_details[0]
                                            if resources[next_resource] == 0:
                                                waiting_queue.append(current_process)
                                                deadlock_detected, waiting_processes = detect_deadlock(processes,resources,waiting_queue)
                                                if deadlock_detected:
                                                    aborted_process,ready_queue=handle_deadlock(waiting_queue, resources,ready_queue)
                                                    for process in ready_queue:
                                                        if process['PID'] == aborted_process['PID']:
                                                            process['Arrival Time'] += 10
                                                            print(
                                                                f"Aborted process PID {aborted_process['PID']} arrival time updated to {process['Arrival Time']}")
                                                            process_dict[aborted_process['PID']]['Arrival Time'] = \
                                                            process[
                                                                'Arrival Time']
                                                            break
                                            else:
                                                resources[next_resource] = 0
                                                burst_details.pop(0)
                            while burst_details and burst_details[0] in ["F[1]", "F[2]"]:
                                burst_time = burst_details[0]
                                if burst_time == "F[1]":
                                    resources['R[1]'] = 1
                                    burst_details.pop(0)
                                elif burst_time == "F[2]":
                                    resources['R[2]'] = 1
                                    burst_details.pop(0)
                            if burst_details:
                                burst_time = burst_details[0]
                            else:
                                burst_time = None
                            if burst_details:
                                if burst_time is not None and burst_time != "F[1]" and burst_time != "F[2]":
                                    process_dict[current_PID]['Start Time'] = time
                                    print(f'CPU burst started at :{time} for {current_PID}')
                                    execution_time = burst_time
                                    time += execution_time
                                    process_dict[current_PID]['End CPU Time'] = time
                                    print(f'CPU burst ended at :{time} for {current_PID}')
                                    burst_details.pop(0)
                                    process_dict[current_PID]['Waiting Time'] = process_dict[current_PID]['Start Time'] - process_dict[current_PID]['Arrival Time']
                                    process_dict[current_PID]['Turnaround Time'] = process_dict[current_PID]['End CPU Time'] - process_dict[current_PID]['Arrival Time_withoutIO']
                        else:
                            break
                elif burst_type == "IO":
                    io_burst = burst_sequence.pop(0)['details']
                    io_time = io_burst[0]
                    end_io_time = io_time + time
                    print(
                        f"PID {current_process['PID']} performs IO burst for {io_time} units (time: {time} to {end_io_time})")
                    while processes and processes[0]['Arrival Time'] <= time:
                        ready_queue.append(processes.pop(0))
                    if not ready_queue:
                        print(f'CPU burst idle from {time} to {end_io_time} for {current_PID}')
                    if len(current_process['Burst Sequence']) > 0:
                        ready_queue.append(current_process)
                    if ready_queue:
                        # Check if the queue contains only the current process
                        if len(ready_queue) == 1 and ready_queue[0]['PID'] == current_process['PID']:
                            # Update the arrival time for the current process
                            ready_queue[0]['Arrival Time'] = end_io_time
                            # Call the function with end_io_time
                            simulate_priority_round_robin(processes, time_quantum, end_io_time, ready_queue,
                                                          process_dict, resources)
                        else:
                            # Update the arrival time for the current process
                            for process in ready_queue:
                                if process['PID'] == current_process['PID']:
                                    process['Arrival Time'] = end_io_time
                                    break
                            # Call the function with the current time
                            process_dict[current_PID]['Arrival Time'] = end_io_time
                            simulate_priority_round_robin(processes, time_quantum, time, ready_queue, process_dict,
                                                          resources)
                    else:
                        print("Error: ready_queue is empty!")
                if not current_process['Burst Sequence']:
                    completed_processes.append(current_process)
        else:
            time += 1
    return process_dict
#########################################################################################
def detect_deadlock(processes, resources, waiting_queue):
    resource_waits = {resource: 0 for resource in resources}
    waiting_processes = set()
    for process in waiting_queue:
        burst_sequence = process['Burst Sequence']
        for burst in burst_sequence:
            if burst['type'] == 'CPU':
                resource = burst['details'][0]
                if resource in resources and resources[resource] == 0:
                    resource_waits[resource] += 1
                    waiting_processes.add(process['PID'])
    for resource, wait_count in resource_waits.items():
        if wait_count > resources[resource]:
            print(f"Deadlock detected on resource {resource}. {wait_count} processes are waiting.")
            return True, waiting_processes
    return False, None
#########################################################################################
def handle_deadlock(waiting_queue, resources,readyq):
    print("Handling deadlock...")
    aborted_process = {}
    while waiting_queue:
        aborted_process = waiting_queue.pop(0)
        readyq.append(aborted_process)
        print(f"Aborting process PID {aborted_process['PID']} to resolve deadlock.")
        for burst in aborted_process['Burst Sequence']:
            if burst['type'] == 'CPU':
                for resource in burst['details']:
                    if resource in resources:
                        resources[resource] = 1
        deadlock_detected, waiting_processes = detect_deadlock([], resources, waiting_queue)
        if not deadlock_detected:
            return aborted_process, readyq
#########################################################################################
file_path = 'processeslist.txt'
processes = parse_process_file(file_path)
time_quantum = 10
time = 0
resources = {
    'R[1]': 1,
    'R[2]': 1,
}
ready_queue = []
process_dict = {p['PID']: {
    'Arrival Time': p['Arrival Time'],
    'Arrival Time_withoutIO': p['Arrival Time'],
    'Start Time': None,
    'End CPU Time': None,
    'Waiting Time': 0,  # Initialize Waiting Time to 0
    'Turnaround Time': 0  # Initialize Turnaround Time to 0
} for p in processes}
process_dict = simulate_priority_round_robin(processes, time_quantum, time, ready_queue, process_dict, resources)
# Calculate total and average waiting and turnaround times
total_waiting_time = sum(p['Waiting Time'] for p in process_dict.values())
total_turnaround_time = sum(p['Turnaround Time'] for p in process_dict.values())
num_processes = len(process_dict)
avg_waiting_time = total_waiting_time / num_processes if num_processes else 0
avg_turnaround_time = total_turnaround_time / num_processes if num_processes else 0
print(f'Total Waiting Time: {total_waiting_time}')
print(f'Total Turnaround Time: {total_turnaround_time}')
print(f'Average Waiting Time: {avg_waiting_time}')
print(f'Average Turnaround Time: {avg_turnaround_time}')