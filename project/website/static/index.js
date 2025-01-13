async function handleLogin(event) {
  event.preventDefault(); // Prevent the default form submission behavior

  // Collect data from the form
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  // Validate input
  if (!username || !password) {
    alert('Please enter both username and password');
    return;
}

  const loginData = {
    username: username,
    password: password
  };

  try {
    console.log('Sending login data:', loginData); // Debug log
    const response = await fetch('/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(loginData)
    });

    // Log the raw response for debugging
    const rawResponse = await response.text();
    console.log('Raw server response:', rawResponse);

    let result;

    try {
      result = JSON.parse(rawResponse);
  } catch (parseError) {
      console.error('Failed to parse JSON response:', parseError);
      console.log('Raw response that failed to parse:', rawResponse);
      throw new Error('Invalid JSON response from server');
  }
  
  console.log('Parsed response:', result);

  if (response.ok) {
    // Store tokens
    localStorage.setItem('access_token', result.tokens.access);
    localStorage.setItem('refresh_token', result.tokens.refresh);
    
    // Instead of using window.location.href directly, make an authenticated request
    const homeResponse = await fetch(result.redirect_url, {
        headers: {
            'Authorization': `Bearer ${result.tokens.access}`
        }
    });
    
    if (homeResponse.ok) {
        window.location.href = result.redirect_url;
    } else {
        alert('Error accessing home page');
    }
} else {
    alert(result.error || 'Login failed');
}
  } catch (error) {
    console.error('Error during login:', error);
    alert('An error occurred. Please try again.');
  }
}