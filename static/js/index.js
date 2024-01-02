
const btn = document.querySelector(".switch-btn");
const video = document.querySelector(".video-container");
btn.innerHTML = '<i class="fa-solid fa-pause"></i>';
btn.addEventListener("click", function () {
    if (video.paused) {
        video.play();
        btn.innerHTML = '<i class="fa-solid fa-pause"></i>';
    } else {
        video.pause();
        btn.innerHTML = '<i class="fa-solid fa-play"></i>';
    }
});


    ///scroll------------------------------------------------------------------------------------------------
  //   const box = document.getElementById('box');
  // const upperBox = document.getElementById('upperbox');
  // const lowerBox = document.getElementById('lowerbox');
  // const headBox = document.getElementById('heading-h1');
  let prevScrollPos = window.pageYOffset;
  let isScrollingDown = true;

  window.onscroll = function() {
    const currentScrollPos = window.pageYOffset;

    if (prevScrollPos < currentScrollPos) {
      // Scrolling down
      upperBox.style.marginTop = '-20vh'; // Adjust as needed
      lowerBox.style.width = '1600px'; // Adjust as needed
      headBox.style.fontSize = '2rem'; // Adjust as needed

      isScrollingDown = true;
    } else {
      // Scrolling up
      upperBox.style.marginTop = '0';
      lowerBox.style.width = '1500px'; // Adjust as needed
      headBox.style.fontSize = '2.5rem'; // Adjust as needed

      isScrollingDown = false;
      
    }

    // Adjust the transition duration based on the scroll direction
    const transitionDuration = isScrollingDown ? '0.9s' : '2s';
    upperBox.style.transitionDuration = transitionDuration;
    lowerBox.style.transitionDuration = transitionDuration;

    prevScrollPos = currentScrollPos;
  };
  //show car ------------------------------------------------------------------------------------------------
  function showCarSet(carType) {
// Remove active class from all links
const links = document.querySelectorAll('.explore-container a');
links.forEach(link => link.classList.remove('active'));

// Add active class to the clicked link
const clickedLink = document.querySelector(`.explore-container a[data-car-type='${carType}']`);
clickedLink.classList.add('active');

// Hide all car sets
const carSets = document.querySelectorAll('.car-set');
carSets.forEach(set => set.classList.remove('active'));

// Show the selected car set
const selectedSet = document.getElementById(`${carType}Set`);
selectedSet.classList.add('active');
}
function showCarDetails(carImageLocation, carName) {
  // Update the large car details
  const carDetailsContainer = document.getElementById('carDetails');
  carDetailsContainer.innerHTML = `
      <img src="${carImageLocation}" alt="${carName}">
      <h1>${carName}</h1>
      <div class="slide-button right">
                        <a href="{% url 'add_to_whislist' car_id=car.id %}" >Interested</a>
                    </div>      `;

  // Add the 'active' class to apply styles
  carDetailsContainer.classList.add('active');
}


 


  