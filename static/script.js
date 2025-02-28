async function fetchDetails() {
    let username = document.getElementById("username").value;

    // Show loading animation
    document.getElementById("loading").style.display = "block";
    document.getElementById("result-card").style.display = "none";

    try {
        let response = await fetch(`https://fake-id-detection-3.onrender.com/get_details?username=${username}`);
        let data = await response.json();

        document.getElementById("loading").style.display = "none";

        if (data.error) {
            alert(data.error);
        } else {
            document.getElementById("fake").innerText = data.fake ? "🚨 Fake Account" : "✅ Real Account";
            document.getElementById("result-card").style.display = "block";
        }
    } catch (error) {
        document.getElementById("loading").style.display = "none";
        alert("Error connecting to server. Make sure Flask is running.");
    }
}
