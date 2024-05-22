document.addEventListener("DOMContentLoaded", function () {
  const forwardForm = document.getElementById("forward-form");
  const forwardResult = document.getElementById("forward-result");

  const inverseForm = document.getElementById("inverse-form");
  const inverseResult = document.getElementById("inverse-result");

  forwardForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const theta1 = document.getElementById("theta_1").value;
    const theta2 = document.getElementById("theta_2").value;
    const theta3 = document.getElementById("theta_3").value;

    const response = await fetch("/api/forward_kinematics/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        theta_1: parseFloat(theta1),
        theta_2: parseFloat(theta2),
        theta_3: parseFloat(theta3),
      }),
    });

    const result = await response.json();
    if (response.ok) {
      forwardResult.innerHTML = `
                <p>Position X: ${result.pos_x.toFixed(2)}</p>
                <p>Position Y: ${result.pos_y.toFixed(2)}</p>
                <p>Position Z: ${result.pos_z.toFixed(2)}</p>
            `;
    } else {
      forwardResult.innerHTML = `<p>Error: ${result.detail}</p>`;
    }
  });

  inverseForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const posX = document.getElementById("pos_x").value;
    const posY = document.getElementById("pos_y").value;
    const posZ = document.getElementById("pos_z").value;

    const response = await fetch("/api/inverse_kinematics/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        pos_x: parseFloat(posX),
        pos_y: parseFloat(posY),
        pos_z: parseFloat(posZ),
      }),
    });

    const result = await response.json();
    if (response.ok) {
      inverseResult.innerHTML = `
                <p>Theta 1: ${result.theta_1.toFixed(2)}</p>
                <p>Theta 2: ${result.theta_2.toFixed(2)}</p>
                <p>Theta 3: ${result.theta_3.toFixed(2)}</p>
            `;
    } else {
      inverseResult.innerHTML = `<p>Error: ${result.detail}</p>`;
    }
  });
});
