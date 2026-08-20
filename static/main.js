// 当前活跃的 SSE 连接与 AI 回复容器引用
let currentEventSource = null;
let aiMessageDiv = null;
let finalAnswer = null;
let thoughtQuote = null;
let chatMessages = null;
let chat_state = 'idle';

function getMarkedText(text) {
    return DOMPurify.sanitize(marked.parse(text))
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showErrorToast(message) {
    const toastEl = document.getElementById('errorToast');
    const toastBody = toastEl.querySelector('.toast-body');
    toastBody.textContent = message;
    const toast = new bootstrap.Toast(toastEl);
    toast.show();
}

function toggle_chat_state(state) {
    chat_state = state;
    document.getElementById('send-spinner').style.display = state === 'working' ? '' : 'none';
}

// 创建一条 AI 回复的容器：可选包含「思考过程」折叠区，始终包含最终答案区
function createAIResponseContainer(showThinking) {
    aiMessageDiv = document.createElement('div');
    aiMessageDiv.className = 'message ai-message';

    const iconDiv = document.createElement('div');
    iconDiv.className = 'message-icon';
    const icon = document.createElement('i');
    icon.className = 'bi bi-robot';
    iconDiv.appendChild(icon);

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    if (showThinking) {
        thoughtQuote = document.createElement('div');
        thoughtQuote.className = 'thought-quote';
        thoughtQuote.innerHTML = `
            <div class="quote-header">
                <span>思考过程</span>
                <span class="toggle-icon expanded"><i class="bi bi-chevron-down"></i></span>
            </div>
            <div class="quote-content"></div>
        `;
        thoughtQuote.addEventListener('click', function (e) {
            if (e.target.closest('.quote-header')) {
                const isCollapsing = !this.classList.contains('collapsed');
                this.classList.toggle('collapsed');
                const iconEl = this.querySelector('.toggle-icon');
                iconEl.innerHTML = isCollapsing ? '<i class="bi bi-chevron-up"></i>' : '<i class="bi bi-chevron-down"></i>';
            }
        });
        contentDiv.appendChild(thoughtQuote);
    } else {
        thoughtQuote = null;
    }

    finalAnswer = document.createElement('div');
    finalAnswer.className = 'ai-final-answer';
    contentDiv.appendChild(finalAnswer);

    aiMessageDiv.appendChild(iconDiv);
    aiMessageDiv.appendChild(contentDiv);
    chatMessages.appendChild(aiMessageDiv);
    scrollView();
}

function createChat() {
    const showThinking = document.getElementById('longThoughtCheckbox').checked;
    const promptInput = document.getElementById('messageInput');
    const prompt = promptInput.value.trim();

    if (!prompt) {
        showErrorToast("请输入有效的问题");
        promptInput.focus();
        return;
    }

    if (currentEventSource) {
        currentEventSource.close();
        currentEventSource = null;
    }

    fetch('/tasks', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt })
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.detail || '请求失败'); });
            }
            return response.json();
        })
        .then(data => {
            if (!data.task_id) {
                throw new Error('无效的任务 ID');
            }
            addMessage(prompt, 'user');
            setupSSE(data.task_id, showThinking);
            promptInput.value = '';
        })
        .catch(error => {
            showErrorToast(error.message);
            console.error('Failed to create task:', error);
        });
}

