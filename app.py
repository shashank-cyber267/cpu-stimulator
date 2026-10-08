from flask import Flask, render_template, request, jsonify
import copy

app = Flask(__name__)

# ==========================================
# CPU Scheduling Algorithms Implementation
# ==========================================

def schedule_fcfs(processes):
    """First-Come, First-Served (Non-preemptive)"""
    procs = sorted(copy.deepcopy(processes), key=lambda p: (p['arrival'], p['id']))
    time = 0
    schedule = []
    
    for p in procs:
        if time < p['arrival']:
            schedule.append({
                'pid': 'IDLE',
                'start': time,
                'end': p['arrival'],
                'burst': p['arrival'] - time,
                'is_idle': True
            })
            time = p['arrival']
        start = time
        end = start + p['burst']
        schedule.append({
            'pid': p['id'],
            'start': start,
            'end': end,
            'burst': p['burst'],
            'is_idle': False
        })
        time = end
    return schedule

def schedule_sjf_non_preemptive(processes):
    """Shortest Job First (Non-preemptive)"""
    procs = copy.deepcopy(processes)
    schedule = []
    time = 0
    completed = []
    total_procs = len(procs)
    
    while len(completed) < total_procs:
        available = [p for p in procs if p['arrival'] <= time and p['id'] not in completed]
        if not available:
            # CPU is idle until next process arrives
            next_arrival = min(p['arrival'] for p in procs if p['id'] not in completed)
            schedule.append({
                'pid': 'IDLE',
                'start': time,
                'end': next_arrival,
                'burst': next_arrival - time,
                'is_idle': True
            })
            time = next_arrival
            continue
        
        # Select shortest burst time (tie break by arrival time, then id)
        p = min(available, key=lambda x: (x['burst'], x['arrival'], x['id']))
        start = time
        end = start + p['burst']
        schedule.append({
            'pid': p['id'],
            'start': start,
            'end': end,
            'burst': p['burst'],
            'is_idle': False
        })
        time = end
        completed.append(p['id'])
        
    return schedule

def schedule_srtf_preemptive(processes):
    """Shortest Remaining Time First (Preemptive SJF)"""
    procs = copy.deepcopy(processes)
    n = len(procs)
    remaining = {p['id']: p['burst'] for p in procs}
    time = 0
    completed = 0
    raw_timeline = []
    
    while completed < n:
        available = [p for p in procs if p['arrival'] <= time and remaining[p['id']] > 0]
        if not available:
            # Advance to next arrival
            uncompleted = [p['arrival'] for p in procs if remaining[p['id']] > 0]
            next_arr = min(uncompleted)
            for t in range(time, next_arr):
                raw_timeline.append(('IDLE', True))
            time = next_arr
            continue
        
        # Pick process with minimum remaining time
        curr = min(available, key=lambda x: (remaining[x['id']], x['arrival'], x['id']))
        raw_timeline.append((curr['id'], False))
        remaining[curr['id']] -= 1
        time += 1
        
        if remaining[curr['id']] == 0:
            completed += 1
            
    return compress_timeline(raw_timeline)

def schedule_priority_non_preemptive(processes):
    """Priority Scheduling (Non-preemptive, Lower value = Higher Priority)"""
    procs = copy.deepcopy(processes)
    schedule = []
    time = 0
    completed = []
    total_procs = len(procs)
    
    while len(completed) < total_procs:
        available = [p for p in procs if p['arrival'] <= time and p['id'] not in completed]
        if not available:
            next_arrival = min(p['arrival'] for p in procs if p['id'] not in completed)
            schedule.append({
                'pid': 'IDLE',
                'start': time,
                'end': next_arrival,
                'burst': next_arrival - time,
                'is_idle': True
            })
            time = next_arrival
            continue
        
        # Lowest priority number = highest priority
        p = min(available, key=lambda x: (x['priority'], x['arrival'], x['id']))
        start = time
        end = start + p['burst']
        schedule.append({
            'pid': p['id'],
            'start': start,
            'end': end,
            'burst': p['burst'],
            'is_idle': False
        })
        time = end
        completed.append(p['id'])
        
    return schedule

def schedule_priority_preemptive(processes):
    """Priority Scheduling (Preemptive, Lower value = Higher Priority)"""
    procs = copy.deepcopy(processes)
    n = len(procs)
    remaining = {p['id']: p['burst'] for p in procs}
    time = 0
    completed = 0
    raw_timeline = []
    
    while completed < n:
        available = [p for p in procs if p['arrival'] <= time and remaining[p['id']] > 0]
        if not available:
            uncompleted = [p['arrival'] for p in procs if remaining[p['id']] > 0]
            next_arr = min(uncompleted)
            for t in range(time, next_arr):
                raw_timeline.append(('IDLE', True))
            time = next_arr
            continue
        
        curr = min(available, key=lambda x: (x['priority'], x['arrival'], x['id']))
        raw_timeline.append((curr['id'], False))
        remaining[curr['id']] -= 1
        time += 1
        
        if remaining[curr['id']] == 0:
            completed += 1
            
    return compress_timeline(raw_timeline)

