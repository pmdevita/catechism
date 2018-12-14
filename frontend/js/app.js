import "../scss/app.scss";
import { $ } from "./nanojs.js"

document.addEventListener("DOMContentLoaded", function(event) { 
  $("#navigation").insertFirst("test");
});