function setupSSE(taskId, showThinking) {
    let retryCount = 0;
    const maxRetries = 3;
    const retryDelay = 2000;
    let lastResultContent = '';
    let responseContainerCreated = false;

    function ensureResponseContainer() {
        if (responseContainerCreated) return;
        responseContainerCreated = true;
        createAIResponseContainer(showThinking);
    }

    function connect() {
        const eventSource = new EventSource(`/tasks/${taskId}/events`);
        currentEventSource = eventSource;

        // 思考过程事件
        eventSource.addEventListener('think', (event) => {
            if (!showThinking) return;
            try {
                const data = JSON.parse(event.data);
                ensureResponseContainer();
                const stepDiv = document.createElement('div');
                stepDiv.className = 'thinking-message';
                stepDiv.textContent = data.result;
                thoughtQuote.querySelector('.quote-content').appendChild(stepDiv);
                scrollView();
            } catch (e) {
                console.error('Error handling think event:', e);
            }
        });

        // 任务执行失败
        eventSource.addEventListener('task_error', (event) => {
            try {
                const data = JSON.parse(event.data);
                const errorMsg = data.message || '未知错误';
                ensureResponseContainer();
                if (finalAnswer) {
                    finalAnswer.innerHTML = '<div class="text-danger"><strong>执行失败：</strong>' + escapeHtml(errorMsg) + '</div>';
                }
                scrollView();
                eventSource.close();
                currentEventSource = null;
                showErrorToast(errorMsg);
            } catch (e) {
                console.error('Error handling task_error event:', e);
            }
            toggle_chat_state('idle');
        });

        // 最终结果
        eventSource.addEventListener('complete', (event) => {
            try {
                const data = JSON.parse(event.data);
                lastResultContent = data.result || '';
                if (lastResultContent) {
                    ensureResponseContainer();
                    if (finalAnswer) {
                        // 折叠思考过程，仅展示最终结果（用户可点击展开回顾）
                        if (thoughtQuote && !thoughtQuote.classList.contains('collapsed')) {
                            thoughtQuote.classList.add('collapsed');
                            const iconEl = thoughtQuote.querySelector('.toggle-icon');
                            if (iconEl) iconEl.innerHTML = '<i class="bi bi-chevron-up"></i>';
                        }
                        finalAnswer.innerHTML = getMarkedText(lastResultContent);
                    }
                }
                scrollView();
                eventSource.close();
                currentEventSource = null;
            } catch (e) {
                console.error('Error handling complete event:', e);
            }
            toggle_chat_state('idle');
        });

        // SSE 传输层错误（如后端异常断开）
        eventSource.addEventListener('error', (event) => {
            if (event.data) {
                try {
                    const data = JSON.parse(event.data);
                    showErrorToast(data.message || '连接错误');
                } catch (e) {
                    console.error('Error parsing SSE error event:', e);
                }
            }
        });

        eventSource.onerror = (err) => {
            if (eventSource.readyState === EventSource.CLOSED) return;
            console.error('SSE connection error:', err);
            eventSource.close();
            fetch(`/tasks/${taskId}`)
                .then(response => response.json())
                .then(task => {
                    if (task.status === 'completed') {
                        // 已通过 complete 事件处理
                    } else if (task.status && task.status.startsWith('failed')) {
                        ensureResponseContainer();
                        if (finalAnswer) {
                            finalAnswer.innerHTML = '<div class="text-danger"><strong>执行失败：</strong>' + escapeHtml(task.error || task.status) + '</div>';
                        }
                        showErrorToast(task.error || task.status);
                        toggle_chat_state('idle');
                    } else if (retryCount < maxRetries) {
                        retryCount++;
                        showErrorToast(`连接断开，${retryDelay / 1000}秒后重连 (${retryCount}/${maxRetries})`);
                        setTimeout(connect, retryDelay);
                    } else {
                        showErrorToast('连接断开，请刷新页面重试');
                        toggle_chat_state('idle');
                    }
                })
                .catch(error => {
                    console.error('Task status check failed:', error);
                    if (retryCount < maxRetries) {
                        retryCount++;
                        setTimeout(connect, retryDelay);
                    } else {
                        toggle_chat_state('idle');
                    }
                });
        };
    }

    connect();
}

function loadHistory() {
    fetch('/tasks')
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => {
                    throw new Error(`请求失败: ${response.status} - ${text.substring(0, 100)}`);
                });
            }
            return response.json();
        })
        .then(tasks => {
            applyHistory(tasks)
        })
        .catch(error => {
            console.error('Failed to load history records:', error);
            showErrorToast(error.message)
        });
}

function applyHistory(tasks) {
    if (!tasks) return;
    const historyModal = new bootstrap.Modal(document.getElementById('historyModal'));
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '';

    if (tasks.length === 0) {
        historyList.innerHTML = '<li class="list-group-item text-muted">暂无历史记录</li>';
    } else {
        tasks.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        tasks.forEach(item => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center';

            const title = document.createElement('div');
            title.className = 'fw-bold';
            title.textContent = item.prompt;

            const time = document.createElement('small');
            time.className = 'text-muted';
            time.textContent = new Date(item.created_at).toLocaleString();

            li.appendChild(title);
            li.appendChild(time);

            li.addEventListener('click', function () {
                replayTask(item);
                historyModal.hide();
            });

            historyList.appendChild(li);
        });
    }

    historyModal.show();
}

