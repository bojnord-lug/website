function getPagination(pageNumber) {
  const data = pageNumber;
  axios
    .post("http://localhost:8000/bloglist/", data)
    .then(res => {
      document.getElementById("bloglist").innerHTML = res.data;
    })
    .catch(error => console.log(error));
}
function saveEmail() {
  if (document.getElementById("newsletterEmail").value != "") {
    const data = document.getElementById("newsletterEmail").value;
    axios
      .post("http://localhost:8000/saveEmail/", data)
      .then(res => {
        alert("با موفقیت ثبت شد");
      })
      .catch(error => console.log(error));
  }
}
