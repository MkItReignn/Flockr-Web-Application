# Flockr

This is a web application using Flask, which facilitates team-based communication, comparable to that of Slack

## Features

1. Ability to login, register if not registered, and log out
2. Ability to reset password if forgotten
3. Ability to see a list of channels
4. Ability to create a channel, join a channel, invite someone else to a channel, and leave a channel
5. Within a channel, ability to view all messages, view the members of the channel, and the details of the channel
6. Within a channel, ability to send a message now, or to send a message at a specified time in the future
7. Within a channel, ability to edit, remove, pin, unpin, react, or unreact to a message
8. Ability to view user anyone's user profile, and modify a user's own profile (name, email, handle, and profile photo)
9. Ability to search for messages based on a search string
10. Ability to modify a user's admin permissions: (MEMBER, OWNER)
11. Ability to begin a "standup", which is an X minute period where users can send messages that at the end of the period will automatically be collated and summarised to all users

## How to start it

1. ```python3 src/server.py``` begins the backend servers

2. Copy the back end port

3. ```./project-frontend```

4. ```python3 frontend.py [BACKEND PORT]```

   For example: ```python3 frontend.py 5000```

## Demo

[![](http://img.youtube.com/vi/GLAlBz1QbFs/0.jpg)](http://www.youtube.com/watch?v=GLAlBz1QbFs "Flockr Web Application Demo")
