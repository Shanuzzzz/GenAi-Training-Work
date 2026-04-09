document.getElementById('sentimentForm').addEventListener('submit', function(e) {
    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.innerHTML;
    
    // Show loading state
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    submitBtn.disabled = true;
    
    // Re-enable after 10 seconds in case of slow response
    setTimeout(() => {
        submitBtn.innerHTML = originalText;
        submitBtn.disabled = false;
    }, 10000);
});

document.getElementById('textInput').addEventListener('input', function() {
    const text = this.value.trim();
    const submitBtn = document.getElementById('submitBtn');
    
    if (text.length > 0) {
        submitBtn.classList.remove('btn-secondary');
        submitBtn.classList.add('btn-success');
    } else {
        submitBtn.classList.remove('btn-success');
        submitBtn.classList.add('btn-secondary');
    }
});