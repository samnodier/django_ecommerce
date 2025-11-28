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
