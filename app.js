// --- STATE & DATA ---
const STORAGE_KEY = 'smartFocusData';
const THEME_KEY = 'smartFocusTheme';

let state = {
    timeLeft: 25 * 60, // mặc định 25 phút
    mode: 'focus',     // 'focus' | 'break'
    isRunning: false,
    tasks: [],
    stats: {
        pomoCount: 0,
        totalTime: 0   // phút
    }
};

let timerInterval = null;

// --- DOM ELEMENTS ---
const timeDisplay = document.getElementById('timeDisplay');
const timerMode = document.getElementById('timerMode');
const characterState = document.getElementById('characterState');

const btnStart = document.getElementById('btnStart');
const btnPause = document.getElementById('btnPause');
const btnReset = document.getElementById('btnReset');

const taskNameInput = document.getElementById('taskName');
const taskEstInput = document.getElementById('taskEst');
const btnAddTask = document.getElementById('btnAddTask');
const taskList = document.getElementById('taskList');

const statPomoCount = document.getElementById('statPomoCount');
const statTotalTime = document.getElementById('statTotalTime');

const youtubeLinkInput = document.getElementById('youtubeLink');
const youtubeIframe = document.getElementById('youtubeIframe');
const themeToggle = document.getElementById('themeToggle');

// --- INIT & LOCAL STORAGE ---
function init() {
    loadData();
    applyTheme();
    updateTimerUI();
    renderTasks();
    updateStatsUI();
}

function loadData() {
    try {
        const data = localStorage.getItem(STORAGE_KEY);
        if (data) {
            const parsed = JSON.parse(data);
            state.tasks = parsed.tasks || [];
            state.stats = parsed.stats || { pomoCount: 0, totalTime: 0 };
        }
    } catch (e) {
        console.error("Lỗi khi đọc dữ liệu LocalStorage:", e);
    }
}

function saveData() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify({
        tasks: state.tasks,
        stats: state.stats
    }));
}

function applyTheme() {
    const savedTheme = localStorage.getItem(THEME_KEY);
    if (savedTheme === 'dark') {
        document.body.setAttribute('data-theme', 'dark');
    } else {
        document.body.removeAttribute('data-theme');
    }
}

