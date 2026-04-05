const pageEles = document.querySelectorAll('.page');
const headerEle = document.querySelector('header');
const footerEle = document.querySelector('footer');
let currentIndex = 0;

function updatePageCount (currentIndex) {
    const pageCount = pageEles.length;
    const currentPage = currentIndex + 1;
    const pageCountEle = document.querySelector('.page-count');
    pageCountEle.innerHTML = `Page ${currentPage} of ${pageCount}`;
}


if (pageEles) {
    // extract page number from url
    const urlParams = new URLSearchParams(window.location.search);
    const page = urlParams.get('page');
    if (page) {
        currentIndex = page - 1;
    }
    pageEles[currentIndex].classList.add('active');

    const nextPageEle = document.createElement('button');
    const prevPageEle = document.createElement('button');
    const pageCountEle = document.createElement('span');
    pageCountEle.classList.add('page-count');


    prevPageEle.classList.add('prev');
    prevPageEle.innerHTML = '&lt;Prev';

    nextPageEle.classList.add('next');
    nextPageEle.innerHTML = 'Next&gt;';


    nextPageEle.addEventListener('click', () => {
        const activePage = document.querySelector('.active');
        const nextPage = activePage.nextElementSibling;
        if (nextPage) {
            activePage.classList.remove('active');
            nextPage.classList.add('active');
            currentIndex = currentIndex + 1;
            updatePageCount(currentIndex);
            history.pushState(null, null, `?page=${currentIndex + 1}`);
        }
    });

    prevPageEle.addEventListener('click', () => {
        const activePage = document.querySelector('.active');
        const prevPage = activePage.previousElementSibling;
        if (prevPage) {
            activePage.classList.remove('active');
            prevPage.classList.add('active');
            currentIndex = currentIndex - 1;
            updatePageCount(currentIndex);
            history.pushState(null, null, `?page=${currentIndex + 1}`);
        }
    });

    footerEle.appendChild(prevPageEle);
    footerEle.appendChild(pageCountEle);
    footerEle.appendChild(nextPageEle);

    updatePageCount(currentIndex);
}