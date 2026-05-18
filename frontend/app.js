// SRE Gateway Mapping & Configurations
const SERVICES = {
    auth: '/api/auth/',
    user: '/api/users/',
    product: '/api/products/',
    order: '/api/orders/',
    payment: '/api/payment/',
    notification: '/api/notification/'
};

let allTasks = [];
let teamMembers = [];
let activeTaskId = null;

// ── 1. CLUSTER STATUS CONTROLLER ──────────────────────────────────────────
async function checkClusterStatus() {
    for (const [key, base_url] of Object.entries(SERVICES)) {
        const badge = document.getElementById(`badge-${key}`);
        try {
            const res = await fetch(`${base_url}health`);
            if (res.ok) {
                const data = await res.json();
                if (data.status === 'healthy') {
                    badge.className = "status-indicator green";
                } else {
                    badge.className = "status-indicator red";
                }
            } else {
                badge.className = "status-indicator red";
            }
        } catch (e) {
            badge.className = "status-indicator red";
        }
    }
}

// ── 2. DATA FECHERS & INTEGRATIONS ──────────────────────────────────────
async function loadSreDashboard() {
    await checkClusterStatus();
    await loadTeamProfiles();
    await loadBoardTasks();
    await loadActivityLogs();
}

async function loadTeamProfiles() {
    try {
        const res = document.getElementById('badge-auth').classList.contains('red') 
            ? null 
            : await fetch(SERVICES.auth);
            
        if (res && res.ok) {
            const data = await res.json();
            teamMembers = data.users || [];
            
            // Populate select dropdown in modal
            const select = document.getElementById('select-assignee');
            select.innerHTML = '<option value="">-- Unassigned --</option>';
            teamMembers.forEach(user => {
                select.innerHTML += `<option value="${user.id}">${user.name} (${user.role})</option>`;
            });
            
            document.getElementById('val-active-devs').innerText = teamMembers.length;
        }
    } catch (e) {
        console.error("Failed to load user profiles", e);
    }
}

