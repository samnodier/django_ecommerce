document.addEventListener("DOMContentLoaded", () => {
  const searchButton = document.querySelector("#search-toggle");
  if (!searchButton) return;
  searchButton.addEventListener("click", toggleSearch);

  // Scroll functionality (one item at a time)
  const scrollContainer = document.getElementById("category-scroll");
  const leftScrollBtn = document.getElementById("category-scroll-left");
  const rightScrollBtn = document.getElementById("category-scroll-right");

  const scrollAmount = 130; // approximately one item;

  leftScrollBtn.addEventListener("click", () => {
    scrollContainer.scrollBy({ left: -scrollAmount, behavior: "smooth" });
  });

  rightScrollBtn.addEventListener("click", () => {
    scrollContainer.scrollBy({ left: scrollAmount, behavior: "smooth" });
  });

  // Check the status of scrollContainer and update the buttons
  scrollContainer.addEventListener("scroll", updateScrollButtons);

  // Create a function to check the scroll position of the categories in the navigation
  function updateScrollButtons() {
    // Create a tolerance to aid in comparison
    const tolerance = 5;

    // check left
    if (scrollContainer.scrollLeft <= tolerance) {
      leftScrollBtn.classList.add("invisible");
    } else {
      leftScrollBtn.classList.remove("invisible");
    }

    // Check right
    if (
      Math.ceil(scrollContainer.scrollLeft + scrollContainer.clientWidth) >=
      scrollContainer.scrollWidth - tolerance
    ) {
      rightScrollBtn.classList.add("invisible");
    } else {
      rightScrollBtn.classList.remove("invisible");
    }
  }

  // Initial check on page load
  updateScrollButtons();

  // Check on the resize of the window
  window.addEventListener("resize", updateScrollButtons);
});

document.addEventListener("click", (event) => {
  // Close search when clicking outside
  const searchContainer = document.getElementById("search-container");
  const searchButton = event.target.closest("#search-toggle");
  if (
    !searchContainer.contains(event.target) &&
    !searchButton &&
    !searchContainer.classList.contains("hidden")
  ) {
    toggleSearch();
  }
});

function toggleSearch() {
  const searchContainer = document.getElementById("search-container");
  const searchInput = document.getElementById("search-input");

  if (searchContainer.classList.contains("hidden")) {
    // Open it
    searchContainer.classList.remove("hidden");
    searchContainer.classList.add("animate-fade-in-down");

    setTimeout(() => {
      searchInput.focus();
    }, 100);
  } else {
    // Close the search
    searchContainer.classList.add("hidden");
    searchContainer.classList.remove("animate-fade-in-down");
  }
}
