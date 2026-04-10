document.addEventListener('DOMContentLoaded', function() {
  // Add fade-in to elements with data-animate
  var els = document.querySelectorAll('[data-animate]');
  var observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('fade-in');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  els.forEach(function(el) { observer.observe(el); });

  // Active nav link
  var path = window.location.pathname;
  var links = document.querySelectorAll('.navbar__links a');
  links.forEach(function(link) {
    if (link.getAttribute('href') === path) link.classList.add('active');
  });
});
