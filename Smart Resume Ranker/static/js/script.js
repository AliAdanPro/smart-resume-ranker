document.addEventListener('DOMContentLoaded', () => {
    // --- Particle Effect ---
    const canvas = document.getElementById('particles-js');
    if (canvas) {
        const ctx = canvas.getContext('2d');
        let particles = [];

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);
        resize();

        class Particle {
            constructor() {
                this.x = Math.random() * canvas.width;
                this.y = Math.random() * canvas.height;
                this.size = Math.random() * 2 + 0.5;
                this.speedX = Math.random() * 1 - 0.5;
                this.speedY = Math.random() * 1 - 0.5;
                this.color = `rgba(99, 102, 241, ${Math.random() * 0.5})`;
            }
            update() {
                this.x += this.speedX;
                this.y += this.speedY;
                if (this.x > canvas.width) this.x = 0;
                if (this.x < 0) this.x = canvas.width;
                if (this.y > canvas.height) this.y = 0;
                if (this.y < 0) this.y = canvas.height;
            }
            draw() {
                ctx.fillStyle = this.color;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
                ctx.fill();
            }
        }

        function initParticles() {
            for (let i = 0; i < 100; i++) {
                particles.push(new Particle());
            }
        }

        function animateParticles() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < particles.length; i++) {
                particles[i].update();
                particles[i].draw();
            }
            requestAnimationFrame(animateParticles);
        }

        initParticles();
        animateParticles();
    }

    // --- Drag and Drop Logic ---
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('resumeInput');
    const fileList = document.getElementById('fileList');

    if (dropZone) {
        dropZone.addEventListener('click', () => fileInput.click());

        dropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            dropZone.classList.add('dragover');
        });

        dropZone.addEventListener('dragleave', () => {
            dropZone.classList.remove('dragover');
        });

        dropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            dropZone.classList.remove('dragover');

            if (e.dataTransfer.files.length) {
                fileInput.files = e.dataTransfer.files;
                updateFileList(fileInput.files);
            }
        });

        fileInput.addEventListener('change', () => {
            updateFileList(fileInput.files);
        });
    }

    function updateFileList(files) {
        fileList.innerHTML = '';
        Array.from(files).forEach(file => {
            const div = document.createElement('div');
            div.className = 'file-item';
            div.innerHTML = `
                <span><i class="fas fa-file-alt"></i> ${file.name}</span>
                <span style="font-size: 0.8rem; color: #94a3b8;">${(file.size / 1024).toFixed(1)} KB</span>
            `;
            fileList.appendChild(div);
        });
    }

    // --- Slider Value Updates ---
    const sliders = ['weight_skills', 'weight_exp', 'weight_edu'];
    sliders.forEach(id => {
        const slider = document.getElementById(id);
        const display = document.getElementById(id.replace('weight_', 'val_'));
        if (slider && display) {
            slider.addEventListener('input', (e) => {
                display.textContent = e.target.value;
            });
        }
    });

    // --- Form Submission & Progress ---
    const form = document.getElementById('uploadForm');
    const progressBarContainer = document.getElementById('progressBarContainer');
    const progressBar = document.getElementById('progressBar');
    const progressText = document.getElementById('progressText');
    const analyzeBtn = document.getElementById('analyzeBtn');

    if (form) {
        form.addEventListener('submit', (e) => {
            if (fileInput.files.length === 0) {
                e.preventDefault();
                alert('Please upload at least one resume.');
                return;
            }

            analyzeBtn.disabled = true;
            analyzeBtn.style.opacity = '0.7';
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Processing...';
            progressBarContainer.style.display = 'block';

            let width = 0;
            const interval = setInterval(() => {
                if (width >= 95) clearInterval(interval);
                width += Math.random() * 5;
                if (width > 95) width = 95;
                progressBar.style.width = width + '%';
            }, 300);
        });
    }
});
