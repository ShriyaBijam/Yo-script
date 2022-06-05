console.log('extension running')

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.message == "generate")
    {  
      console.log('message received')
      console.log(request.id);
      fetch(`http://127.0.0.1:5000/api/summarize/?id=${request.id}`)
      .then(res=>res.json())
      .then(result=>{
        console.log(result.message);
        sendResponse({message: result});
      })
      .catch(err=>{
        console.log('error generated')
        sendResponse({message:err})
      });
      return true;
    }
  }
      
);