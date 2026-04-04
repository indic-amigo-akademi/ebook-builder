const pageEles = document.querySelectorAll('.page');
const headerEle = document.querySelector('header');
const footerEle = document.querySelector('footer');
let currentIndex = 0;

if (pageEles) {
    pageEles[currentIndex].classList.add('active');
    const pageCount = pageEles.length;

    const nextPageEle = document.createElement('a');
    const prevPageEle = document.createElement('a');
    const pageCountEle = document.createElement('span');


    prevPageEle.classList.add('prev');
    prevPageEle.innerHTML = '&lt;Prev';

    nextPageEle.classList.add('next');
    nextPageEle.innerHTML = 'Next&gt;';
    pageCountEle.innerHTML = `Page 1 of ${pageCount}`;

    nextPageEle.addEventListener('click', () => {
        const activePage = document.querySelector('.active');
        const nextPage = activePage.nextElementSibling;
        if (nextPage) {
            activePage.classList.remove('active');
            nextPage.classList.add('active');
            currentIndex = currentIndex + 1;
            pageCountEle.innerHTML = `Page ${currentIndex + 1} of ${pageCount}`;
        }
    });

    prevPageEle.addEventListener('click', () => {
        const activePage = document.querySelector('.active');
        const prevPage = activePage.previousElementSibling;
        if (prevPage) {
            activePage.classList.remove('active');
            prevPage.classList.add('active');
            currentIndex = currentIndex - 1;
            pageCountEle.innerHTML = `Page ${currentIndex + 1} of ${pageCount}`;
        }
    });

    footerEle.appendChild(prevPageEle);
    footerEle.appendChild(pageCountEle);
    footerEle.appendChild(nextPageEle);
}