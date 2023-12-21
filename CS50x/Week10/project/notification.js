chrome.notifications.onCreated.addListener((notificationId, notification) => {
    if (notification.type === 'basic') {
      const audio = new Audio(`CS50audio.mp3`); 
      audio.play();
    }
  });