async function loadBoardTasks() {
    let catalogTasks = [];
    let activeBoardTasks = [];
    
    // Clear Board columns
    const containers = {
        backlog: document.getElementById('container-backlog'),
        todo: document.getElementById('container-todo'),
        in_progress: document.getElementById('container-in-progress'),
        done: document.getElementById('container-done')
    };
    Object.values(containers).forEach(c => c.innerHTML = '');

    // Fetch Backlog items from Product service
    try {
        const res = await fetch(SERVICES.product);
        if (res.ok) {
            const data = await res.json();
            catalogTasks = data.tasks || [];
        }
    } catch (e) {
        appendTerminalLog("OUTAGE ERROR: Unable to reach Product Service (Catalog API)", "critical");
    }

    // Fetch Active items from Order service
    try {
        const res = await fetch(SERVICES.order);
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'offline') {
                appendTerminalLog("CRITICAL ALERT: ORDER-SERVICE DATABASE CONNECTION FAILING! (DB_HOST Outage)", "critical");
            } else {
                activeBoardTasks = data.tasks || [];
            }
        }
    } catch (e) {
        appendTerminalLog("OUTAGE ERROR: Unable to reach Order Service (Kanban API)", "critical");
    }

    // Combine All tasks
    allTasks = [...catalogTasks, ...activeBoardTasks];

    // Filter duplicates by favoring active board states
    const uniqueTasksMap = {};
    allTasks.forEach(t => {
        uniqueTasksMap[t.id] = t;
    });
    const uniqueTasks = Object.values(uniqueTasksMap);

    let totalPoints = 0;
    const counts = { backlog: 0, todo: 0, in_progress: 0, done: 0 };

    // Render cards
    uniqueTasks.forEach(task => {
        const col = task.column || 'backlog';
        if (containers[col]) {
            counts[col]++;
            totalPoints += task.points || 0;
            
            const assigneeName = task.assignee_name || "Unassigned";
            const initials = task.assignee_name 
                ? task.assignee_name.split(' ').map(n => n[0]).join('') 
                : "?";
            
            let priorityClass = "priority-low";
            if (task.priority === "High") priorityClass = "priority-high";
            else if (task.priority === "Medium") priorityClass = "priority-medium";

            const cardHtml = `
                <div class="task-card" onclick="openMoveModal('${task.id}')">
                    <span class="card-priority ${priorityClass}">${task.priority}</span>
                    <h3 class="card-title">${task.title}</h3>
                    <p class="card-desc">${task.desc}</p>
                    <div class="card-footer">
                        <div class="card-points">${task.points} SP</div>
                        <div class="card-assignee" title="${assigneeName}">${initials}</div>
                    </div>
                </div>
            `;
            containers[col].innerHTML += cardHtml;
        }
    });

    // Update Counts & Total Points
    document.getElementById('val-total-points').innerText = totalPoints;
    for (const [col, count] of Object.entries(counts)) {
        document.getElementById(`count-${col}`).innerText = count;
    }

    // Dynamic Sprint Velocity Cost computation via Payment Service
    try {
        const res = await fetch(`${SERVICES.payment}calculate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ total_points: totalPoints })
        });
        if (res.ok) {
            const data = await res.json();
            document.getElementById('val-sprint-cost').innerText = data.total_sprint_cost || `$${(totalPoints * 120).toLocaleString()}`;
        } else {
            // HTTP error fallback (e.g. 405, 502, 404)
            document.getElementById('val-sprint-cost').innerText = `$${(totalPoints * 120).toLocaleString()}`;
        }
    } catch (e) {
        // Network error fallback
        document.getElementById('val-sprint-cost').innerText = `$${(totalPoints * 120).toLocaleString()}`;
    }
}

// ── 3. LIVE TERMINAL LOGS ────────────────────────────────────────────────
async function loadActivityLogs() {
    try {
        const res = await fetch(SERVICES.notification);
        if (res.ok) {
            const data = await res.json();
            const logs = data.logs || [];
            const term = document.getElementById('terminal-stream');
            term.innerHTML = '';
            logs.forEach(log => {
                let colClass = "green";
                if (log.severity === "warning") colClass = "yellow";
                else if (log.severity === "critical") colClass = "red";
                
                term.innerHTML += `<div class="term-line"><span class="term-time">[${log.timestamp}]</span> <span class="term-msg ${colClass}">${log.event}</span></div>`;
            });
        }
    } catch (e) {
        console.error("Failed to load notification logs", e);
    }
}

function appendTerminalLog(message, severity = "info") {
    // Add local log instantly for reactive UX
    const term = document.getElementById('terminal-stream');
    const timeStr = new Date().toLocaleTimeString();
    let colClass = "green";
    if (severity === "warning") colClass = "yellow";
    else if (severity === "critical") colClass = "red";

    term.innerHTML = `<div class="term-line"><span class="term-time">[${timeStr}]</span> <span class="term-msg ${colClass}">${message}</span></div>` + term.innerHTML;
    
    // Forward audit event log to Notification microservice
    fetch(`${SERVICES.notification}log`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ event: message, severity: severity })
    }).catch(e => console.error("Logger dispatch offline"));
}

// ── 4. KANBAN MODAL OPERATIONS ───────────────────────────────────────────
function openMoveModal(taskId) {
    activeTaskId = taskId;
    const task = allTasks.find(t => t.id === taskId);
    if (!task) return;

    document.getElementById('modal-task-title').innerText = `${task.title} (${task.points} Story Points)`;
    document.getElementById('select-column').value = task.column || 'backlog';
    document.getElementById('select-assignee').value = task.assignee_id || '';
    
    document.getElementById('move-modal').classList.add('active');
}

function closeModal() {
    document.getElementById('move-modal').classList.remove('active');
    activeTaskId = null;
}

// Handle State changes
document.getElementById('btn-submit-move').addEventListener('click', async () => {
    if (!activeTaskId) return;

    const newCol = document.getElementById('select-column').value;
    const assigneeId = document.getElementById('select-assignee').value;
    const userObj = teamMembers.find(u => u.id === assigneeId);
    const assigneeName = userObj ? userObj.name : "";

    const task = allTasks.find(t => t.id === activeTaskId);
    const prevCol = task ? (task.column || 'backlog') : 'unknown';

    try {
        const res = await fetch(`${SERVICES.order}move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                task_id: activeTaskId,
                column: newCol,
                assignee_id: assigneeId,
                assignee_name: assigneeName
            })
        });

        if (res.ok) {
            const data = await res.json();
            closeModal();
            
            // Dispatch logs
            const taskTitle = task ? task.title : activeTaskId;
            const logMsg = assigneeName 
                ? `${assigneeName} assigned and moved "${taskTitle}" from [${prevCol.toUpperCase()}] to [${newCol.toUpperCase()}].`
                : `Unassigned card "${taskTitle}" moved from [${prevCol.toUpperCase()}] to [${newCol.toUpperCase()}].`;
            
            appendTerminalLog(logMsg, newCol === 'done' ? 'success' : 'info');
            
            // Reload layout states
            await loadBoardTasks();
        } else {
            const err = await res.json();
            appendTerminalLog(`STATE ERROR: Moving task failed. Details: ${err.detail || 'Service returned error.'}`, "critical");
        }
    } catch (e) {
        appendTerminalLog("CRITICAL ERROR: Unable to apply state transition. Order Service cluster node offline!", "critical");
    }
});

// ── 5. INITIALIZATION & REPEATER ─────────────────────────────────────────
loadSreDashboard();

// Poll every 3 seconds for live active changes
setInterval(loadSreDashboard, 3000);
