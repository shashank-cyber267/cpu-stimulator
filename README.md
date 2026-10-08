# CPU Scheduling Algorithm Simulator

A modern, full-stack web application for simulating, visualizing, and comparing CPU scheduling algorithms in Operating Systems.

Built with **Python Flask** for scheduling computations and **Tailwind CSS + Vanilla JavaScript** for an interactive, glassmorphic dark dashboard.

---

## 🌟 Features

- **Interactive Process Input**:
  - Dynamically add, edit, randomize, or delete processes.
  - Configure **Process ID**, **Arrival Time (AT)**, **Burst Time (BT)**, and **Priority**.
  - Configurable **Time Quantum** for Round Robin scheduling.
  - **Quick Presets** (*Standard*, *Idle Gaps*, *Round Robin Demo*, *Priority Demo*) for instant testing.
- **Supported Scheduling Algorithms**:
  1. **FCFS (First-Come, First-Served)** [Non-preemptive]
  2. **SJF (Shortest Job First)** [Non-preemptive]
  3. **SRTF (Shortest Remaining Time First)** [Preemptive SJF]
  4. **Priority Scheduling** [Non-preemptive] (Lower value = Higher Priority)
  5. **Priority Scheduling** [Preemptive]
  6. **Round Robin (RR)** [Preemptive with configurable Time Quantum]
- **Outputs & Visualizations**:
  - **Interactive Gantt Chart**: Timeline with color-coded process blocks, tooltips, segment durations, and explicit **CPU IDLE** intervals.
  - **Performance Metrics Table**: Process-by-process Completion Time (CT), Turnaround Time (TAT), Waiting Time (WT), and Response Time (RT).
  - **KPI Summary Cards**: Average Waiting Time, Average Turnaround Time, Average Response Time, CPU Utilization (%), and Throughput.
  - **Side-by-Side Comparison Mode**: Runs all algorithms on the same process dataset and generates a comparison table highlighting optimal metrics alongside individual timelines.

---

## 📁 Project Structure

```
cpu_scheduler/
├── app.py                  # Flask backend with scheduling algorithms & REST API
├── test_scheduler.py       # Unit test suite verifying scheduling logic & edge cases
├── templates/
│   └── index.html          # Modern dashboard UI with Tailwind CSS & Lucide Icons
├── static/
│   ├── css/
│   │   └── main.css        # Custom styles, animations, and Gantt charts
│   └── js/
│       └── app.js          # Interactive UI logic, Gantt rendering & API calls
└── README.md               # Documentation and setup instructions
```

---

## 🚀 Setup & Execution

### 1. Prerequisites
- Python 3.8+ (or Python 3.10+ recommended)

### 2. Install Dependencies
```bash
pip install flask
```

### 3. Run the Application
```bash
python app.py
# Or on Windows with Python launcher:
py -3 app.py
```

### 4. Access the Simulator
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 🧪 Running Unit Tests
To verify all scheduling algorithms against edge cases (such as CPU idle gaps and tie-breakers):
```bash
python test_scheduler.py
# Or
py -3 test_scheduler.py
```

---

## 📊 Formulas Used

$$\text{Turnaround Time (TAT)} = \text{Completion Time (CT)} - \text{Arrival Time (AT)}$$

$$\text{Waiting Time (WT)} = \text{Turnaround Time (TAT)} - \text{Burst Time (BT)}$$

$$\text{Response Time (RT)} = \text{First CPU Start Time} - \text{Arrival Time (AT)}$$

$$\text{CPU Utilization (\%)} = \left( \frac{\sum \text{Burst Times}}{\text{Total Schedule Duration}} \right) \times 100$$
