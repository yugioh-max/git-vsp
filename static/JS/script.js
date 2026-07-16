const form = document.getElementById('uploadForm');
const submitBtn = document.getElementById('submitBtn');
const loaderContainer = document.getElementById('loaderContainer');


form.addEventListener('submit', function(e){
    submitBtn.disabled = true;
    submitBtn.textContent = 'Upload en cours';
    loaderContainer.style.display = 'block';
});