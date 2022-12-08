document.addEventListener("DOMContentLoaded", function(){
  
    const igreeEl = document.getElementById("agree-to-legal-policy-api");
    igreeEl.addEventListener("click", function(e){
    const redirectUrl = igreeEl.getAttribute("data-redirect-url");
    const policyRequestId = igreeEl.getAttribute("data-policy-request-id");
    if (e.target.checked){


      // update local storage
      window.localStorage.setItem(policyRequestId, JSON.stringify({iAgree: true}));

      // update server
      const url = "/api/legalpolicies/"+policyRequestId+"/iagreelogs/";

      fetch(url, {
        method: "PUT",
        body: JSON.stringify({"i_agree": true}),
        headers: {"Content-Type": "application/json"}
      })

      // Redirect user to previous page
      window.location.href = redirectUrl;


    }else {


      // update server
      const url = "/api/legalpolicies/"+policyRequestId+"/iagreelogs/";
      fetch(url, {
        method: "PUT",
        body: JSON.stringify({"i_agree": false}),
        headers: {"Content-Type": "application/json"}
      })


      window.localStorage.setItem(policyRequestId, JSON.stringify({iAgree: false}));
    }
  })


})

