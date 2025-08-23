document.addEventListener("DOMContentLoaded", function() {
  const form = document.querySelector(".login-box form");
  const submitButton = document.querySelector(".login-box a");

  submitButton.addEventListener("click", function(event) {
    event.preventDefault();
    form.submit();
  });
});
