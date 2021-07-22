function performOCR() {
    let files = document.getElementById("image_file").files
    let formData = new FormData();
    let endpoint = '/postocr';
    if (files.length == 1) {
      formData.append('image', files[0])
    }

    $("body").addClass("loading");
    
    $.ajax({
        type: 'POST',
        url: endpoint,
        data: formData,
        contentType: false,
        cache: false,
        processData: false,
        success: function(data) {
          if (endpoint == '/postocr') {
            $("body").removeClass("loading");
            swal("Data de validade", data.text);
            let msg = new SpeechSynthesisUtterance(data.text)
            speechSynthesis.speak(msg)
          }
         
        }
    });
  }