
let nextBtn = document.querySelector('.next')
let prevBtn = document.querySelector('.prev')

let slider = document.querySelector('.SLIDER')
let sliderList = slider.querySelector('.SLIDER .LIST')
let thumbnail = document.querySelector('.SLIDER .THUMBNAIL')
let thumbnailItems = thumbnail.querySelectorAll('.ITEMS')

thumbnail.appendChild(thumbnailItems[0])

// Function for next button
nextBtn.onclick = function() {
    moveSlider('next')
}


// Function for prev button
prevBtn.onclick = function() {
    moveSlider('prev')
}


function moveSlider(direction) {
    let sliderItems = sliderList.querySelectorAll('.ITEMS')
    let thumbnailItems = document.querySelectorAll('.THUMBNAIL .ITEMS')

    if(direction === 'next'){
        sliderList.appendChild(sliderItems[0])
        thumbnail.appendChild(thumbnailItems[0])
        slider.classList.add('next')
    } else {
        sliderList.prepend(sliderItems[sliderItems.length - 1])
        thumbnail.prepend(thumbnailItems[thumbnailItems.length - 1])
        slider.classList.add('prev')
    }


    slider.addEventListener('animationend', function() {
        if(direction === 'next'){
            slider.classList.remove('next')
        } else {
            slider.classList.remove('prev')
        }
    }, {once: true}) // Remove the event listener after it's triggered once
}