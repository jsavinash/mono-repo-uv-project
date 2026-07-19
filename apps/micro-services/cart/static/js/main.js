/* ─────────────────────────────────────────────────────────────
   main.js  ─  Small interactive behaviours
   ───────────────────────────────────────────────────────────── */

document.addEventListener("DOMContentLoaded", () => {

  // ─── Auto-dismiss flash messages after 5s ─────────────────
  document.querySelectorAll(".flash").forEach((el) => {
    setTimeout(() => {
      el.style.transition = "opacity .4s ease";
      el.style.opacity = "0";
      setTimeout(() => el.remove(), 420);
    }, 5000);
  });

  // ─── Cart quantity update buttons (if on cart page) ───────
  document.querySelectorAll(".cart-qty-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const input = btn.closest(".cart-qty").querySelector("input");
      if (!input) return;
      let val = parseInt(input.value, 10) || 1;
      const delta = btn.dataset.delta === "-1" ? -1 : 1;
      val = Math.max(1, val + delta);
      input.value = val;
    });
  });

  // ─── Smooth scroll for internal anchors ───────────────────
  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const target = document.querySelector(a.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
});
