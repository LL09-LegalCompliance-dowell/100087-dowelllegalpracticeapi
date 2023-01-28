document.addEventListener("DOMContentLoaded", function(){
  
    const igreeEl = document.getElementById("agree-to-legal-policy-api");
    const igreeMessageContainer = this.getElementById("i-agree-message-container");
    const igreeMessage = this.getElementById("i-agree-message");
    const igreeStatus = igreeEl.getAttribute("data-i-agree-status");
    const igreedAlreadyMessage = igreeEl.getAttribute("data-agreed-already-message");

    // Disable igree checkbox
    if (igreeStatus === "1"){

      igreeMessage.innerHTML = igreedAlreadyMessage;
      igreeMessageContainer.style.display = "block";
      document.getElementById("igree-checkbox-form").style.display = "none";

    }


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
            }).then(response => {
                // Redirect user to previous page
                // window.location.href = redirectUrl;
            })


            // Prevent redirection
            if (redirectUrl != "none") {
              window.location.href = redirectUrl;
            }



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

