document.querySelectorAll('.sidebar__dropdown-toggle').forEach(toggle => {
  toggle.addEventListener('click', function () {
      const parent = this.parentElement; // Sidebar item
      const dropdownMenu = parent.querySelector('.sidebar__dropdown-menu');

      // Toggle visibility of the dropdown
      const isOpen = parent.classList.contains('open');
      document.querySelectorAll('.sidebar__item').forEach(item => item.classList.remove('open')); // Close other dropdowns
      if (!isOpen) {
          parent.classList.add('open'); // Open current dropdown
      }
  });
});


document.addEventListener("DOMContentLoaded", () => {
    // Sidebar links
    const dashboardLink = document.querySelector("a[href='#admin-dashboard']");
    const serviceLink = document.querySelector("a[href='#admin-service']");
    const petLink = document.querySelector("a[href='#admin-pet']");
    const ownerLink = document.querySelector("a[href='#admin-pet-owner']");
    const groomerLink = document.querySelector("a[href='#admin-groomer']");
    const appointmentLink = document.querySelector("a[href='#admin-appointment']");
  
    // Content containers
    const dashboardContent = document.getElementById("admin-dashboard");
    const serviceContent = document.getElementById("admin-service");
    const petContent = document.getElementById("admin-pet");
    const ownerContent = document.getElementById("admin-pet-owner");
    const groomerContent = document.getElementById("admin-groomer");
    const appointmentContent = document.getElementById("admin-appointment");
  
    // Function to hide all content
    function hideAllContent() {
      dashboardContent.style.display = "none";
      serviceContent.style.display = "none";
      petContent.style.display = "none";
      ownerContent.style.display = "none";
      groomerContent.style.display = "none";
      appointmentContent.style.display = "none";
    }
  
    // Function to remove 'active-link' class from all sidebar links
    function removeActiveClass() {
      document.querySelectorAll(".sidebar__link").forEach((link) => {
        link.classList.remove("active-link");
      });
    }
  
    // Event listener for "Dashboard" link
    dashboardLink.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent default anchor behavior
      hideAllContent(); // Hide other content
      removeActiveClass(); // Remove active class from other links
      dashboardContent.style.display = "block"; // Show Dashboard content
      dashboardLink.classList.add("active-link"); // Highlight the active link
    });
  
    // Event listener for "Service" link
    serviceLink.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent default anchor behavior
      hideAllContent(); // Hide other content
      removeActiveClass(); // Remove active class from other links
      serviceContent.style.display = "block"; // Show Service content
      serviceLink.classList.add("active-link"); // Highlight the active link
    });

     // Event listener for "Pet" link
     petLink.addEventListener("click", (event) => {
      event.preventDefault(); // Prevent default anchor behavior
      hideAllContent(); // Hide other content
      removeActiveClass(); // Remove active class from other links
      petContent.style.display = "block"; // Show Pet content
      petLink.classList.add("active-link"); // Highlight the active link
    });

      // Event listener for "Owner" link
      ownerLink.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default anchor behavior
        hideAllContent(); // Hide other content
        removeActiveClass(); // Remove active class from other links
        ownerContent.style.display = "block"; // Show Pet content
        ownerLink.classList.add("active-link"); // Highlight the active link
      });

      // Event listener for "Groomer" link
      groomerLink.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default anchor behavior
        hideAllContent(); // Hide other content
        removeActiveClass(); // Remove active class from other links
        groomerContent.style.display = "block"; // Show Pet content
        groomerLink.classList.add("active-link"); // Highlight the active link
      });

       // Event listener for "Appointment" link
       appointmentLink.addEventListener("click", (event) => {
        event.preventDefault(); // Prevent default anchor behavior
        hideAllContent(); // Hide other content
        removeActiveClass(); // Remove active class from other links
        appointmentContent.style.display = "block"; // Show Pet content
        appointmentLink.classList.add("active-link"); // Highlight the active link
      });
  
    // Initialize by hiding all content and showing only the dashboard
    hideAllContent();
    dashboardContent.style.display = "block"; // Default to showing Dashboard on page load
    dashboardLink.classList.add("active-link");
  });
  


/*=============== SHOW SIDEBAR ===============*/
const showSidebar = (toggleId, sidebarId, headerId, mainId) => {
    const toggle = document.getElementById(toggleId),
          sidebar = document.getElementById(sidebarId),
          header = document.getElementById(headerId),
          main = document.getElementById(mainId);

    if (toggle && sidebar && header && main) {
        toggle.addEventListener('click', () => {
            /* Toggle sidebar visibility */
            sidebar.classList.toggle('show-sidebar');

            /* Adjust main content padding */
            header.classList.toggle('left-pd');
            main.classList.toggle('left-pd');
        });
    }
};
showSidebar('header-toggle', 'sidebar', 'header', 'main');

/*=============== LINK ACTIVE ===============*/
const sidebarLinks = document.querySelectorAll('.sidebar__link');

function activateLink() {
    sidebarLinks.forEach(link => link.classList.remove('active-link'));
    this.classList.add('active-link');
}

sidebarLinks.forEach(link => link.addEventListener('click', activateLink));

const sidebarLink = document.querySelectorAll('.sidebar__list a')

function linkColor(){
    sidebarLink.forEach(l => l.classList.remove('active-link'))
    this.classList.add('active-link')
}

sidebarLink.forEach(l => l.addEventListener('click', linkColor))

/*=============== DARK LIGHT THEME ===============*/
const themeButton = document.getElementById('theme-button')
const darkTheme = 'dark-theme'
const iconTheme = 'ri-sun-fill'

// Previously selected topic (if user selected)
const selectedTheme = localStorage.getItem('selected-theme')
const selectedIcon = localStorage.getItem('selected-icon')

// We obtain the current theme that the interface has by validating the dark-theme class
const getCurrentTheme = () => document.body.classList.contains(darkTheme) ? 'dark' : 'light'
const getCurrentIcon = () => themeButton.classList.contains(iconTheme) ? 'ri-moon-clear-fill' : 'ri-sun-fill'

// We validate if the user previously chose a topic
if (selectedTheme) {
  // If the validation is fulfilled, we ask what the issue was to know if we activated or deactivated the dark
  document.body.classList[selectedTheme === 'dark' ? 'add' : 'remove'](darkTheme)
  themeButton.classList[selectedIcon === 'ri-moon-clear-fill' ? 'add' : 'remove'](iconTheme)
}

// Activate / deactivate the theme manually with the button
themeButton.addEventListener('click', () => {
    // Add or remove the dark / icon theme
    document.body.classList.toggle(darkTheme)
    themeButton.classList.toggle(iconTheme)
    // We save the theme and the current icon that the user chose
    localStorage.setItem('selected-theme', getCurrentTheme())
    localStorage.setItem('selected-icon', getCurrentIcon())
})
