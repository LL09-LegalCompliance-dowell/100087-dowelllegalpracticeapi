let base64String = "";

// Assume that the input field is a file input with an ID 
const signatureImage = document.getElementById('signature-image');
const signatureImageDisplay = document.getElementById('signature-image-display');
const signatureImageContainer = document.getElementById("signature-image-container");
const signatureDate = document.getElementById("signature-date");


document.addEventListener("DOMContentLoaded", function(){
  const wrapEl = document.getElementById("wrap");
  const isLocked = wrapEl.getAttribute("data-is-locked");
  if (isLocked === "true"){
    document.getElementById('i-give-consent').disabled = true;
    document.getElementById('i-give-consent').readOnly = true;
  }
})


// Listen for the "change" event on the input field
signatureImage.addEventListener('change', function() {
  const file = signatureImage.files[0];

  // Create a FileReader object to read the image file
  const reader = new FileReader();

  // Listen for the "load" event on the reader
  reader.addEventListener('load', function() {
    // Get the Base64-encoded data URL from the reader
    const dataUrl = reader.result;

    // Remove the data URL prefix
    base64String = dataUrl.replace(/^data:image\/(png|jpg);base64,/, '');

    // The base64String variable now contains the Base64-encoded image data
    console.log(base64String);
    signatureImageDisplay.setAttribute("src", `data:image/png;base64,${base64String}`);
    signatureImageContainer.style.display = "block";

  });

  // Read the image file as a data URL
  reader.readAsDataURL(file);
});


document.getElementById("i-give-consent").addEventListener('click', function() {
    if (this.checked){
        document.getElementById("signature-details").style.display = "block";
    }else{
        document.getElementById("signature-details").style.display = "none";
    }
});


// listen to the signature form submition
document.getElementById("form").addEventListener('submit', function(event) {
    event.preventDefault();

    if (validateInput()){

      const wrapEl = document.getElementById("wrap");
      const eventId = wrapEl.getAttribute("data-event-id");
      const isLocked = wrapEl.getAttribute("data-is-locked");
      const baseUrl = wrapEl.getAttribute("data-base-url");
      
      const name = document.getElementById("name-of-individua-providing-consent").value;
      const address = document.getElementById("address-of-individua-providing-consent").value;
      let data = {
        action_type: "submit-signature",
        name: name,
        address: address,
        signature: base64String,
        consent_status: "Confirmed"
      };

      fetch(`${baseUrl}/api/privacyconsents/${eventId}/`,{
        method: "PUT",
        body: JSON.stringify(data),
        headers: {"Content-Type": "application/json"}
      }).then(res => {

        if (res.status === 200){

          // disable give consent
          document.getElementById('i-give-consent').disabled = true;
          document.getElementById('i-give-consent').readOnly = true;

        }else{
          return res.json();
        }

      }).then(jsonData => {

      })

    }
    
});



const validateInput = () => {
  let isValid = true;
  const name = document.getElementById("name-of-individua-providing-consent").value;
  const address = document.getElementById("address-of-individua-providing-consent").value;

  if (name === ""){
    document.getElementById("name-error").style.display = "block";
    isValid = false;
  }else{
    document.getElementById("name-error").style.display = "none";
  }


  if (address === ""){
    document.getElementById("address-error").style.display = "block";
    isValid = false;
  }else{
    document.getElementById("address-error").style.display = "none";
  }

  if (base64String === ""){
    document.getElementById("signature-image-error").style.display = "block";
    isValid = false;
  }else{
    document.getElementById("signature-image-error").style.display = "none";
  }

  return isValid;

}
