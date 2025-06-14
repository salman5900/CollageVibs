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

// Toggle members dropdown
document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("membersToggleBtn");
  const dropdown = document.getElementById("membersDropdown");

  toggleBtn.addEventListener("click", (e) => {
    e.preventDefault();
    dropdown.classList.toggle("show");

    // Re-trigger animation for each entry
    if (dropdown.classList.contains("show")) {
      const entries = dropdown.querySelectorAll(".member-entry");
      entries.forEach((entry, index) => {
        entry.style.animationDelay = `${index * 0.05}s`;
        entry.style.opacity = 0;
        entry.classList.remove("animated"); // reset
        void entry.offsetWidth; // trigger reflow
        entry.classList.add("animated");
      });
    }
  });

  // 👇 Close dropdown when clicking outside of it
  document.addEventListener("click", (e) => {
    if (!dropdown.contains(e.target) && !toggleBtn.contains(e.target)) {
      dropdown.classList.remove("show");
    }
  });
});


// dropdown js 
document.addEventListener('DOMContentLoaded', function() {
  const dropdowns = document.querySelectorAll('.dropdown');
  
  dropdowns.forEach(dropdown => {
    const dropbtn = dropdown.querySelector('.dropbtn');
    const dropdownContent = dropdown.querySelector('.dropdown-content');
    
    dropbtn.addEventListener('click', function() {
      // Get tile position
      const rect = dropdown.getBoundingClientRect();
      const windowHeight = window.innerHeight;
      
      // If tile is in bottom half of screen, make it dropup
      if (rect.bottom > windowHeight / 2) {
        dropdownContent.classList.add('dropup');
      } else {
        dropdownContent.classList.remove('dropup');
      }
      
      // Toggle dropdown
      dropdownContent.classList.toggle('show');
    });
  });
});