var demoForm = document.querySelector(".demoForm");
demoForm.addEventListener(
  "submit",
  function (e) {
    var demoInput = document.querySelector('input[name="rate"]:checked');
    if (!demoInput) {
      console.log("NO...");
    } else {
      console.log(demoInput.value);
    }
  },
  true
);
