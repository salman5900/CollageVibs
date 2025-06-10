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

// ✅ Dropdown toggle logic using class 'show'
document.querySelectorAll('.dropdown').forEach(dropdown => {
  const button = dropdown.querySelector('.dropbtn');

  button.addEventListener('click', function (e) {
    e.stopPropagation();

    // Close other dropdowns
    document.querySelectorAll('.dropdown').forEach(other => {
      if (other !== dropdown) other.classList.remove('show');
    });

    // Toggle this one
    dropdown.classList.toggle('show');
  });
});

// ✅ Close dropdowns when clicking outside
document.addEventListener('click', function () {
  document.querySelectorAll('.dropdown').forEach(drop => {
    drop.classList.remove('show');
  });
});
