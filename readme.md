#  RiotAuth Python Library

RiotAuth is a Python library that provides authentication and access to Riot Games' services, allowing you to interact with the League of Legends API and access user-specific data. This library simplifies the process of authenticating with Riot Games' servers, handling captcha challenges, and retrieving authentication tokens.


#  Usage

> ```py
> from RiotAuth import authentication
> Replace with your Riot Games credentials
> username = "your_username" 
>password = "your_password" 
>try: # Authenticate with Riot Games servers 
>     user_info = authentication(username, password) 
>except Exception as e: print(f"Authentication failed: {e}")```

Here's a basic example of how to use the RiotAuth library to authenticate and retrieve user data:

## Dependencies

-   `requests`: This library uses the `requests` library to make HTTP requests to Riot Games' servers.
-   `hcaptcha-python`: This library uses `hcaptcha-python` to solve hCaptcha challenges.

## Acknowledgment

This project took inspiration from the [PyRiotAuth](https://github.com/Bbalduzz/PyRiotAuth) repository by [Bbalduzz](https://github.com/Bbalduzz). We extend our gratitude to the original project for its contributions to Riot Games authentication in Python.
