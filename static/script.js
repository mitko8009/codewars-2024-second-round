document.addEventListener('DOMContentLoaded', function() {
    const passwordInput = document.getElementById('password');
    const togglePasswordButton = document.createElement('button');
    togglePasswordButton.type = 'button';
    togglePasswordButton.textContent = 'Show';
    
    togglePasswordButton.addEventListener('click', function() {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            togglePasswordButton.textContent = 'Hide';
        } else {
            passwordInput.type = 'password';
            togglePasswordButton.textContent = 'Show';
        }
    });

    passwordInput.parentNode.insertBefore(togglePasswordButton, passwordInput.nextSibling);
});
