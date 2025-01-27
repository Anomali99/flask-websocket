// Menghubungkan ke WebSocket server
const ws = new WebSocket(`ws://${window.location.hostname}:5000/sensor_data`);

// Elemen DOM untuk menampilkan data
const temperatureEl = document.getElementById("temperature");
const humidityEl = document.getElementById("humidity");
const relayOnBtn = document.getElementById("relay-on");
const relayOffBtn = document.getElementById("relay-off");

// WebSocket menerima data dari server
ws.onmessage = (event) => {
  const data = JSON.parse(event.data); // Data JSON dari server
  temperatureEl.textContent = data.temperature || "N/A";
  humidityEl.textContent = data.humidity || "N/A";
};

// Kontrol relay dengan HTTP POST
const controlRelay = async (relayState) => {
  try {
    const response = await fetch("/relay", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ relay: relayState }),
    });
    const result = await response.json();
    console.log("Relay status:", result);
  } catch (error) {
    console.error("Failed to control relay:", error);
  }
};

// Event listener untuk tombol kontrol relay
relayOnBtn.addEventListener("click", () => controlRelay(true));
relayOffBtn.addEventListener("click", () => controlRelay(false));