def schedule_round_robin(processes, quantum):
    """Round Robin (Preemptive with Quantum)"""
    procs = sorted(copy.deepcopy(processes), key=lambda p: (p['arrival'], p['id']))
    remaining = {p['id']: p['burst'] for p in procs}
    
    time = 0
    schedule = []
    queue = []
    arrived = set()
    total_procs = len(procs)
    completed_count = 0
    
    # Enqueue processes that arrive at time 0
    for p in procs:
        if p['arrival'] <= time:
            queue.append(p['id'])
            arrived.add(p['id'])
            
    while completed_count < total_procs:
        if not queue:
            # Find next arriving process
            uncompleted = [p for p in procs if remaining[p['id']] > 0 and p['id'] not in arrived]
            if not uncompleted:
                break
            next_arrival = min(p['arrival'] for p in uncompleted)
            schedule.append({
                'pid': 'IDLE',
                'start': time,
                'end': next_arrival,
                'burst': next_arrival - time,
                'is_idle': True
            })
            time = next_arrival
            for p in procs:
                if p['arrival'] <= time and p['id'] not in arrived and remaining[p['id']] > 0:
                    queue.append(p['id'])
                    arrived.add(p['id'])
            continue
            
        pid = queue.pop(0)
        exec_time = min(quantum, remaining[pid])
        start = time
        end = start + exec_time
        
        schedule.append({
            'pid': pid,
            'start': start,
            'end': end,
            'burst': exec_time,
            'is_idle': False
        })
        
        remaining[pid] -= exec_time
        time = end
        
        # Add processes that arrived during this quantum execution window
        for p in procs:
            if p['arrival'] <= time and p['id'] not in arrived and remaining[p['id']] > 0 and p['id'] != pid:
                queue.append(p['id'])
                arrived.add(p['id'])
                
        # If the current process still has remaining execution, add it to back of queue
        if remaining[pid] > 0:
            queue.append(pid)
        else:
            completed_count += 1
            
    return schedule

def compress_timeline(raw_timeline):
    """Compress unit-step timeline into start-end blocks"""
    if not raw_timeline:
        return []
    schedule = []
    current_pid, is_idle = raw_timeline[0]
    start = 0
    
    for i in range(1, len(raw_timeline)):
        pid, idle = raw_timeline[i]
        if pid != current_pid:
            schedule.append({
                'pid': current_pid,
                'start': start,
                'end': i,
                'burst': i - start,
                'is_idle': is_idle
            })
            current_pid = pid
            is_idle = idle
            start = i
            
    schedule.append({
        'pid': current_pid,
        'start': start,
        'end': len(raw_timeline),
        'burst': len(raw_timeline) - start,
        'is_idle': is_idle
    })
    return schedule

# ==========================================
# Performance Metrics Computation
# ==========================================

def compute_metrics(processes, schedule):
    """Calculate CT, TAT, WT, RT and summary stats"""
    completion_times = {}
    first_response_times = {}
    
    for entry in schedule:
        if entry.get('is_idle'):
            continue
        pid = entry['pid']
        if pid not in first_response_times:
            first_response_times[pid] = entry['start']
        completion_times[pid] = entry['end']
        
    metrics = []
    total_wt = 0
    total_tat = 0
    total_rt = 0
    
    for p in processes:
        pid = p['id']
        ct = completion_times.get(pid, 0)
        tat = ct - p['arrival']
        wt = tat - p['burst']
        rt = first_response_times.get(pid, p['arrival']) - p['arrival']
        
        wt = max(0, wt)
        tat = max(0, tat)
        rt = max(0, rt)
        
        total_wt += wt
        total_tat += tat
        total_rt += rt
        
        metrics.append({
            'pid': pid,
            'arrival': p['arrival'],
            'burst': p['burst'],
            'priority': p.get('priority', 0),
            'completion_time': ct,
            'turnaround_time': tat,
            'waiting_time': wt,
            'response_time': rt
        })
        
    n = len(processes) if processes else 1
    avg_wt = total_wt / n
    avg_tat = total_tat / n
    avg_rt = total_rt / n
    
    total_schedule_time = schedule[-1]['end'] if schedule else 0
    total_burst_time = sum(p['burst'] for p in processes)
    cpu_utilization = (total_burst_time / total_schedule_time * 100) if total_schedule_time > 0 else 0
    throughput = (len(processes) / total_schedule_time) if total_schedule_time > 0 else 0
    
    return {
        'metrics': metrics,
        'average_waiting_time': round(avg_wt, 2),
        'average_turnaround_time': round(avg_tat, 2),
        'average_response_time': round(avg_rt, 2),
        'cpu_utilization': round(cpu_utilization, 2),
        'throughput': round(throughput, 4),
        'total_time': total_schedule_time
    }

