'use strict';

/**
 * navbar variables
 */

const navOpenBtn = document.querySelector("[data-menu-open-btn]");
const navCloseBtn = document.querySelector("[data-menu-close-btn]");
const navbar = document.querySelector("[data-navbar]");
const overlay = document.querySelector("[data-overlay]");

const navElemArr = [navOpenBtn, navCloseBtn, overlay];

for (let i = 0; i < navElemArr.length; i++) {

  navElemArr[i].addEventListener("click", function () {

    navbar.classList.toggle("active");
    overlay.classList.toggle("active");
    document.body.classList.toggle("active");

  });

}



/**
 * header sticky
 */

const header = document.querySelector("[data-header]");

window.addEventListener("scroll", function () {

  window.scrollY >= 10 ? header.classList.add("active") : header.classList.remove("active");

});




const goTopBtn = document.querySelector("[data-go-top]");

window.addEventListener("scroll", function () {

  window.scrollY >= 500 ? goTopBtn.classList.add("active") : goTopBtn.classList.remove("active");

});

document.getElementById('searchButton').addEventListener('click', function() {
  var searchTerm = document.getElementById('searchInput').value;
  alert('Searching for: ' + searchTerm);
  
});

function func(){
  var email= document.getElementById("submit").value;
  var email = document.getElementById("email").value;
  if (email == 'saiyajuprabesh2526@gmail.com'){
      alert("sucessfull! ")
      window.location.assign('index.html')
      
  }
  else{
      alert("wrong entry invalid")
  }
}

