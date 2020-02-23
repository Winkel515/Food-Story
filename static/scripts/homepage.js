 // First we get the viewport height and we multiple it by 1% to get a value for a vh unit
$(document).on("pagecreate", () => {
  let vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
})
$(window).on('orientationchange', () => {
  // We execute the same script as before
  let vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
});