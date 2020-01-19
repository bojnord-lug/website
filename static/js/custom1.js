function getPagination(pageNumber) {
  const data = pageNumber;
  axios
    .post("http://localhost:8000/bloglist/", data)
    .then(res => {
      document.getElementById("bloglist").innerHTML = res.data;
    })
    .catch(error => console.log(error));
}
