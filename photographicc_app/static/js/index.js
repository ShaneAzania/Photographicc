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