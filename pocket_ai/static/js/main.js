// ポケットAI (Pocket AI) - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const settingsButton = document.getElementById('settings-button');
    const apiKeyModal = document.getElementById('api-key-modal');
    const apiKeyInput = document.getElementById('api-key-input');
    const saveApiKeyButton = document.getElementById('save-api-key');
    const cancelApiKeyButton = document.getElementById('cancel-api-key');
    const codeModal = document.getElementById('code-modal');
    const languageSelect = document.getElementById('language-select');
    const codeEditor = document.getElementById('code-editor');
    const outputContent = document.getElementById('output-content');
    const runCodeButton = document.getElementById('run-code');
    const closeCodeModalButton = document.getElementById('close-code-modal');
    const toolItems = document.querySelectorAll('.tool-item');

    // State
    let apiKey = localStorage.getItem('pocketAI_apiKey') || '';
    let isWaitingForResponse = false;

    // Initialize
    init();

    // Functions
    function init() {
        // Set API key from localStorage if available
        if (apiKey) {
            apiKeyInput.value = apiKey;
        } else {
            // Show API key modal on first load if no API key is set
            showApiKeyModal();
        }

        // Add event listeners
        sendButton.addEventListener('click', sendMessage);
        userInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        settingsButton.addEventListener('click', showApiKeyModal);
        saveApiKeyButton.addEventListener('click', saveApiKey);
        cancelApiKeyButton.addEventListener('click', hideApiKeyModal);

        runCodeButton.addEventListener('click', executeCode);
        closeCodeModalButton.addEventListener('click', hideCodeModal);

        // Tool items
        toolItems.forEach(item => {
            item.addEventListener('click', function() {
                const tool = this.getAttribute('data-tool');
                handleToolClick(tool);
            });
        });
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message || isWaitingForResponse) return;

        // Add user message to chat
        addMessageToChat(message, 'user');
        
        // Clear input
        userInput.value = '';
        
        // Set waiting state
        isWaitingForResponse = true;
        
        // Send to backend
        callAgent(message);
    }

    function addMessageToChat(content, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        const paragraph = document.createElement('p');
        paragraph.textContent = content;
        
        messageContent.appendChild(paragraph);
        messageDiv.appendChild(messageContent);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function callAgent(task) {
        // Add a loading message
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message system';
        loadingDiv.id = 'loading-message';
        
        const loadingContent = document.createElement('div');
        loadingContent.className = 'message-content';
        
        const loadingText = document.createElement('p');
        loadingText.textContent = '考え中...';
        
        loadingContent.appendChild(loadingText);
        loadingDiv.appendChild(loadingContent);
        chatMessages.appendChild(loadingDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Call the API
        fetch('/api/run', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                task: task,
                api_key: apiKey
            })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading message
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                chatMessages.removeChild(loadingMessage);
            }
            
            if (data.success) {
                // Process the response
                const result = data.result;
                
                // Get the final evaluation or action results
                let responseMessage = '';
                
                if (result.evaluation && result.evaluation.feedback) {
                    responseMessage = result.evaluation.feedback;
                } else if (result.action_results) {
                    if (result.action_results.message) {
                        responseMessage = result.action_results.message;
                    } else if (result.action_results.output) {
                        responseMessage = result.action_results.output;
                    } else {
                        responseMessage = 'タスクを実行しました。';
                    }
                } else {
                    responseMessage = 'タスクを受け取りました。';
                }
                
                // Add response to chat
                addMessageToChat(responseMessage, 'system');
            } else {
                // Handle error
                addMessageToChat(`エラーが発生しました: ${data.error}`, 'system');
            }
        })
        .catch(error => {
            // Remove loading message
            const loadingMessage = document.getElementById('loading-message');
            if (loadingMessage) {
                chatMessages.removeChild(loadingMessage);
            }
            
            // Handle error
            addMessageToChat(`通信エラーが発生しました: ${error.message}`, 'system');
        })
        .finally(() => {
            // Reset waiting state
            isWaitingForResponse = false;
        });
    }

    function executeCode() {
        const code = codeEditor.value.trim();
        const language = languageSelect.value;
        
        if (!code) return;
        
        // Clear previous output
        outputContent.textContent = '実行中...';
        
        // Call the API
        fetch('/api/execute_code', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                language: language
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const result = data.result;
                
                if (result.success) {
                    outputContent.textContent = result.output || '出力なし';
                    outputContent.style.color = 'var(--text-color)';
                } else {
                    outputContent.textContent = result.error || 'エラーが発生しました';
                    outputContent.style.color = 'var(--error-color)';
                }
            } else {
                outputContent.textContent = data.error || 'エラーが発生しました';
                outputContent.style.color = 'var(--error-color)';
            }
        })
        .catch(error => {
            outputContent.textContent = `通信エラーが発生しました: ${error.message}`;
            outputContent.style.color = 'var(--error-color)';
        });
    }

    function handleToolClick(tool) {
        switch (tool) {
            case 'code':
                showCodeModal();
                break;
            case 'browser':
                addMessageToChat('ブラウザツールを使用するには、タスクを入力してください。例: "Pythonの配列操作について調べて"', 'system');
                break;
            case 'search':
                addMessageToChat('コード検索ツールを使用するには、タスクを入力してください。例: "Pythonでファイルを読み込む方法を探して"', 'system');
                break;
            case 'analyze':
                addMessageToChat('コード分析ツールを使用するには、タスクを入力してください。例: "このコードを分析して改善点を教えて"', 'system');
                break;
        }
    }

    function showApiKeyModal() {
        apiKeyModal.style.display = 'flex';
    }

    function hideApiKeyModal() {
        apiKeyModal.style.display = 'none';
    }

    function saveApiKey() {
        const newApiKey = apiKeyInput.value.trim();
        
        if (newApiKey) {
            apiKey = newApiKey;
            localStorage.setItem('pocketAI_apiKey', apiKey);
            hideApiKeyModal();
            
            // Show confirmation message
            addMessageToChat('APIキーが設定されました。', 'system');
        }
    }

    function showCodeModal() {
        codeModal.style.display = 'flex';
    }

    function hideCodeModal() {
        codeModal.style.display = 'none';
    }
});