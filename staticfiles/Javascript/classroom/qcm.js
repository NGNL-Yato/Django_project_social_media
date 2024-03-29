/* ETOILES */

// inputHidden
var qStarStarValue = document.querySelector("input[id$='qStar-star-value']");

// Gestion chargement : hidden value (si existe) -> étoile correspondante
if (
  qStarStarValue.getAttribute("value") !== null &&
  qStarStarValue.getAttribute("value") != ""
) {
  document.getElementById(
    "qStar-rating-" + qStarStarValue.getAttribute("value")
  ).checked = true;
}

// étoiles
var inputs = document.querySelectorAll("#qStar input[type=radio]");

// Gestion clic : étoile -> hidden value
for (var i = 0; i < inputs.length; i++) {
  if (inputs.item(i).className == "star-cb-clear") {
    inputs.item(i).onchange = function () {
      qStarStarValue.removeAttribute("value");
    };
  } else {
    inputs.item(i).onchange = function () {
      qStarStarValue.value = this.value;
    };
  }
}
