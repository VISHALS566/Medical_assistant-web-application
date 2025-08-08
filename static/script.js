document.getElementById('findDoctorBtn').addEventListener('click', () => {
  if (!navigator.geolocation) {
    alert('Geolocation is not supported by your browser.');
    return;
  }
  
  navigator.geolocation.getCurrentPosition(async (position) => {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;

    try {
      const response = await fetch(`http://127.0.0.1:5000/find-doctor?lat=${lat}&lng=${lng}`);
      const data = await response.json();
      displayDoctors(data.results);
    } catch (error) {
      alert("Error fetching doctor data: " + error.message);
    }
  }, () => {
    alert("Unable to retrieve your location.");
  });
});

function displayDoctors(results) {
  let container = document.getElementById('doctorResults');
  if (!container) {
    container = document.createElement('div');
    container.id = 'doctorResults';
    container.style.marginTop = '20px';
    document.body.appendChild(container);
  }
  
  if (!results || results.length === 0) {
    container.textContent = "No nearby clinics found.";
    return;
  }
  
  container.innerHTML = '<h3>Nearest Clinics/Hospitals:</h3>';
  const ul = document.createElement('ul');
  results.forEach(place => {
    const li = document.createElement('li');
    li.textContent = `${place.name} - ${place.vicinity}`;
    ul.appendChild(li);
  });
  container.appendChild(ul);
}




