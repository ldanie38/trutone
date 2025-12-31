// hero-slideshow.js (patch/augmentation)
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('heroSlideshow');
  if (!container) return;
  const slides = Array.from(container.querySelectorAll('.slide'));
  const videoSlide = slides.find(s => s.dataset.type === 'video');
  const video = videoSlide ? videoSlide.querySelector('video') : null;
  const imageSlides = slides.filter(s => s.dataset.type === 'image');
  const imageDuration = 4000; // ms per image
  let currentIndex = 0;
  let imageTimer = null;
  let imagesLoaded = 0;

  // --- preload images (your existing logic) ---
  imageSlides.forEach(slide => {
    const img = slide.querySelector('img');
    if (!img) { imagesLoaded++; return; }
    if (img.complete && img.naturalWidth !== 0) { imagesLoaded++; return; }
    img.addEventListener('load', () => { imagesLoaded++; });
    img.addEventListener('error', () => {
      console.warn('Image failed to load:', img.src);
      imagesLoaded++;
      slide.dataset.broken = 'true';
    });
  });

  function showSlideByIndex(index) {
    slides.forEach((s, i) => s.classList.toggle('active', i === index));
    currentIndex = index;
  }

  function nextSlide() {
    let next = (currentIndex + 1) % slides.length;
    for (let i = 0; i < slides.length; i++) {
      const s = slides[next];
      if (s.dataset.broken !== 'true') return showSlideByIndex(next);
      next = (next + 1) % slides.length;
    }
  }

  function startImageCycle() {
    clearInterval(imageTimer);
    imageTimer = setInterval(() => {
      if (slides[currentIndex].dataset.type === 'video') {
        const firstImageIndex = slides.findIndex(s => s.dataset.type === 'image' && s.dataset.broken !== 'true');
        if (firstImageIndex >= 0) showSlideByIndex(firstImageIndex);
        return;
      }
      let next = currentIndex;
      do { next = (next + 1) % slides.length; } while (slides[next].dataset.type !== 'image' && next !== currentIndex);
      showSlideByIndex(next);
    }, imageDuration);
  }

  function revealSlideshowAndStart() {
    // Reveal container slides if hidden by CSS/display
    slides.forEach(s => { if (getComputedStyle(s).display === 'none') s.style.display = ''; });
    // hide video element (so badge and slides are visible)
    if (video) video.style.display = 'none';
    // show first valid image and start cycle
    const firstImageIndex = slides.findIndex(s => s.dataset.type === 'image' && s.dataset.broken !== 'true');
    if (firstImageIndex >= 0) {
      showSlideByIndex(firstImageIndex);
      startImageCycle();
    } else {
      console.warn('No valid image slides found.');
    }
  }

  // Start: show video slide first (or first slide in markup)
  showSlideByIndex(0);

  // Skip button fallback (create if missing)
  let skipBtn = document.getElementById('skipVideo');
  if (!skipBtn) {
    skipBtn = document.createElement('button');
    skipBtn.id = 'skipVideo';
    skipBtn.textContent = 'Skip video';
    skipBtn.style.position = 'absolute';
    skipBtn.style.zIndex = 99999;
    skipBtn.style.top = '10px';
    skipBtn.style.right = '10px';
    skipBtn.style.display = 'none';
    container.appendChild(skipBtn);
  }

  skipBtn.addEventListener('click', () => {
    revealSlideshowAndStart();
    skipBtn.style.display = 'none';
  });

  if (video) {
    // Try autoplay; muted helps browsers allow autoplay
    video.play().catch(() => {
      console.warn('Autoplay blocked or failed; using fallback.');
      // show skip button so user can reveal slideshow
      skipBtn.style.display = '';
      // fallback reveal after a short delay so users see poster briefly
      setTimeout(revealSlideshowAndStart, 1200);
    });

    // When video ends, reveal slideshow and start cycling
    video.addEventListener('ended', () => {
      revealSlideshowAndStart();
    });

    // If user pauses the video manually and you want to reveal slideshow, handle here:
    // video.addEventListener('pause', () => { /* optional behavior */ });
  } else {
    // No video: start image cycle after a short delay
    setTimeout(() => {
      revealSlideshowAndStart();
    }, 300);
  }

  // Safety: if images never load within X seconds, start cycle anyway
  setTimeout(() => {
    if (imagesLoaded < imageSlides.length) {
      console.warn('Some images still loading or failed; starting slideshow anyway.');
    }
    // If video already finished or not present, start cycling images
    if (!video || video.ended || video.paused) startImageCycle();
  }, 3000);

  // Pause cycling on hover
  container.addEventListener('mouseenter', () => clearInterval(imageTimer));
  container.addEventListener('mouseleave', () => {
    if (!video || video.ended) startImageCycle();
  });

  // Optional: ensure badge is visible (if you added inline SVG)
  const badge = container.querySelector('.hero-slogan');
  if (badge) {
    badge.style.pointerEvents = 'none';
    badge.style.zIndex = 9999;
  }
});


