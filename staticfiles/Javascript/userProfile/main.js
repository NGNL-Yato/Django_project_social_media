/*=============== CHANGE BACKGROUND HEADER ===============*/
function scrollHeader() {
  const header = document.getElementById("header");
  // When the scroll is greater than 50 viewport height, add the scroll-header class to the header tag
  if (this.scrollY >= 50) header.classList.add("scroll-header");
  else header.classList.remove("scroll-header");
}
window.addEventListener("scroll", scrollHeader);

/*=============== SERVICES MODAL ===============*/
// Get the modal
const modalViews = document.querySelectorAll(".services__modal");
let modalBtns = document.getElementById("contact_trigger");

let cardcontent = document.getElementById("profile_card");
// work with this id to manipulate the layout
let modalClose = document.querySelectorAll(".services__modal-close");

const modalCloseButtons = document.querySelectorAll(".services__modal-close");

console.log(modalBtns);
// When the user clicks on the button, open the modal
modalBtns.onclick = function () {
  layoutpop(cardcontent);
};

modalCloseButtons.forEach((button) => {
  button.addEventListener("click", function () {
    cardcontent.style.display = "none";
  });
});

function layoutpop(cardcontent) {
  if (cardcontent.style.display === "none") {
    cardcontent.style.display = "block";
  } else {
    cardcontent.style.display = "none";
  }
}

