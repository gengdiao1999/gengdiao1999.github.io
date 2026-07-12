(function () {
  "use strict";

  const TOC_ROOT_ID = "toc-root";
  const CONTENT_SELECTOR = ".book-content";
  const HEADING_SELECTORS = "h2, h3";

  function slugify(text) {
    return text
      .toLowerCase()
      .replace(/\s+/g, "-")
      .replace(/[^\w\-]/g, "")
      .replace(/-+/g, "-")
      .substring(0, 64);
  }

  function ensureHeadingId(heading) {
    if (!heading.id) {
      const text = heading.textContent.trim();
      heading.id = "section-" + slugify(text);
    }
    return heading.id;
  }

  function buildTree(headings) {
    const root = [];
    let currentH2 = null;

    headings.forEach(function (heading) {
      const level = parseInt(heading.tagName[1], 10);
      const node = {
        level: level,
        text: heading.textContent.trim(),
        id: ensureHeadingId(heading),
      };

      if (level === 2) {
        currentH2 = Object.assign({}, node, { children: [] });
        root.push(currentH2);
      } else if (level === 3 && currentH2) {
        currentH2.children.push(node);
      }
    });

    return root;
  }

  function renderToc(tree) {
    const rootEl = document.getElementById(TOC_ROOT_ID);
    if (!rootEl || tree.length === 0) return;

    const ul = document.createElement("ul");
    ul.className = "toc-list";

    tree.forEach(function (h2) {
      const li = document.createElement("li");
      li.className = "toc-h2 expanded";
      li.dataset.target = h2.id;

      const toggle = document.createElement("button");
      toggle.className = "toc-toggle";
      toggle.setAttribute("aria-expanded", "true");
      toggle.textContent = "▾";
      toggle.addEventListener("click", function (e) {
        e.preventDefault();
        const isExpanded = li.classList.contains("expanded");
        li.classList.toggle("expanded", !isExpanded);
        toggle.setAttribute("aria-expanded", String(!isExpanded));
        toggle.textContent = isExpanded ? "▸" : "▾";
      });

      const link = document.createElement("a");
      link.href = "#" + h2.id;
      link.textContent = h2.text;

      li.appendChild(toggle);
      li.appendChild(link);

      if (h2.children.length > 0) {
        const subUl = document.createElement("ul");
        subUl.className = "toc-h3-list";

        h2.children.forEach(function (h3) {
          const subLi = document.createElement("li");
          subLi.dataset.target = h3.id;

          const subLink = document.createElement("a");
          subLink.href = "#" + h3.id;
          subLink.textContent = h3.text;

          subLi.appendChild(subLink);
          subUl.appendChild(subLi);
        });

        li.appendChild(subUl);
      }

      ul.appendChild(li);
    });

    rootEl.appendChild(ul);
  }

  function setupScrollSpy(headings) {
    const tocItems = document.querySelectorAll("[data-target]");
    if (tocItems.length === 0) return;

    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            const id = entry.target.id;
            tocItems.forEach(function (item) {
              item.classList.toggle("active", item.dataset.target === id);
            });

            const activeH3 = document.querySelector(
              '.toc-h3-list li[data-target="' + id + '"]'
            );
            if (activeH3) {
              const h2Li = activeH3.closest(".toc-h2");
              if (h2Li && !h2Li.classList.contains("expanded")) {
                h2Li.classList.add("expanded");
                const toggle = h2Li.querySelector(".toc-toggle");
                if (toggle) {
                  toggle.setAttribute("aria-expanded", "true");
                  toggle.textContent = "▾";
                }
              }
            }
          }
        });
      },
      {
        rootMargin: "-80px 0px -60% 0px",
        threshold: 0,
      }
    );

    headings.forEach(function (heading) {
      observer.observe(heading);
    });
  }

  function setupMobileNav() {
    const toggle = document.getElementById("nav-toggle");
    const sidebar = document.getElementById("sidebar-left");
    const overlay = document.getElementById("overlay");

    if (!toggle || !sidebar || !overlay) return;

    function open() {
      sidebar.classList.add("open");
      overlay.classList.add("show");
      toggle.setAttribute("aria-expanded", "true");
    }

    function close() {
      sidebar.classList.remove("open");
      overlay.classList.remove("show");
      toggle.setAttribute("aria-expanded", "false");
    }

    toggle.addEventListener("click", function () {
      if (sidebar.classList.contains("open")) {
        close();
      } else {
        open();
      }
    });

    overlay.addEventListener("click", close);
  }

  function init() {
    if (window.MathJax && window.MathJax.typesetPromise) {
      window.MathJax.typesetPromise().then(run).catch(run);
    } else {
      run();
    }
  }

  function run() {
    const content = document.querySelector(CONTENT_SELECTOR);
    if (!content) return;

    const headings = Array.from(content.querySelectorAll(HEADING_SELECTORS));
    const tree = buildTree(headings);
    renderToc(tree);
    setupScrollSpy(headings);
    setupMobileNav();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