// --- TIMER LOGIC ---
function formatTime(seconds) {
    const m = Math.floor(seconds / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

function updateTimerUI() {
    timeDisplay.textContent = formatTime(state.timeLeft);
    const titleStatus = state.mode === 'focus' ? 'Làm việc' : 'Nghỉ ngơi';
    document.title = `${formatTime(state.timeLeft)} - ${titleStatus}`;
}

function playNotification() {
    // Âm thanh thông báo đơn giản bằng bộ tổng hợp web audio hoặc HTML Audio (sử dụng base64 beep cho chắc chắn)
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
    const oscillator = audioCtx.createOscillator();
    const gainNode = audioCtx.createGain();

    oscillator.type = 'bell';
    oscillator.frequency.setValueAtTime(880, audioCtx.currentTime); // A5
    gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime);
    
    oscillator.connect(gainNode);
    gainNode.connect(audioCtx.destination);
    
    oscillator.start();
    gainNode.gain.exponentialRampToValueAtTime(0.00001, audioCtx.currentTime + 1);
    oscillator.stop(audioCtx.currentTime + 1);
}

function switchMode() {
    if (state.mode === 'focus') {
        // Hoàn thành 1 Pomodoro
        state.stats.pomoCount++;
        state.stats.totalTime += 25;
        saveData();
        updateStatsUI();
        
        state.mode = 'break';
        state.timeLeft = 5 * 60; // 5 phút nghỉ
        timerMode.textContent = 'Chế độ Nghỉ ngơi ☕';
        characterState.textContent = '☕ Chơi thôi...';
        playNotification();
        alert('Tuyệt vời! Bạn đã hoàn thành 1 phiên làm việc. Hãy nghỉ ngơi 5 phút nhé.');
    } else {
        // Hết giờ nghỉ
        state.mode = 'focus';
        state.timeLeft = 25 * 60; // 25 phút làm
        timerMode.textContent = 'Chế độ Làm việc 🔴';
        characterState.textContent = '👨‍💻 Tập trung...';
        playNotification();
        alert('Hết giờ nghỉ! Quay lại làm việc nào.');
    }
    updateTimerUI();
}

function startTimer() {
    if (state.isRunning) return;
    
    state.isRunning = true;
    btnStart.disabled = true;
    btnPause.disabled = false;
    
    characterState.textContent = state.mode === 'focus' ? '🔥 Đang cháy!' : '💆 Thư giãn...';

    timerInterval = setInterval(() => {
        state.timeLeft--;
        
        if (state.timeLeft <= 0) {
            clearInterval(timerInterval);
            state.isRunning = false;
            btnStart.disabled = false;
            btnPause.disabled = true;
            
            switchMode();
        }
        
        updateTimerUI();
    }, 1000);
}

function pauseTimer() {
    clearInterval(timerInterval);
    state.isRunning = false;
    btnStart.disabled = false;
    btnPause.disabled = true;
    characterState.textContent = '⏸️ Đã tạm dừng';
}

function resetTimer() {
    clearInterval(timerInterval);
    state.isRunning = false;
    btnStart.disabled = false;
    btnPause.disabled = true;
    
    if (state.mode === 'focus') {
         state.timeLeft = 25 * 60;
         characterState.textContent = '👨‍💻 Đang sẵn sàng...';
    } else {
         state.timeLeft = 5 * 60;
         characterState.textContent = '☕ Đang nghỉ ngơi...';
    }
    updateTimerUI();
}

btnStart.addEventListener('click', startTimer);
btnPause.addEventListener('click', pauseTimer);
btnReset.addEventListener('click', resetTimer);

// --- TASK MANAGER ---
function renderTasks() {
    taskList.innerHTML = '';
    
    if (state.tasks.length === 0) {
        taskList.innerHTML = '<li class="task-item" style="justify-content: center; opacity: 0.5;">Chưa có công việc nào.</li>';
        return;
    }

    state.tasks.forEach(task => {
        const li = document.createElement('li');
        li.className = `task-item ${task.completed ? 'completed' : ''}`;
        
        li.innerHTML = `
            <span class="task-text">
                ${task.name} 
                <small>(${task.est} pomodoro)</small>
            </span>
            ${!task.completed ? 
                `<button class="btn-success" onclick="completeTask('${task.id}')">Hoàn thành</button>` : 
                `<span style="margin-right: 10px;">✅</span>`
            }
        `;
        taskList.appendChild(li);
    });
}

function addTask() {
    const name = taskNameInput.value.trim();
    const est = parseInt(taskEstInput.value, 10);
    
    if (!name || isNaN(est) || est < 1) return;
    
    state.tasks.unshift({
        id: Date.now().toString(),
        name,
        est,
        completed: false
    });
    
    taskNameInput.value = '';
    taskEstInput.value = '1';
    
    saveData();
    renderTasks();
}

window.completeTask = (id) => {
    const taskIndex = state.tasks.findIndex(t => t.id === id);
    if (taskIndex !== -1) {
        state.tasks[taskIndex].completed = true;
        // Đẩy task đã hoàn thành xuống cuối
        const completedTask = state.tasks.splice(taskIndex, 1)[0];
        state.tasks.push(completedTask);
        
        saveData();
        renderTasks();
    }
};

btnAddTask.addEventListener('click', addTask);
taskNameInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addTask();
});

// --- STATS UI ---
function updateStatsUI() {
    statPomoCount.textContent = state.stats.pomoCount;
    statTotalTime.textContent = state.stats.totalTime;
}

// --- YOUTUBE INTEGRATION ---
youtubeLinkInput.addEventListener('input', (e) => {
    const url = e.target.value.trim();
    let videoId = 'jfKfPfyJRdk'; // Lofi Girl mặc định
    
    if (url) {
        const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
        const match = url.match(regExp);
        if (match && match[2].length === 11) {
            videoId = match[2];
        }
    }
    
    youtubeIframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
});

// --- THEME ---
themeToggle.addEventListener('click', () => {
    const isDark = document.body.hasAttribute('data-theme');
    
    if (isDark) {
        document.body.removeAttribute('data-theme');
        localStorage.setItem(THEME_KEY, 'light');
    } else {
        document.body.setAttribute('data-theme', 'dark');
        localStorage.setItem(THEME_KEY, 'dark');
    }
});

// Chạy ứng dụng
document.addEventListener("DOMContentLoaded", init);
