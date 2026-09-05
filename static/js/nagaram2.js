const launcher = document.getElementById('chat-launcher');
const panel = document.getElementById('chat-panel');
const close = document.getElementById('chat-close');
const form = document.getElementById('chat-form');
const input = document.getElementById('chat-input');
const messages = document.getElementById('chat-messages');

function addBubble(text, type) {
  const el = document.createElement('div');
  el.className = `bubble ${type}`;
  el.textContent = text;
  messages.appendChild(el);
  messages.scrollTop = messages.scrollHeight;
}

function openChat() {
  panel.classList.add('open');
  panel.setAttribute('aria-hidden', 'false');
  input.focus();
}

launcher.addEventListener('click', openChat);
close.addEventListener('click', () => {
  panel.classList.remove('open');
  panel.setAttribute('aria-hidden', 'true');
});

document.querySelectorAll('[data-prompt]').forEach((button) => {
  button.addEventListener('click', () => {
    input.value = button.dataset.prompt;
    form.requestSubmit();
  });
});

form.addEventListener('submit', async (event) => {
  event.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addBubble(text, 'user');
  input.value = '';

  const pending = document.createElement('div');
  pending.className = 'bubble bot';
  pending.textContent = 'Thinking…';
  messages.appendChild(pending);
  messages.scrollTop = messages.scrollHeight;

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    });
    if (!response.ok) throw new Error('Assistant unavailable');
    const data = await response.json();
    pending.textContent = data.answer;
  } catch (error) {
    pending.textContent = 'I’m having trouble reaching the assistant. You can still use the Citizen or Farmer portal from the navigation.';
  }
  messages.scrollTop = messages.scrollHeight;
});
