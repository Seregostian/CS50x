if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('background.js');
  }
  
  const CS50_CHANNEL_ID = 'CHANNEL ID GOES HERE';
  const LAST_VIDEO_KEY = 'last_video_id';
  
  function checkForNewVideos() {
    chrome.storage.local.get(LAST_VIDEO_KEY, ({ lastVideoId }) => {
      const url = `GOOGLE API'S=${Key part 1}&maxResults=10&order=date&key=${Key part 2}`;
  
      fetch(url)
        .then(response => response.json())
        .then(data => {
          const newestVideo = data.items[0];
          if (newestVideo.id.videoId !== lastVideoId) {
            notifyUser(newestVideo);
            chrome.storage.local.set({ lastVideoId: newestVideo.id.videoId });
          }
        })
        .catch(error => console.error(error));
    });
  }
  
  function playNotificationSound(scriptUrl) {
    chrome.scripting.executeScript({
      file: scriptUrl,
      args: ['CS50audio.mp3'],
    }).catch(error => console.error(error));
  }
  
  function notifyUser(video) {
    chrome.notifications.create('new-video', {
      type: 'basic',
      iconUrl: video.snippet.thumbnails.default.url,
      title: 'New Video!',
      message: video.snippet.title,
      imageUrl: video.snippet.thumbnails.high.url,
    }, () => {
      // latestVideo data
      chrome.storage.local.set({ latestVideo: video });
  
      // CS50! audio
      playNotificationSound(chrome.runtime.getURL('notification.js'));
  
      chrome.notifications.onClicked.addListener(() => {
        chrome.tabs.create({ url: `https://youtu.be/${video.id.videoId}` });
      });
    });
  }
  
  chrome.alarms.create('check-videos', { periodInMinutes: 15 });
  chrome.alarms.onAlarm.addListener(checkForNewVideos);
