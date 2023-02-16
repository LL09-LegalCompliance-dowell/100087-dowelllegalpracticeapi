let base64String = "";

// Assume that the input field is a file input with an ID 
const signatureImage = document.getElementById('signature-image');
const signatureImageDisplay = document.getElementById('signature-image-display');
const signatureImageContainer = document.getElementById("signature-image-container");
const signatureDate = document.getElementById("signature-date");
const otherUsage = document.getElementById("other-usage-for-personal-data-input-display")



document.addEventListener("DOMContentLoaded", function(){
  const wrapEl = document.getElementById("wrap");
  const isLocked = wrapEl.getAttribute("data-is-locked");
  if (isLocked === "True"){

    document.getElementById("i-give-consent").checked = true;
    document.getElementById('i-give-consent').disabled = true;
    document.getElementById('i-give-consent').readOnly = true;
    document.getElementById("signature-details-display").style.display = "block";

    // disable consent to personal data usage
    const personsalDataUsageEl = document.querySelectorAll(".consent-to-personal-data-usage");
    personsalDataUsageEl.forEach(element => {
      element.disabled = true;
    })

    const otherUsageData = otherUsage.getAttribute("data-other-usage");
    if (otherUsageData){
      document.getElementById("other-usage-for-personal-data").checked = true;
      document.getElementById("other-usage-for-personal-data").disabled = true;
      document.getElementById("other-usage-for-personal-data-display").style.display = "block";    
    }else{
      document.getElementById("other-usage-for-personal-data").checked = false;
      document.getElementById("other-usage-for-personal-data").disabled = false;
      document.getElementById("other-usage-for-personal-data-display").style.display = "none";
    }


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
    // console.log(base64String);
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


document.getElementById("other-usage-for-personal-data").addEventListener('click', function() {
  if (this.checked){
      document.getElementById("other-usage-for-personal-data-input-display").style.display = "block";
  }else{
      document.getElementById("other-usage-for-personal-data-input-display").style.display = "none";
  }



});



// listen to the signature form submition
document.getElementById("form").addEventListener('submit', function(event) {
    event.preventDefault();

    if (validateInput()){

      const btnSaveSignature = document.getElementById("btn-save-signature");
      btnSaveSignature.innerHTML = "Saving ...";
      btnSaveSignature.disabled = true;

      const wrapEl = document.getElementById("wrap");
      const eventId = wrapEl.getAttribute("data-event-id");
      const isLocked = wrapEl.getAttribute("data-is-locked");
      const baseUrl = wrapEl.getAttribute("data-base-url");
      
      const name = document.getElementById("name-of-individua-providing-consent").value;
      const address = document.getElementById("address-of-individua-providing-consent").value;
      const otherUsageOfPersonalData = document.getElementById("other-usage-for-personal-data-input").value;
      let data = {
        action_type: "submit-signature",
        name: name,
        address: address,
        signature: base64String,
        consent_status: "Confirmed",
        personal_data_usage: getPersonalDataUsage(),
        other_usage_of_personal_data: otherUsageOfPersonalData
      };

      console.log(JSON.stringify(data))

      fetch(`${baseUrl}/api/privacyconsents/${eventId}/`,{
        method: "PUT",
        body: JSON.stringify(data),
        headers: {"Content-Type": "application/json"}
      }).then(res => {

        if (res.status === 200){

          // disable give consent
          document.getElementById("signature-field-container").style.display = "none";
          document.getElementById('i-give-consent').disabled = true;
          document.getElementById('i-give-consent').readOnly = true;
          document.getElementById("name-of-individua-providing-consent").readOnly = true;
          document.getElementById("address-of-individua-providing-consent").readOnly = true;
          document.getElementById("btn-save-signature").remove();
          

        }else{
          btnSaveSignature.disabled = false;
          btnSaveSignature.innerHTML = "Submit Consent";
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



const getPersonalDataUsage = () => {
  let data = []
  const personsalDataUsageEl = document.querySelectorAll(".consent-to-personal-data-usage");
  personsalDataUsageEl.forEach(element => {
    const description = element.getAttribute("data-description");
    if( element.checked ){
      data.push(description);
    }
  })


  return data;
}



