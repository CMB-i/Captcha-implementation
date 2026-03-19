# Captcha-implementation
A simple demonstration of a CAPTCHA-based human verification system inspired by the Turing Test.
The system presents users with an image-selection challenge and determines whether the interaction resembles human behavior or automated bot activity.

This project was built as part of an AI / Intelligent Systems assignment to explore practical implementations of Turing test–style human verification mechanisms.

## Concept
The Turing Test evaluates whether a machine can behave indistinguishably from a human.

CAPTCHAs apply a similar idea in reverse: 'Instead of asking if a machine can imitate a human, we test whether a user interaction behaves like a human.'

Humans can easily recognize patterns or objects in images, while automated scripts often struggle with these tasks.

## How the System Works
When a user opens the site:

A CAPTCHA challenge is generated.
The user must select all matching icons in a grid.
The server verifies the response.

Rules:
- Users have 3 attempts to solve the challenge.
- If solved correctly: The user is marked as human verified.
- If all attempts fail: The system displays a message indicating non-human behavior.

## How to run:
- intsall python
- install Flask:
```
pip install flask
```
- run:
```
python server.py
```
you should see:  ```'Running on http://127.0.0.1:5000'```
- Open the demo in your browser

## Features
- Interactive 3×3 CAPTCHA grid
- Randomized icons for each challenge
- Server-side verification
- Limited number of attempts
- Protection against challenge replay

## stack:
- Python
- Flask
- HTML
- JavaScript
- HMAC signing for challenge integrity
