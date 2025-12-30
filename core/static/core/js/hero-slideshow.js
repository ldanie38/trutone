// hero-slideshow.js
document.addEventListener('DOMContentLoaded', () => {
  const container = document.getElementById('heroSlideshow');
  const slides = Array.from(container.querySelectorAll('.slide'));
  const videoSlide = slides.find(s => s.dataset.type === 'video');
  const video = videoSlide ? videoSlide.querySelector('video') : null;
  const imageSlides = slides.filter(s => s.dataset.type === 'image');
  const imageDuration = 4000; // ms per image
  let currentIndex = 0; // index in slides array
  let imageTimer = null;
  let imagesLoaded = 0;

  // Preload images and detect load errors
  imageSlides.forEach(slide => {
    const img = slide.querySelector('img');
    if (!img) { imagesLoaded++; return; }
    if (img.complete && img.naturalWidth !== 0) {
      imagesLoaded++;
      return;
    }
    img.addEventListener('load', () => { imagesLoaded++; });
    img.addEventListener('error', () => {
      console.warn('Image failed to load:', img.src);
      // mark as loaded so slideshow won't wait forever
      imagesLoaded++;
      // optionally hide the slide so it never shows blank
      slide.dataset.broken = 'true';
    });
  });

  // Helper to show a slide by index
  function showSlideByIndex(index) {
    slides.forEach((s, i) => s.classList.toggle('active', i === index));
    currentIndex = index;
  }

  // Advance to next non-broken slide (wraps)
  function nextSlide() {
    let next = (currentIndex + 1) % slides.length;
    // skip broken slides
    for (let i = 0; i < slides.length; i++) {
      const s = slides[next];
      if (s.dataset.broken !== 'true') return showSlideByIndex(next);
      next = (next + 1) % slides.length;
    }
    // if all broken, do nothing
  }

  // Start cycling images only (skip the video slide)
  function startImageCycle() {
    clearInterval(imageTimer);
    // find index of first image slide after current
    imageTimer = setInterval(() => {
      // if currently on video, move to first image
      if (slides[currentIndex].dataset.type === 'video') {
        const firstImageIndex = slides.findIndex(s => s.dataset.type === 'image' && s.dataset.broken !== 'true');
        if (firstImageIndex >= 0) showSlideByIndex(firstImageIndex);
        return;
      }
      // otherwise advance to next image slide
      let next = currentIndex;
      do {
        next = (next + 1) % slides.length;
      } while (slides[next].dataset.type !== 'image' && next !== currentIndex);
      showSlideByIndex(next);
    }, imageDuration);
  }

  // Called when video ends or fallback triggers
  function onVideoDone() {
    // move to first image slide
    const firstImageIndex = slides.findIndex(s => s.dataset.type === 'image' && s.dataset.broken !== 'true');
    if (firstImageIndex >= 0) {
      showSlideByIndex(firstImageIndex);
      startImageCycle();
    } else {
      // no images available, keep video or show poster
      console.warn('No valid image slides found.');
    }
  }

  // Start: show video slide first
  showSlideByIndex(0);

  if (video) {
    // Try to autoplay; muted helps browsers allow autoplay
    video.play().then(() => {
      // playing; wait for ended
    }).catch(() => {
      // autoplay blocked: show poster and advance after short fallback
      console.warn('Autoplay blocked or failed; using fallback.');
      setTimeout(onVideoDone, 1200);
    });

    // When video ends, go to images
    video.addEventListener('ended', onVideoDone);

    // If user interaction pauses or seeks, you can handle it here
  } else {
    // No video: start image cycle after a short delay
    setTimeout(startImageCycle, 300);
  }

  // Safety: if images never load within X seconds, start cycle anyway
  setTimeout(() => {
    if (imagesLoaded < imageSlides.length) {
      console.warn('Some images still loading or failed; starting slideshow anyway.');
    }
    // If video already finished or not present, start cycling images
    if (!video || video.ended || video.paused) startImageCycle();
  }, 3000);

  // Optional: pause cycling when user hovers
  container.addEventListener('mouseenter', () => clearInterval(imageTimer));
  container.addEventListener('mouseleave', () => {
    if (!video || video.ended) startImageCycle();
  });
});


