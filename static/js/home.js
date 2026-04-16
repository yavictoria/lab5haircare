(function () {
  'use strict';

  var hero = document.getElementById('hero-area');
  var bubblesWrap = document.getElementById('parallax-bubbles');
  var bowsWrap = document.getElementById('parallax-bows');

  var mouseX = 0.5;
  var mouseY = 0.5;
  var currentX = 0.5;
  var currentY = 0.5;
  var rafId = null;

  function getElements() {
    var els = [];
    if (bubblesWrap) {
      var bubbles = bubblesWrap.querySelectorAll('.parallax-bubble[data-speed]');
      for (var i = 0; i < bubbles.length; i++) els.push(bubbles[i]);
    }
    if (bowsWrap) {
      var bows = bowsWrap.querySelectorAll('.parallax-bow[data-speed]');
      for (var j = 0; j < bows.length; j++) els.push(bows[j]);
    }
    return els;
  }

  function onMouseMove(e) {
    var w = window.innerWidth;
    var h = window.innerHeight;
    mouseX = e.clientX / w;
    mouseY = e.clientY / h;
  }

  function update() {
    currentX += (mouseX - currentX) * 0.08;
    currentY += (mouseY - currentY) * 0.08;

    var centerX = 0.5;
    var centerY = 0.5;
    var offsetX = (currentX - centerX) * 2;
    var offsetY = (currentY - centerY) * 2;

    var elements = getElements();
    var maxMove = 36;

    for (var i = 0; i < elements.length; i++) {
      var el = elements[i];
      var speed = parseFloat(el.getAttribute('data-speed')) || 0.04;
      var move = maxMove * speed * 20;
      var x = offsetX * move;
      var y = offsetY * move;
      var rot = el.getAttribute('data-rotate');
      var base = el.classList.contains('parallax-bow') && rot ? ' rotate(' + rot + 'deg)' : '';
      el.style.transform = 'translate(' + x + 'px, ' + y + 'px)' + base;
    }

    rafId = requestAnimationFrame(update);
  }

  function startLoop() {
    if (rafId == null) rafId = requestAnimationFrame(update);
  }

  function stopLoop() {
    if (rafId != null) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
  }

  if (hero) {
    hero.addEventListener('mouseenter', startLoop);
    hero.addEventListener('mouseleave', stopLoop);
  }
  document.addEventListener('mousemove', onMouseMove);

  if (hero && document.querySelector('.parallax-bubble')) {
    startLoop();
  }
})();
