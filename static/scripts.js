// Menghubungkan ke WebSocket server
// const url = `ws://${window.location.hostname}:5000/sensor_data`
const url = "wss://chatserver.anomali99.my.id/sensor_data";
const ws = new WebSocket(url);

// Elemen DOM untuk menampilkan data
const temperatureEl = document.getElementById("temperature");
const humidityEl = document.getElementById("humidity");
const luxEl = document.getElementById("lux");
const moistureEl = document.getElementById("moisture");
const relayOnBtn = document.getElementById("relay-on");
const relayOffBtn = document.getElementById("relay-off");

// WebSocket menerima data dari server
ws.onmessage = (event) => {
  const data = JSON.parse(event.data); // Data JSON dari server
  temperatureEl.textContent = data.temperature || "N/A";
  humidityEl.textContent = data.humidity || "N/A";
  luxEl.textContent = data.lux || "N/A";
  moistureEl.textContent = data.moisture || "N/A";
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