# ==========================================
# Routes
# ==========================================

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.get_json() or {}
        raw_processes = data.get('processes', [])
        algorithm = data.get('algorithm', 'FCFS')
        quantum = int(data.get('quantum', 2))
        
        if not raw_processes:
            return jsonify({'error': 'No processes provided.'}), 400
            
        processes = []
        for i, p in enumerate(raw_processes):
            pid = str(p.get('id', f'P{i+1}')).strip() or f'P{i+1}'
            arrival = int(p.get('arrival', 0))
            burst = int(p.get('burst', 1))
            priority = int(p.get('priority', 0))
            if burst <= 0:
                return jsonify({'error': f'Burst time for process {pid} must be greater than 0.'}), 400
            if arrival < 0:
                return jsonify({'error': f'Arrival time for process {pid} cannot be negative.'}), 400
            processes.append({
                'id': pid,
                'arrival': arrival,
                'burst': burst,
                'priority': priority
            })
            
        if quantum <= 0:
            quantum = 2
            
        if algorithm == 'FCFS':
            schedule = schedule_fcfs(processes)
        elif algorithm == 'SJF':
            schedule = schedule_sjf_non_preemptive(processes)
        elif algorithm == 'SRTF':
            schedule = schedule_srtf_preemptive(processes)
        elif algorithm == 'Priority':
            schedule = schedule_priority_non_preemptive(processes)
        elif algorithm == 'Priority_Preemptive':
            schedule = schedule_priority_preemptive(processes)
        elif algorithm == 'RR':
            schedule = schedule_round_robin(processes, quantum)
        else:
            return jsonify({'error': f'Unknown algorithm: {algorithm}'}), 400
            
        stats = compute_metrics(processes, schedule)
        
        return jsonify({
            'success': True,
            'algorithm': algorithm,
            'schedule': schedule,
            'metrics': stats['metrics'],
            'average_waiting_time': stats['average_waiting_time'],
            'average_turnaround_time': stats['average_turnaround_time'],
            'average_response_time': stats['average_response_time'],
            'cpu_utilization': stats['cpu_utilization'],
            'throughput': stats['throughput'],
            'total_time': stats['total_time']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/simulate-all', methods=['POST'])
def simulate_all():
    """Simulate all algorithms simultaneously for comprehensive comparison"""
    try:
        data = request.get_json() or {}
        raw_processes = data.get('processes', [])
        quantum = int(data.get('quantum', 2))
        
        if not raw_processes:
            return jsonify({'error': 'No processes provided.'}), 400
            
        processes = []
        for i, p in enumerate(raw_processes):
            pid = str(p.get('id', f'P{i+1}')).strip() or f'P{i+1}'
            arrival = int(p.get('arrival', 0))
            burst = int(p.get('burst', 1))
            priority = int(p.get('priority', 0))
            processes.append({
                'id': pid,
                'arrival': arrival,
                'burst': burst,
                'priority': priority
            })
            
        algos = {
            'FCFS': ('First-Come, First-Served', schedule_fcfs(processes)),
            'SJF': ('Shortest Job First (Non-preemptive)', schedule_sjf_non_preemptive(processes)),
            'SRTF': ('Shortest Remaining Time First (Preemptive)', schedule_srtf_preemptive(processes)),
            'Priority': ('Priority (Non-preemptive)', schedule_priority_non_preemptive(processes)),
            'Priority_Preemptive': ('Priority (Preemptive)', schedule_priority_preemptive(processes)),
            'RR': (f'Round Robin (Quantum={quantum})', schedule_round_robin(processes, quantum))
        }
        
        results = {}
        for key, (label, sched) in algos.items():
            stats = compute_metrics(processes, sched)
            results[key] = {
                'label': label,
                'schedule': sched,
                'metrics': stats['metrics'],
                'average_waiting_time': stats['average_waiting_time'],
                'average_turnaround_time': stats['average_turnaround_time'],
                'average_response_time': stats['average_response_time'],
                'cpu_utilization': stats['cpu_utilization'],
                'throughput': stats['throughput'],
                'total_time': stats['total_time']
            }
            
        return jsonify({'success': True, 'results': results})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
