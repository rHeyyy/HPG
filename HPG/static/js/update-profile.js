document.addEventListener("DOMContentLoaded", () => {
    const delmodal = document.getElementById("deleteModal");
    const closeBtn = delmodal.querySelector(".close-btn"); // Fix: use delmodal here
    const delmodalFormContainer = document.getElementById("delete-modal-form-container");
    const delLinks = document.querySelectorAll(".delete-link");

    // Handle clicking on the delete link
    delLinks.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const userId = link.getAttribute("data-user-id1");

            // Load the form dynamically via fetch
            fetch(`/delete-user/${userId}/`)
                .then((response) => response.text())
                .then((data) => {
                    delmodalFormContainer.innerHTML = data;
                    delmodal.classList.add("show"); // Show the modal
                })
                .catch((error) => {
                    delmodalFormContainer.innerHTML = "<h2>Error loading form</h2>";
                    console.error("Error:", error);
                });
        });
    });

    // Close modal using close button only
    closeBtn.addEventListener("click", () => {
        delmodal.classList.remove("show"); // Close the modal
    });
});



// for update-profile

  document.addEventListener("DOMContentLoaded", () => {
        const modal = document.getElementById("profileModal");
        const closeBtn = modal.querySelector(".close-btn");
        const modalFormContainer = document.getElementById("modal-form-container");
        const editLinks = document.querySelectorAll(".edit-profile");

        // Handle clicking on the edit link
        editLinks.forEach((link) => {
            link.addEventListener("click", (e) => {
                e.preventDefault();
                const userId = link.getAttribute("data-user-id");

                // Load the form dynamically via fetch
                fetch(`/update_profile/${userId}/`)
                    .then((response) => response.text())
                    .then((data) => {
                        modalFormContainer.innerHTML = data;
                        modal.classList.add("show"); // Show the modal
                    })
                    .catch((error) => {
                        modalFormContainer.innerHTML = "<h2>Error loading form</h2>";
                        console.error("Error:", error);
                    });
            });
        });

        // Close modal using close button only
        closeBtn.addEventListener("click", () => {
            console.log('Close button clicked');
            modal.classList.remove("show");
        });
    });


// FOr Search input
document.addEventListener("DOMContentLoaded", () => {
    const searchInput = document.getElementById("search-input");
    const userTable = document.getElementById("user-tbody");

    // Real-time search functionality
    searchInput.addEventListener("input", () => {
        const query = searchInput.value.toLowerCase();
        const rows = userTable.querySelectorAll("tr");

        rows.forEach((row) => {
            const cells = row.querySelectorAll("td");
            const text = Array.from(cells)
                .map((cell) => cell.textContent.toLowerCase())
                .join(" ");
            row.style.display = text.includes(query) ? "" : "none";
        });
    });
});