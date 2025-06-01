window.addEventListener('scroll', function() {
  const navbar = document.querySelector('.navbar');

  if (window.scrollY > 0) {
    navbar.classList.add('scrolled');
  } else {
    navbar.classList.remove('scrolled');
  }
});


// js for full sreen notice borad
document.addEventListener('DOMContentLoaded', function() {
  const modal = document.getElementById("imageModal");
  const modalImg = document.getElementById("fullImage");
  const closeBtn = document.getElementsByClassName("close")[0];

  const images = document.querySelectorAll('.notice-image');
  images.forEach(img => {
    img.addEventListener('click', function() {
      modal.style.display = "block";
      modalImg.src = this.src;
    });
  });

  closeBtn.onclick = function() {
    modal.style.display = "none";
  }
  window.onclick = function(event) {
    if (event.target == modal) {
      modal.style.display = "none";
    }
  }
});