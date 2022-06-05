console.log('background running')
chrome.runtime.onInstalled.addListener(function() {
    chrome.tabs.onActivated.addListener(async info => {
      const tab = await chrome.tabs.get(info.tabId);
      const isYouTube = tab.url.startsWith('https://www.youtube.com');
      console.log(isYouTube)
      isYouTube 
        ? chrome.action.enable(tab.tabId) 
        : chrome.action.disable(tab.tabId);
    });

    chrome.tabs.onUpdated.addListener(async (tabId, changeInfo) => { 
        var tab = await chrome.tabs.get(tabId);	
        if (tab.active && changeInfo.url) {	
          const isYouTube = tab.url.startsWith('https://www.youtube.com');
        console.log(isYouTube)
        isYouTube 
          ? chrome.action.enable(tab.tabId) 
          : chrome.action.disable(tab.tabId);   
      } });

  });
