document.addEventListener('DOMContentLoaded', () => {
    const uploadButton = document.getElementById('uploadButton');
    const videoInput = document.getElementById('fileToUpload');
    const resultDiv = document.getElementById('result');
  
    uploadButton.addEventListener('click', async (event) => {
        event.preventDefault();
        const file = videoInput.files[0];
        if (!file) {
            alert('Please select a video file.');
            return;
        }
  
        const formData = new FormData();
        formData.append('video', file);
  
        try {
            const response = await fetch("http://127.0.0.1:5000/summary", {
                method: 'POST',
                body: formData
            });
  
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
  
            const data = await response.json();
            resultDiv.innerHTML = `<p>Result: ${data.is_deepfake}</p>`;
        } catch (error) {
            console.error('Error:', error);
            resultDiv.innerHTML = '<p>An error occurred. Please try again later.</p>';
        }
    });
  });
  