function update(stream) {
  document.querySelector('video').src = stream.url;
}

function hasGetUserMedia() {
  return !!(navigator.mediaDevices &&
    navigator.mediaDevices.getUserMedia);
}


const constraints = {
  video: true
};

const video = document.querySelector('video');

navigator.mediaDevices.getUserMedia(constraints).
  then((stream) => {video.srcObject = stream});


// Take screenshot
const screenshotButton = document.querySelector('#screenshot-button');
const img = document.querySelector('#screenshot-img');

const canvas = document.createElement('canvas');

screenshotButton.onclick = video.onclick = function() {
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  canvas.getContext('2d').drawImage(video, 0, 0);
  // Other browsers will fall back to image/png
  img.src = canvas.toDataURL('image/jpeg');


  copyImageSrc()
};

function handleSuccess(stream) {
  screenshotButton.disabled = false;
  video.srcObject = stream;
}


function copyImageSrc() {
  const screenshot_img = document.querySelector('#screenshot-img');
  const img_src = document.querySelector('#img-src');
  console.log(screenshot_img.src)
  img_src.setAttribute("value", screenshot_img.src);
}