// 回放某条历史任务的思考过程与最终结果
function replayTask(task) {
    chatMessages.innerHTML = '';
    addMessage(task.prompt, 'user');

    const steps = task.steps || [];
    if (steps.length === 0) {
        addMessage(task.status === 'completed' ? '任务已完成。' : '任务尚未完成。', 'ai');
        return;
    }

    const hasThoughts = steps.some(step => step.type === 'think');
    createAIResponseContainer(hasThoughts);
    const quoteContent = hasThoughts ? thoughtQuote.querySelector('.quote-content') : null;

    steps.forEach(step => {
        if (step.type === 'think') {
            const stepDiv = document.createElement('div');
            stepDiv.className = 'thinking-message';
            stepDiv.textContent = step.result;
            quoteContent.appendChild(stepDiv);
        } else if (step.type === 'result') {
            finalAnswer.innerHTML = getMarkedText(step.result);
        } else if (step.type === 'error') {
            finalAnswer.innerHTML = '<div class="text-danger"><strong>执行失败：</strong>' + escapeHtml(step.result) + '</div>';
        }
    });

    scrollView();
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add(sender + '-message');

    const iconDiv = document.createElement('div');
    iconDiv.className = 'message-icon';
    const icon = document.createElement('i');
    icon.className = sender === 'user' ? 'bi bi-person-fill' : 'bi bi-robot';
    iconDiv.appendChild(icon);

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    if (sender === 'user') {
        const promptDiv = document.createElement('div');
        promptDiv.className = 'user-prompt';
        promptDiv.textContent = text;

        const copyBtn = document.createElement('button');
        copyBtn.className = 'copy-btn';
        copyBtn.setAttribute('onclick', 'copyMessage(this)');
        copyBtn.title = '复制';
        copyBtn.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-copy"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"></rect><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"></path></svg>';

        contentDiv.appendChild(promptDiv);
        contentDiv.appendChild(copyBtn);
    } else {
        contentDiv.textContent = text;
    }

    if (sender === 'user') {
        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(iconDiv);
    } else {
        messageDiv.appendChild(iconDiv);
        messageDiv.appendChild(contentDiv);
    }

    chatMessages.appendChild(messageDiv);
    scrollView();
}

function scrollView() {
    if (!chatMessages) return
    chatMessages.scrollIntoView({ behavior: "auto", block: "end" })
}

document.addEventListener('DOMContentLoaded', function () {
    // 初始化 tooltip
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(tooltipTriggerEl => {
        new bootstrap.Tooltip(tooltipTriggerEl);
    });

    document.getElementById('btn-paperclip').addEventListener('click', function () {
        document.getElementById('fileInput').click();
    });

    document.getElementById('fileInput').addEventListener('change', function (event) {
        const fileInput = event.target;
        const file = event.target.files[0];
        if (file) {
            if (file.type === 'text/plain') {
                const reader = new FileReader();
                reader.onload = function (e) {
                    document.getElementById('messageInput').value = e.target.result;
                };
                reader.readAsText(file);
            } else {
                showErrorToast('请选择文本 (.txt) 文件');
                document.getElementById('messageInput').value = '';
            }
            fileInput.value = '';
        }
    });

    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    chatMessages = document.getElementById('chatMessages');

    if (!messageInput || !sendButton || !chatMessages) {
        console.error('Required elements not found!');
        return;
    }

    toggle_chat_state('idle');

    const promptShortcuts = document.querySelectorAll('.prompt-shortcut');

    function sendMessage() {
        if (chat_state !== 'idle') {
            showErrorToast('Agent 正在处理中，请稍候...');
            return;
        }
        const message = messageInput.value.trim();
        if (message) {
            toggle_chat_state('working');
            createChat();
        }
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    promptShortcuts.forEach(shortcut => {
        shortcut.addEventListener('click', function () {
            messageInput.value = this.textContent;
            messageInput.focus();
        });
    });

    document.querySelector('.btn-chat').addEventListener('click', function () {
        if (currentEventSource) {
            currentEventSource.close();
            currentEventSource = null;
        }
        chatMessages.innerHTML = '';
        toggle_chat_state('idle');
    });

    document.querySelector('.btn-history').addEventListener('click', function () {
        loadHistory();
    });
});
