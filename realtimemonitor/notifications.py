def send_push_notification(user, title, message):
    """
    Simulates sending a push notification to a user's device.
    """
    if not user:
        return
    
    # In a real implementation, you would use Firebase Cloud Messaging (FCM) 
    # or a similar service to send the notification to the device token 
    # associated with the user.
    
    print(f"--- PUSH NOTIFICATION ---")
    print(f"To: {user.username} ({user.email})")
    print(f"Title: {title}")
    print(f"Message: {message}")
    print(f"-------------------------")
    return True
