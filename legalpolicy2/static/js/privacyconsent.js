let base64String = "";

// Assume that the input field is a file input with an ID 
const signatureImage = document.getElementById('signature-image');
const signatureImageDisplay = document.getElementById('signature-image-display');
const signatureImageContainer = document.getElementById("signature-image-container");
const signatureDate = document.getElementById("signature-date");

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



document.getElementById("form").addEventListener('submit', function(event) {
    event.preventDefault();

    
});
