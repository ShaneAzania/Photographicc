const info_button = document.querySelector('#info');
const info_box = document.querySelector('#info-box');
const close_btn = info_box.querySelector('.close-btn');
info_button.addEventListener('click', e => {
    info_box.style.width = '20em';
    info_box.style.padding = '1.5em';
});
close_btn.addEventListener('click', e => {
    info_box.style.width = '0';
    info_box.style.padding = '0';
});

// image_view back_btn returns to previous page in history
const back_btn = document.querySelector('#back_btn');
back_btn.addEventListener('click', e => {
    history.back()
});
