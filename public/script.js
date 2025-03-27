document.addEventListener('DOMContentLoaded', function() {
    // Toggle enable/disable of the custom CSP header input field based on the checkbox state.
    var cspCheckbox = document.getElementById('enable_csp');
    var cspInput = document.getElementById('csp_value');
    if (cspCheckbox && cspInput) {
        cspCheckbox.addEventListener('change', function() {
            cspInput.disabled = !this.checked;
        });
    }
    // Toggle enable/disable of the custom CORS header input field based on the checkbox state.
    var corsCheckbox = document.getElementById('enable_cors');
    var corsInput = document.getElementById('cors_value');
    if (corsCheckbox && corsInput) {
        corsCheckbox.addEventListener('change', function() {
            corsInput.disabled = !this.checked;
        });
    }
});
