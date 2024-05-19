function detect() {
  fetch('/detect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({})
  })
  .then(response => response.json())
  .then(data => alert(data.message))
  .catch(error => console.error('Error:', error));
}

function displayMedia(event) {
  const file = event.target.files[0];
  if (file) {
    const mediaType = file.type.startsWith("image") ? "image" : "video";
    const reader = new FileReader();
    reader.onload = function(event) {
      const mediaContainer = document.getElementById("outputVideoElement");
      mediaContainer.innerHTML = "";
      if (mediaType === "image") {
        const img = document.createElement("img");
        img.src = event.target.result;
        img.style.maxWidth = "100%";
        img.style.height = "auto";
        mediaContainer.appendChild(img);
      } else if (mediaType === "video") {
        const video = document.createElement("video");
        video.src = event.target.result;
        video.controls = true;
        video.autoplay = true;
        video.style.maxWidth = "100%";
        video.style.height = "auto";
        mediaContainer.appendChild(video);
      }
    };
    reader.readAsDataURL(file);
  }
}
const file = document.getElementById("detectButton");
file.addEventListener("change", displayMedia);

function solveProblem(problem, coordinates) {
  document.getElementById("coordinatesDisplay").textContent = "Coordinates: " + coordinates;
}

const problemsWithCoordinates = [
  { problem: "Issue 1", coordinates: "x1_y1" },
  { problem: "Issue 2", coordinates: "x2_y2" },
  { problem: "Issue 3", coordinates: "x3_y3" },
  { problem: "Issue 4", coordinates: "x4_y4" },
  { problem: "Issue 5", coordinates: "x5_y5" },
  { problem: "Issue 6", coordinates: "x6_y6" },
  { problem: "Issue 7", coordinates: "x7_y7" },
  { problem: "Issue 8", coordinates: "x8_y8" },
  { problem: "Issue 9", coordinates: "x9_y9" },
  { problem: "Issue 10", coordinates: "x10_y10" }

];

const problemList = document.getElementById("problemList");
problemsWithCoordinates.forEach(item => {
  const li = document.createElement("li");
  li.textContent = item.problem;
  const solveButton = document.createElement("button");
  solveButton.textContent = "Solve";
  solveButton.classList.add("solve-button");
  solveButton.addEventListener("click", function() {
    solveProblem(item.problem, item.coordinates);
  });
  li.appendChild(solveButton);
  problemList.appendChild(li);
});


function fetchAndPlayVideo() {
  const coordinatesDisplay = document.getElementById("coordinatesDisplay").textContent;
  const coordinates = coordinatesDisplay.split("Coordinates: ")[1];
  if (!coordinates) {
    alert("No coordinates selected.");
    return;
  }

  const mediaContainer = document.getElementById("mediaContainer");
  mediaContainer.innerHTML = ""; // Clear previous content

  // Fetch the video from the Flask server
  const videoPath = `/videos/${coordinates}/video1.mp4`;
  console.log(`Fetching video from: ${videoPath}`); // Debugging path
  const video = document.createElement("video");
  video.src = videoPath;
  video.controls = true;
  video.autoplay = true;
  video.style.maxWidth = "100%";
  video.style.height = "auto";
  mediaContainer.appendChild(video);
}
const fileInput = document.getElementById("fetchButton");
fileInput.addEventListener("change", displayMedia);

// script.js
document.getElementById('detectButton').addEventListener('click', function() {
  const progressBar = document.getElementById('progressBar');
  const progressBarFill = document.querySelector('.progress-bar-fill');
  const outputVideo = document.getElementById('outputVideo');
  const outputVideoElement = document.getElementById('outputVideoElement');

  // Show progress bar
  progressBar

  progressBar.classList.remove('hidden');
  progressBarFill.style.width = '0%';

  // Reset the output video section
  outputVideo.classList.add('hidden');
  outputVideoElement.src = '';

  // Simulate progress bar fill (for demo purposes, you can replace this with actual progress from the backend)
  let progress = 0;
  const interval = setInterval(() => {
    progress += 10;
    progressBarFill.style.width = `${progress}%`;
    if (progress >= 100) {
      clearInterval(interval);
      progressBarFill.style.width = '100%';
      progressBar.classList.add('hidden');

      // Simulate backend call and response
      detectAndShowVideo();
    }
  }, 500);
});

function detectAndShowVideo() {
  // Call backend service to run Python script
  const coordinatesDisplay = document.getElementById("coordinatesDisplay").textContent;
  const coordinates = coordinatesDisplay.split("Coordinates: ")[1];
  if (!coordinates) {
    alert("No coordinates selected.");
    return;
  }
  const mediaContainer = document.getElementById("outputVideoElement");
  mediaContainer.innerHTML = ""; // Clear previous content

  // Fetch the video from the Flask server
  const videoPath = `/videos/${coordinates}/output.mp4`;
  console.log(`Fetching video from: ${videoPath}`); // Debugging path
  const video = document.createElement("video");
  video.src = videoPath;
  video.controls = true;
  video.autoplay = true;
  video.style.maxWidth = "100%";
  video.style.height = "auto";
  mediaContainer.appendChild(video);

  fetch('/detect', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      coordinatesFolder: coordinates
    })
  })
  .then(response => response.json())
  .then(data => {
    // Assuming the backend returns the path to the output video
    const videoPath = data.outputVideoPath;
    const outputVideoElement = document.getElementById('outputVideoElement');
    outputVideoElement.src = videoPath.replace(/\\/g, '/'); // Replace backslashes with forward slashes
    const outputVideo = document.getElementById('outputVideo');
    outputVideo.classList.remove('hidden');
  })
  
  .catch(error => {
    console.error('Error:', error);
    // Handle error case, optionally hide the progress bar
  });
}

// Function to generate report message based on coordinates
function generateReportMessage(coordinates) {
  switch(coordinates) {
      case "x1_y1":
          return "Tree fall detected";
      case "x2_y2":
          return "Road encroachment detected";
      default:
          return "No specific report for these coordinates";
  }
}

// Attach click event listener to the "Send Report" button
document.getElementById('sendReportButton').addEventListener('click', function() {
  const coordinatesDisplay = document.getElementById("coordinatesDisplay").textContent;
  const coordinates = coordinatesDisplay.split("Coordinates: ")[1];
  if (!coordinates) {
      alert("No coordinates selected.");
      return;
  }

  // Get the report message based on coordinates
  const reportMessage = generateReportMessage(coordinates);

  // Display the report message
  const reportMessageContainer = document.getElementById("reportMessage");
  reportMessageContainer.textContent = reportMessage;

  // Show report sent message
  alert("Report sent.");
});

