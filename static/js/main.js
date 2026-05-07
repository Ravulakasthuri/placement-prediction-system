// Function to update the displayed value of a slider
function updateRangeValue(inputId, spanId) {
    const input = document.getElementById(inputId);
    const span = document.getElementById(spanId);
    if (input && span) {
        span.textContent = input.value;
        input.addEventListener('input', function() {
            span.textContent = this.value;
        });
    }
}

// Initialize sliders matching Dashboard IDs
document.addEventListener('DOMContentLoaded', function() {
    updateRangeValue('aptitude', 'aptitudeValue');
    updateRangeValue('technical_skills', 'techSkillsValue');
    updateRangeValue('communication', 'commValue');
});
