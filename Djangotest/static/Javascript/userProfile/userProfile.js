var div = document.getElementById("main");
var display = 0;

function hideShow() {
  if (display == 1) {
    div.style.display = "block";
    display = 0;
  } else {
    div.style.display = "none";
    display = 1;
  }
}
let profilpic = document.getElementById("profile-pic");
let inputfile = document.getElementById("input-file");

inputfile.onchange = function () {
  profilpic.src = URL.createObjectURL(inputfile.files[0]);
};
