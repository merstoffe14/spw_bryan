// Initialize current angles for motors S and Q
let currentAngleS = 0;
let currentAngleQ = 180;

// Function to send command
async function sendCommand() {
  const motorSelect = document.getElementById("motorSelect");
  const angleInput = document.getElementById("angleInput");

  const motor = motorSelect.value;
  const angle = angleInput.value;

  // Construct command
  const command = `${motor} ${angle}`;

  // Update current location display
  updateCurrentLocation(motor, angle);

  try {
    // Send serial command
    await fetch(`/api/sendcommand?command=${command}`);
  } catch (error) {
    console.error("Error sending command:", error);
  }
}

// Function to update and display current location
function updateCurrentLocation(motor, angle) {
  if (motor === "S") {
    currentAngleS = angle;
  } else if (motor === "Q") {
    currentAngleQ = angle;
  }

  document.getElementById(
    "currentLocation"
  ).textContent = `Current Location: Motor S - ${currentAngleS}, Motor Q - ${currentAngleQ}`;
}

// Function to update slider value display
function updateSliderValue() {
  const angleInput = document.getElementById("angleInput");
  const angleValue = document.getElementById("angleValue");
  angleValue.textContent = angleInput.value;
}

// Function to update slider position based on motor selection
function updateSliderPosition() {
  const motorSelect = document.getElementById("motorSelect");
  const angleInput = document.getElementById("angleInput");

  const motor = motorSelect.value;
  const angle = motor === "S" ? currentAngleS : currentAngleQ;

  angleInput.value = angle;
  updateSliderValue();
}

// Display initial current location
updateCurrentLocation("S", currentAngleS);
updateCurrentLocation("Q", currentAngleQ);

// Initialize slider value display
updateSliderValue();
