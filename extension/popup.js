document.addEventListener("DOMContentLoaded", function () {
  const captureButton = document.getElementById("captureButton");
  const outputDiv = document.getElementById("output");

  if (captureButton && outputDiv) {
    captureButton.addEventListener("click", async function () {
      try {
        const displayMediaOptions = {
          video: {
            displaySurface: "browser",
          },
        };
        const captureStream = await navigator.mediaDevices.getDisplayMedia(
          displayMediaOptions
        );

        // Create a video element to display the captured stream
        const videoElement = document.createElement("video");
        videoElement.srcObject = captureStream;
        videoElement.autoplay = true;
        videoElement.onloadedmetadata = async function () {
          // Create a canvas element to draw the video frame
          const canvas = document.createElement("canvas");
          const context = canvas.getContext("2d");
          canvas.width = videoElement.videoWidth;
          canvas.height = videoElement.videoHeight;
          context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);

          // Append the canvas element to the FormData object
          const formData = new FormData();
          formData.append("image", canvas.toDataURL("image/png"));

          const response = await fetch("http://127.0.0.1:5000/summary", {
            method: "POST",
            body: formData,
          });
          const data = await response.json();
          outputDiv.innerText = data.message;
        };
      } catch (error) {
        console.error("Error processing image:", error);
        outputDiv.innerText = "Error processing image.";
      }
    });
  } else {
    console.error("Button or output element not found");
  }
});
