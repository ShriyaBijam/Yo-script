const button=document.querySelector('.btn');
const summary=document.querySelector('.summary');

button.addEventListener('click',()=>{
    button.classList.add('activebtn');
    summary.classList.add('active');
    summary.classList.add('loading');

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      var videoid = tabs[0].url.match(/(?:https?:\/{2})?(?:w{3}\.)?youtu(?:be)?\.(?:com|be)(?:\/watch\?v=|\/)([^\s&]+)/);
      if (videoid !== null)
      {
        chrome.tabs.sendMessage(tabs[0].id, {message: "generate", id:videoid[1]}, function(response) {
          summary.classList.remove('loading');
          summary.innerHTML=response.message.response;
        });
      }
    });
})