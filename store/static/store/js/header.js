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
