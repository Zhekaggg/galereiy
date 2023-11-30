function uploadPhoto() {
    var photoInput = document.getElementById('photoInput');
    var descriptionInput = document.getElementById('descriptionInput');
    var gallery = document.getElementById('gallery');

    var file = photoInput.files[0];
    if (file) {
        var reader = new FileReader();
        reader.onload = function(e) {
            var photoDiv = document.createElement('div');
            photoDiv.className = 'photo';
            photoDiv.innerHTML = '<img src="' + e.target.result + '" alt="Uploaded Photo">' +
                                 '<p>' + descriptionInput.value + '</p>';
            gallery.appendChild(photoDiv);
            // Очистка формы после загрузки
            document.getElementById('uploadForm').reset();
        };
        reader.readAsDataURL(file);
    }
}
