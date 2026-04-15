"""
OS Teaching & Learning Platform — v2.0
========================================
Upgraded complete platform covering the full OS syllabus.
Run with: streamlit run app.py

Dependencies:
    pip install streamlit matplotlib psutil numpy pandas
"""

import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
import psutil
import time

# ═════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG & THEME
# ═════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="OS Teaching Platform",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded",
)

ACCENT     = "#4F8EF7"
ACCENT2    = "#F7844F"
BG_CARD    = "#1E2330"
BG_DARK    = "#141824"
TEXT_LIGHT = "#E8EAF0"
SUCCESS    = "#4CAF50"
WARNING    = "#FFC107"
DANGER     = "#F44336"
PURPLE     = "#9C27B0"
TEAL       = "#00BCD4"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

  html, body, [class*="css"] {{
      font-family: 'DM Sans', sans-serif;
      background-color: {BG_DARK};
      color: {TEXT_LIGHT};
  }}

  /* Sidebar */
  section[data-testid="stSidebar"] {{
      background: linear-gradient(180deg, #1a1f2e 0%, #0f1319 100%);
      border-right: 1px solid #2a3044;
  }}
  section[data-testid="stSidebar"] .stRadio label {{
      font-size: 13px; color: {TEXT_LIGHT};
  }}

  /* Cards */
  .os-card {{
      background: {BG_CARD}; border: 1px solid #2a3044;
      border-radius: 12px; padding: 20px 24px;
      margin-bottom: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);
  }}
  .os-card-accent  {{ border-left: 4px solid {ACCENT}; }}
  .os-card-warning {{ border-left: 4px solid {WARNING}; }}
  .os-card-success {{ border-left: 4px solid {SUCCESS}; }}
  .os-card-danger  {{ border-left: 4px solid {DANGER}; }}
  .os-card-purple  {{ border-left: 4px solid {PURPLE}; }}
  .os-card-teal    {{ border-left: 4px solid {TEAL}; }}

  /* Typography */
  .hero-title {{
      font-family: 'Space Mono', monospace; font-size: 2.4rem; font-weight: 700;
      background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT2} 100%);
      -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2;
  }}
  .section-title {{
      font-family: 'Space Mono', monospace; font-size: 1rem; color: {ACCENT};
      letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px;
  }}
  .slide-title {{
      font-family: 'Space Mono', monospace; font-size: 1.45rem; color: {TEXT_LIGHT};
      border-bottom: 2px solid {ACCENT}; padding-bottom: 8px; margin-bottom: 16px;
  }}
  .tag {{
      display: inline-block; background: rgba(79,142,247,0.15); color: {ACCENT};
      border: 1px solid rgba(79,142,247,0.3); border-radius: 20px;
      padding: 2px 12px; font-size: 12px; margin: 2px; font-family: 'Space Mono', monospace;
  }}
  .tag-orange {{
      display: inline-block; background: rgba(247,132,79,0.15); color: {ACCENT2};
      border: 1px solid rgba(247,132,79,0.3); border-radius: 20px;
      padding: 2px 12px; font-size: 12px; margin: 2px; font-family: 'Space Mono', monospace;
  }}
  .analogy-box {{
      background: rgba(247,132,79,0.1); border: 1px solid rgba(247,132,79,0.3);
      border-radius: 8px; padding: 12px 16px; margin: 10px 0; font-style: italic;
  }}
  .teacher-box {{
      background: rgba(76,175,80,0.08); border: 1px dashed rgba(76,175,80,0.4);
      border-radius: 8px; padding: 12px 16px; margin: 10px 0;
  }}
  .formula-box {{
      background: rgba(79,142,247,0.08); border: 1px solid rgba(79,142,247,0.25);
      border-radius: 8px; padding: 12px 18px; margin: 10px 0;
      font-family: 'Space Mono', monospace; font-size: 0.95rem;
  }}
  .mistake-box {{
      background: rgba(244,67,54,0.08); border: 1px solid rgba(244,67,54,0.3);
      border-radius: 8px; padding: 12px 16px; margin: 10px 0;
  }}
  .sim-link-box {{
      background: rgba(0,188,212,0.08); border: 1px solid rgba(0,188,212,0.3);
      border-radius: 8px; padding: 10px 16px; margin: 10px 0;
  }}
  /* Always-on large font mode */
  p, li, td, th {{ font-size: 1.08rem !important; line-height: 1.85 !important; }}
  .slide-title {{ font-size: 2rem !important; }}
  /* Streamlit overrides */
  .stButton > button {{
      background: linear-gradient(135deg, {ACCENT} 0%, #3a6fd8 100%); color: white;
      border: none; border-radius: 8px; padding: 8px 20px;
      font-family: 'DM Sans', sans-serif; font-weight: 500; transition: opacity 0.2s;
  }}
  .stButton > button:hover {{ opacity: 0.85; }}
  .stSelectbox > div > div,
  .stTextInput > div > div > input,
  .stNumberInput > div > div > input {{
      background: #1a1f2e !important; border: 1px solid #2a3044 !important;
      color: {TEXT_LIGHT} !important; border-radius: 8px !important;
  }}
  div[data-testid="stExpander"] {{
      background: {BG_CARD}; border: 1px solid #2a3044; border-radius: 10px;
  }}
  hr {{ border-color: #2a3044; }}
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═════════════════════════════════════════════════════════════════════════════

def init_state():
    defaults = {
        "learn_topic": 0, "learn_slide": 0,
        "active_module": "🏠 Home",
        # quiz state
        "quiz_answers": {},   # key: (topic_name, q_idx) → chosen option index
        "quiz_submitted": {}, # key: (topic_name, q_idx) → True/False
        "quiz_score": 0,
        "quiz_total": 0,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()

# ═════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown('<div class="hero-title">🖥️ OS<br>Platform</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-title">Navigation</div>', unsafe_allow_html=True)

    module = st.radio("", [
        "🏠 Home",
        "📚 Learn Mode",
        "⚙️ CPU Scheduling",
        "🧠 Memory Management",
        "💿 Disk Scheduling",
        "📊 System Monitor",
    ], key="main_nav", label_visibility="collapsed")

    st.session_state.active_module = module

    st.markdown("---")
    st.markdown('<span class="tag-orange">🏫 Classroom Mode Active</span>', unsafe_allow_html=True)

    st.markdown("---")
    # Quick-jump from learn mode to simulator
    if module == "📚 Learn Mode":
        st.markdown('<div class="section-title">Quick Jump</div>', unsafe_allow_html=True)
        st.caption("Jump to a simulator directly:")
        if st.button("⚙️ CPU Sim"):
            st.session_state.main_nav = "⚙️ CPU Scheduling"
            st.rerun()
        if st.button("🧠 Memory Sim"):
            st.session_state.main_nav = "🧠 Memory Management"
            st.rerun()
        if st.button("💿 Disk Sim"):
            st.session_state.main_nav = "💿 Disk Scheduling"
            st.rerun()

    st.markdown("---")
    st.caption("OS Teaching Platform v2.0")

# ═════════════════════════════════════════════════════════════════════════════
# UI HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def section_header(icon, title, subtitle=""):
    st.markdown(f'<div class="section-title" style="font-size:1.5rem">{icon} {title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.caption(subtitle)

def info_card(title, body, kind="accent"):
    color_map = {"accent": ACCENT, "warning": WARNING, "success": SUCCESS, "danger": DANGER, "purple": PURPLE, "teal": TEAL}
    color = color_map.get(kind, ACCENT)
    st.markdown(f"""
    <div class="os-card" style="border-left:4px solid {color}">
        <b style="color:{color}">{title}</b><br>
        <span style="font-size:14px;color:#b0b8cc">{body}</span>
    </div>""", unsafe_allow_html=True)

def analogy(text):
    st.markdown(f'<div class="analogy-box">💡 <b>Real-life analogy:</b> {text}</div>', unsafe_allow_html=True)

def formula_box(text):
    st.markdown(f'<div class="formula-box">📐 {text}</div>', unsafe_allow_html=True)

def mistake_box(title, items):
    content = "".join(f"<li>{i}</li>" for i in items)
    st.markdown(f'<div class="mistake-box">⚠️ <b>Common Student Mistakes:</b><ul style="margin:6px 0 0 0">{content}</ul></div>', unsafe_allow_html=True)

def sim_link_box(module_name, icon="💻"):
    st.markdown(f'<div class="sim-link-box">{icon} <b>Try it!</b> Navigate to <b>{module_name}</b> in the sidebar to run the simulation.</div>', unsafe_allow_html=True)

def teacher_note(text):
    with st.expander("📋 Teacher Notes (Click to expand)"):
        st.markdown(f'<div class="teacher-box">🎓 {text}</div>', unsafe_allow_html=True)

def classroom_font(text, tag="p"):
    st.markdown(f'<{tag} style="font-size:1.1rem;line-height:1.85">{text}</{tag}>', unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# MATPLOTLIB HELPERS
# ═════════════════════════════════════════════════════════════════════════════

def styled_fig(w=10, h=3.5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_CARD)
    ax.spines[:].set_color("#2a3044")
    ax.tick_params(colors=TEXT_LIGHT)
    return fig, ax

def close_show(fig):
    st.pyplot(fig)
    plt.close(fig)

# ═════════════════════════════════════════════════════════════════════════════
# ██  LEARN MODE — FULL SYLLABUS CONTENT
# ═════════════════════════════════════════════════════════════════════════════

LEARN_CONTENT = [

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 1-A  Introduction to OS
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "🖥️ Introduction to Operating Systems",
    "section": "Section 1 — Foundations",
    "slides": [
      { "title": "What is an Operating System?",
        "content": """
An **Operating System (OS)** is system software that acts as an intermediary between the user and computer hardware.

**Core roles of an OS:**
- **Resource Manager** — manages CPU, memory, storage, I/O devices
- **Extended Machine** — hides hardware complexity from users/programs
- **Control Program** — controls execution of programs to prevent errors

**Examples:** Linux, Windows, macOS, Android, iOS

**Two main views:**
| View | Description |
|------|-------------|
| User View | Easy interface, apps run smoothly |
| System View | Efficient resource allocation, fairness |

The OS is the **most fundamental** piece of software — without it, raw hardware is unusable.
""",
        "bullets": ["OS is always running (the kernel is always in memory)", "Kernel = core of OS; Shell = interface to kernel", "System programs vs Application programs"],
        "analogy": "An OS is like a hotel manager: manages all rooms (memory), assigns tasks to staff (CPU), handles guest requests (system calls), and ensures no two guests disturb each other.",
        "formula": None,
        "teacher_note": "Start by asking: 'What happens when you press the power button?' Walk through BIOS → Bootloader → Kernel → Shell. This hooks students immediately.",
        "mistakes": ["Confusing the OS with the GUI — Windows Explorer is NOT the OS", "Thinking 'kernel' and 'OS' mean the same thing — kernel is just one part"],
        "simulator": None },

      { "title": "OS Functions & Services",
        "content": """
**Main Functions of an OS:**

🔧 **Process Management**
- Creating, scheduling, and terminating processes
- Handling process synchronization and communication

💾 **Memory Management**
- Allocating/deallocating memory to processes
- Virtual memory, paging, segmentation

📁 **File System Management**
- Creating/deleting files and directories
- Access control, file locking

📡 **I/O Management**
- Device drivers, buffering, caching, spooling

🔒 **Security & Protection**
- User authentication, access control, sandboxing

🌐 **Networking**
- Protocol stack, sockets, network device drivers

**OS Services visible to users:**
- Program execution, I/O operations, file manipulation
- Communication, error detection, resource allocation
""",
        "bullets": ["System calls are the interface between user programs and OS", "OS keeps user processes isolated — one crash shouldn't crash the whole system", "Dual mode operation: User mode vs Kernel mode"],
        "analogy": "OS services are like a government: it provides infrastructure (roads = memory), law enforcement (security), public services (I/O), and manages the economy (CPU scheduling).",
        "formula": None,
        "teacher_note": "Show Task Manager (Windows) or `htop` (Linux) live in class. Point out each OS function being visible in real time.",
        "mistakes": ["Assuming OS services are always free — they have overhead (system call cost)", "Not understanding that switching from user mode to kernel mode takes time"],
        "simulator": None },

      { "title": "OS & Hardware Interaction",
        "content": """
The OS interacts with hardware through a precise layered model:

```
User Applications
      ↓ System Calls
  OS Kernel
      ↓ Device Drivers
  Hardware Abstraction Layer (HAL)
      ↓
   Physical Hardware
```

**Key interaction mechanisms:**

**Interrupts** — Hardware signals CPU to stop current task
- Timer interrupt (for preemptive scheduling)
- I/O interrupt (device finished)
- Software interrupt / trap (system call)

**Dual Mode Operation:**
- **User Mode** — restricted access, runs user programs
- **Kernel Mode** — full hardware access, runs OS code
- Mode bit in CPU register tracks current mode
- System call → switches to kernel mode → returns to user mode

**Memory-Mapped I/O** — I/O devices appear as memory addresses
**DMA (Direct Memory Access)** — devices transfer data directly to RAM without CPU
""",
        "bullets": ["Interrupt-driven I/O is far more efficient than polling", "DMA frees the CPU during large data transfers", "Privileged instructions can ONLY execute in kernel mode"],
        "analogy": "Dual mode is like a hospital: patients (user programs) can't operate medical equipment directly. They request a nurse/doctor (system call → kernel mode) who has the authority.",
        "formula": None,
        "teacher_note": "Draw the interrupt cycle on the board: Normal execution → Interrupt arrives → Save state (PCB) → Run ISR → Restore state → Resume. Quiz: 'What's saved during an interrupt?'",
        "mistakes": ["Thinking user programs can directly access hardware — they cannot", "Confusing interrupt and exception — interrupts are async, exceptions are sync"],
        "simulator": None },
    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 1-B  Types of OS
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "📋 Types of Operating Systems",
    "section": "Section 1 — Foundations",
    "slides": [
      { "title": "Batch & Multiprogramming OS",
        "content": """
**Batch Operating System** (1950s–60s)
- Jobs collected, grouped into batches, submitted together
- No user interaction during execution
- CPU often idle waiting for I/O

**Problems with Batch OS:**
- Poor CPU utilization (CPU waits for I/O)
- No interactivity
- Long turnaround time

---

**Multiprogramming OS** (1960s)
- Multiple jobs kept in memory simultaneously
- When one job waits for I/O, another uses CPU
- **Goal: Maximize CPU utilization**

**Key idea:** CPU never sits idle if there's work to do.

| | Batch | Multiprogramming |
|--|--|--|
| CPU Utilization | Low | High |
| User Interaction | None | None |
| Jobs in Memory | 1 | Many |
""",
        "bullets": ["Multiprogramming ≠ multitasking — there is no time-sharing", "OS must decide which job runs next → early scheduling", "Memory must hold multiple jobs → memory management needed"],
        "analogy": "Batch = cooking one dish at a time. Multiprogramming = starting the rice, then chopping vegetables while it cooks. CPU is always busy!",
        "formula": None,
        "teacher_note": "Ask: 'If Job A needs 10ms CPU then 50ms I/O, what does CPU do in Batch vs Multiprogramming?' Use a timeline to show CPU utilization improvement.",
        "mistakes": ["Saying multiprogramming means multitasking — it doesn't preempt", "Thinking batch OS is completely useless — still used for payroll, billing"],
        "simulator": None },

      { "title": "Time-Sharing, Real-Time & Distributed OS",
        "content": """
**Time-Sharing OS** (Multitasking)
- Extension of multiprogramming with **preemption**
- Each user/process gets a small time slice (quantum)
- Creates illusion of simultaneous execution
- Examples: UNIX, Linux, Windows

**Real-Time OS (RTOS)**
- Must respond to events within a **guaranteed deadline**
- **Hard RTOS**: Missing deadline = catastrophic failure (airbags, flight control)
- **Soft RTOS**: Missing deadline = degraded performance (video streaming)
- Examples: VxWorks, FreeRTOS, QNX

**Distributed OS**
- Manages a collection of networked computers as one system
- Transparent to the user (looks like one machine)
- Examples: Google's Borg, Hadoop YARN

**Embedded OS**
- Runs on dedicated hardware (IoT, appliances)
- Extremely resource-constrained
- Examples: Android (phones), TinyOS (sensors)
""",
        "bullets": ["Time-sharing adds user interactivity that multiprogramming lacks", "RTOS correctness = right answer + delivered on time", "Distributed OS handles consistency, fault tolerance, and communication"],
        "analogy": "Time-sharing = a teacher taking 30 questions from students round-robin. RTOS = 911 dispatcher — must respond within seconds, no excuses.",
        "formula": None,
        "teacher_note": "Show where each type is used in real life. Ask: 'Your ATM — which type of OS?' (Embedded/RTOS). 'Your laptop?' (Time-sharing). This grounds abstract theory.",
        "mistakes": ["Thinking real-time means fast — it means predictable/guaranteed", "Confusing distributed OS with networked OS (distributed = transparent)"],
        "simulator": None },
    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 1-C  System Calls & Linux
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "📞 System Calls & Linux Basics",
    "section": "Section 1 — Foundations",
    "slides": [
      { "title": "System Calls",
        "content": """
A **system call** is how a user program requests a service from the OS kernel.

**Types of System Calls:**

| Category | Examples |
|---|---|
| **Process Control** | `fork()`, `exec()`, `exit()`, `wait()` |
| **File Management** | `open()`, `read()`, `write()`, `close()` |
| **Device Management** | `ioctl()`, `read()`, `write()` |
| **Information** | `getpid()`, `alarm()`, `sleep()` |
| **Communication** | `pipe()`, `socket()`, `send()`, `recv()` |

**How a system call works:**
1. User program calls library function (e.g., `printf`)
2. Library prepares arguments, puts system call number in register
3. Executes trap instruction → switches to **kernel mode**
4. OS looks up system call table, executes handler
5. Returns result → switches back to **user mode**
6. Library returns to user program

**Windows vs POSIX**: Windows uses Win32 API; Linux/Mac use POSIX standard.
""",
        "bullets": ["Each system call has a unique number (e.g., read=0, write=1 on x86-64 Linux)", "System calls are expensive — minimize them in performance-critical code", "strace command shows all system calls made by a program"],
        "analogy": "System call = asking a bank teller (OS) to access your safe (hardware). You can't go into the vault yourself — you fill out a form (registers), show ID, and the teller does it.",
        "formula": None,
        "teacher_note": "Run `strace ls` in terminal during lecture. Students are amazed to see ~100 system calls just to list a directory. Ask: 'Why so many calls for a simple `ls`?'",
        "mistakes": ["Thinking function calls and system calls are the same", "Not knowing that printf eventually calls the `write` system call"],
        "simulator": None },

      { "title": "Essential Linux Commands",
        "content": """
**Process & System Info:**
```bash
ps aux          # List all processes
top / htop      # Live process monitor
kill -9 PID     # Force-kill process
nice -n 10 cmd  # Run with lower priority
```

**File System:**
```bash
ls -la          # List files with permissions
chmod 755 file  # Change permissions
chown user file # Change ownership
df -h           # Disk free space
du -sh folder/  # Folder size
```

**Memory & CPU:**
```bash
free -h         # RAM usage
vmstat          # Virtual memory stats
cat /proc/cpuinfo    # CPU details
cat /proc/meminfo    # Memory details
```

**I/O & Disk:**
```bash
lsblk           # List block devices
iostat          # I/O statistics
fdisk -l        # Disk partitions
```

**Useful for OS teaching:**
```bash
strace cmd      # Trace system calls
ltrace cmd      # Trace library calls
/proc/          # Live kernel data filesystem
```
""",
        "bullets": ["/proc is a virtual filesystem — reads directly from kernel data structures", "Everything in Linux is a file — devices, pipes, even processes (/proc/PID)", "`fork()` creates a copy of the parent process"],
        "analogy": "Linux commands are like asking questions to the OS directly. `/proc` is like the OS's open diary — you can read its internal state in real time.",
        "formula": None,
        "teacher_note": "Live demo: run `cat /proc/1/status` to show process info. Run `cat /proc/meminfo`. Students see OS internals live — much more impactful than slides.",
        "mistakes": ["Forgetting that Linux is case-sensitive (File ≠ file)", "Not knowing that `kill` sends a signal, not necessarily a death — `kill -l` shows all signals"],
        "simulator": None },
    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 1-D  Process Management
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "🔄 Process Management",
    "section": "Section 1 — Foundations",
    "slides": [
      { "title": "What is a Process? PCB & Context Switching",
        "content": """
A **process** is a program in execution. It is the OS's unit of work.

**Process vs Program:**
- Program = passive entity (file on disk)
- Process = active entity (program in execution)
- Same program can create multiple processes (5 Chrome tabs = 5 processes)

**Process Control Block (PCB)** — OS's data structure for each process:

| PCB Field | Description |
|---|---|
| Process ID (PID) | Unique identifier |
| Process State | Running, Ready, Waiting... |
| Program Counter | Address of next instruction |
| CPU Registers | All register values |
| Memory Info | Base/limit registers, page tables |
| I/O Status | Open files, devices |
| Accounting Info | CPU time used, priority |

**Context Switch** — Saving/restoring state when CPU switches processes:
1. Save current process's registers & PC to its PCB
2. Update process state (Running → Ready or Waiting)
3. Load next process's PCB (registers, PC, memory maps)
4. Resume execution of new process
""",
        "bullets": ["Context switch is pure overhead — no useful work done during it", "Modern CPUs have hardware support to speed up context switches", "On Linux, PCB is the `task_struct` structure in the kernel"],
        "analogy": "Context switch = a student saving their work and closing books before switching to another subject. The more subjects (processes), the more time spent switching.",
        "formula": "Context Switch Time ≈ 1–10 microseconds on modern hardware",
        "teacher_note": "Ask: 'If context switch takes 1ms and CPU quantum is 10ms, what % of CPU time is wasted on switching?' (Answer: 1/11 ≈ 9%). Makes tradeoffs concrete.",
        "mistakes": ["Thinking context switch is free — it has real overhead", "Confusing PCB with process memory — PCB is in OS kernel space"],
        "simulator": None },

      { "title": "Process States — 3, 5 & 7 State Models",
        "content": """
**3-State Model** (Basic):
```
New → Ready ↔ Running → Terminated
              ↕
           Blocked/Waiting
```

**5-State Model** (Standard):
- **New**: Process being created
- **Ready**: Waiting for CPU (in ready queue)
- **Running**: Executing on CPU
- **Waiting/Blocked**: Waiting for I/O or event
- **Terminated**: Finished execution

**7-State Model** (with Swapping):
Adds two **suspended** states for when OS swaps processes to disk:
- **Ready-Suspended**: Ready but swapped to disk
- **Blocked-Suspended**: Blocked and swapped to disk

**Key Transitions:**
| Transition | Cause |
|---|---|
| Ready → Running | Scheduler dispatches |
| Running → Ready | Preempted (time-slice expires) |
| Running → Waiting | I/O request made |
| Waiting → Ready | I/O completes |
| Running → Terminated | `exit()` called |
| Ready → Ready-Suspended | OS swaps out to free RAM |
""",
        "bullets": ["Only ONE process per CPU core can be in Running state", "Multiple processes can be Ready and Waiting simultaneously", "Zombie: finished but parent hasn't called wait() yet"],
        "analogy": "Process states = a student's day: New=enrolled, Ready=outside office, Running=talking to professor, Waiting=in library, Terminated=graduated, Suspended=on leave.",
        "formula": None,
        "teacher_note": "Draw state diagram on board incrementally. Start with 3 states, then ask 'What if the process needs I/O?' to motivate the 5th state, then 'What if RAM is full?' for 7-state.",
        "mistakes": ["Drawing arrow from Waiting directly to Running — it must go through Ready", "Forgetting that preemption causes Running → Ready, not Running → Waiting"],
        "simulator": None },

    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 1-E  Threads
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "🧵 Threads & Multithreading",
    "section": "Section 1 — Foundations",
    "slides": [
      { "title": "Process vs Thread",
        "content": """
A **thread** is a lightweight unit of CPU execution within a process.

**Process vs Thread:**

| Aspect | Process | Thread |
|---|---|---|
| Memory | Own address space | Shares process memory |
| Creation | Expensive (fork) | Cheap |
        | Communication | IPC needed | Shared memory directly |
| Switching | Slow (context switch) | Fast |
| Crash effect | Isolated | Crashes whole process |
| Example | Chrome Browser | Each tab's JS engine |

**What threads share:**
- Code section, data section, OS resources (files, signals)

**What threads have privately:**
- Program Counter, Registers, Stack

**Benefits of threads:**
- Responsiveness (UI + background work simultaneously)
- Resource sharing (cheaper than IPC)
- Economy (faster to create/switch than processes)
- Scalability (use multiple CPU cores)
""",
        "bullets": ["Multi-threaded programs are harder to debug — race conditions, deadlocks", "Python GIL prevents true parallelism in CPython threads (use processes instead)", "Java threads = user-level threads mapped to kernel threads"],
        "analogy": "Process = a restaurant. Threads = different waiters in that restaurant. They share the kitchen (memory) but each serves different tables (tasks) independently.",
        "formula": None,
        "teacher_note": "Show Chrome's Task Manager (Shift+Esc). Each tab is a process; within each tab, multiple threads handle JS, rendering, network, etc. Real and visible!",
        "mistakes": ["Thinking threads are always faster — synchronization overhead can make them slower", "Assuming threads are safe by default — shared data requires locks"],
        "simulator": None },

      { "title": "Multithreading Models & Types",
        "content": """
**User-Level Threads (ULT):**
- Managed by user-space library (not the OS)
- Kernel sees only one thread per process
- Fast creation/switching (no kernel involvement)
- **Problem**: One thread blocking blocks ALL threads

**Kernel-Level Threads (KLT):**
- Managed directly by the OS
- True parallelism on multi-core CPUs
- Context switch is slower (kernel involved)
- Examples: Windows threads, Linux `pthreads`

**Multithreading Models:**

| Model | Description | Example |
|---|---|---|
| Many-to-One | Many ULT → 1 KLT | Green threads (old Java) |
| One-to-One | 1 ULT → 1 KLT | Linux, Windows |
| Many-to-Many | Many ULT → Many KLT | Solaris, older IRIX |
| Two-Level | Many-to-Many + 1-to-1 | HP-UX |

**Modern systems use One-to-One** (Linux, Windows) because multi-core CPUs make true parallelism valuable.
""",
        "bullets": ["pthreads = POSIX thread standard, used in C/C++ on Linux/macOS", "Python's threading module uses OS threads but GIL limits parallelism", "Thread pool pattern: reuse threads instead of creating/destroying repeatedly"],
        "analogy": "ULT = actors in a play — the director (runtime) manages them, but the venue (OS) only sees one booking. KLT = real employees on the company org chart — management (OS) knows each one.",
        "formula": None,
        "teacher_note": "Write a simple Java/Python multi-threaded example (counter increment without locks) and show the race condition. Then fix it with a lock. Students remember bugs they see!",
        "mistakes": ["Confusing Many-to-One with single-threaded — multiple ULTs exist, just can't run in parallel", "Not knowing that blocking system call in Many-to-One blocks all threads"],
        "simulator": None },
    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 1-F  Concurrency & Synchronization
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "🔒 Concurrency & Synchronization",
    "section": "Section 1 — Foundations",
    "slides": [
      { "title": "Race Conditions & Critical Section",
        "content": """
**Race Condition**: When the result of execution depends on the **timing/order** of thread scheduling.

**Example** — two threads incrementing a shared counter:
```
Thread 1: LOAD x  (x=5)
Thread 2: LOAD x  (x=5)  ← reads stale value!
Thread 1: ADD 1   (x=6)
Thread 1: STORE x (x=6)
Thread 2: ADD 1   (x=6)  ← should be 7!
Thread 2: STORE x (x=6)  ← LOST UPDATE!
```

**Critical Section Problem:**
A code segment that accesses shared data and must not be executed by more than one process at a time.

**Three requirements for a valid solution:**
1. **Mutual Exclusion** — only one process in CS at a time
2. **Progress** — if CS is free, a waiting process must get in
3. **Bounded Waiting** — no process waits forever (no starvation)

**Peterson's Solution** (software-based, 2 processes):
```python
# Process Pi wanting to enter CS:
flag[i] = True      # I want to enter
turn = j            # But I'll give priority to j
while flag[j] and turn == j:
    pass            # Wait
# --- CRITICAL SECTION ---
flag[i] = False     # Done
```
""",
        "bullets": ["Race conditions are non-deterministic — hard to reproduce and debug", "Peterson's solution works conceptually but isn't used in practice (hardware reordering)", "Memory visibility issues (caches) make software solutions unreliable without memory barriers"],
        "analogy": "Two people editing the same Google Doc at the exact same time without collaborative locking — they overwrite each other's changes. That's a race condition.",
        "formula": "Critical Section must satisfy: Mutual Exclusion ∧ Progress ∧ Bounded Waiting",
        "teacher_note": "Run a live demo: create a simple Python script with two threads incrementing a shared variable 100,000 times without a lock. Final answer will be wrong every time. Then add a Lock and show it works.",
        "mistakes": ["Thinking a single x++ is atomic — it's actually 3 machine instructions (load, add, store)", "Forgetting Progress condition — a solution that always blocks isn't valid"],
        "simulator": None },

      { "title": "Mutex, Semaphores & Classical Problems",
        "content": """
**Mutex (Mutual Exclusion Lock):**
- Binary lock: 0 (locked) or 1 (unlocked)
- `acquire()` → if locked, block; else lock and proceed
- `release()` → unlock, wake waiting thread
- Only the locking thread can unlock it

**Semaphore:**
- Generalized integer counter
- `wait(S)` (P operation): S--; if S<0, block
- `signal(S)` (V operation): S++; if waiting thread, wake one
- **Binary semaphore** = mutex
- **Counting semaphore** = controls access to N resources

**Classical Synchronization Problems:**

**1. Producer-Consumer (Bounded Buffer):**
- Producer fills buffer, consumer empties it
- Semaphores: `empty` (N), `full` (0), `mutex` (1)

**2. Readers-Writers:**
- Multiple readers OK simultaneously
- Writers need exclusive access
- Risk: writer starvation if readers never stop

**3. Dining Philosophers (5 philosophers, 5 forks):**
- Need 2 forks (left + right) to eat
- Naive solution → deadlock possible
- Solutions: ordering, asymmetry, monitor
""",
        "bullets": ["Semaphore signal/wait must be atomic — done at hardware/OS level", "Monitor = high-level synchronization (Java synchronized, Python with statement)", "Spinlock = busy-wait; sleeping lock = block and wake — tradeoff between CPU and latency"],
        "analogy": "Mutex = a bathroom key. Only one person at a time. Semaphore = parking garage with N spots — a counter controls entry. Dining Philosophers = engineers sharing limited lab equipment.",
        "formula": "Semaphore: wait(S): S--; if S<0 → block | signal(S): S++; if S≤0 → wake one",
        "teacher_note": "Trace the Producer-Consumer solution step by step with semaphore values written on the board. Show what happens if we forget `mutex` — data corruption. If we forget `empty` — buffer overflow.",
        "mistakes": ["Using a semaphore as a mutex when you need ownership semantics (only locker can unlock)", "Calling signal before wait during initialization — classic off-by-one deadlock", "Solving Dining Philosophers by having all pick up left fork first — immediate deadlock"],
        "simulator": None },
    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 2-A  CPU Scheduling (Deep)
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "⚙️ CPU Scheduling — Deep Dive",
    "section": "Section 2 — Core Algorithms",
    "slides": [
      { "title": "Scheduling Algorithms Overview",
        "content": """
**Preemptive vs Non-Preemptive:**
- **Non-preemptive**: Once CPU assigned, process runs until it finishes or blocks
- **Preemptive**: OS can take CPU away mid-execution (e.g., higher priority arrives, time-slice expires)

**Algorithm Summary:**

| Algorithm | Preemptive | Starvation | Best For |
|---|---|---|---|
| FCFS | No | No | Batch, simple |
| SJF (non-preemptive) | No | Yes | Minimize avg wait |
| SRTF (preemptive SJF) | Yes | Yes | Interactive |
| Round Robin | Yes | No | Time-sharing |
| Priority | Both | Yes | Real-time |
| Multilevel Queue | Both | Yes | Mixed workloads |

**Key Formulas:**
- Turnaround Time (TAT) = Completion Time − Arrival Time
- Waiting Time (WT) = TAT − Burst Time
- Response Time = First CPU allocation − Arrival Time
- CPU Utilization = (CPU busy time / Total time) × 100%
""",
        "bullets": ["SRTF (preemptive SJF) is optimal for minimizing avg waiting time", "Priority scheduling with aging prevents starvation", "Multilevel Feedback Queue is used in most real OS (Linux CFS, Windows)"],
        "analogy": "FCFS = first in line at a coffee shop. SJF = quick orders first. Round Robin = teacher gives each student equal time. Priority = VIP queue — but VIPs must sometimes wait if the desk is busy.",
        "formula": "WT = TAT − BT | TAT = CT − AT | Avg WT = ΣWT / n",
        "teacher_note": "Solve one numerical example on the board for each algorithm. Students must practice computations — it's always in exams. Walk through the Gantt chart drawing technique.",
        "mistakes": ["Forgetting to subtract arrival time in TAT calculation", "Computing WT as CT − AT instead of TAT − BT", "In Round Robin, not tracking remaining burst time carefully"],
        "simulator": "⚙️ CPU Scheduling" },

      { "title": "Convoy Effect & Algorithm Selection",
        "content": """
**Convoy Effect in FCFS:**
When a long process holds the CPU, all shorter processes behind it wait.

**Example:**
- P1 (BT=20), P2 (BT=1), P3 (BT=1) all arrive at t=0
- FCFS order: P1→P2→P3
- Avg WT = (0 + 20 + 21)/3 = **13.67**
- SJF order: P2→P3→P1
- Avg WT = (0 + 1 + 2)/3 = **1.0** ← 13x better!

**When to use which algorithm:**

| Scenario | Best Algorithm | Why |
|---|---|---|
| Batch with known burst times | SJF | Optimal avg waiting time |
| Interactive systems | Round Robin | Fair, responsive |
| Real-time with deadlines | Priority (preemptive) | Meets deadlines |
| Simple/fairness needed | FCFS | No starvation, simple |
| Mixed workloads | Multilevel Feedback Queue | Adaptive |

**Why other algorithms aren't always best:**
- FCFS: convoy effect, high avg wait
- SJF: starvation, needs burst time prediction
- RR: high avg TAT, quantum selection is tricky
""",
        "bullets": ["Aging fixes starvation in priority scheduling: increase priority over time", "Linux uses CFS (Completely Fair Scheduler) — gives each process fair share of CPU", "The 'best' algorithm is always workload-dependent — no universal winner"],
        "analogy": "Convoy effect = one truck blocking a narrow road, making all cars behind it go at 20 km/h even though they could do 100 km/h. Passing (preemption) solves it!",
        "formula": "Convoy increases Avg WT. SJF minimizes it. RR balances response time.",
        "teacher_note": "Use the CPU Scheduling simulator to show the same input (P1=20, P2=1, P3=1) on FCFS vs SJF. The visual difference in Gantt charts is dramatic and memorable.",
        "mistakes": ["Claiming one algorithm is 'always best' — context matters", "Forgetting that SJF requires knowing burst time in advance (not always possible)"],
        "simulator": "⚙️ CPU Scheduling" },
    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 2-B  Deadlocks
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "💀 Deadlocks",
    "section": "Section 2 — Core Algorithms",
    "slides": [
      { "title": "Deadlock Conditions & Resource Allocation Graph",
        "content": """
A **deadlock** is a set of processes permanently blocked, each waiting for a resource held by another.

**Four Necessary Conditions (ALL must hold simultaneously):**

1. **Mutual Exclusion** — resource can only be held by one process
2. **Hold and Wait** — process holds resources while waiting for more
3. **No Preemption** — resources cannot be forcibly taken
4. **Circular Wait** — P1 waits for P2, P2 waits for P3, ..., Pn waits for P1

**Resource Allocation Graph (RAG):**
- Circle = Process, Square = Resource
- Arrow P→R = process requests resource
- Arrow R→P = resource assigned to process
- **Cycle in RAG = DEADLOCK** (if single instances per resource)

**Example:**
```
P1 → R1 ← P2
↑         ↓
R2 ←------+
```
P1 holds R2, wants R1. P2 holds R1, wants R2. **Deadlock!**
""",
        "bullets": ["If any ONE of the four conditions is prevented → no deadlock", "With multiple instances per resource, cycle ≠ always deadlock", "Deadlocks are rare but catastrophic — OS needs a strategy"],
        "analogy": "Four cars at a 4-way intersection, each pulling forward blocking the car to its right. Nobody can move. Eliminating any one condition (e.g., only 3 cars enter at once) prevents it.",
        "formula": "Deadlock ⟺ All 4 Coffman Conditions hold simultaneously",
        "teacher_note": "Draw the RAG on the board. Add resources one by one until the cycle forms. Ask students: 'At what point did deadlock become inevitable?' Great for intuition building.",
        "mistakes": ["Saying cycle always means deadlock — only if resources are single-instance", "Forgetting that all 4 conditions must hold simultaneously — one alone isn't enough"],
        "simulator": None },

      { "title": "Banker's Algorithm",
        "content": """
**Banker's Algorithm** (Dijkstra, 1965) — a deadlock avoidance strategy.

**Key idea:** Before granting a resource request, check if the resulting state is **safe**. If not safe, make the process wait.

**A state is safe if** there exists at least one safe sequence in which all processes can finish.

**Data structures needed:**
- `Available[R]` — available instances of each resource
- `Max[N][R]` — maximum demand of each process
- `Allocation[N][R]` — currently allocated resources
- `Need[N][R]` = Max − Allocation

**Safety Algorithm:**
```
Work = Available
Finish[i] = False for all i
Repeat:
  Find i where Finish[i]=False AND Need[i] ≤ Work
  If found: Work += Allocation[i], Finish[i] = True
  Else: break
If all Finish[i] = True → Safe State
```

**Resource-Request Algorithm:**
1. If Request ≤ Need → proceed (else error)
2. If Request ≤ Available → proceed (else wait)
3. Pretend to allocate, run safety algorithm
4. If safe → grant; else → rollback and wait
""",
        "bullets": ["Banker's requires knowing maximum resource needs in advance", "Named after banks that only grant loans if they can still cover all worst-case needs", "O(n²r) time complexity where n=processes, r=resource types"],
        "analogy": "You're a bank manager. Before giving a loan, you check: 'Even if all customers need their max loan simultaneously, can I still pay everyone?' If yes — safe. If no — deny the request.",
        "formula": "Need[i][j] = Max[i][j] − Allocation[i][j]",
        "teacher_note": "Work a full Banker's example: 5 processes, 3 resource types. Find available resources, compute Need matrix, find safe sequence. This is a guaranteed exam problem — practice it multiple times.",
        "mistakes": ["Forgetting to update Work after 'executing' a process in the safety algorithm", "Confusing Allocation (current) with Need (still needed) — Need = Max − Allocation", "Not resetting the pretend-allocation if the state is unsafe"],
        "simulator": None },

      { "title": "Deadlock Prevention, Detection & Recovery",
        "content": """
**1. Prevention** — Eliminate one Coffman condition:
- **No Mutual Exclusion**: make resources sharable (only for read-only resources)
- **No Hold & Wait**: request ALL resources at once before starting
- **Allow Preemption**: forcibly take resources if needed
- **No Circular Wait**: impose resource ordering (always request R1 before R2)

**2. Avoidance** — Use extra info (Banker's Algorithm)

**3. Detection** — Allow deadlocks, detect them periodically:
- Single-instance: check for cycle in RAG
- Multi-instance: similar to Banker's safety algorithm
- When to run: periodically, or when CPU utilization drops sharply

**4. Recovery:**
- **Process Termination**: kill all deadlocked processes, OR kill one at a time until cycle broken
- **Resource Preemption**: forcibly take resources, rollback affected processes

**5. Ostrich Algorithm (Ignorance):**
- Pretend deadlocks don't happen
- Used by: Windows, Linux (for most cases!)
- Rational: deadlocks are rare; prevention overhead > occasional restart cost
""",
        "bullets": ["Prevention is simplest to implement but often wastes resources", "Hold & Wait prevention causes low resource utilization", "Most OS use a combination: some prevention + ostrich algorithm"],
        "analogy": "Prevention = design the intersection without a deadlock possibility. Detection = traffic camera watches for gridlock. Recovery = traffic police physically moves cars. Ostrich = assume it won't happen!",
        "formula": None,
        "teacher_note": "Ask students to debate: 'Is the Ostrich Algorithm reasonable?' For a desktop OS, occasional system hang → reboot is acceptable. For nuclear plant control? Absolutely not. Context matters!",
        "mistakes": ["Thinking avoidance and prevention are the same thing", "Not knowing that most OS actually use the Ostrich algorithm", "Forgetting that recovery must choose a victim process carefully"],
        "simulator": None },
    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 2-C  Memory Management Deep
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "🧠 Memory Management — Deep Dive",
    "section": "Section 2 — Core Algorithms",
    "slides": [
      { "title": "Logical vs Physical Address & Address Binding",
        "content": """
**Logical Address** (Virtual Address):
- Generated by the CPU during program execution
- What the process "thinks" is its address
- Range: 0 to max (each process starts at 0)

**Physical Address:**
- Actual address in RAM
- What the memory controller sees

**Memory Management Unit (MMU):**
- Hardware chip that translates logical → physical
- Uses **relocation register** (base register)
- Physical = Logical + Base Register value

**Address Binding** — when is the translation done?
| Stage | Description |
|---|---|
| **Compile Time** | Absolute code generated, must load at fixed address |
| **Load Time** | Relocatable code, bound when loaded into memory |
| **Execution Time** | Logical→Physical mapping done at runtime by MMU |

Modern OS use **execution-time binding** with paging for full flexibility.

**Logical Address Space vs Physical Address Space:**
- Logical space can be LARGER than physical (virtual memory!)
""",
        "bullets": ["Every modern CPU has an MMU built in", "Base-and-limit registers define each process's valid memory range", "Without MMU, one process could read/write another's memory (security disaster)"],
        "analogy": "Logical address = house number on a map (relative). Physical address = GPS coordinates (absolute). MMU = your GPS that translates one to the other as you navigate.",
        "formula": "Physical Address = Logical Address + Relocation Register (Base)",
        "teacher_note": "Show on board: draw two processes in memory, each thinking they start at address 0. Show how the MMU translates P1's 0x100 to physical 0x4100 and P2's 0x100 to 0x8100.",
        "mistakes": ["Thinking logical and physical address are the same thing", "Forgetting that the MMU translation happens in hardware, not software (fast!)"],
        "simulator": None },

      { "title": "Paging & Segmentation",
        "content": """
**Paging** — divide memory into fixed-size blocks:
- Physical memory → **frames** (fixed size, e.g., 4KB)
- Logical memory → **pages** (same size as frames)
- OS maintains a **page table** per process
- Physical Address = Frame Number × Frame Size + Offset

**Page Table Entry contains:**
- Frame number, valid bit, dirty bit, reference bit, protection bits

**Translation Lookaside Buffer (TLB):**
- Fast cache for page table entries (hardware)
- TLB hit → direct frame number (1 memory access)
- TLB miss → walk page table (2+ memory accesses)

---

**Segmentation** — divide by logical meaning:
- Code segment, data segment, stack segment, heap segment
- Each segment has a **base** and **limit**
- Segments can grow/shrink independently

**Paging vs Segmentation:**
| | Paging | Segmentation |
|--|--|--|
| Division | Fixed size | Logical meaning |
| Fragmentation | Internal | External |
| Size | Equal | Variable |
| User visible | No | Yes |

**Modern OS: Segmented Paging** — segments divided into pages (best of both worlds).
""",
        "bullets": ["Internal fragmentation in paging: last page may not be fully used", "External fragmentation in segmentation: free memory scattered in small chunks", "x86-64 uses 4-level paging — 48-bit virtual address space"],
        "analogy": "Paging = dividing a book into equal-length chapters regardless of content. Segmentation = dividing by chapters naturally (intro, ch1, ch2...). Real OS combines both!",
        "formula": "Physical Addr = Frame# × Page_Size + Offset | TLB hit rate → Effective Access Time = h×(c+m) + (1-h)×(c+2m)",
        "teacher_note": "Walk through a page table example: 4-bit logical address, 2-bit page number, 2-bit offset. Show 4 page table entries. Translate address 1010 → find page 10 → frame 11 → physical 1110.",
        "mistakes": ["Confusing page number and page offset in the address split", "Thinking TLB miss is catastrophic — it just adds one extra memory access", "Not knowing that modern x86 uses multi-level page tables (too large for single-level)"],
        "simulator": None },

      { "title": "Virtual Memory & Thrashing",
        "content": """
**Virtual Memory** — the OS creates the illusion that processes have more memory than physically available by using disk as an extension of RAM.

**Demand Paging:**
- Only load pages into RAM when they are actually needed
- Lazy allocation — don't load the entire program at start
- **Page fault** occurs when a needed page is not in RAM

**Page Fault Handling:**
1. CPU traps to OS (page fault interrupt)
2. OS finds the page on disk
3. If free frame available → load page, update page table
4. If no free frame → page replacement algorithm → evict a page
5. Resume process

**Working Set Model:**
- Working set W(t,Δ) = set of pages used in last Δ time units
- OS must keep the working set in memory
- If total working sets > RAM → **Thrashing**

**Thrashing:**
- Process spends more time on page faults than execution
- CPU utilization collapses
- Solution: reduce multiprogramming, add RAM

**Copy-on-Write (COW):**
- `fork()` doesn't copy all memory immediately
- Parent and child share pages marked read-only
- Only when a process writes → create a private copy
""",
        "bullets": ["Virtual memory allows programs larger than physical RAM", "Page fault penalty: disk access ~5ms vs RAM ~50ns → 100,000x slower", "Linux uses transparent huge pages (2MB instead of 4KB) for performance"],
        "analogy": "Virtual memory = a librarian who keeps popular books on the desk (RAM) and less-used ones in the back room (disk). When you need a book from the back, they fetch it (page fault).",
        "formula": "Effective Access Time = (1-p)×m + p×(page_fault_time) where p = page fault rate",
        "teacher_note": "Show thrashing graph: CPU utilization vs degree of multiprogramming. Sharp drop after peak = thrashing. Ask: 'How would you fix thrashing without buying more RAM?' (Reduce active processes.)",
        "mistakes": ["Thinking virtual memory makes the computer faster — it actually slows it down (disk is slow)", "Forgetting that page fault frequency, not just count, determines thrashing"],
        "simulator": "🧠 Memory Management" },
    ]
  },

  # ──────────────────────────────────────────────────────────────────────────
  # SECTION 2-D  Disk Scheduling (Extended)
  # ──────────────────────────────────────────────────────────────────────────
  { "topic": "💿 Disk Scheduling — All Algorithms",
    "section": "Section 2 — Core Algorithms",
    "slides": [
      { "title": "Disk Structure & Seek Time",
        "content": """
**Hard Disk Drive (HDD) Structure:**
- **Platters**: magnetic spinning disks (5400–15000 RPM)
- **Tracks**: concentric circles on each platter surface
- **Sectors**: arc segments of a track (typically 512 bytes or 4KB)
- **Cylinders**: same track number across all platters
- **Read/Write Head**: one per platter surface, moves radially

**Access Time Components:**
| Component | Description | Typical Time |
|---|---|---|
| **Seek Time** | Move head to correct track | 1–20 ms |
| **Rotational Latency** | Wait for sector to rotate under head | 0–10 ms |
| **Transfer Time** | Actual data read/write | < 1 ms |

**Total Access Time = Seek + Rotational Latency + Transfer**

Since seek time dominates, disk scheduling focuses on **minimizing total head movement (seek distance)**.

**Why SSDs are different:**
- No moving parts → no seek time, no rotational latency
- Disk scheduling matters much less for SSDs
- But HDDs still dominate in large-scale data centers (cost)
""",
        "bullets": ["Average seek time ≈ 1/3 of max seek time", "Average rotational latency = time for 1/2 revolution", "Modern HDDs have internal scheduling firmware (NCQ — Native Command Queuing)"],
        "analogy": "HDD = vinyl record player. Moving the needle (seek), waiting for the right song position (rotational latency), then reading the groove (transfer). Fast seeking = less wait.",
        "formula": "Avg Rotational Latency = 60/(2×RPM) seconds | e.g. 7200 RPM → 4.17ms",
        "teacher_note": "Play a YouTube video of an HDD head seeking — students have never seen inside one. Show the physical movement to motivate why seek time is the bottleneck.",
        "mistakes": ["Applying disk scheduling logic to SSDs — irrelevant for SSDs", "Forgetting that seek time is the bottleneck, not transfer time"],
        "simulator": "💿 Disk Scheduling" },

      { "title": "All Disk Scheduling Algorithms",
        "content": """
Given: Head at 53, Requests: [98, 183, 37, 122, 14, 124, 65, 67]

**FCFS** (First Come First Served):
- Order: 53→98→183→37→122→14→124→65→67
- Total seek: 640 tracks

**SSTF** (Shortest Seek Time First):
- Always pick closest track to current head
- Order: 53→65→67→37→14→98→122→124→183
- Total seek: 236 tracks ← much better!
- Risk: **starvation** of far tracks

**SCAN** (Elevator):
- Move in one direction, service all requests, then reverse
- Order: 53→65→67→98→122→124→183→(end)→37→14
- Total seek: 208 tracks

**C-SCAN** (Circular SCAN):
- Move in one direction only, jump back to start
- Order: 53→65→67→98→122→124→183→199→0→14→37
- More uniform wait times than SCAN

**LOOK** (Optimized SCAN):
- Like SCAN but doesn't go to end of disk — only as far as last request
- Better than SCAN in practice

**C-LOOK** (Optimized C-SCAN):
- Like C-SCAN but jumps back to lowest request, not track 0
- Best commonly used algorithm
""",
        "bullets": ["LOOK and C-LOOK are what most real OS implement, not pure SCAN", "SSTF can cause starvation if requests near head keep arriving", "For SSDs: simple FCFS often best — no penalty for random access"],
        "analogy": "SCAN = elevator going to floor 20, servicing everyone on the way up, then coming back down. C-SCAN = one-way elevator: goes up, teleports to lobby, goes up again.",
        "formula": "Total Seek Distance = Σ|head_i+1 − head_i| for all movements",
        "teacher_note": "Use the Disk Scheduling simulator and show the same requests on all 5 algorithms. Ask: 'Which algorithm would you choose for a web server with many random small reads?' (SSTF or C-LOOK)",
        "mistakes": ["Thinking SCAN goes to track 0 always — LOOK only goes to last request", "Calculating seek for SCAN without going to the disk end", "Claiming SSTF is always better than FCFS — starvation is a real problem"],
        "simulator": "💿 Disk Scheduling" },
    ]
  },
]

# ═════════════════════════════════════════════════════════════════════════════
# QUIZ DATA — 3-4 MCQs per topic (keyed by exact topic string)
# Each question: {"q", "opts": [4 strings], "ans": int (0-based), "exp": str}
# ═════════════════════════════════════════════════════════════════════════════

QUIZ_DATA = {
  "🖥️ Introduction to Operating Systems": [
    { "q": "Which of the following best describes the role of an OS?",
      "opts": ["A word processor", "An intermediary between user and hardware", "A web browser", "A compiler"],
      "ans": 1,
      "exp": "The OS acts as an intermediary between the user/programs and the computer hardware, managing resources and providing services." },
    { "q": "The 'kernel' refers to:",
      "opts": ["The GUI of the OS", "A type of system call", "The core part of the OS always in memory", "A hardware component"],
      "ans": 2,
      "exp": "The kernel is the central core of the OS that remains in memory at all times and manages hardware resources directly." },
    { "q": "Which is an example of an OS function NOT directly visible to users?",
      "opts": ["Opening a file", "CPU scheduling", "Typing text", "Clicking a button"],
      "ans": 1,
      "exp": "CPU scheduling happens transparently in the background — users never directly see or control it." },
    { "q": "Interrupts in an OS are used to:",
      "opts": ["Display graphics", "Signal the CPU that a hardware event needs attention", "Compile code", "Format disks"],
      "ans": 1,
      "exp": "Interrupts allow hardware devices to signal the CPU asynchronously, enabling interrupt-driven I/O which is far more efficient than polling." },
  ],
  "📋 Types of Operating Systems": [
    { "q": "Which OS type gives each user the illusion of a dedicated machine by time-slicing?",
      "opts": ["Batch OS", "Real-Time OS", "Time-Sharing OS", "Embedded OS"],
      "ans": 2,
      "exp": "Time-Sharing OS uses preemptive scheduling with time slices (quanta) so multiple users feel they have exclusive CPU access." },
    { "q": "Multiprogramming improves over Batch OS primarily by:",
      "opts": ["Adding a GUI", "Keeping multiple jobs in memory and switching during I/O", "Running one job faster", "Using multiple CPUs"],
      "ans": 1,
      "exp": "Multiprogramming keeps several jobs in RAM so the CPU can switch to another job when the current one waits for I/O, maximizing CPU utilization." },
    { "q": "An airbag controller uses which type of OS?",
      "opts": ["Batch OS", "Distributed OS", "Hard Real-Time OS", "Time-Sharing OS"],
      "ans": 2,
      "exp": "Airbag systems require Hard RTOS — missing a deadline (e.g., not deploying in time) has catastrophic consequences." },
    { "q": "Which statement about multiprogramming is FALSE?",
      "opts": ["It keeps multiple jobs in memory", "It improves CPU utilization", "It preempts jobs on a timer", "It switches CPU when a job does I/O"],
      "ans": 2,
      "exp": "Multiprogramming does NOT preempt on a timer — that is time-sharing. Multiprogramming switches only when a job voluntarily waits (e.g., for I/O)." },
  ],
  "📞 System Calls & Linux Basics": [
    { "q": "A system call is best described as:",
      "opts": ["A function call within user code", "A hardware interrupt", "An interface for user programs to request OS services", "A network request"],
      "ans": 2,
      "exp": "System calls are the programmatic interface through which user-space programs request services (file I/O, process creation, etc.) from the OS kernel." },
    { "q": "Which Linux command shows all system calls made by a running program?",
      "opts": ["ls", "strace", "chmod", "ps aux"],
      "ans": 1,
      "exp": "`strace cmd` traces every system call the program makes — great for debugging and understanding OS interaction." },
    { "q": "When a system call is made, the CPU mode switches to:",
      "opts": ["Idle mode", "User mode", "Kernel mode", "Interrupt mode"],
      "ans": 2,
      "exp": "A system call triggers a trap instruction that switches the CPU from user mode to kernel mode, giving the OS full hardware access to service the request." },
    { "q": "What does `fork()` do in Linux?",
      "opts": ["Opens a file", "Sends a signal", "Creates a copy of the current process", "Terminates the process"],
      "ans": 2,
      "exp": "`fork()` creates a new child process that is an almost exact copy of the parent process, including its memory and open file descriptors." },
  ],
  "🔄 Process Management": [
    { "q": "A PCB (Process Control Block) stores:",
      "opts": ["User files only", "Process ID, state, registers, memory info, etc.", "Only the process ID", "The source code of the process"],
      "ans": 1,
      "exp": "The PCB is the OS's complete data structure for a process — it stores PID, state, program counter, CPU registers, memory maps, and accounting info." },
    { "q": "Context switching is considered overhead because:",
      "opts": ["It runs useful computations", "It saves CPU registers", "No useful work is done while switching — only state save/restore", "It allocates new memory"],
      "ans": 2,
      "exp": "During a context switch, the CPU only saves the outgoing process's state and loads the incoming one — no user-visible computation happens, so it is pure overhead." },
    { "q": "In the 5-state model, which transition is INVALID?",
      "opts": ["Running → Waiting", "Waiting → Running", "Running → Ready", "Waiting → Ready"],
      "ans": 1,
      "exp": "A process cannot go directly from Waiting to Running. It must first move to the Ready queue and then be dispatched by the scheduler." },
    { "q": "A zombie process is one that:",
      "opts": ["Is consuming 100% CPU", "Has finished but its parent has not called wait()", "Is blocked on I/O", "Has been swapped to disk"],
      "ans": 1,
      "exp": "A zombie process has completed execution but its entry remains in the process table until the parent reads its exit status via wait()." },
  ],
  "🧵 Threads & Multithreading": [
    { "q": "What do threads within the same process share?",
      "opts": ["Stack and registers", "Program counter only", "Code, data, and OS resources (files, signals)", "Nothing — threads are fully isolated"],
      "ans": 2,
      "exp": "Threads share the code section, data section, and OS resources of their process but each has its own private stack, program counter, and registers." },
    { "q": "In the Many-to-One threading model, if one thread blocks:",
      "opts": ["Only that thread blocks", "All threads in the process block", "The OS creates a new thread", "The process terminates"],
      "ans": 1,
      "exp": "In Many-to-One, all user threads map to a single kernel thread, so a blocking system call by one thread blocks the entire process." },
    { "q": "Python's GIL (Global Interpreter Lock) means:",
      "opts": ["Python threads cannot be created", "Only one Python thread runs at a time, limiting CPU parallelism", "Python uses Many-to-Many model", "Python processes are slower than threads"],
      "ans": 1,
      "exp": "CPython's GIL prevents true parallel execution of Python threads. For CPU-bound parallelism in Python, use the multiprocessing module instead." },
    { "q": "Which multithreading model does modern Linux use?",
      "opts": ["Many-to-One", "One-to-One", "Many-to-Many", "Two-Level"],
      "ans": 1,
      "exp": "Linux uses the One-to-One model (via pthreads/NPTL) — each user thread maps directly to a kernel thread, enabling true parallelism on multi-core CPUs." },
  ],
  "🔒 Concurrency & Synchronization": [
    { "q": "A race condition occurs when:",
      "opts": ["Two processes run on separate CPUs", "The result depends on the timing/order of thread execution", "A process runs too slowly", "Memory is full"],
      "ans": 1,
      "exp": "A race condition is when the program outcome depends on the non-deterministic scheduling order of concurrent threads accessing shared data." },
    { "q": "Peterson's Solution satisfies which three conditions?",
      "opts": ["Speed, Safety, Progress", "Mutual Exclusion, Progress, Bounded Waiting", "Fairness, Isolation, Atomicity", "Locking, Signaling, Waking"],
      "ans": 1,
      "exp": "Any correct critical section solution must guarantee: (1) Mutual Exclusion, (2) Progress (no unnecessary blocking), and (3) Bounded Waiting (no starvation)." },
    { "q": "A counting semaphore with initial value N controls access to:",
      "opts": ["Only one resource", "N resources simultaneously", "Zero resources", "Unlimited resources"],
      "ans": 1,
      "exp": "A counting semaphore initialized to N allows up to N concurrent accesses. Each wait() decrements and each signal() increments the counter." },
    { "q": "In the Dining Philosophers problem, the naive solution of everyone picking the left fork first leads to:",
      "opts": ["Starvation", "A race condition", "Deadlock", "Priority inversion"],
      "ans": 2,
      "exp": "If all philosophers pick up their left fork simultaneously, each waits for the right fork held by their neighbor — a circular wait causing deadlock." },
  ],
  "⚙️ CPU Scheduling — Deep Dive": [
    { "q": "Turnaround Time (TAT) is calculated as:",
      "opts": ["Burst Time − Arrival Time", "Completion Time − Arrival Time", "Completion Time − Burst Time", "Waiting Time + Arrival Time"],
      "ans": 1,
      "exp": "TAT = Completion Time − Arrival Time. It represents the total time from when a process arrives to when it finishes." },
    { "q": "Which algorithm minimizes average waiting time?",
      "opts": ["FCFS", "Round Robin", "SJF (non-preemptive)", "Priority (non-preemptive)"],
      "ans": 2,
      "exp": "SJF (Shortest Job First) is proven to minimize average waiting time for a given set of processes — it is optimal for this metric." },
    { "q": "The convoy effect is a problem with:",
      "opts": ["SJF", "Round Robin", "FCFS", "Priority Scheduling"],
      "ans": 2,
      "exp": "In FCFS, a long process at the head of the queue forces all shorter processes behind it to wait, causing the 'convoy effect' and poor CPU utilization." },
    { "q": "Aging is a technique used to prevent:",
      "opts": ["Deadlock", "Thrashing", "Starvation in priority scheduling", "Race conditions"],
      "ans": 2,
      "exp": "Aging gradually increases the priority of long-waiting processes so that low-priority processes eventually get CPU time and don't starve indefinitely." },
  ],
  "💀 Deadlocks": [
    { "q": "How many conditions must ALL hold simultaneously for a deadlock to occur?",
      "opts": ["1", "2", "3", "4"],
      "ans": 3,
      "exp": "All four Coffman conditions must hold at the same time: Mutual Exclusion, Hold and Wait, No Preemption, and Circular Wait." },
    { "q": "In a Resource Allocation Graph (RAG), a cycle indicates deadlock when:",
      "opts": ["Always", "Never", "Only when all resources have exactly one instance", "Only when processes > resources"],
      "ans": 2,
      "exp": "A cycle in the RAG guarantees deadlock only if every resource type has exactly one instance. With multiple instances, a cycle may or may not indicate deadlock." },
    { "q": "In Banker's Algorithm, Need[i][j] is calculated as:",
      "opts": ["Allocation[i][j] − Max[i][j]", "Max[i][j] − Allocation[i][j]", "Max[i][j] + Available[j]", "Available[j] − Allocation[i][j]"],
      "ans": 1,
      "exp": "Need[i][j] = Max[i][j] − Allocation[i][j]. This represents how many more resources of type j process i may still request." },
    { "q": "The 'Ostrich Algorithm' for deadlock handling means:",
      "opts": ["Detect and kill all deadlocked processes", "Prevent deadlock by resource ordering", "Ignore the possibility of deadlock", "Use Banker's Algorithm proactively"],
      "ans": 2,
      "exp": "The Ostrich Algorithm simply ignores the deadlock problem — used by most general-purpose OS (Windows, Linux) where deadlocks are rare and the cost of prevention outweighs occasional restarts." },
  ],
  "🧠 Memory Management — Deep Dive": [
    { "q": "Physical Address = Logical Address + ?",
      "opts": ["Page Size", "Relocation Register (Base)", "Limit Register", "Frame Number"],
      "ans": 1,
      "exp": "The MMU computes Physical Address = Logical Address + Base Register. The base register holds the starting physical address of the process's memory." },
    { "q": "A TLB (Translation Lookaside Buffer) is:",
      "opts": ["A type of RAM", "A hardware cache for page table entries", "A disk scheduling queue", "A type of semaphore"],
      "ans": 1,
      "exp": "The TLB is a small, fast hardware cache that stores recent page-to-frame mappings, converting what would be 2 memory accesses into effectively 1 for a TLB hit." },
    { "q": "Thrashing occurs when:",
      "opts": ["CPU utilization is 100%", "Processes spend more time on page faults than actual execution", "Disk seek time is excessive", "Too many threads are created"],
      "ans": 1,
      "exp": "Thrashing happens when the combined working sets of all running processes exceed available RAM, causing constant page faults and near-zero useful CPU work." },
    { "q": "Internal fragmentation is a problem in:",
      "opts": ["Segmentation", "Paging", "Contiguous allocation only", "Virtual memory"],
      "ans": 1,
      "exp": "Paging causes internal fragmentation because the last page of a process may not be fully used — the unused portion of that page frame is wasted." },
  ],
  "💿 Disk Scheduling — All Algorithms": [
    { "q": "Which disk scheduling algorithm services the request closest to the current head position?",
      "opts": ["FCFS", "SCAN", "SSTF", "C-LOOK"],
      "ans": 2,
      "exp": "SSTF (Shortest Seek Time First) always picks the pending request with the minimum seek distance from the current head — greedy but risks starvation of far tracks." },
    { "q": "The main advantage of C-SCAN over SCAN is:",
      "opts": ["Lower total seek distance", "More uniform waiting times for all tracks", "No starvation", "Fewer disk rotations"],
      "ans": 1,
      "exp": "C-SCAN provides more uniform wait times by always moving in one direction and jumping back to the start, avoiding the situation where recently-passed requests wait a full sweep." },
    { "q": "Which algorithm is the optimized version of SCAN that doesn't travel to disk ends?",
      "opts": ["SSTF", "C-SCAN", "LOOK", "FCFS"],
      "ans": 2,
      "exp": "LOOK is like SCAN but reverses direction at the last actual request rather than going all the way to the physical end of the disk, reducing unnecessary movement." },
    { "q": "Disk scheduling algorithms are largely unnecessary for SSDs because:",
      "opts": ["SSDs are slower than HDDs", "SSDs have no moving parts — no seek time or rotational latency", "SSDs use FCFS by default", "SSDs have infinite bandwidth"],
      "ans": 1,
      "exp": "SSDs have no physical read/write head to move, so there is no seek time or rotational latency. All locations are accessed in roughly equal time, making scheduling irrelevant." },
  ],
}

# ═════════════════════════════════════════════════════════════════════════════
# DIAGRAMS — SVG/matplotlib-based visuals for Learn Mode
# ═════════════════════════════════════════════════════════════════════════════

def draw_process_state_diagram():
    """Draw the 5-state process model using matplotlib."""
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')

    states = {"New": (1, 2), "Ready": (3.5, 2), "Running": (6, 2),
              "Waiting": (6, 0.7), "Terminated": (8.5, 2)}
    colors = {"New": "#4F8EF7", "Ready": "#FFC107", "Running": "#4CAF50",
              "Waiting": "#F7844F", "Terminated": "#F44336"}

    for name, (x, y) in states.items():
        circle = plt.Circle((x, y), 0.55, color=colors[name], zorder=3)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=9,
                fontweight='bold', color='white', fontfamily='monospace', zorder=4)

    # Arrows
    arrows = [
        ("New", "Ready", "admitted", 0.02, 0),
        ("Ready", "Running", "scheduler\ndispatch", 0.02, 0),
        ("Running", "Ready", "preempted", -0.02, 0.25),
        ("Running", "Waiting", "I/O request", 0.02, 0),
        ("Waiting", "Ready", "I/O complete", -0.02, 0),
        ("Running", "Terminated", "exit()", 0.02, 0),
    ]
    for src, dst, label, dx, dy_off in arrows:
        x1, y1 = states[src]
        x2, y2 = states[dst]
        ax.annotate("", xy=(x2 - 0.55 * np.sign(x2 - x1) * 0.9, y2 + dy_off),
                    xytext=(x1 + 0.55 * np.sign(x2 - x1) * 0.9, y1 + dy_off),
                    arrowprops=dict(arrowstyle='->', color='#8892a4', lw=1.5))
        mx, my = (x1 + x2) / 2 + dx, (y1 + y2) / 2 + 0.2 + dy_off
        ax.text(mx, my, label, ha='center', va='bottom', fontsize=7,
                color='#8892a4', style='italic')

    ax.set_title("5-State Process Model", color=TEXT_LIGHT, fontfamily='monospace', fontsize=11, pad=10)
    return fig

def draw_deadlock_rag():
    """Draw a simple Resource Allocation Graph showing deadlock."""
    fig, ax = plt.subplots(figsize=(7, 4))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 5)
    ax.axis('off')

    # Processes (circles)
    for name, pos, color in [("P1", (1.5, 3.5), ACCENT), ("P2", (6, 3.5), ACCENT2)]:
        c = plt.Circle(pos, 0.5, color=color, zorder=3)
        ax.add_patch(c)
        ax.text(pos[0], pos[1], name, ha='center', va='center',
                fontsize=11, fontweight='bold', color='white', zorder=4)

    # Resources (squares)
    for name, pos in [("R1", (3.75, 4)), ("R2", (3.75, 2))]:
        rect = plt.Rectangle((pos[0]-0.55, pos[1]-0.4), 1.1, 0.8,
                              color="#2a3044", ec="#4F8EF7", linewidth=2, zorder=3)
        ax.add_patch(rect)
        dot = plt.Circle(pos, 0.15, color="#4CAF50", zorder=4)
        ax.add_patch(dot)
        ax.text(pos[0], pos[1] - 0.7, name, ha='center', va='top',
                fontsize=10, color=TEXT_LIGHT, fontweight='bold')

    # Arrows: P1 holds R2 (R2→P1), P1 wants R1 (P1→R1)
    #         P2 holds R1 (R1→P2), P2 wants R2 (P2→R2)
    arrow_style = dict(arrowstyle='->', lw=2)
    arrows = [
        ((2.0, 3.5), (3.2, 4.0), DANGER, "P1 requests R1"),
        ((3.75, 3.6), (2.0, 3.8), SUCCESS, "R1 held by P1? No\nR2→P1"),
        ((5.5, 3.5), (4.3, 4.0), DANGER, "P2 requests R2"),
        ((3.75, 2.4), (5.5, 3.2), SUCCESS, "R1 given to P2"),
        ((3.2, 3.8), (5.5, 3.6), "#9C27B0", ""),
        ((3.75, 1.6), (2.0, 3.2), "#FFC107", ""),
    ]
    # Simplified readable arrows
    ax.annotate("", xy=(3.2, 4.0), xytext=(2.0, 3.7),
                arrowprops=dict(arrowstyle='->', color=DANGER, lw=2))
    ax.text(2.5, 4.15, "requests R1", fontsize=8, color=DANGER)

    ax.annotate("", xy=(2.0, 3.3), xytext=(3.2, 2.3),
                arrowprops=dict(arrowstyle='->', color=SUCCESS, lw=2))
    ax.text(2.1, 2.6, "R2 held by P1", fontsize=8, color=SUCCESS)

    ax.annotate("", xy=(4.3, 4.0), xytext=(5.5, 3.7),
                arrowprops=dict(arrowstyle='->', color=DANGER, lw=2))
    ax.text(4.7, 4.2, "requests R2", fontsize=8, color=DANGER)

    ax.annotate("", xy=(5.5, 3.3), xytext=(4.3, 2.3),
                arrowprops=dict(arrowstyle='->', color=SUCCESS, lw=2))
    ax.text(4.8, 2.6, "R1 held by P2", fontsize=8, color=SUCCESS)

    ax.set_title("Resource Allocation Graph — DEADLOCK (Cycle Present)",
                 color=DANGER, fontfamily='monospace', fontsize=10, pad=8)
    return fig

def draw_paging_diagram():
    """Draw logical→physical address translation via page table."""
    fig, ax = plt.subplots(figsize=(10, 3.5))
    fig.patch.set_facecolor(BG_DARK)
    ax.set_facecolor(BG_DARK)
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 4)
    ax.axis('off')

    # Logical address box
    ax.add_patch(plt.Rectangle((0.2, 1.5), 3, 1, color=BG_CARD, ec=ACCENT, lw=2))
    ax.text(1.7, 2.8, "Logical Address", ha='center', color=ACCENT, fontsize=9, fontfamily='monospace')
    ax.add_patch(plt.Rectangle((0.25, 1.55), 1.4, 0.9, color=PURPLE, alpha=0.7))
    ax.text(0.95, 2.0, "Page\nNum", ha='center', va='center', color='white', fontsize=8)
    ax.add_patch(plt.Rectangle((1.75, 1.55), 1.4, 0.9, color=TEAL, alpha=0.7))
    ax.text(2.45, 2.0, "Offset", ha='center', va='center', color='white', fontsize=8)

    # Arrow
    ax.annotate("", xy=(5.0, 2.0), xytext=(3.2, 2.0),
                arrowprops=dict(arrowstyle='->', color='#8892a4', lw=2))

    # Page table
    ax.add_patch(plt.Rectangle((5.0, 0.5), 1.5, 3, color=BG_CARD, ec=WARNING, lw=2))
    ax.text(5.75, 3.65, "Page Table", ha='center', color=WARNING, fontsize=8, fontfamily='monospace')
    for i, (pg, fr) in enumerate([(0, 3), (1, 7), (2, 1), (3, 5)]):
        y = 2.8 - i * 0.55
        ax.text(5.35, y, f"P{pg}→", ha='right', va='center', color='#8892a4', fontsize=8)
        ax.add_patch(plt.Rectangle((5.4, y - 0.22), 1.0, 0.44, color=ACCENT, alpha=0.4))
        ax.text(5.9, y, f"F{fr}", ha='center', va='center', color=TEXT_LIGHT, fontsize=9, fontweight='bold')

    # Arrow
    ax.annotate("", xy=(8.0, 2.0), xytext=(6.5, 2.0),
                arrowprops=dict(arrowstyle='->', color='#8892a4', lw=2))
    ax.text(7.25, 2.25, "Frame #", ha='center', color='#8892a4', fontsize=8)

    # Physical address box
    ax.add_patch(plt.Rectangle((8.0, 1.5), 3.5, 1, color=BG_CARD, ec=SUCCESS, lw=2))
    ax.text(9.75, 2.8, "Physical Address", ha='center', color=SUCCESS, fontsize=9, fontfamily='monospace')
    ax.add_patch(plt.Rectangle((8.05, 1.55), 1.6, 0.9, color=SUCCESS, alpha=0.7))
    ax.text(8.85, 2.0, "Frame\nNum", ha='center', va='center', color='white', fontsize=8)
    ax.add_patch(plt.Rectangle((9.75, 1.55), 1.7, 0.9, color=TEAL, alpha=0.7))
    ax.text(10.6, 2.0, "Offset", ha='center', va='center', color='white', fontsize=8)
    ax.text(9.5, 1.1, "(same offset as logical address)", ha='center', color='#8892a4', fontsize=8)

    ax.set_title("Paging: Logical → Physical Address Translation",
                 color=TEXT_LIGHT, fontfamily='monospace', fontsize=10, pad=5)
    return fig

# Helper: render topic-specific diagrams
def render_topic_diagram(topic_name):
    """Show a contextual diagram if the topic has one."""
    if "Process" in topic_name and "Management" in topic_name:
        fig = draw_process_state_diagram()
        close_show(fig)
    elif "Deadlock" in topic_name:
        fig = draw_deadlock_rag()
        close_show(fig)
    elif "Memory" in topic_name and "Deep" in topic_name:
        fig = draw_paging_diagram()
        close_show(fig)

# ═════════════════════════════════════════════════════════════════════════════
# QUIZ RENDERER
# ═════════════════════════════════════════════════════════════════════════════

def render_quiz(topic_name):
    """Render MCQ quiz for the given topic below the slide content."""
    questions = QUIZ_DATA.get(topic_name)
    if not questions:
        return

    st.markdown("---")
    st.markdown(
        f'<div style="font-family:Space Mono,monospace;font-size:1.5rem;color:{ACCENT};'
        f'border-left:4px solid {ACCENT};padding-left:12px;margin-bottom:16px">'
        f'🧠 Topic Quiz</div>',
        unsafe_allow_html=True,
    )

    # Compute answered count for this topic
    answered = sum(
        1 for q_idx in range(len(questions))
        if st.session_state.quiz_submitted.get((topic_name, q_idx), False)
    )
    correct = sum(
        1 for q_idx, q in enumerate(questions)
        if st.session_state.quiz_submitted.get((topic_name, q_idx), False)
        and st.session_state.quiz_answers.get((topic_name, q_idx)) == q["ans"]
    )

    # Score banner
    if answered > 0:
        pct = int(correct / answered * 100)
        bar_color = SUCCESS if pct >= 70 else WARNING if pct >= 40 else DANGER
        st.markdown(
            f'<div class="os-card" style="border-left:4px solid {bar_color};padding:10px 16px">'
            f'<b style="color:{bar_color}">Score: {correct}/{answered} answered</b> &nbsp;'
            f'<span style="color:#8892a4">({pct}% correct so far)</span></div>',
            unsafe_allow_html=True,
        )

    for q_idx, q in enumerate(questions):
        state_key = (topic_name, q_idx)
        already_submitted = st.session_state.quiz_submitted.get(state_key, False)

        st.markdown(
            f'<div class="os-card os-card-accent" style="margin-top:12px">'
            f'<b style="color:{TEXT_LIGHT}">Q{q_idx+1}. {q["q"]}</b></div>',
            unsafe_allow_html=True,
        )

        # Radio — disabled after submission (Streamlit doesn't support disabled radio,
        # so we just hide the button and show the chosen answer statically)
        if already_submitted:
            chosen = st.session_state.quiz_answers.get(state_key, 0)
            is_correct = chosen == q["ans"]
            result_color = SUCCESS if is_correct else DANGER
            result_icon  = "✅" if is_correct else "❌"
            bg_color = "rgba(76,175,80,0.08)" if is_correct else "rgba(244,67,54,0.08)"
            # Show options as plain text with highlight
            for oi, opt in enumerate(q["opts"]):
                if oi == q["ans"]:
                    prefix = "✅"
                    color  = SUCCESS
                elif oi == chosen and not is_correct:
                    prefix = "❌"
                    color  = DANGER
                else:
                    prefix = "◦"
                    color  = "#8892a4"
                st.markdown(
                    f'<div style="padding:3px 0;color:{color}">{prefix} {opt}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(
                f'<div style="margin-top:8px;padding:10px 14px;border-radius:8px;'
                f'background:{bg_color};border:1px solid {result_color}">'
                f'{result_icon} <b style="color:{result_color}">'
                f'{"Correct!" if is_correct else "Incorrect."}</b>&nbsp;'
                f'<span style="color:#b0b8cc">{q["exp"]}</span></div>',
                unsafe_allow_html=True,
            )
        else:
            # Use index=None so no option is pre-selected by default;
            # restore the saved selection only if the student had already chosen one.
            saved_idx = st.session_state.quiz_answers.get(state_key)
            chosen = st.radio(
                f"q_{topic_name}_{q_idx}",
                options=q["opts"],
                index=saved_idx,  # None = no pre-selection; int = restore prior answer
                key=f"quiz_radio_{topic_name}_{q_idx}",
                label_visibility="collapsed",
            )
            if chosen is None:
                st.caption("⬆️ Select an answer above before submitting.")
                st.button("Submit Answer", key=f"quiz_submit_{topic_name}_{q_idx}", disabled=True)
            else:
                chosen_idx = q["opts"].index(chosen)
                if st.button("Submit Answer", key=f"quiz_submit_{topic_name}_{q_idx}"):
                    if not st.session_state.quiz_submitted.get(state_key, False):
                        st.session_state.quiz_answers[state_key]   = chosen_idx
                        st.session_state.quiz_submitted[state_key] = True
                        st.session_state.quiz_total += 1
                        if chosen_idx == q["ans"]:
                            st.session_state.quiz_score += 1
                    st.rerun()

    # Reset button for this topic
    if answered == len(questions):
        pct_final = int(correct / len(questions) * 100)
        grade_color = SUCCESS if pct_final >= 70 else WARNING if pct_final >= 40 else DANGER
        st.markdown(
            f'<div class="os-card" style="border-left:4px solid {grade_color};margin-top:16px">'
            f'🏁 <b style="color:{grade_color}">Final Score: {correct}/{len(questions)} ({pct_final}%)</b></div>',
            unsafe_allow_html=True,
        )
    if answered > 0:
        if st.button(f"🔄 Retry Quiz — {topic_name[:30]}", key=f"quiz_reset_{topic_name}"):
            for q_idx in range(len(questions)):
                st.session_state.quiz_answers.pop((topic_name, q_idx), None)
                st.session_state.quiz_submitted.pop((topic_name, q_idx), None)
            st.rerun()


# ═════════════════════════════════════════════════════════════════════════════
# ██  LEARN MODE PAGE
# ═════════════════════════════════════════════════════════════════════════════

def page_learn():
    st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:2rem;color:{ACCENT}">📚 Learn Mode</div>', unsafe_allow_html=True)
    st.caption("Full OS syllabus — interactive slide-based lessons")

    # ── Topic selector ─────────────────────────────────────────────────────
    topic_names  = [t["topic"] for t in LEARN_CONTENT]
    sections     = [t.get("section", "") for t in LEARN_CONTENT]

    # Group by section
    section_labels = sorted(set(sections), key=lambda s: sections.index(s))

    col_sec, col_top = st.columns([1, 2])
    with col_sec:
        selected_section = st.selectbox("📂 Section", section_labels, key="section_sel")
    with col_top:
        filtered_topics = [t for t in LEARN_CONTENT if t.get("section") == selected_section]
        filtered_names = [t["topic"] for t in filtered_topics]
        chosen_topic_name = st.selectbox("📖 Topic", filtered_names, key="topic_sel")

    # Update global topic index
    global_idx = topic_names.index(chosen_topic_name)
    if st.session_state.learn_topic != global_idx:
        st.session_state.learn_topic = global_idx
        st.session_state.learn_slide = 0

    topic_data = LEARN_CONTENT[st.session_state.learn_topic]
    slides     = topic_data["slides"]
    total      = len(slides)

    if st.session_state.learn_slide >= total:
        st.session_state.learn_slide = 0

    # ── Progress bar ────────────────────────────────────────────────────────
    progress = (st.session_state.learn_slide + 1) / total
    st.progress(progress)
    st.caption(f"Slide {st.session_state.learn_slide + 1} of {total}  ·  {topic_data['topic']}")

    slide = slides[st.session_state.learn_slide]

    # ── Slide Title ─────────────────────────────────────────────────────────
    # fs variable removed — font size is already applied globally via CSS
    st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:2rem;color:{TEXT_LIGHT};border-bottom:2px solid {ACCENT};padding-bottom:8px;margin-bottom:16px">{slide["title"]}</div>', unsafe_allow_html=True)

    # ── Main two-column layout ──────────────────────────────────────────────
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown(slide["content"])

        # Formula
        if slide.get("formula"):
            formula_box(slide["formula"])

        # Bullets
        if slide.get("bullets"):
            st.markdown(f'<b style="color:{ACCENT}">Key Takeaways:</b>', unsafe_allow_html=True)
            for b in slide["bullets"]:
                st.markdown(f'<div style="padding:2px 0">▸ {b}</div>', unsafe_allow_html=True)

    with col_side:
        # Analogy box
        if slide.get("analogy"):
            analogy(slide["analogy"])

        # Common mistakes
        if slide.get("mistakes"):
            mistake_box("Common Mistakes", slide["mistakes"])

        # Simulator link
        if slide.get("simulator"):
            sim_link_box(slide["simulator"])

        # Teacher notes
        if slide.get("teacher_note"):
            teacher_note(slide["teacher_note"])

    # ── Topic-specific diagram ──────────────────────────────────────────────
    if st.session_state.learn_slide == 0:
        render_topic_diagram(topic_data["topic"])

    # ── Navigation ──────────────────────────────────────────────────────────
    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1, 2, 1])

    with nav1:
        if st.button("⬅️ Previous", disabled=st.session_state.learn_slide == 0, key="prev_slide"):
            st.session_state.learn_slide -= 1
            st.rerun()

    with nav2:
        dots = "".join(
            f'<span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:{ACCENT if i == st.session_state.learn_slide else "#2a3044"};margin:0 4px"></span>'
            for i in range(total)
        )
        st.markdown(f'<div style="text-align:center;margin-top:6px">{dots}</div>', unsafe_allow_html=True)

    with nav3:
        if st.button("Next ➡️", disabled=st.session_state.learn_slide == total - 1, key="next_slide"):
            st.session_state.learn_slide += 1
            st.rerun()

    # ── All slides panel ────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 All Slides in this Topic"):
        for i, s in enumerate(slides):
            active = i == st.session_state.learn_slide
            col_a, col_b = st.columns([3, 1])
            col_a.markdown(f'<span style="color:{ACCENT if active else "#8892a4"}">{"→ " if active else "   "}Slide {i+1}: {s["title"]}</span>', unsafe_allow_html=True)
            if col_b.button("Go", key=f"jump_{i}"):
                st.session_state.learn_slide = i
                st.rerun()

    # ── Quiz — shown on last slide of topic ────────────────────────────────
    if st.session_state.learn_slide == total - 1:
        render_quiz(topic_data["topic"])

    # ── Full syllabus overview ───────────────────────────────────────────────
    with st.expander("🗂️ Full Syllabus Overview"):
        for sec in section_labels:
            st.markdown(f'<div class="section-title">{sec}</div>', unsafe_allow_html=True)
            for t in LEARN_CONTENT:
                if t.get("section") == sec:
                    active = t["topic"] == topic_data["topic"]
                    color = ACCENT if active else "#8892a4"
                    slides_count = len(t["slides"])
                    st.markdown(f'<span style="color:{color};font-size:13px">{"▶ " if active else "  "}{t["topic"]} ({slides_count} slides)</span>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# ██  CPU SCHEDULING SIMULATOR
# ═════════════════════════════════════════════════════════════════════════════

def fcfs(processes):
    procs = sorted(processes, key=lambda x: x[1])
    timeline, current_time, waiting_times = [], 0, {}
    for pid, at, bt in procs:
        start = max(current_time, at)
        end = start + bt
        timeline.append((pid, start, end))
        waiting_times[pid] = start - at
        current_time = end
    wt_list = [waiting_times[p[0]] for p in processes]
    return timeline, wt_list

def sjf(processes):
    remaining = list(processes)
    timeline, current_time, waiting_times = [], 0, {}
    while remaining:
        available = [p for p in remaining if p[1] <= current_time]
        if not available:
            current_time = min(p[1] for p in remaining)
            available = [p for p in remaining if p[1] <= current_time]
        chosen = min(available, key=lambda x: x[2])
        pid, at, bt = chosen
        timeline.append((pid, current_time, current_time + bt))
        waiting_times[pid] = current_time - at
        current_time += bt
        remaining.remove(chosen)
    return timeline, [waiting_times[p[0]] for p in processes]

def round_robin(processes, quantum):
    sorted_p = sorted(processes, key=lambda x: x[1])
    rbt = {p[0]: p[2] for p in sorted_p}
    gantt, t, rq, added, finish = [], 0, [], set(), {}
    # Seed the ready queue with ALL processes that arrive at the first tick
    first_at = sorted_p[0][1]
    t = first_at
    for p in sorted_p:
        if p[1] <= t:
            rq.append(p[0])
            added.add(p[0])
    while len(finish) < len(sorted_p):
        if not rq:
            # Jump directly to next arrival — no O(n-per-tick) spin
            next_at = min(p[1] for p in sorted_p if p[0] not in added)
            t = next_at
            for p in sorted_p:
                if p[1] <= t and p[0] not in added:
                    rq.append(p[0])
                    added.add(p[0])
            continue
        pid = rq.pop(0)
        run = min(quantum, rbt[pid])
        gantt.append((pid, t, t + run))
        t += run
        rbt[pid] -= run
        for p in sorted_p:
            if p[1] <= t and p[0] not in added:
                rq.append(p[0])
                added.add(p[0])
        if rbt[pid] == 0:
            finish[pid] = t
        else:
            rq.append(pid)
    wt = [max(0, finish[p[0]] - p[1] - p[2]) for p in processes]
    return gantt, wt

def draw_gantt(timeline, title="Gantt Chart"):
    """Draw a Gantt chart with grey idle-time bars for CPU gaps."""
    # Insert IDLE segments wherever the CPU has no work
    filled = []
    prev_end = timeline[0][1]  # start from the first process's start time
    for pid, s, e in timeline:
        if s > prev_end:
            filled.append(("IDLE", prev_end, s))
        filled.append((pid, s, e))
        prev_end = e

    fig, ax = styled_fig(12, 2.5)
    colors = [ACCENT, ACCENT2, SUCCESS, WARNING, DANGER, PURPLE, TEAL]
    pid_colors, ci = {}, 0
    for pid, start, end in filled:
        if pid == "IDLE":
            ax.barh(0, end - start, left=start, height=0.6,
                    color="#2a3044", edgecolor="#0f1319", linewidth=1.5)
            ax.text((start + end) / 2, 0, "IDLE", ha='center', va='center',
                    fontsize=8, color='#8892a4', fontfamily='monospace')
        else:
            if pid not in pid_colors:
                pid_colors[pid] = colors[ci % len(colors)]
                ci += 1
            ax.barh(0, end - start, left=start, height=0.6,
                    color=pid_colors[pid], edgecolor="#0f1319", linewidth=1.5)
            ax.text((start + end) / 2, 0, f"P{pid}", ha='center', va='center',
                    fontsize=9, fontweight='bold', color='white', fontfamily='monospace')
    all_times = sorted(set([t[1] for t in filled] + [filled[-1][2]]))
    ax.set_xticks(all_times)
    ax.set_xticklabels([str(t) for t in all_times], color=TEXT_LIGHT, fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("Time Units", color=TEXT_LIGHT)
    ax.set_title(title, color=TEXT_LIGHT, fontfamily='monospace', fontsize=11)
    plt.tight_layout()
    return fig

def page_cpu():
    section_header("⚙️", "CPU Scheduling Simulator",
                   "Simulate FCFS, SJF & Round Robin — compare algorithms visually")

    info_card("What is CPU Scheduling?",
              "The OS decides which process runs on the CPU and when. Try different algorithms below and observe how waiting time changes.", "accent")

    # ── Predefined examples ────────────────────────────────────────────────
    st.markdown('<div class="section-title">📥 Input</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    if c1.button("📘 Basic"):
        st.session_state["cpu_input"] = "P1,0,6\nP2,1,4\nP3,2,2"
    if c2.button("📙 Convoy Effect"):
        st.session_state["cpu_input"] = "P1,0,20\nP2,0,1\nP3,0,1"
    if c3.button("📗 Mixed AT"):
        st.session_state["cpu_input"] = "P1,0,8\nP2,2,4\nP3,4,1\nP4,6,3"
    if c4.button("📕 SJF Classic"):
        st.session_state["cpu_input"] = "P1,0,7\nP2,2,4\nP3,4,1\nP4,5,4"

    col_inp, col_algo = st.columns([2, 1])
    with col_inp:
        raw = st.text_area("Processes (Name, Arrival Time, Burst Time — one per line)",
                           value=st.session_state.get("cpu_input", "P1,0,6\nP2,1,4\nP3,2,2"),
                           height=130, help="Format: Name,ArrivalTime,BurstTime")
    with col_algo:
        algorithms = st.multiselect("Algorithms", ["FCFS", "SJF", "Round Robin"],
                                    default=["FCFS", "SJF", "Round Robin"])
        quantum = st.number_input("RR Quantum", min_value=1, max_value=20, value=2)

    try:
        processes = []
        for i, line in enumerate(raw.strip().split("\n")):
            parts = [p.strip() for p in line.split(",")]
            processes.append((i + 1, int(parts[1]), int(parts[2])))
    except (ValueError, IndexError):
        st.error("⚠️ Invalid format. Use: Name,ArrivalTime,BurstTime")
        return

    df_in = pd.DataFrame([(f"P{p[0]}", p[1], p[2]) for p in processes],
                         columns=["Process", "Arrival Time", "Burst Time"])
    st.dataframe(df_in, use_container_width=True, hide_index=True)
    st.markdown("---")

    # ── Run algorithms ─────────────────────────────────────────────────────
    if not algorithms:
        st.warning("⚠️ Please select at least one algorithm to run.")
        return

    results = {}
    if "FCFS" in algorithms:       results["FCFS"]        = fcfs(processes)
    if "SJF" in algorithms:        results["SJF"]         = sjf(processes)
    if "Round Robin" in algorithms: results["Round Robin"] = round_robin(processes, quantum)

    algo_icons = {"FCFS": "🔵", "SJF": "🟠", "Round Robin": "🟢"}

    for algo_name, (tl, wt) in results.items():
        st.markdown(f'<div class="section-title">{algo_icons.get(algo_name,"")} {algo_name}</div>', unsafe_allow_html=True)
        fig = draw_gantt(tl, f"{algo_name} — Gantt Chart")
        close_show(fig)

        # Per-process metrics table
        pid_finish = {}
        for pid, s, e in tl:
            if e > pid_finish.get(pid, 0):
                pid_finish[pid] = e
        rows = []
        for i, (pid, at, bt) in enumerate(processes):
            ft = pid_finish.get(pid, at + bt)
            tat = ft - at
            wt_val = wt[i] if i < len(wt) else 0
            rows.append((f"P{pid}", at, bt, ft, tat, wt_val))
        df_out = pd.DataFrame(rows, columns=["Process", "AT", "BT", "CT", "TAT", "WT"])
        st.dataframe(df_out, use_container_width=True, hide_index=True)

        avg_wt  = round(sum(r[5] for r in rows) / len(rows), 2)
        avg_tat = round(sum(r[4] for r in rows) / len(rows), 2)
        mc1, mc2 = st.columns(2)
        mc1.metric("Avg Waiting Time",     f"{avg_wt} units")
        mc2.metric("Avg Turnaround Time",  f"{avg_tat} units")

        # What is happening explanation
        explain = {
            "FCFS": "**FCFS:** Processes ran in arrival order. Simple, fair, but can cause convoy effect when a long process arrives first.",
            "SJF": "**SJF:** Shortest burst time ran first. Minimizes average waiting time but requires knowing burst times in advance.",
            "Round Robin": f"**Round Robin (Q={quantum}):** Each process got {quantum} time units then yielded CPU. Fair, prevents starvation, good for interactive systems.",
        }
        st.info(f"💬 **What happened?** {explain.get(algo_name,'')}")

        why_best = {
            "FCFS": "Best when: all jobs have similar burst times, or simplicity is needed. Worst when: long jobs arrive before short ones (convoy effect).",
            "SJF": "Best when: burst times are known in advance, batch systems. Not good for interactive systems because long processes may starve.",
            "Round Robin": f"Best when: interactive or time-sharing system. Quantum {quantum} means response time ≤ {quantum * len(processes)} units for any process.",
        }
        with st.expander(f"📋 Why use {algo_name}? When is it best?"):
            st.markdown(why_best.get(algo_name, ""))
        st.markdown("---")

    # ── Comparison ─────────────────────────────────────────────────────────
    if len(results) > 1:
        section_header("📊", "Algorithm Comparison")
        comp_wt = {}
        comp_tat = {}
        for algo_name, (tl, wt) in results.items():
            pid_finish = {}
            for pid, s, e in tl:
                if e > pid_finish.get(pid, 0): pid_finish[pid] = e
            # Fallback: use at + bt (not 0) so TAT is never negative for unseen pids
            rows = [(processes[i][0], processes[i][1], processes[i][2],
                     pid_finish.get(processes[i][0], processes[i][1] + processes[i][2])) for i in range(len(processes))]
            comp_wt[algo_name]  = round(sum(wt) / len(wt), 2)
            comp_tat[algo_name] = round(sum(r[3] - r[1] for r in rows) / len(rows), 2)

        fig_cmp, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.5))
        for ax in (ax1, ax2):
            ax.set_facecolor(BG_CARD)
            ax.spines[:].set_color("#2a3044")
            ax.tick_params(colors=TEXT_LIGHT)
        fig_cmp.patch.set_facecolor(BG_DARK)

        bar_colors = [ACCENT, ACCENT2, SUCCESS]
        names = list(comp_wt.keys())
        ax1.bar(names, comp_wt.values(), color=bar_colors[:len(names)], edgecolor="#0f1319", width=0.5)
        ax1.set_title("Avg Waiting Time",     color=TEXT_LIGHT, fontfamily='monospace')
        ax1.set_ylabel("Time Units", color=TEXT_LIGHT)
        for i, v in enumerate(comp_wt.values()):
            ax1.text(i, v + 0.1, str(v), ha='center', color=TEXT_LIGHT, fontsize=10)

        ax2.bar(names, comp_tat.values(), color=bar_colors[:len(names)], edgecolor="#0f1319", width=0.5)
        ax2.set_title("Avg Turnaround Time",  color=TEXT_LIGHT, fontfamily='monospace')
        ax2.set_ylabel("Time Units", color=TEXT_LIGHT)
        for i, v in enumerate(comp_tat.values()):
            ax2.text(i, v + 0.1, str(v), ha='center', color=TEXT_LIGHT, fontsize=10)

        plt.tight_layout()
        close_show(fig_cmp)

        best = min(comp_wt, key=comp_wt.get)
        st.success(f"🏆 **Best Algorithm:** {best} (Avg WT = {comp_wt[best]} units)")

        with st.expander("📋 Why others are not best + Common Mistakes"):
            for algo_name in results:
                if algo_name != best:
                    st.markdown(f"**Why not {algo_name}?** Avg WT = {comp_wt[algo_name]} vs {comp_wt[best]} for {best}.")
            st.markdown("---")
            st.markdown("""
**⚠️ Common Student Mistakes in CPU Scheduling:**
- Forgetting to subtract AT when computing WT → WT = TAT − BT, not CT − AT
- Drawing Gantt chart without accounting for idle CPU time (when no process available)
- In Round Robin, not tracking remaining burst time carefully
- Confusing turnaround time (CT−AT) with waiting time (TAT−BT)
- Claiming FCFS never has waiting time — it does whenever a process must wait
""")

# ═════════════════════════════════════════════════════════════════════════════
# ██  MEMORY MANAGEMENT SIMULATOR
# ═════════════════════════════════════════════════════════════════════════════

def fifo_replacement(pages, frames):
    memory, faults, history, order = [], 0, [], []
    for page in pages:
        fault = page not in memory
        if fault:
            faults += 1
            if len(memory) < frames:
                memory.append(page)
                order.append(page)
            else:
                evict = order.pop(0)
                memory[memory.index(evict)] = page
                order.append(page)
        history.append((list(memory), fault, page))
    return history, faults

def lru_replacement(pages, frames):
    memory, faults, history, recently_used = [], 0, [], []
    for page in pages:
        fault = page not in memory
        if fault:
            faults += 1
            if len(memory) < frames:
                memory.append(page)
            else:
                evict = recently_used.pop(0)
                memory[memory.index(evict)] = page
            recently_used.append(page)
        else:
            recently_used.remove(page)
            recently_used.append(page)
        history.append((list(memory), fault, page))
    return history, faults

def optimal_replacement(pages, frames):
    memory, faults, history = [], 0, []
    for i, page in enumerate(pages):
        fault = page not in memory
        if fault:
            faults += 1
            if len(memory) < frames:
                memory.append(page)
            else:
                future_use = {}
                for m in memory:
                    try:    future_use[m] = pages[i+1:].index(m)
                    except: future_use[m] = float('inf')
                evict = max(future_use, key=future_use.get)
                memory[memory.index(evict)] = page
        history.append((list(memory), fault, page))
    return history, faults

def page_memory():
    section_header("🧠", "Memory Management — Page Replacement",
                   "Simulate FIFO, LRU, and Optimal — track page faults step by step")

    info_card("What is Page Replacement?",
              "When RAM is full and a new page is needed, the OS evicts a page to make room. The algorithm chosen determines how many page faults occur.", "accent")

    st.markdown('<div class="section-title">📥 Input</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("📘 Classic Example"):
        st.session_state["mem_pages"] = "7 0 1 2 0 3 0 4 2 3 0 3 2"
        st.session_state["mem_frames"] = 3
    if c2.button("📙 Belady's Anomaly"):
        st.session_state["mem_pages"] = "1 2 3 4 1 2 5 1 2 3 4 5"
        st.session_state["mem_frames"] = 3

    col_p, col_f = st.columns([3, 1])
    with col_p:
        pages_raw = st.text_input("Reference String (space-separated page numbers)",
                                   value=st.session_state.get("mem_pages", "7 0 1 2 0 3 0 4 2 3 0 3 2"))
    with col_f:
        frames = st.number_input("Number of Frames", min_value=1, max_value=8,
                                  value=st.session_state.get("mem_frames", 3))

    try:
        pages = [int(x) for x in pages_raw.strip().split()]
        if not pages:
            raise ValueError("empty")
    except (ValueError, AttributeError):
        st.error("Invalid input — enter space-separated integers.")
        return

    algorithms_mem = st.multiselect("Algorithms", ["FIFO", "LRU", "Optimal"],
                                     default=["FIFO", "LRU", "Optimal"])

    if not algorithms_mem:
        st.warning("⚠️ Please select at least one algorithm to run.")
        return

    # Belady's anomaly info
    if "FIFO" in algorithms_mem:
        st.info("ℹ️ **Belady's Anomaly** (FIFO only): Adding more frames can sometimes INCREASE page faults! Try the Belady example with 3 vs 4 frames.")

    st.markdown("---")

    all_results = {}
    if "FIFO"    in algorithms_mem: all_results["FIFO"]    = fifo_replacement(pages, frames)
    if "LRU"     in algorithms_mem: all_results["LRU"]     = lru_replacement(pages, frames)
    if "Optimal" in algorithms_mem: all_results["Optimal"] = optimal_replacement(pages, frames)

    for algo, (history, faults) in all_results.items():
        icon = {"FIFO": "🔵", "LRU": "🟠", "Optimal": "🟢"}.get(algo, "")
        st.markdown(f'<div class="section-title">{icon} {algo}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Total References", len(pages))
        c2.metric("Page Faults", faults)
        c3.metric("Hit Rate", f"{round((1 - faults/len(pages))*100, 1)}%")

        # Step-by-step table
        rows = []
        for step, (mem_state, fault, page) in enumerate(history):
            row = {"Step": step+1, "Page Ref": page, "Status": "❌ FAULT" if fault else "✅ HIT"}
            for fi in range(frames):
                row[f"Frame {fi+1}"] = mem_state[fi] if fi < len(mem_state) else "—"
            rows.append(row)
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        # Frame-state heatmap
        fig, ax = styled_fig(12, 2.5)
        for step, (mem_state, fault, page) in enumerate(history):
            for fi, pg in enumerate(mem_state):
                is_new = (pg == page and fault)
                color = DANGER if is_new else (ACCENT if pg == page else "#2a3044")
                ax.add_patch(plt.Rectangle((step, fi), 0.9, 0.9,
                                            facecolor=color, edgecolor="#0f1319", linewidth=1))
                ax.text(step+0.45, fi+0.45, str(pg), ha='center', va='center',
                        fontsize=8, color='white', fontfamily='monospace')
        ax.set_xlim(-0.1, len(pages))
        ax.set_ylim(-0.1, frames)
        ax.set_xticks(range(len(pages)))
        ax.set_xticklabels([str(p) for p in pages], fontsize=8, color=TEXT_LIGHT)
        ax.set_yticks([f+0.45 for f in range(frames)])
        ax.set_yticklabels([f"Frame {f+1}" for f in range(frames)], color=TEXT_LIGHT, fontsize=8)
        ax.set_title(f"{algo} — Frame State (🔴=fault load, 🔵=page accessed)", color=TEXT_LIGHT, fontfamily='monospace')
        close_show(fig)

        explain_mem = {
            "FIFO":    f"FIFO evicts the oldest page. Simple but suffers from Belady's Anomaly. Faults: {faults}",
            "LRU":     f"LRU evicts the Least Recently Used page. Good practical performance. Faults: {faults}",
            "Optimal": f"Optimal replaces the page used furthest in the future — theoretical lower bound. Faults: {faults} (minimum possible).",
        }
        st.info(f"💬 {explain_mem.get(algo, '')}")

        why = {
            "FIFO": "Not always best. The Belady's Anomaly means more frames → more faults (counterintuitive!). Not used in modern OS alone.",
            "LRU": "Approximated in real OS using reference bits or clock algorithm. Near-optimal in practice. No Belady's Anomaly.",
            "Optimal": "Cannot be implemented in practice — requires knowing the future. Used only as a benchmark to measure how far other algorithms are from ideal.",
        }
        with st.expander(f"📋 {algo} — Analysis"):
            st.markdown(why.get(algo, ""))
        st.markdown("---")

    # Comparison bar chart
    if len(all_results) > 1:
        section_header("📊", "Page Fault Comparison")
        comp = {a: r[1] for a, r in all_results.items()}
        fig3, ax3 = styled_fig(6, 3)
        colors_bar = [ACCENT, ACCENT2, SUCCESS]
        bars = ax3.bar(comp.keys(), comp.values(), color=colors_bar[:len(comp)],
                       edgecolor="#0f1319", linewidth=1.5, width=0.5)
        for bar, val in zip(bars, comp.values()):
            ax3.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.1, str(val),
                     ha='center', color=TEXT_LIGHT, fontsize=11, fontfamily='monospace')
        ax3.set_ylabel("Page Faults", color=TEXT_LIGHT)
        ax3.set_title("Page Faults Comparison", color=TEXT_LIGHT, fontfamily='monospace')
        close_show(fig3)

        best = min(comp, key=comp.get)
        st.success(f"🏆 **{best}** has fewest page faults ({comp[best]})")
        if "Optimal" in comp:
            st.info("ℹ️ Optimal is always best but CANNOT be used in practice — it requires knowing future page references (impossible at runtime).")

        with st.expander("⚠️ Common Student Mistakes — Memory Management"):
            st.markdown("""
- **Belady's Anomaly**: Students assume more frames always helps — only true for LRU and Optimal, NOT for FIFO
- **Optimal ≠ LRU**: Optimal looks forward (future), LRU looks backward (past history) — different!
- **Page fault ≠ page replacement**: Page fault happens when page not in memory; replacement only if memory is FULL
- **Not tracking the frame state carefully**: In exams, trace each step — write the full frame contents at every reference
- **Forgetting the dirty bit**: In real systems, modified pages must be written to disk before eviction (extra I/O)
""")

# ═════════════════════════════════════════════════════════════════════════════
# ██  DISK SCHEDULING SIMULATOR (extended: + C-SCAN, LOOK, C-LOOK)
# ═════════════════════════════════════════════════════════════════════════════

def disk_fcfs(requests, head):
    order = list(requests)
    path = [head] + order
    seek = sum(abs(path[i+1]-path[i]) for i in range(len(path)-1))
    return order, seek

def disk_sstf(requests, head):
    remaining, current, order, seek = list(requests), head, [], 0
    while remaining:
        closest = min(remaining, key=lambda x: abs(x-current))
        seek += abs(closest-current)
        current = closest
        order.append(closest)
        remaining.remove(closest)
    return order, seek

def disk_scan(requests, head, disk_size=200):
    # r < head (strict): head position itself needs no movement, avoids redundant entry
    left  = sorted([r for r in requests if r < head], reverse=True)
    right = sorted([r for r in requests if r > head])
    order = right + [disk_size-1] + left
    path  = [head] + order
    seek  = sum(abs(path[i+1]-path[i]) for i in range(len(path)-1))
    return order, seek

def disk_cscan(requests, head, disk_size=200):
    # r > head (strict) for right; r <= head for left (excluding current)
    right = sorted([r for r in requests if r > head])
    left  = sorted([r for r in requests if r <= head])
    order = right + [disk_size-1, 0] + left
    path  = [head] + order
    seek  = sum(abs(path[i+1]-path[i]) for i in range(len(path)-1))
    return order, seek

def disk_look(requests, head):
    # r < head (strict): head position itself needs no movement
    left  = sorted([r for r in requests if r < head], reverse=True)
    right = sorted([r for r in requests if r > head])
    order = right + left
    path  = [head] + order
    seek  = sum(abs(path[i+1]-path[i]) for i in range(len(path)-1))
    return order, seek

def disk_clook(requests, head):
    right = sorted([r for r in requests if r >= head])
    left  = sorted([r for r in requests if r < head])
    order = right + left
    path  = [head] + order
    seek  = sum(abs(path[i+1]-path[i]) for i in range(len(path)-1))
    return order, seek

def page_disk():
    section_header("💿", "Disk Scheduling Simulator",
                   "Simulate FCFS, SSTF, SCAN, C-SCAN, LOOK & C-LOOK")

    info_card("What is Disk Scheduling?",
              "The disk read/write head must move between tracks. Scheduling algorithms decide the movement order to minimize total seek distance.", "accent")

    st.markdown('<div class="section-title">📥 Input</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    if c1.button("📘 Example 1"):
        st.session_state["disk_req"]  = "98 183 37 122 14 124 65 67"
        st.session_state["disk_head"] = 53
    if c2.button("📙 Example 2"):
        st.session_state["disk_req"]  = "55 58 39 18 90 160 150 38 184"
        st.session_state["disk_head"] = 100
    if c3.button("📗 Example 3"):
        st.session_state["disk_req"]  = "82 170 43 140 24 16 190"
        st.session_state["disk_head"] = 50

    col_r, col_h = st.columns([3, 1])
    with col_r:
        req_raw  = st.text_input("Request Queue (space-separated track numbers)",
                                  value=st.session_state.get("disk_req", "98 183 37 122 14 124 65 67"))
    with col_h:
        head_pos = st.number_input("Initial Head", min_value=0, max_value=499,
                                    value=st.session_state.get("disk_head", 53))

    disk_size = st.slider("Disk Size (tracks)", 100, 500, 200, 50)
    algorithms_disk = st.multiselect("Algorithms",
                                      ["FCFS", "SSTF", "SCAN", "C-SCAN", "LOOK", "C-LOOK"],
                                      default=["FCFS", "SSTF", "SCAN", "C-LOOK"])

    try:
        requests = [int(x) for x in req_raw.strip().split()]
        if not requests:
            raise ValueError("empty")
    except (ValueError, AttributeError):
        st.error("Invalid input — enter space-separated track numbers.")
        return

    # Validate head position against disk size
    if head_pos >= disk_size:
        st.error(f"⚠️ Initial head position ({head_pos}) must be less than disk size ({disk_size}). Adjust the slider or head position.")
        return

    # Clamp any out-of-range requests to valid track range
    invalid = [r for r in requests if r < 0 or r >= disk_size]
    if invalid:
        st.warning(f"⚠️ Requests {invalid} are out of range [0, {disk_size-1}] and will be ignored.")
        requests = [r for r in requests if 0 <= r < disk_size]
        if not requests:
            st.error("No valid requests remain after filtering.")
            return

    if not algorithms_disk:
        st.warning("⚠️ Please select at least one algorithm to run.")
        return

    st.markdown("---")

    results_disk = {}
    if "FCFS"   in algorithms_disk: results_disk["FCFS"]   = disk_fcfs(requests, head_pos)
    if "SSTF"   in algorithms_disk: results_disk["SSTF"]   = disk_sstf(requests, head_pos)
    if "SCAN"   in algorithms_disk: results_disk["SCAN"]   = disk_scan(requests, head_pos, disk_size)
    if "C-SCAN" in algorithms_disk: results_disk["C-SCAN"] = disk_cscan(requests, head_pos, disk_size)
    if "LOOK"   in algorithms_disk: results_disk["LOOK"]   = disk_look(requests, head_pos)
    if "C-LOOK" in algorithms_disk: results_disk["C-LOOK"] = disk_clook(requests, head_pos)

    if not results_disk:
        return

    # Draw graphs — 3 per row
    algo_list = list(results_disk.items())
    colors_disk = {"FCFS": ACCENT, "SSTF": ACCENT2, "SCAN": SUCCESS,
                   "C-SCAN": WARNING, "LOOK": PURPLE, "C-LOOK": TEAL}

    for row_start in range(0, len(algo_list), 3):
        batch = algo_list[row_start:row_start+3]
        fig, axes = plt.subplots(1, len(batch), figsize=(6*len(batch), 5))
        if len(batch) == 1:
            axes = [axes]
        fig.patch.set_facecolor(BG_DARK)

        for ax, (algo, (order, seek)) in zip(axes, batch):
            ax.set_facecolor(BG_CARD)
            path = [head_pos] + order
            color = colors_disk.get(algo, ACCENT)
            ax.plot(path, range(len(path)), marker='o', color=color,
                    linewidth=2.5, markersize=7, markerfacecolor='white', markeredgecolor=color)
            ax.axvline(x=head_pos, color='yellow', linestyle='--', alpha=0.5, linewidth=1)
            # Annotate requests on Y axis
            for j, t in enumerate(path[1:], 1):
                ax.text(t + 2, j, str(t), va='center', fontsize=7, color='#8892a4')
            ax.set_title(f"{algo}\nSeek: {seek}", color=TEXT_LIGHT, fontfamily='monospace', fontsize=11)
            ax.set_xlabel("Track Number", color=TEXT_LIGHT)
            ax.set_ylabel("Request Order", color=TEXT_LIGHT)
            ax.spines[:].set_color("#2a3044")
            ax.tick_params(colors=TEXT_LIGHT)
            ax.set_xlim(0, disk_size)
            ax.invert_yaxis()

        plt.tight_layout()
        close_show(fig)

    # Summary table
    section_header("📊", "Summary Comparison")
    summary_rows = [(algo, seek, ' → '.join(map(str, [head_pos]+order[:5]))+(' ...' if len(order) > 5 else ''))
                    for algo, (order, seek) in results_disk.items()]
    df_disk = pd.DataFrame(summary_rows, columns=["Algorithm", "Total Seek Distance", "Path (first 5)"])
    st.dataframe(df_disk, use_container_width=True, hide_index=True)

    best_disk = min(results_disk, key=lambda k: results_disk[k][1])
    st.success(f"🏆 **{best_disk}** minimizes total seek distance ({results_disk[best_disk][1]} tracks)")

    # Algorithm explanations
    algo_explain = {
        "FCFS":   "Services requests in arrival order. Fair but inefficient — large head movement.",
        "SSTF":   "Always picks the closest request. Greedy — good average but risks **starvation** of far tracks.",
        "SCAN":   "Elevator algorithm — moves in one direction to end of disk, reverses. Fair, no starvation.",
        "C-SCAN": "One-directional SCAN — jumps from end back to start. More uniform wait times.",
        "LOOK":   "Like SCAN but only goes as far as the last request in each direction. More efficient than SCAN.",
        "C-LOOK": "Like C-SCAN but jumps back to lowest request (not track 0). Best practical algorithm.",
    }
    with st.expander("📋 Algorithm Explanations"):
        for algo, (order, seek) in results_disk.items():
            color = colors_disk.get(algo, ACCENT)
            st.markdown(f'<span style="color:{color}">**{algo}**</span>: {algo_explain.get(algo,"")}', unsafe_allow_html=True)

    with st.expander("⚠️ Common Student Mistakes — Disk Scheduling"):
        st.markdown("""
- **SCAN vs LOOK**: Students often draw SCAN stopping at last request — SCAN goes to END of disk; LOOK stops at last request
- **Seek distance calculation**: Must include the jump back in C-SCAN (from last track to 0, then to first request)
- **SSTF starvation**: Students think SSTF is always best — it can starve requests far from the current head position
- **SSDs**: Disk scheduling algorithms are irrelevant for SSDs — no physical head movement
- **Not accounting for direction**: SCAN must continue in current direction first, not jump to closest
""")

# ═════════════════════════════════════════════════════════════════════════════
# ██  SYSTEM MONITOR
# ═════════════════════════════════════════════════════════════════════════════

def page_monitor():
    section_header("📊", "System Monitor", "Live OS metrics from your machine via psutil")
    st.markdown('<p style="color:#8892a4;font-size:13px">Real system data. Demonstrates OS resource management in action.</p>', unsafe_allow_html=True)

    auto_refresh = st.toggle("🔄 Auto Refresh (every 2s)", value=False)

    # ── CPU ────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🖥️ CPU</div>', unsafe_allow_html=True)
    cpu_pct   = psutil.cpu_percent(interval=0.5)
    cpu_count = psutil.cpu_count()
    cpu_freq  = psutil.cpu_freq()
    load_avg  = psutil.getloadavg() if hasattr(psutil, 'getloadavg') else (0, 0, 0)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("CPU Usage",   f"{cpu_pct}%")
    c2.metric("CPU Cores",   cpu_count)
    c3.metric("Frequency",   f"{cpu_freq.current:.0f} MHz" if cpu_freq else "N/A")
    c4.metric("Load Avg 1m", f"{load_avg[0]:.2f}")

    per_core = psutil.cpu_percent(interval=0.1, percpu=True)
    fig_cpu, ax_cpu = styled_fig(10, 2.5)
    colors_cpu = [SUCCESS if p < 50 else WARNING if p < 80 else DANGER for p in per_core]
    bars = ax_cpu.bar([f"C{i}" for i in range(len(per_core))], per_core,
                      color=colors_cpu, edgecolor="#0f1319")
    for bar, val in zip(bars, per_core):
        ax_cpu.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5, f"{val}%",
                    ha='center', va='bottom', color=TEXT_LIGHT, fontsize=8)
    ax_cpu.set_ylim(0, 105)
    ax_cpu.set_ylabel("Usage %", color=TEXT_LIGHT)
    ax_cpu.set_title("Per-Core CPU Usage (🟢<50% 🟡<80% 🔴>80%)", color=TEXT_LIGHT, fontfamily='monospace')
    close_show(fig_cpu)

    info_card("What you're seeing",
              "The OS scheduler distributes processes across these cores. High usage = many processes competing for CPU. This is CPU scheduling in action!", "teal")

    # ── Memory ─────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🧠 Memory</div>', unsafe_allow_html=True)
    mem  = psutil.virtual_memory()
    swap = psutil.swap_memory()

    cm1, cm2, cm3, cm4 = st.columns(4)
    cm1.metric("Total RAM",  f"{mem.total/1e9:.1f} GB")
    cm2.metric("Used",       f"{mem.used/1e9:.1f} GB")
    cm3.metric("Available",  f"{mem.available/1e9:.1f} GB")
    cm4.metric("Usage",      f"{mem.percent}%")

    fig_mem, ax_mem = styled_fig(8, 1.8)
    used_pct = mem.percent
    color_mem = SUCCESS if used_pct < 60 else WARNING if used_pct < 85 else DANGER
    ax_mem.barh(0, used_pct, color=color_mem, height=0.5, edgecolor="#0f1319")
    ax_mem.barh(0, 100-used_pct, left=used_pct, color="#2a3044", height=0.5)
    ax_mem.text(used_pct/2, 0, f"Used {used_pct}%", ha='center', va='center',
                color='white', fontsize=11, fontfamily='monospace')
    ax_mem.set_xlim(0, 100); ax_mem.set_yticks([])
    ax_mem.set_title("RAM Utilization", color=TEXT_LIGHT, fontfamily='monospace')
    close_show(fig_mem)

    s1, s2, s3 = st.columns(3)
    s1.metric("Swap Total", f"{swap.total/1e9:.1f} GB")
    s2.metric("Swap Used",  f"{swap.used/1e9:.1f} GB")
    s3.metric("Swap %",     f"{swap.percent}%")
    if swap.percent > 20:
        st.warning("⚠️ High swap usage! This means the system may be **thrashing** — processes are using more memory than available RAM.")

    # ── Processes ──────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">🔄 Processes</div>', unsafe_allow_html=True)
    procs_data = []
    for p in psutil.process_iter(['pid', 'name', 'status', 'cpu_percent', 'memory_percent', 'num_threads']):
        try:
            procs_data.append({
                "PID": p.info['pid'],
                "Name": p.info['name'][:25],
                "State": p.info['status'],
                "CPU %": round(p.info['cpu_percent'] or 0, 2),
                "Mem %": round(p.info['memory_percent'] or 0, 2),
                "Threads": p.info.get('num_threads', '?'),
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    df_procs = pd.DataFrame(procs_data).sort_values("CPU %", ascending=False).head(20)
    st.dataframe(df_procs, use_container_width=True, hide_index=True)

    # State distribution pie chart
    if procs_data:
        state_counts = pd.DataFrame(procs_data)['State'].value_counts()
        fig_pie, ax_pie = styled_fig(5, 3)
        pie_colors = [ACCENT, SUCCESS, WARNING, DANGER, PURPLE, TEAL, ACCENT2]
        wedges, texts, autotexts = ax_pie.pie(
            state_counts.values, labels=state_counts.index,
            colors=pie_colors[:len(state_counts)],
            autopct='%1.1f%%', startangle=90,
            textprops={'color': TEXT_LIGHT, 'fontsize': 9})
        for a in autotexts: a.set_color('white')
        ax_pie.set_title("Process State Distribution", color=TEXT_LIGHT, fontfamily='monospace')
        close_show(fig_pie)

        info_card("Process States in Action",
                  "Most processes are 'sleeping' (waiting for I/O or events). Very few are 'running' at any moment — this is why the OS needs scheduling!", "teal")

    # ── Disk ───────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown('<div class="section-title">💾 Disk Partitions</div>', unsafe_allow_html=True)
    disk_info = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disk_info.append({"Device": part.device, "Mount": part.mountpoint,
                               "FS": part.fstype,
                               "Total (GB)": round(usage.total/1e9, 1),
                               "Used (GB)":  round(usage.used/1e9, 1),
                               "Free (GB)":  round(usage.free/1e9, 1),
                               "Usage %":    usage.percent})
        except (PermissionError, OSError):
            pass
    if disk_info:
        st.dataframe(pd.DataFrame(disk_info), use_container_width=True, hide_index=True)

    if auto_refresh:
        time.sleep(2)
        st.rerun()

# ═════════════════════════════════════════════════════════════════════════════
# ██  HOME
# ═════════════════════════════════════════════════════════════════════════════

def page_home():
    st.markdown(f'<div style="font-family:Space Mono,monospace;font-size:2.8rem;font-weight:700;background:linear-gradient(135deg,{ACCENT},{ACCENT2});-webkit-background-clip:text;-webkit-text-fill-color:transparent">Operating Systems<br>Teaching Platform</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#8892a4;font-size:1.05rem;margin-top:8px">A complete interactive classroom tool · Full OS Syllabus · Simulations · Diagrams</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Module cards — row 1
    r1 = st.columns(3)
    cards1 = [
        ("📚", "Learn Mode",       "Full OS syllabus with 30+ slides covering theory, analogies, and formulas.", ACCENT,  "Section 1 + 2"),
        ("⚙️", "CPU Scheduling",  "FCFS · SJF · Round Robin — Gantt charts, WT/TAT tables, algorithm comparison.",  WARNING, "3 Algorithms"),
        ("🧠", "Memory Mgmt",     "FIFO · LRU · Optimal page replacement — step-by-step visualization.",           SUCCESS, "3 Algorithms"),
    ]
    for col, (icon, title, desc, color, badge) in zip(r1, cards1):
        col.markdown(f"""
        <div class="os-card" style="border-top:3px solid {color};text-align:center;min-height:170px">
            <div style="font-size:2.2rem">{icon}</div>
            <div style="font-family:Space Mono,monospace;font-size:0.95rem;color:{color};margin:8px 0">{title}</div>
            <div style="font-size:12px;color:#8892a4;margin-bottom:8px">{desc}</div>
            <span class="tag">{badge}</span>
        </div>""", unsafe_allow_html=True)

    r2 = st.columns(3)
    cards2 = [
        ("💿", "Disk Scheduling", "FCFS · SSTF · SCAN · C-SCAN · LOOK · C-LOOK — head movement graphs.",    DANGER,  "6 Algorithms"),
        ("📊", "System Monitor",  "Live CPU, memory, process, and disk stats from your real system.",       TEAL,    "Real-time"),
        ("📋", "Full Syllabus",   "All OS topics with analogies, teacher notes, and common mistakes always visible.", PURPLE, "Always On"),
    ]
    for col, (icon, title, desc, color, badge) in zip(r2, cards2):
        col.markdown(f"""
        <div class="os-card" style="border-top:3px solid {color};text-align:center;min-height:170px">
            <div style="font-size:2.2rem">{icon}</div>
            <div style="font-family:Space Mono,monospace;font-size:0.95rem;color:{color};margin:8px 0">{title}</div>
            <div style="font-size:12px;color:#8892a4;margin-bottom:8px">{desc}</div>
            <span class="tag">{badge}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    # Syllabus overview
    st.markdown('<div class="section-title">📋 Full Syllabus Coverage</div>', unsafe_allow_html=True)
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.markdown(f'<b style="color:{ACCENT}">Section 1 — Foundations</b>', unsafe_allow_html=True)
        for item in ["Introduction to OS (functions, hardware interaction)", "Types of OS (Batch, Multiprogramming, Time-sharing, RTOS)", "System Calls & Linux Commands", "Process Management (PCB, Context Switching)", "Process States (3, 5, 7-state models)", "Threads (Process vs Thread, ULT vs KLT, Models)", "Concurrency (Race Condition, Critical Section, Semaphores)"]:
            st.markdown(f"✅ {item}")
    with col_s2:
        st.markdown(f'<b style="color:{ACCENT2}">Section 2 — Core Algorithms</b>', unsafe_allow_html=True)
        for item in ["CPU Scheduling — deep dive (FCFS, SJF, RR, Priority)", "Deadlocks (4 conditions, RAG, Banker's Algorithm)", "Prevention · Avoidance · Detection · Recovery", "Memory: Logical vs Physical, Paging, Segmentation", "Virtual Memory, Demand Paging, Thrashing", "Page Replacement (FIFO, LRU, Optimal)", "Disk Scheduling (FCFS, SSTF, SCAN, C-SCAN, LOOK, C-LOOK)"]:
            st.markdown(f"✅ {item}")

    st.markdown("---")
    i1, i2, i3 = st.columns(3)
    i1.info("📚 Start in **Learn Mode** → pick a section → navigate slides like a presentation.")
    i2.success("⚙️ Use **predefined example** buttons in simulators for instant classroom demos.")
    i3.warning("🎓 All teacher notes, analogies, and common mistakes are always shown — ready for classroom use.")

# ═════════════════════════════════════════════════════════════════════════════
# MAIN ROUTER
# ═════════════════════════════════════════════════════════════════════════════

# Classroom-mode fonts are always applied via global CSS above

if module == "🏠 Home":
    page_home()
elif module == "📚 Learn Mode":
    page_learn()
elif module == "⚙️ CPU Scheduling":
    page_cpu()
elif module == "🧠 Memory Management":
    page_memory()
elif module == "💿 Disk Scheduling":
    page_disk()
elif module == "📊 System Monitor":
    page_monitor()
